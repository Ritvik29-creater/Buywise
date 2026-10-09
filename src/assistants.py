# src/assistants.py
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from .prompts import sales_rep_prompt, support_prompt
from .state import State
from .tools import (
    DEFAULT_USER_ID,
    EscalateToHuman,
    RouteToCustomerSupport,
    analyze_reviews,
    cart_tool,
    cancel_order,
    compare_products,
    recommend_products,
    search_tool,
    structured_search_tool,
    track_order,
    view_cart,
    set_thread_id,
    set_user_id,
)

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Gemini 3 Thought Signature Compatibility Patch for Tool Calling
# ─────────────────────────────────────────────────────────────────────────────
try:
    import langchain_google_genai.chat_models as _cm
    from google.ai.generativelanguage_v1beta.types import Part

    _thought_signatures = {}
    _orig_response_to_result = _cm._response_to_result

    def _patched_response_to_result(response, stream=False):
        res = _orig_response_to_result(response, stream)
        try:
            for candidate in response.candidates:
                for p in candidate.content.parts:
                    if p.function_call and hasattr(p, "thought_signature") and p.thought_signature:
                        fn_name = p.function_call.name
                        _thought_signatures[fn_name] = p.thought_signature
                        for tc in getattr(res.generations[0].message, "tool_calls", []):
                            if tc.get("name") == fn_name:
                                tc["thought_signature"] = p.thought_signature
                                _thought_signatures[tc.get("id")] = p.thought_signature
                        res.generations[0].message.additional_kwargs["thought_signature"] = p.thought_signature
        except Exception:
            pass
        return res

    _cm._response_to_result = _patched_response_to_result

    _orig_parse_chat_history = _cm._parse_chat_history

    def _patched_parse_chat_history(input_messages, convert_system_message_to_human=False):
        sys_inst, messages = _orig_parse_chat_history(input_messages, convert_system_message_to_human)
        for c in messages:
            if c.role == "model":
                new_parts = []
                for p in c.parts:
                    if p.function_call:
                        ts = getattr(p, "thought_signature", None)
                        if not ts:
                            ts = _thought_signatures.get(p.function_call.name)
                        if ts:
                            p = Part(function_call=p.function_call, thought_signature=ts)
                    new_parts.append(p)
                c.parts = new_parts
        return sys_inst, messages

    _cm._parse_chat_history = _patched_parse_chat_history
except Exception as _patch_err:
    print(f"Notice: Thought signature patch skipped: {_patch_err}")

# ─────────────────────────────────────────────────────────────────────────────
# LangSmith Observability (optional — set vars in .env to enable)
# ─────────────────────────────────────────────────────────────────────────────
if os.environ.get("LANGCHAIN_TRACING_V2", "").lower() == "true":
    os.environ.setdefault("LANGCHAIN_PROJECT", "SmartShop-Elite")

# ─────────────────────────────────────────────────────────────────────────────
# LLM Setup
# ─────────────────────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
    else:
        raise ValueError(
            "No API Key found. Please set GOOGLE_API_KEY or OPENAI_API_KEY in .env"
        )
else:
    gemini_model = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
    if gemini_model in ("gemini-3.5-flash", "models/gemini-3.5-flash"):
        gemini_model = "gemini-flash-lite-latest"
    llm = ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Tool Registration
# ─────────────────────────────────────────────────────────────────────────────

# Sales agent has all discovery, cart, comparison, recommendation, and review tools
sales_tools = [
    RouteToCustomerSupport,
    search_tool,
    structured_search_tool,
    compare_products,
    recommend_products,
    analyze_reviews,
    cart_tool,
    view_cart,
    track_order,
]

# Support agent can escalate to humans and cancel orders / handle refunds
support_tools = [
    EscalateToHuman,
    track_order,
    cancel_order,
]

# ─────────────────────────────────────────────────────────────────────────────
# Runnable Pipelines
# ─────────────────────────────────────────────────────────────────────────────
sales_runnable = sales_rep_prompt.partial(time=datetime.now) | llm.bind_tools(sales_tools)
support_runnable = support_prompt.partial(time=datetime.now) | llm.bind_tools(support_tools)


# ─────────────────────────────────────────────────────────────────────────────
# Agent Node Functions (Sync and Async implementations)
# ─────────────────────────────────────────────────────────────────────────────


def sales_assistant_sync(
    state: State, config: RunnableConfig, runnable=sales_runnable
) -> dict:
    """
    Synchronous LangGraph node function for running the sales assistant LLM agent.
    """
    thread_id = config["configurable"].get("thread_id")
    if thread_id:
        set_thread_id(thread_id)

    set_user_id(DEFAULT_USER_ID)

    result = runnable.invoke(state, config=config)
    return {"messages": result}


async def sales_assistant(
    state: State, config: RunnableConfig, runnable=sales_runnable
) -> dict:
    """
    LangGraph node function for running the sales assistant LLM agent.
    """
    thread_id = config["configurable"].get("thread_id")
    if thread_id:
        set_thread_id(thread_id)

    set_user_id(DEFAULT_USER_ID)

    if hasattr(runnable, "ainvoke"):
        result = await runnable.ainvoke(state, config=config)
    else:
        result = runnable.invoke(state, config=config)

    return {"messages": result}


def support_assistant_sync(state: State, config: RunnableConfig) -> dict:
    """
    Synchronous LangGraph node function for the customer support LLM agent.
    """
    thread_id = config["configurable"].get("thread_id")
    if thread_id:
        set_thread_id(thread_id)

    result = support_runnable.invoke(state, config=config)
    return {"messages": result}


async def support_assistant(state: State, config: RunnableConfig) -> dict:
    """
    LangGraph node function for the customer support LLM agent.
    """
    thread_id = config["configurable"].get("thread_id")
    if thread_id:
        set_thread_id(thread_id)

    if hasattr(support_runnable, "ainvoke"):
        result = await support_runnable.ainvoke(state, config=config)
    else:
        result = support_runnable.invoke(state, config=config)

    return {"messages": result}

