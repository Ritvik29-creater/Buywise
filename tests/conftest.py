"""
tests/conftest.py — Shared pytest fixtures.
Creates a lightweight mock dataset so tests run without the full download.
"""
import os
import sys
import shutil
import pytest
import pandas as pd

# Ensure src is importable from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset")


def _create_mock_dataset():
    """Create minimal CSV files so tools.py can load without errors."""
    os.makedirs(DATASET_DIR, exist_ok=True)

    # products.csv
    products = pd.DataFrame([
        {"product_id": 1, "product_name": "Organic Bananas",      "aisle_id": 24, "department_id": 4},
        {"product_id": 2, "product_name": "Whole Milk",           "aisle_id": 84, "department_id": 16},
        {"product_id": 3, "product_name": "Sourdough Bread",      "aisle_id": 112,"department_id": 3},
        {"product_id": 4, "product_name": "Greek Yogurt",         "aisle_id": 120,"department_id": 16},
        {"product_id": 5, "product_name": "Almond Milk",          "aisle_id": 91, "department_id": 16},
        {"product_id": 6, "product_name": "Oat Milk",             "aisle_id": 91, "department_id": 16},
        {"product_id": 7, "product_name": "Orange Juice",         "aisle_id": 98, "department_id": 7},
        {"product_id": 8, "product_name": "Granola Bar",          "aisle_id": 50, "department_id": 19},
        {"product_id": 9, "product_name": "Chicken Breast",       "aisle_id": 49, "department_id": 12},
        {"product_id": 10,"product_name": "Sparkling Water",      "aisle_id": 115,"department_id": 7},
    ])
    products.to_csv(os.path.join(DATASET_DIR, "products.csv"), index=False)

    # aisles.csv
    aisles = pd.DataFrame([
        {"aisle_id": 24,  "aisle": "fresh fruits"},
        {"aisle_id": 84,  "aisle": "milk"},
        {"aisle_id": 112, "aisle": "bread"},
        {"aisle_id": 120, "aisle": "yogurt"},
        {"aisle_id": 91,  "aisle": "soy lactosefree"},
        {"aisle_id": 98,  "aisle": "juice nectars"},
        {"aisle_id": 50,  "aisle": "granola bars"},
        {"aisle_id": 49,  "aisle": "poultry counter"},
        {"aisle_id": 115, "aisle": "water seltzer sparkling water"},
    ])
    aisles.to_csv(os.path.join(DATASET_DIR, "aisles.csv"), index=False)

    # departments.csv
    departments = pd.DataFrame([
        {"department_id": 4,  "department": "produce"},
        {"department_id": 16, "department": "dairy eggs"},
        {"department_id": 3,  "department": "bakery"},
        {"department_id": 7,  "department": "beverages"},
        {"department_id": 19, "department": "snacks"},
        {"department_id": 12, "department": "meat seafood"},
    ])
    departments.to_csv(os.path.join(DATASET_DIR, "departments.csv"), index=False)

    # orders.csv (2 users, 3 orders)
    orders = pd.DataFrame([
        {"order_id": 100, "user_id": 1, "order_number": 1, "order_dow": 0, "order_hour_of_day": 10, "days_since_prior_order": 0},
        {"order_id": 101, "user_id": 1, "order_number": 2, "order_dow": 1, "order_hour_of_day": 11, "days_since_prior_order": 7},
        {"order_id": 102, "user_id": 2, "order_number": 1, "order_dow": 2, "order_hour_of_day": 14, "days_since_prior_order": 0},
    ])
    orders.to_csv(os.path.join(DATASET_DIR, "orders.csv"), index=False)

    # order_products__prior.csv
    prior = pd.DataFrame([
        {"order_id": 100, "product_id": 1, "add_to_cart_order": 1, "reordered": 0},
        {"order_id": 100, "product_id": 2, "add_to_cart_order": 2, "reordered": 0},
        {"order_id": 101, "product_id": 1, "add_to_cart_order": 1, "reordered": 1},
        {"order_id": 101, "product_id": 3, "add_to_cart_order": 2, "reordered": 0},
        {"order_id": 102, "product_id": 4, "add_to_cart_order": 1, "reordered": 0},
        {"order_id": 102, "product_id": 5, "add_to_cart_order": 2, "reordered": 0},
    ])
    prior.to_csv(os.path.join(DATASET_DIR, "order_products__prior.csv"), index=False)


# ── Auto-create mock dataset before any test collects ────────────────────────
_dataset_ready = False


def pytest_configure(config):
    """Called early — create mock dataset before any imports happen."""
    global _dataset_ready
    products_path = os.path.join(DATASET_DIR, "products.csv")
    if not os.path.exists(products_path):
        _create_mock_dataset()
        print(f"\n[INFO] Mock dataset created at {DATASET_DIR}")
    _dataset_ready = True


@pytest.fixture(scope="session", autouse=True)
def mock_dataset():
    """Session-scoped fixture: ensures mock dataset exists for all tests."""
    products_path = os.path.join(DATASET_DIR, "products.csv")
    if not os.path.exists(products_path):
        _create_mock_dataset()
    yield
    # Cleanup is optional — leave dataset in place for faster re-runs


@pytest.fixture
def unique_thread_id():
    """Provides a unique thread ID per test to isolate cart state."""
    import uuid
    from src.tools import set_thread_id
    tid = str(uuid.uuid4())
    set_thread_id(tid)
    return tid
