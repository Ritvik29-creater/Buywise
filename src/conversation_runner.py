import sys
from langgraph.types import Command

from .graph import graph


def safe_print(text: str):
    """Safely print text handling character encoding issues on Windows consoles."""
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        print(text.encode(encoding, errors="replace").decode(encoding))


def run_single_turn(user_input, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {"messages": [("user", user_input)]}
    safe_print(f"\nUSER: {user_input}")
    try:
        result = graph.invoke(input_state, config)
        snapshot = graph.get_state(config)
        interrupt_info = None
        for task in snapshot.tasks:
            if hasattr(task, "interrupts") and task.interrupts:
                for intr in task.interrupts:
                    if hasattr(intr, "value") and isinstance(intr.value, dict):
                        interrupt_info = intr.value
        state = snapshot.values
        dialog_state = state.get("dialog_state", [])
        current_mode = dialog_state[-1] if dialog_state else "sales_rep"
        if len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            response = last_message.content
            response_type = last_message.__class__.__name__
        else:
            response = "No response yet"
            response_type = "None"
        agent_type = current_mode.upper().replace("_", " ")
        if not interrupt_info:
            safe_print(f"{agent_type}: {response}")
        else:
            safe_print(
                f"{agent_type}: [INTERRUPTED FOR APPROVAL] {interrupt_info.get('message', '')}"
            )
        return {
            "user_input": user_input,
            "response": response,
            "response_type": response_type,
            "thread_id": thread_id,
            "current_mode": current_mode,
            "interrupt_info": interrupt_info,
        }
    except Exception as e:
        safe_print(f"ERROR: {str(e)}")
        return {
            "user_input": user_input,
            "error": str(e),
            "thread_id": thread_id,
            "current_mode": "unknown",
        }


def resume_with_approval(thread_id, supervisor_response):

    config = {"configurable": {"thread_id": thread_id}}
    try:
        result = graph.invoke(
            Command(resume=supervisor_response), config
        )  # <-- Correct usage!
        snapshot = graph.get_state(config)
        state = snapshot.values
        dialog_state = state.get("dialog_state", [])
        current_mode = dialog_state[-1] if dialog_state else "sales_rep"
        if len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            response = last_message.content
            response_type = last_message.__class__.__name__
        else:
            response = "No response after approval"
            response_type = "None"
        agent_type = current_mode.upper().replace("_", " ")
        safe_print(f"{agent_type}: {response}")
        return {
            "supervisor_response": supervisor_response,
            "response": response,
            "response_type": response_type,
            "thread_id": thread_id,
            "current_mode": current_mode,
        }
    except Exception as e:
        safe_print(f"ERROR RESUMING: {str(e)}")
        return {
            "supervisor_response": supervisor_response,
            "error": str(e),
            "thread_id": thread_id,
            "current_mode": "unknown",
        }


def show_conversation_history(thread_id):
    safe_print("\n----- FULL CONVERSATION HISTORY -----")
    snapshot = graph.get_state({"configurable": {"thread_id": thread_id}}).values
    for i, msg in enumerate(snapshot["messages"]):
        msg_type = msg.__class__.__name__
        content = getattr(msg, "content", "")
        if msg_type == "HumanMessage":
            safe_print(f"{i+1}. USER: {content}")
        elif msg_type == "AIMessage":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_details = []
                for tc in msg.tool_calls:
                    tool_name = tc.get("name", "unknown_tool")
                    tool_details.append(f"{tool_name}")
                safe_print(f"{i+1}. AGENT → TOOL: {', '.join(tool_details)}")
            else:
                safe_print(f"{i+1}. AGENT: {content}")
        elif msg_type == "ToolMessage":
            tool_call_id = getattr(msg, "tool_call_id", "unknown_id")
            tool_name = "TOOL"
            for prev_msg in snapshot["messages"]:
                if hasattr(prev_msg, "tool_calls"):
                    for tc in prev_msg.tool_calls:
                        if tc.get("id") == tool_call_id:
                            tool_name = tc.get("name", "TOOL")
                            break
            if "Human supervisor response" in content:
                safe_print(f"{i+1}. SUPERVISOR: {content}")
            else:
                safe_print(f"{i+1}. {tool_name.upper()}: {content}")
        else:
            safe_print(f"{i+1}. {msg_type}: {content}")
    safe_print("----- END OF HISTORY -----")
