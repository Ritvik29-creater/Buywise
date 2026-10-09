# src/tools.py
import os
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal, Optional, Union
from dotenv import load_dotenv

load_dotenv()
# Chroma / HuggingFace are imported lazily so the module loads even when
# langchain-chroma / langchain-huggingface are not yet installed.
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

# ------------------------------------------------------------------
# GLOBAL CONTEXT & DATA LOADING
# ------------------------------------------------------------------

_current_user_id: Optional[int] = None
_current_thread_id: Optional[str] = None


def set_user_id(uid: int):
    global _current_user_id
    _current_user_id = uid


def get_user_id() -> Optional[int]:
    return _current_user_id


def set_thread_id(tid: str):
    global _current_thread_id
    _current_thread_id = tid


# Load DataFrames safely
try:
    products = pd.read_csv("./dataset/products.csv", engine="python")
    departments = pd.read_csv("./dataset/departments.csv", engine="python")
    aisles = pd.read_csv("./dataset/aisles.csv", engine="python")
    prior = pd.read_csv("./dataset/order_products__prior.csv", engine="python")
    orders = pd.read_csv("./dataset/orders.csv", engine="python")

    _product_lookup = dict(zip(products["product_id"], products["product_name"]))
    _product_price_lookup = dict(zip(products["product_id"], products["price"])) if "price" in products.columns else {}
    _product_brand_lookup = dict(zip(products["product_id"], products["brand"])) if "brand" in products.columns else {}
    _product_rating_lookup = dict(zip(products["product_id"], products["rating"])) if "rating" in products.columns else {}
    _product_reviews_lookup = dict(zip(products["product_id"], products["review_count"])) if "review_count" in products.columns else {}
    _product_desc_lookup = dict(zip(products["product_id"], products["description"])) if "description" in products.columns else {}

    DEPARTMENT_NAMES = sorted(departments["department"].dropna().unique().tolist())
    VALID_USER_IDS = sorted(orders["user_id"].dropna().unique().tolist())
    DEFAULT_USER_ID = VALID_USER_IDS[0] if VALID_USER_IDS else 1
except Exception as e:
    print(f"WARNING: Could not load datasets: {e}")
    DEPARTMENT_NAMES = []
    DEFAULT_USER_ID = 1
    _product_lookup = {}
    _product_price_lookup = {}
    _product_brand_lookup = {}
    _product_rating_lookup = {}
    _product_reviews_lookup = {}
    _product_desc_lookup = {}


def get_product_price(pid: int) -> float:
    """Retrieve actual product price from catalog or generate reasonable fallback."""
    if pid in _product_price_lookup and pd.notna(_product_price_lookup[pid]):
        return float(_product_price_lookup[pid])
    return round((int(pid) % 100) * 0.1 + 1.99, 2)


# ------------------------------------------------------------------
# VECTOR STORE (RAG) SETUP
# ------------------------------------------------------------------

CHROMA_DIR = "./vector_db"
CHROMA_COLLECTION = "product_catalog"
_vector_store = None


def get_vector_store():
    """Singleton accessor for the Chroma Vector Store (uses Gemini embeddings if key set, else HuggingFace)."""
    global _vector_store
    if _vector_store is None:
        import os
        from langchain_chroma import Chroma
        key = os.getenv("GOOGLE_API_KEY")
        emb_model = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-2")
        if key:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            embeddings = GoogleGenerativeAIEmbeddings(model=emb_model, google_api_key=key)
        else:
            try:
                from langchain_huggingface import HuggingFaceEmbeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={"device": "cpu"},
                    encode_kwargs={"normalize_embeddings": True},
                )
            except ImportError as exc:
                raise ImportError(
                    "Vector search requires: pip install langchain-chroma langchain-huggingface"
                ) from exc
        _vector_store = Chroma(
            collection_name=CHROMA_COLLECTION,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
        )
    return _vector_store


