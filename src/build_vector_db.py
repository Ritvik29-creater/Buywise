# src/build_vector_db.py
import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

DATASET_DIR = os.getenv("DATASET_DIR", "./dataset")
CHROMA_DIR = os.getenv("VECTOR_DB_PATH", "./vector_db")
CHROMA_COLLECTION = "product_catalog"


def get_embeddings():
    """Returns Gemini embeddings if GOOGLE_API_KEY exists, else falls back to HuggingFace."""
    key = os.getenv("GOOGLE_API_KEY")
    emb_model = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-2")
    if key:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model=emb_model, google_api_key=key)
    else:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )


def make_product_embedding_text(row):
    """Construct rich semantic representation of product for embedding."""
    name = row.get("product_name", "")
    brand = row.get("brand", "")
    aisle = row.get("aisle", "")
    dept = row.get("department", "")
    price = row.get("price", 0.0)
    rating = row.get("rating", "")
    desc = row.get("description", "")

    parts = [f"{name}."]
    if brand and pd.notna(brand):
        parts.append(f"Brand: {brand}.")
    if dept and pd.notna(dept):
        parts.append(f"Department: {dept}, Aisle: {aisle}.")
    if price and pd.notna(price):
        parts.append(f"Price: ${float(price):.2f}.")
    if rating and pd.notna(rating):
        parts.append(f"Rating: {rating} stars.")
    if desc and pd.notna(desc):
        parts.append(f"Features: {desc}")
    return " ".join(parts)


def load_and_prepare_product_catalog(dataset_dir=DATASET_DIR):
    products = pd.read_csv(os.path.join(dataset_dir, "products.csv"), engine="python")
    aisles = pd.read_csv(os.path.join(dataset_dir, "aisles.csv"), engine="python")
    departments = pd.read_csv(os.path.join(dataset_dir, "departments.csv"), engine="python")

    # Filter: keep only rows where aisle_id and department_id are both numeric
    is_aisle_numeric = products["aisle_id"].astype(str).str.strip().str.isnumeric()
    is_dept_numeric = products["department_id"].astype(str).str.strip().str.isnumeric()
    products = products[is_aisle_numeric & is_dept_numeric].copy()

    # Cast merge keys to int
    products["aisle_id"] = products["aisle_id"].astype(int)
    products["department_id"] = products["department_id"].astype(int)

    merged = products.merge(aisles, on="aisle_id", how="left").merge(
        departments, on="department_id", how="left"
    )
    merged["embedding_text"] = merged.apply(make_product_embedding_text, axis=1)
    return merged


def make_langchain_documents(df):
    docs = []
    for _, row in df.iterrows():
        meta = {
            "product_id": int(row["product_id"]),
            "product_name": str(row["product_name"]),
            "aisle": str(row.get("aisle", "")),
            "department": str(row.get("department", "")),
        }
        if "price" in row and pd.notna(row["price"]):
            meta["price"] = float(row["price"])
        if "rating" in row and pd.notna(row["rating"]):
            meta["rating"] = float(row["rating"])
        if "review_count" in row and pd.notna(row["review_count"]):
            meta["review_count"] = int(row["review_count"])
        if "brand" in row and pd.notna(row["brand"]):
            meta["brand"] = str(row["brand"])
        if "description" in row and pd.notna(row["description"]):
            meta["description"] = str(row["description"])

        docs.append(Document(page_content=row["embedding_text"], metadata=meta))
    return docs


def build_and_persist_chroma(docs, persist_directory=CHROMA_DIR, batch_size=40):
    import time
    print(f"Embedding {len(docs)} documents into Chroma vector store in batches of {batch_size}...")

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )

    for i in range(0, len(docs), batch_size):
        chunk = docs[i : i + batch_size]
        print(f"Embedding batch {i + 1} - {i + len(chunk)} of {len(docs)}...")
        for attempt in range(5):
            try:
                vector_store.add_documents(documents=chunk)
                break
            except Exception as e:
                print(f"Rate limit / retry ({e}). Waiting 6 seconds...")
                time.sleep(6)
        if i + batch_size < len(docs):
            time.sleep(4)

    print(f"[OK] Chroma DB built and persisted ({len(docs)} products) at: {persist_directory}")


if __name__ == "__main__":
    df = load_and_prepare_product_catalog()
    docs = make_langchain_documents(df)
    build_and_persist_chroma(docs)
    print("[OK] Vector DB built and ready.")
