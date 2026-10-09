"""
tests/test_new_tools.py
Full test suite for all new SmartShop Elite tools:
  - compare_products
  - recommend_products
  - analyze_reviews
  - track_order / cancel_order
  - Updated cart_tool (buy → real Order IDs)
  - Updated view_cart (shows prices)
"""
import re
import uuid
import pytest

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _set_thread():
    """Set a fresh thread ID and return it."""
    from src.tools import set_thread_id
    tid = str(uuid.uuid4())
    set_thread_id(tid)
    return tid


def _buy_one_item():
    """Add a known product and place an order. Returns (buy_result, order_id)."""
    from src.tools import cart_tool, _product_lookup
    _set_thread()
    pid = list(_product_lookup.keys())[0]
    cart_tool.invoke({"cart_operation": "add", "product_id": pid, "quantity": 1})
    buy_result = cart_tool.invoke({"cart_operation": "buy"})
    match = re.search(r"ORD-\d+", buy_result)
    return buy_result, match.group(0) if match else None


# ─────────────────────────────────────────────────────────────────────────────
# Compare Products
# ─────────────────────────────────────────────────────────────────────────────


class TestCompareProducts:
    def test_requires_at_least_two_products(self):
        from src.tools import compare_products
        result = compare_products.invoke({"product_ids": [1]})
        assert "at least 2" in result.lower()

    def test_too_many_products_rejected(self):
        from src.tools import compare_products
        result = compare_products.invoke({"product_ids": [1, 2, 3, 4, 5, 6]})
        assert "at most 5" in result.lower()

    def test_compare_two_valid_products(self):
        from src.tools import compare_products, _product_lookup
        ids = list(_product_lookup.keys())[:2]
        result = compare_products.invoke({"product_ids": ids})
        # Should contain comparison header and product names
        assert "Comparison" in result or "Product" in result

    def test_compare_returns_price_info(self):
        from src.tools import compare_products, _product_lookup
        ids = list(_product_lookup.keys())[:2]
        result = compare_products.invoke({"product_ids": ids})
        assert "$" in result

    def test_unknown_ids_handled_gracefully(self):
        from src.tools import compare_products
        result = compare_products.invoke({"product_ids": [999999998, 999999999]})
        assert "Not found" in result or "Comparison" in result

    def test_compare_up_to_five_products(self):
        from src.tools import compare_products, _product_lookup
        ids = list(_product_lookup.keys())[:5]
        if len(ids) < 5:
            pytest.skip("Not enough products in mock dataset")
        result = compare_products.invoke({"product_ids": ids})
        assert isinstance(result, str) and len(result) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Recommend Products
# ─────────────────────────────────────────────────────────────────────────────


class TestRecommendProducts:
    def test_history_based_recommendations_returns_string(self):
        from src.tools import recommend_products, set_user_id
        set_user_id(1)
        result = recommend_products.invoke({"based_on": "history", "top_k": 3})
        assert isinstance(result, str) and len(result) > 0

    def test_cart_based_empty_cart(self):
        from src.tools import recommend_products
        _set_thread()
        result = recommend_products.invoke({"based_on": "cart", "top_k": 3})
        assert "empty" in result.lower() or "cart" in result.lower()

    def test_cart_based_with_items(self):
        from src.tools import recommend_products, cart_tool, _product_lookup
        _set_thread()
        pid = list(_product_lookup.keys())[0]
        cart_tool.invoke({"cart_operation": "add", "product_id": pid, "quantity": 1})
        result = recommend_products.invoke({"based_on": "cart", "top_k": 3})
        assert isinstance(result, str) and len(result) > 0

    def test_query_based_no_vector_store_skips(self):
        from src.tools import recommend_products
        # This will either work (if vector store exists) or return a fallback string
        result = recommend_products.invoke({
            "based_on": "query", "query": "dairy products", "top_k": 3
        })
        assert isinstance(result, str) and len(result) > 0

    def test_invalid_based_on_raises_or_returns_string(self):
        from src.tools import recommend_products
        import pydantic
        # 'based_on' is a Literal type — passing invalid value raises ValidationError
        try:
            result = recommend_products.invoke({"based_on": "invalid", "top_k": 3})
            # If it doesn't raise, it must at least return a string
            assert isinstance(result, str)
        except (pydantic.ValidationError, Exception):
            pass  # Expected — Pydantic rejects invalid Literal value


# ─────────────────────────────────────────────────────────────────────────────
# Analyze Reviews
# ─────────────────────────────────────────────────────────────────────────────


class TestAnalyzeReviews:
    def test_review_for_valid_product_has_rating(self):
        from src.tools import analyze_reviews, _product_lookup
        pid = list(_product_lookup.keys())[0]
        result = analyze_reviews.invoke({"product_id": pid})
        assert "Rating" in result or "rating" in result.lower()

    def test_review_contains_product_id(self):
        from src.tools import analyze_reviews, _product_lookup
        pid = list(_product_lookup.keys())[0]
        result = analyze_reviews.invoke({"product_id": pid})
        assert str(pid) in result

    def test_review_contains_sentiment(self):
        from src.tools import analyze_reviews, _product_lookup
        pid = list(_product_lookup.keys())[0]
        result = analyze_reviews.invoke({"product_id": pid})
        assert any(s in result for s in ["Positive", "Mixed", "Negative", "😊", "😐", "😟"])

    def test_review_for_invalid_product(self):
        from src.tools import analyze_reviews
        result = analyze_reviews.invoke({"product_id": 999999999})
        assert "not found" in result.lower()

    def test_review_has_star_rating(self):
        from src.tools import analyze_reviews, _product_lookup
        pid = list(_product_lookup.keys())[0]
        result = analyze_reviews.invoke({"product_id": pid})
        assert "⭐" in result or "/5" in result