def make_query_prompt(query: str) -> str:
    """Formats the query for better embedding retrieval."""
    return f"Represent this sentence for searching relevant passages: {query.strip().replace(chr(10), ' ')}"


# ------------------------------------------------------------------
# SEARCH TOOLS
# ------------------------------------------------------------------


def search_products(query: str, top_k: int = 5) -> List[Dict]:
    """
    Perform a semantic vector search over the product catalog.
    """
    try:
        vector_store = get_vector_store()
        query_prompt = make_query_prompt(query)
        results = vector_store.similarity_search(query_prompt, k=top_k)
        formatted_results = []
        for doc in results:
            pid = doc.metadata.get("product_id")
            price = doc.metadata.get("price")
            if price is None and pid:
                price = get_product_price(int(pid))
            formatted_results.append(
                {
                    "product_id": pid,
                    "product_name": doc.metadata.get("product_name"),
                    "brand": doc.metadata.get("brand", _product_brand_lookup.get(pid, "")),
                    "price": float(price) if price is not None else 0.0,
                    "rating": doc.metadata.get("rating", _product_rating_lookup.get(pid, 4.8)),
                    "review_count": doc.metadata.get("review_count", _product_reviews_lookup.get(pid, 120)),
                    "aisle": doc.metadata.get("aisle"),
                    "department": doc.metadata.get("department"),
                    "description": doc.metadata.get("description", _product_desc_lookup.get(pid, "")),
                    "text": doc.page_content,
                }
            )
        return formatted_results
    except Exception as e:
        print(f"Vector search failed: {e}")
        return []


@tool
def search_tool(query: str) -> str:
    """
    Look up products by meaning (e.g., "laptop for programming", "noise cancelling headphones", "espresso machine").
    Returns matching products with brand, price, rating, reviews, aisle, and description.
    """
    matches = search_products(query)

    if not matches:
        return "No products found matching your search. Try different keywords or browse departments."

    lines = []
    for item in matches:
        brand_tag = f"🏷️ Brand: {item['brand']} | " if item.get('brand') else ""
        price_val = item.get('price', 0.0)
        rating_val = item.get('rating', 4.8)
        rev_val = item.get('review_count', 0)
        desc_val = item.get('description') or item.get('text', '')[:120]
        lines.append(
            f"📦 **{item['product_name']}** (ID: {item['product_id']})\n"
            f"   {brand_tag}📍 {item['department']} → {item['aisle']}\n"
            f"   💰 **${price_val:.2f}** | ⭐ {rating_val}/5.0 ({rev_val:,} reviews)\n"
            f"   📝 {desc_val}"
        )
    return "\n\n".join(lines)


@tool
def structured_search_tool(
    product_name: Optional[str] = None,
    department: Optional[str] = None,
    aisle: Optional[str] = None,
    reordered: Optional[bool] = None,
    min_orders: Optional[int] = None,
    order_by: Optional[Literal["count", "add_to_cart_order"]] = None,
    ascending: Optional[bool] = False,
    top_k: Optional[int] = None,
    group_by: Optional[Literal["department", "aisle"]] = None,
    history_only: Optional[bool] = False,
) -> List[Dict[str, Any]]:
    """
    Filter the catalog using SQL-like criteria.
    Use history_only=True to search the user's past purchases.
    """
    try:
        if history_only:
            user_id = get_user_id() or DEFAULT_USER_ID
            user_orders = orders[orders["user_id"] == user_id]["order_id"]
            if user_orders.empty:
                return []
            user_products = prior[prior["order_id"].isin(user_orders)]
            df = user_products.merge(products, on="product_id")
            stats = (
                df.groupby("product_id")
                .agg(
                    count=("product_id", "count"),
                    avg_cart_pos=("add_to_cart_order", "mean"),
                    reordered_sum=("reordered", "sum"),
                )
                .reset_index()
            )
            df_unique = products[products["product_id"].isin(stats["product_id"])].copy()
            df = df_unique.merge(stats, on="product_id")
        else:
            df = products.copy()

        df = df.merge(aisles, on="aisle_id", how="left")
        df = df.merge(departments, on="department_id", how="left")

        if product_name:
            df = df[df["product_name"].str.contains(product_name, case=False, na=False)]
        if department:
            df = df[df["department"] == department]
        if aisle:
            df = df[df["aisle"].str.contains(aisle, case=False, na=False)]
        if history_only:
            if reordered is True:
                df = df[df["reordered_sum"] > 0]
            if min_orders:
                df = df[df["count"] >= min_orders]

        if group_by:
            if group_by not in df.columns:
                return [{"error": f"Cannot group by {group_by}"}]
            counts = df[group_by].value_counts().reset_index()
            counts.columns = [group_by, "num_products"]
            return counts.to_dict(orient="records")

        if order_by and history_only:
            col_map = {"count": "count", "add_to_cart_order": "avg_cart_pos"}
            sort_col = col_map.get(order_by)
            if sort_col:
                df = df.sort_values(by=sort_col, ascending=ascending)

        if top_k:
            df = df.head(top_k)

        return df.to_dict(orient="records")

    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


