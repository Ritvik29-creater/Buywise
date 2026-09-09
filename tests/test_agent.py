from app.agent import run_shopping_agent

def test_product_search():
    result = run_shopping_agent("Find me wireless headphones")
    assert result["intent"] == "product_search"
    assert result["route"] == "product_search"
    assert len(result["products"]) > 0

def test_cart_request():
    result = run_shopping_agent("Add this product to my cart")
    assert result["intent"] == "cart"
    assert result["route"] == "cart"

def test_ambiguous_request():
    result = run_shopping_agent("I need help")
    assert result["route"] == "clarification"
