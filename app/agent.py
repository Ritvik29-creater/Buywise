from typing import TypedDict
from langgraph.graph import StateGraph, END
from .products import search_products

POLICIES = {
    "recommendation": "Recommendations should match the customer's stated requirements and avoid unsupported claims.",
    "cart": "Cart changes should be confirmed by the customer before a final purchase is placed.",
    "refund": "Refund requests must follow the platform refund policy and may require order verification.",
}

class ShoppingState(TypedDict):
    message: str
    intent: str
    confidence: float
    policy: str
    products: list
    response: str
    route: str

def classify(state: ShoppingState):
    text = state["message"].lower()

    if any(x in text for x in ["find", "search", "looking for", "recommend", "suggest"]):
        intent = "product_search"
        confidence = 0.90
    elif any(x in text for x in ["compare", "comparison", "difference"]):
        intent = "comparison"
        confidence = 0.88
    elif any(x in text for x in ["cart", "add", "remove"]):
        intent = "cart"
        confidence = 0.86
    elif any(x in text for x in ["refund", "return", "money back"]):
        intent = "refund"
        confidence = 0.85
    else:
        intent = "unknown"
        confidence = 0.40

    return {
        "intent": intent,
        "confidence": confidence,
        "policy": POLICIES.get(intent, POLICIES["recommendation"])
    }

def route(state: ShoppingState):
    return "clarify" if state["confidence"] < 0.65 else "process"

def process(state: ShoppingState):
    products = search_products(state["message"])

    if state["intent"] == "product_search":
        if products:
            top = products[:3]
            names = ", ".join(p["name"] for p in top)
            response = f"Here are relevant products: {names}."
        else:
            response = "I could not find matching products in the current catalog."
    elif state["intent"] == "comparison":
        response = "Comparison workflow selected. Provide product IDs to compare specific products."
    elif state["intent"] == "cart":
        response = "Cart workflow selected. Cart-changing actions require explicit confirmation."
    elif state["intent"] == "refund":
        response = "Refund workflow selected. The order and refund policy must be verified."
    else:
        response = "I can help with product search, comparison, cart operations, or refunds."

    return {
        "products": products[:5],
        "response": response,
        "route": state["intent"]
    }

def clarify(state: ShoppingState):
    return {
        "products": [],
        "response": "Could you clarify whether you want to search, compare products, manage your cart, or request a refund?",
        "route": "clarification"
    }

graph = StateGraph(ShoppingState)
graph.add_node("classify", classify)
graph.add_node("process", process)
graph.add_node("clarify", clarify)
graph.set_entry_point("classify")
graph.add_conditional_edges(
    "classify",
    route,
    {"process": "process", "clarify": "clarify"}
)
graph.add_edge("process", END)
graph.add_edge("clarify", END)

shopping_graph = graph.compile()

def run_shopping_agent(message: str):
    state = {
        "message": message,
        "intent": "",
        "confidence": 0.0,
        "policy": "",
        "products": [],
        "response": "",
        "route": ""
    }
    return shopping_graph.invoke(state)