# ------------------------------------------------------------------
# PRODUCT COMPARISON TOOL
# ------------------------------------------------------------------


@tool
def compare_products(product_ids: List[int]) -> str:
    """
    Compare multiple products side-by-side by their product IDs.
    Provide a list of 2-5 product IDs to compare their details including
    name, aisle, department, and purchase popularity.
    """
    if not product_ids or len(product_ids) < 2:
        return "Please provide at least 2 product IDs to compare."
    if len(product_ids) > 5:
        return "Please provide at most 5 product IDs to compare."

    try:
        # Build merged product info
        df = products.copy()
        df = df.merge(aisles, on="aisle_id", how="left")
        df = df.merge(departments, on="department_id", how="left")

        # Get purchase counts from order history
        product_counts = prior.groupby("product_id").size().reset_index(name="total_orders")
        reorder_rates = (
            prior.groupby("product_id")["reordered"].mean().reset_index(name="reorder_rate")
        )
        df = df.merge(product_counts, on="product_id", how="left")
        df = df.merge(reorder_rates, on="product_id", how="left")
        df["total_orders"] = df["total_orders"].fillna(0).astype(int)
        df["reorder_rate"] = df["reorder_rate"].fillna(0.0)

        results = []
        for pid in product_ids:
            row = df[df["product_id"] == pid]
            if row.empty:
                results.append(f"❌ Product ID {pid}: Not found in catalog")
                continue
            r = row.iloc[0]
            price = get_product_price(int(pid))
            brand = _product_brand_lookup.get(pid, "")
            rating = _product_rating_lookup.get(pid, 4.8)
            popularity = "🔥 Best Seller" if r["total_orders"] > 3 else (
                "⭐ Popular" if r["total_orders"] > 1 else "📦 Standard"
            )
            reorder = f"{r['reorder_rate']*100:.0f}% reorder rate"
            brand_str = f"🏷️ {brand} | " if brand else ""
            results.append(
                f"📦 **{r['product_name']}** (ID: {pid})\n"
                f"   {brand_str}📍 {r['department']} → {r['aisle']}\n"
                f"   💰 **${price:.2f}** | ⭐ {rating}/5.0\n"
                f"   {popularity} | {reorder}"
            )

        header = f"=== Product Comparison ({len(product_ids)} items) ===\n\n"
        return header + "\n\n".join(results)

    except Exception as e:
        return f"Comparison failed: {str(e)}"


# ------------------------------------------------------------------
# PRODUCT RECOMMENDATION TOOL
# ------------------------------------------------------------------


