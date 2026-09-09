import json
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

def load_products() -> List[Dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search_products(query: str, max_price: float | None = None) -> List[Dict]:
    products = load_products()
    words = set(query.lower().split())

    scored = []
    for product in products:
        searchable = (
            product["name"] + " " +
            product["category"] + " " +
            " ".join(product["features"])
        ).lower()

        score = sum(word in searchable for word in words)

        if max_price is not None and product["price"] > max_price:
            continue

        if score > 0:
            scored.append((score, product))

    scored.sort(key=lambda item: (-item[0], item[1]["price"]))
    return [product for _, product in scored]

def compare_products(product_ids: List[int]) -> List[Dict]:
    products = load_products()
    selected = [p for p in products if p["id"] in product_ids]
    return selected
