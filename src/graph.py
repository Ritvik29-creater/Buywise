# src/graph.py
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from .assistants import (
    sales_assistant,
    sales_assistant_sync,
    sales_tools,
    support_assistant,
    support_assistant_sync,
    support_tools,
)
from .state import State
from .tools import (
    create_tool_node_with_fallback,
    RouteToCustomerSupport,
    EscalateToHuman,
)


def after_sales_tool(state: State) -> dict:
    """Check if the last tool call was a handoff request."""
    if not state.get("messages"):
        return {}

    tool_msg = state["messages"][-1]

    if isinstance(tool_msg, ToolMessage) and tool_msg.name == "RouteToCustomerSupport":
        return {"dialog_state": "customer_support"}

    return {}


def after_support_tool(state: State) -> dict:
    """Check if the support agent triggered a human escalation."""
    if not state.get("messages"):
        return {}

    tool_msg = state["messages"][-1]

    if isinstance(tool_msg, ToolMessage) and tool_msg.name == "EscalateToHuman":
        # Try to extract severity from the preceding AI message's tool call args
        severity = "high"
        summary = tool_msg.content[:100] if tool_msg.content else "Issue requires review"

        for msg in reversed(state["messages"]):
            if hasattr(msg, "tool_calls"):
                for tc in msg.tool_calls:
                    if tc.get("name") == "EscalateToHuman":
                        args = tc.get("args", {})
                        severity = args.get("severity", "high")
                        summary = args.get("summary", summary)
                        break
                break

        return {
            "need_human_approval": {
                "tool_call_id": tool_msg.tool_call_id,
                "severity": severity,
                "summary": summary,
                "message": f"[{severity.upper()}] {summary}",
            }
        }
    return {}


def human_approval(state: State) -> dict:
    """Node that pauses execution for human supervisor input."""
    approval_data = state.get("need_human_approval")
    if not approval_data:
        return {}

    human_input = interrupt(
        {
            "question": "Supervisor input required",
            "severity": approval_data.get("severity", "unknown"),
            "summary": approval_data.get("summary", ""),
            "message": approval_data.get("message", ""),
        }
    )

    return {
        "messages": [
            ToolMessage(
                tool_call_id=approval_data["tool_call_id"],
                content=f"[SUPERVISOR RESPONSE] {human_input}",
                name="EscalateToHuman",
            )
        ],
        "need_human_approval": None,
    }


def build_graph():
    builder = StateGraph(State)

    # ── Nodes ──────────────────────────────────────────────────────────────────
    builder.add_node(
        "sales_rep", RunnableLambda(sales_assistant_sync, afunc=sales_assistant)
    )
    builder.add_node(
        "customer_support",
        RunnableLambda(support_assistant_sync, afunc=support_assistant),
    )
    builder.add_node("sales_tools", create_tool_node_with_fallback(sales_tools))
    builder.add_node("support_tools", create_tool_node_with_fallback(support_tools))
    builder.add_node("after_sales_tool", after_sales_tool)
    builder.add_node("after_support_tool", after_support_tool)
    builder.add_node("human_approval", human_approval)

    # ── Entry Point ────────────────────────────────────────────────────────────
    def route_start(state: State) -> str:
        dialog = state.get("dialog_state", [])
        if dialog and dialog[-1] == "customer_support":
            return "customer_support"
        return "sales_rep"

    builder.add_conditional_edges(START, route_start)

    # ── Sales Agent Logic ──────────────────────────────────────────────────────
    def route_sales(state: State) -> str:
        last_msg = state["messages"][-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return "sales_tools"
        return END

    builder.add_conditional_edges("sales_rep", route_sales)
    builder.add_edge("sales_tools", "after_sales_tool")

    def route_after_sales(state: State) -> str:
        dialog = state.get("dialog_state", [])
        if dialog and dialog[-1] == "customer_support":
            return "customer_support"
        return "sales_rep"

    builder.add_conditional_edges("after_sales_tool", route_after_sales)

    # ── Support Agent Logic ────────────────────────────────────────────────────
    def route_support(state: State) -> str:
        last_msg = state["messages"][-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return "support_tools"
        return END

    builder.add_conditional_edges("customer_support", route_support)
    builder.add_edge("support_tools", "after_support_tool")

    def route_after_support(state: State) -> str:
        if state.get("need_human_approval"):
            return "human_approval"
        return "customer_support"  # Loop back to read tool output

    builder.add_conditional_edges("after_support_tool", route_after_support)

    # After human approval, return to support agent to communicate decision
    builder.add_edge("human_approval", "customer_support")

    # ── Compile ────────────────────────────────────────────────────────────────
    return builder.compile(checkpointer=MemorySaver())


graph = build_graph()