@tool
def recommend_products(
    based_on: Literal["history", "cart", "query"] = "history",
    query: Optional[str] = None,
    top_k: int = 5,
) -> str:
    """
    Get personalized product recommendations.
    - based_on='history': Recommends items frequently bought alongside your past purchases.
    - based_on='cart': Recommends items that complement your current cart.
    - based_on='query': Semantic recommendations for a natural language query.
    """
    try:
        if based_on == "query" and query:
            try:
                matches = search_products(query, top_k=top_k)
            except ImportError:
                return "Vector search not available. Install langchain-chroma and langchain-huggingface first."
            if not matches:
                return "No recommendations found for that query."
            lines = [f"🎯 Recommendations for '{query}':\n"]
            for i, item in enumerate(matches, 1):
                lines.append(
                    f"{i}. {item['product_name']} (ID: {item['product_id']})\n"
                    f"   🏪 {item['aisle']} → {item['department']}"
                )
            return "\n".join(lines)

        elif based_on == "history":
            user_id = get_user_id() or DEFAULT_USER_ID
            user_orders = orders[orders["user_id"] == user_id]["order_id"]
            if user_orders.empty:
                return "No purchase history found. Try a query-based recommendation instead."

            # Get user's bought products
            bought = prior[prior["order_id"].isin(user_orders)]["product_id"].unique()

            # Find co-purchased products: products bought by users who also bought same items
            # Collaborative filtering simplified: find top products in same departments
            if len(bought) == 0:
                return "No purchase history found."

            # Get departments of bought items
            bought_df = products[products["product_id"].isin(bought)]
            bought_df = bought_df.merge(departments, on="department_id", how="left")
            top_depts = bought_df["department"].value_counts().head(3).index.tolist()

            # Recommend popular items in those departments that user hasn't bought
            all_dept_products = products.merge(departments, on="department_id", how="left")
            dept_products = all_dept_products[
                all_dept_products["department"].isin(top_depts)
                & ~all_dept_products["product_id"].isin(bought)
            ]

            # Score by popularity
            pop_counts = prior.groupby("product_id").size().reset_index(name="cnt")
            dept_products = dept_products.merge(pop_counts, on="product_id", how="left")
            dept_products["cnt"] = dept_products["cnt"].fillna(0)
            dept_products = dept_products.sort_values("cnt", ascending=False).head(top_k)
            dept_products = dept_products.merge(aisles, on="aisle_id", how="left")

            if dept_products.empty:
                return "Could not generate history-based recommendations."

            lines = ["🎯 Personalized Recommendations (based on your history):\n"]
            for i, (_, row) in enumerate(dept_products.iterrows(), 1):
                lines.append(
                    f"{i}. {row['product_name']} (ID: {row['product_id']})\n"
                    f"   🏪 {row.get('aisle', 'N/A')} → {row['department']}"
                )
            return "\n".join(lines)

        elif based_on == "cart":
            cart = get_cart()
            if isinstance(cart, list) or not cart:
                return "Your cart is empty. Add some items first for cart-based recommendations."

            cart_product_ids = list(cart.keys())
            cart_df = products[products["product_id"].isin(cart_product_ids)]
            cart_df = cart_df.merge(departments, on="department_id", how="left")
            cart_depts = cart_df["department"].unique().tolist()

            # Find popular items in same departments not already in cart
            all_dept = products.merge(departments, on="department_id", how="left")
            candidates = all_dept[
                all_dept["department"].isin(cart_depts)
                & ~all_dept["product_id"].isin(cart_product_ids)
            ]
            pop_counts = prior.groupby("product_id").size().reset_index(name="cnt")
            candidates = candidates.merge(pop_counts, on="product_id", how="left")
            candidates["cnt"] = candidates["cnt"].fillna(0)
            candidates = candidates.sort_values("cnt", ascending=False).head(top_k)
            candidates = candidates.merge(aisles, on="aisle_id", how="left")

            if candidates.empty:
                return "Could not generate cart-based recommendations."

            lines = ["🎯 You might also like (based on your cart):\n"]
            for i, (_, row) in enumerate(candidates.iterrows(), 1):
                lines.append(
                    f"{i}. {row['product_name']} (ID: {row['product_id']})\n"
                    f"   🏪 {row.get('aisle', 'N/A')} → {row['department']}"
                )
            return "\n".join(lines)

        return "Invalid recommendation type. Use 'history', 'cart', or 'query'."

    except Exception as e:
        return f"Recommendation error: {str(e)}"