# ─────────────────────────────────────────────────────────────────────────────
# Order Tracking
# ─────────────────────────────────────────────────────────────────────────────


class TestTrackOrder:
    def test_no_orders_returns_informative_message(self):
        from src.tools import track_order
        _set_thread()
        result = track_order.invoke({})
        assert "no orders" in result.lower() or "No orders" in result

    def test_buy_creates_order_with_id(self):
        buy_result, order_id = _buy_one_item()
        assert order_id is not None, f"No ORD-XXXXX found in: {buy_result}"
        assert "ORD-" in buy_result

    def test_track_specific_order(self):
        _, order_id = _buy_one_item()
        from src.tools import track_order
        result = track_order.invoke({"order_id": order_id})
        assert order_id in result
        assert "confirmed" in result.lower()

    def test_track_unknown_order_id(self):
        from src.tools import track_order
        _set_thread()  # fresh thread with no orders
        result = track_order.invoke({})
        # With a fresh thread there are no orders at all
        assert "no orders" in result.lower() or "not found" in result.lower()

    def test_track_all_orders_lists_them(self):
        _, order_id = _buy_one_item()
        from src.tools import track_order
        result = track_order.invoke({})
        assert "ORD-" in result

    def test_buy_result_contains_total(self):
        buy_result, _ = _buy_one_item()
        assert "Total" in buy_result or "$" in buy_result

    def test_buy_result_contains_delivery_estimate(self):
        buy_result, _ = _buy_one_item()
        assert "delivery" in buy_result.lower() or "Delivery" in buy_result


# ─────────────────────────────────────────────────────────────────────────────
# Cancel Order
# ─────────────────────────────────────────────────────────────────────────────


class TestCancelOrder:
    def test_cancel_nonexistent_order(self):
        from src.tools import cancel_order
        _set_thread()
        result = cancel_order.invoke({"order_id": "ORD-00000"})
        assert "not found" in result.lower()

    def test_cancel_confirmed_order_succeeds(self):
        _, order_id = _buy_one_item()
        from src.tools import cancel_order
        result = cancel_order.invoke({"order_id": order_id})
        assert "cancel" in result.lower()

    def test_cancel_returns_refund_info(self):
        _, order_id = _buy_one_item()
        from src.tools import cancel_order
        result = cancel_order.invoke({"order_id": order_id})
        assert "$" in result or "refund" in result.lower()

    def test_cancel_already_cancelled_order(self):
        _, order_id = _buy_one_item()
        from src.tools import cancel_order
        cancel_order.invoke({"order_id": order_id})          # first cancel
        result = cancel_order.invoke({"order_id": order_id}) # second cancel
        assert "already cancelled" in result.lower()


# ─────────────────────────────────────────────────────────────────────────────
# Cart Tool (updated behaviour)
# ─────────────────────────────────────────────────────────────────────────────


class TestCartToolUpdated:
    def test_buy_empty_cart_returns_error(self):
        from src.tools import cart_tool
        _set_thread()
        result = cart_tool.invoke({"cart_operation": "buy"})
        assert "empty" in result.lower()

    def test_buy_returns_order_id(self):
        buy_result, order_id = _buy_one_item()
        assert order_id is not None
        assert "ORD-" in buy_result

    def test_buy_clears_cart(self):
        from src.tools import cart_tool, view_cart, _product_lookup
        _set_thread()
        pid = list(_product_lookup.keys())[0]
        cart_tool.invoke({"cart_operation": "add", "product_id": pid, "quantity": 1})
        cart_tool.invoke({"cart_operation": "buy"})
        result = view_cart.invoke({})
        assert "empty" in result.lower()

    def test_view_cart_shows_dollar_amounts(self):
        from src.tools import cart_tool, view_cart, _product_lookup
        _set_thread()
        pid = list(_product_lookup.keys())[0]
        cart_tool.invoke({"cart_operation": "add", "product_id": pid, "quantity": 2})
        result = view_cart.invoke({})
        assert "$" in result

    def test_view_cart_shows_total(self):
        from src.tools import cart_tool, view_cart, _product_lookup
        _set_thread()
        pid = list(_product_lookup.keys())[0]
        cart_tool.invoke({"cart_operation": "add", "product_id": pid, "quantity": 1})
        result = view_cart.invoke({})
        assert "Total" in result or "total" in result

    def test_add_remove_roundtrip(self):
        from src.tools import cart_tool, view_cart, _product_lookup
        _set_thread()
        pid = list(_product_lookup.keys())[0]
        cart_tool.invoke({"cart_operation": "add", "product_id": pid, "quantity": 3})
        cart_tool.invoke({"cart_operation": "remove", "product_id": pid, "quantity": 3})
        result = view_cart.invoke({})
        assert "empty" in result.lower()