# ------------------------------------------------------------------
# REVIEW ANALYSIS TOOL
# ------------------------------------------------------------------

# Simulated review database (deterministic based on product_id)
_REVIEW_TEMPLATES = [
    ("Great product! Highly recommend.", 5),
    ("Good quality, will buy again.", 4),
    ("Decent product, meets expectations.", 3),
    ("Fresh and tasty, exactly as described.", 5),
    ("A bit pricey but worth it.", 4),
    ("Not what I expected, somewhat disappointed.", 2),
    ("My family loves this! A household staple.", 5),
    ("Good value for money.", 4),
    ("Arrived in perfect condition, very fresh.", 5),
    ("Average product, nothing special.", 3),
    ("Excellent quality, always fresh.", 5),
    ("Good, but packaging could be better.", 3),
]


def _generate_fake_reviews(product_id: int, count: int = 5) -> List[Dict]:
    """Generate deterministic fake reviews for a product."""
    random.seed(product_id)
    reviews = []
    for i in range(count):
        idx = (product_id + i) % len(_REVIEW_TEMPLATES)
        text, rating = _REVIEW_TEMPLATES[idx]
        reviews.append({"rating": rating, "review": text})
    return reviews


@tool
def analyze_reviews(product_id: int) -> str:
    """
    Analyze customer reviews for a product.
    Returns average rating, sentiment summary, and key highlights.
    Provide a product_id obtained from search results.
    """
    try:
        product_name = _product_lookup.get(product_id)
        if not product_name:
            return f"Product ID {product_id} not found in catalog."

        reviews = _generate_fake_reviews(product_id)
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
        positive = [r["review"] for r in reviews if r["rating"] >= 4]
        neutral = [r["review"] for r in reviews if r["rating"] == 3]
        negative = [r["review"] for r in reviews if r["rating"] <= 2]

        stars = "⭐" * round(avg_rating)
        sentiment = "😊 Positive" if avg_rating >= 4 else ("😐 Mixed" if avg_rating >= 3 else "😟 Negative")

        lines = [
            f"📊 Reviews for **{product_name}** (ID: {product_id})",
            f"   Rating: {stars} {avg_rating:.1f}/5.0 ({len(reviews)} reviews)",
            f"   Sentiment: {sentiment}",
        ]
        if positive:
            lines.append(f"\n✅ Highlights: \"{positive[0]}\"")
        if negative:
            lines.append(f"\n⚠️  Concern: \"{negative[0]}\"")

        # Purchase popularity context
        try:
            total_orders = len(prior[prior["product_id"] == product_id])
            reorder_rate = prior[prior["product_id"] == product_id]["reordered"].mean()
            lines.append(f"\n📈 Ordered {total_orders:,} times | Reorder rate: {reorder_rate*100:.0f}%")
        except Exception:
            pass

        return "\n".join(lines)

    except Exception as e:
        return f"Review analysis failed: {str(e)}"


# ------------------------------------------------------------------
# ORDER TRACKING & MANAGEMENT TOOLS
# ------------------------------------------------------------------

# In-memory order store (keyed by thread_id)
_order_storage: Dict[str, List[Dict]] = {}


def _get_orders_for_thread() -> List[Dict]:
    if _current_thread_id is None:
        return []
    return _order_storage.setdefault(_current_thread_id, [])


def _place_order(cart: Dict[int, int]) -> Dict:
    """Create an order record from cart contents."""
    order_id = f"ORD-{random.randint(10000, 99999)}"
    now = datetime.now()
    estimated_delivery = now + timedelta(days=random.randint(2, 5))
    items = []
    total = 0.0
    for pid, qty in cart.items():
        name = _product_lookup.get(pid, "Unknown Product")
        price = get_product_price(int(pid))
        items.append({"product_id": pid, "name": name, "quantity": qty, "price": price})
        total += qty * price
    return {
        "order_id": order_id,
        "status": "confirmed",
        "placed_at": now.strftime("%Y-%m-%d %H:%M"),
        "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d"),
        "items": items,
        "total": round(total, 2),
        "cancellable": True,
        "refund_eligible": False,
    }


@tool
def track_order(order_id: Optional[str] = None) -> str:
    """
    Track the status of your orders.
    If order_id is provided, shows details for that specific order.
    Otherwise, lists all orders for this session.
    """
    order_list = _get_orders_for_thread()

    if not order_list:
        return (
            "No orders found for this session. "
            "Place an order by using the cart_tool with operation='buy'."
        )

    if order_id:
        order = next((o for o in order_list if o["order_id"] == order_id), None)
        if not order:
            return f"Order {order_id} not found."
        items_text = "\n".join(
            f"  - {item['name']} × {item['quantity']} (${item['price']:.2f} ea)"
            for item in order["items"]
        )
        status_icon = {"confirmed": "✅", "shipped": "🚚", "delivered": "📦", "cancelled": "❌"}.get(
            order["status"], "❓"
        )
        return (
            f"{status_icon} **Order {order['order_id']}**\n"
            f"   Status: {order['status'].upper()}\n"
            f"   Placed: {order['placed_at']}\n"
            f"   Est. Delivery: {order['estimated_delivery']}\n"
            f"   Items:\n{items_text}\n"
            f"   Total: ${order['total']:.2f}"
        )

    # List all orders
    lines = [f"📋 Your Orders ({len(order_list)} total):\n"]
    for order in order_list:
        status_icon = {"confirmed": "✅", "shipped": "🚚", "delivered": "📦", "cancelled": "❌"}.get(
            order["status"], "❓"
        )
        lines.append(
            f"{status_icon} {order['order_id']} | {order['status'].upper()} | "
            f"${order['total']:.2f} | Est. {order['estimated_delivery']}"
        )
    return "\n".join(lines)


@tool
def cancel_order(order_id: str) -> str:
    """
    Cancel a pending order by order ID.
    Orders can only be cancelled if they have not yet shipped.
    Provide the exact order ID (e.g. ORD-12345).
    """
    order_list = _get_orders_for_thread()
    order = next((o for o in order_list if o["order_id"] == order_id), None)

    if not order:
        return f"❌ Order {order_id} not found in this session."

    if order["status"] in ("shipped", "delivered"):
        return (
            f"❌ Cannot cancel order {order_id} — it has already {order['status']}. "
            f"Please contact support to request a refund instead."
        )

    if order["status"] == "cancelled":
        return f"Order {order_id} is already cancelled."

    order["status"] = "cancelled"
    order["cancellable"] = False
    order["refund_eligible"] = True
    return (
        f"✅ Order {order_id} has been successfully cancelled.\n"
        f"   A refund of ${order['total']:.2f} will be processed within 3-5 business days.\n"
        f"   Refund eligible: Yes"
    )


# ------------------------------------------------------------------
# CART TOOLS
# ------------------------------------------------------------------

_cart_storage: Dict[str, Dict[int, int]] = {}


def get_cart() -> Union[List[str], Dict[int, int]]:
    if _current_thread_id is None:
        return ["Session error: no thread ID set."]
    return _cart_storage.setdefault(_current_thread_id, {})


@tool
def cart_tool(
    cart_operation: Literal["add", "remove", "update", "buy"],
    product_id: Optional[int] = None,
    quantity: int = 1,
) -> str:
    """
    Manage the shopping cart.
    Operations: 'add', 'remove', 'update', 'buy'.
    - 'buy': Places an order, clears cart, and returns an order ID for tracking.
    """
    cart = get_cart()
    if isinstance(cart, list):
        return cart[0]  # Error state

    try:
        if cart_operation == "buy":
            if not cart:
                return "Cart is empty. Add some items first."
            # Create order record
            order = _place_order(dict(cart))
            orders_list = _get_orders_for_thread()
            orders_list.append(order)
            cart.clear()
            items_summary = ", ".join(
                f"{item['name']} ×{item['quantity']}" for item in order["items"]
            )
            return (
                f"✅ Order placed successfully!\n"
                f"   Order ID: **{order['order_id']}**\n"
                f"   Items: {items_summary}\n"
                f"   Total: ${order['total']:.2f}\n"
                f"   Estimated delivery: {order['estimated_delivery']}\n"
                f"   Use track_order('{order['order_id']}') to check status."
            )

        if not product_id:
            return "Product ID required."

        product_name = _product_lookup.get(product_id, "Unknown Product")

        if cart_operation == "add":
            cart[product_id] = cart.get(product_id, 0) + quantity
            return f"Added {quantity} × {product_name} (ID: {product_id}). Total in cart: {cart[product_id]}"

        elif cart_operation == "update":
            if product_id not in cart:
                return "Item not in cart."
            cart[product_id] = quantity
            return f"Updated {product_name} quantity to {quantity}."

        elif cart_operation == "remove":
            if product_id not in cart:
                return "Item not in cart."
            current_qty = cart[product_id]
            if quantity >= current_qty:
                del cart[product_id]
                return f"Removed {product_name} from cart."
            else:
                cart[product_id] -= quantity
                return f"Removed {quantity} × {product_name}. Remaining: {cart[product_id]}"

    except Exception as e:
        return f"Cart Error: {str(e)}"

    return "Invalid operation"


@tool
def view_cart() -> str:
    """Returns the current cart contents with estimated prices."""
    cart = get_cart()
    if isinstance(cart, list):
        return cart[0]

    if not cart:
        return "Your cart is empty."

    lines = ["Your cart contains:"]
    total = 0.0
    for pid, qty in cart.items():
        name = _product_lookup.get(pid, "Unknown Product")
        price = get_product_price(int(pid))
        subtotal = price * qty
        total += subtotal
        lines.append(f"- {name} (ID: {pid}) × {qty} — ${price:.2f} ea = ${subtotal:.2f}")
    lines.append(f"\n💰 Total: ${total:.2f}")
    return "\n".join(lines)


# ------------------------------------------------------------------
# ESCALATION TOOLS & ERROR HANDLING
# ------------------------------------------------------------------


class RouteToCustomerSupport(BaseModel):
    """Signal to escalate the conversation to human support."""

    reason: str = Field(description="The reason why the customer needs support.")


class EscalateToHuman(BaseModel):
    """Submit a request for human supervisor approval (Support Agent only)."""

    severity: Literal["low", "medium", "high"] = Field(
        description="Severity of the issue."
    )
    summary: str = Field(description="Brief summary of the issue.")


class Search(BaseModel):
    query: str = Field(description="Natural language search query")


def handle_tool_error(state: Dict[str, Any]) -> dict:
    """Fallback function for when tools fail."""
    error = state.get("error")
    try:
        tool_calls = state["messages"][-1].tool_calls
        return {
            "messages": [
                ToolMessage(
                    content=f"Error: {repr(error)}\nPlease fix your arguments and try again.",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }
    except Exception:
        return {"messages": []}


def create_tool_node_with_fallback(tools: list) -> ToolNode:
    """
    Create a ToolNode that handles errors automatically.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


__all__ = [
    "RouteToCustomerSupport",
    "EscalateToHuman",
    "Search",
    "search_products",
    "search_tool",
    "structured_search_tool",
    "compare_products",
    "recommend_products",
    "analyze_reviews",
    "cart_tool",
    "view_cart",
    "track_order",
    "cancel_order",
    "handle_tool_error",
    "create_tool_node_with_fallback",
    "get_cart",
    "set_thread_id",
    "set_user_id",
    "get_user_id",
    "_product_lookup",
    "DEFAULT_USER_ID",
    "DEPARTMENT_NAMES",
]
