# 🛒 SmartShop Elite: Autonomous Retail Agent

> A production-grade Multi-Agent System for e-commerce, built with LangGraph, Google Gemini, ChromaDB, and Streamlit.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| **Multi-Agent Orchestration** | LangGraph StateGraph routing between Sales Agent and Support Agent |
| **Semantic Product Search (RAG)** | ChromaDB + Sentence-Transformers over 50,000+ products |
| **Product Comparison** | Side-by-side comparison with popularity metrics |
| **Personalized Recommendations** | History-based, cart-based, and query-based recommendation engine |
| **Review Analysis** | Sentiment summary, star ratings, and purchase trends |
| **Cart Management** | Add, remove, update, and checkout with real order IDs |
| **Order Tracking** | Full order lifecycle: confirm → track → cancel |
| **Human-in-the-Loop** | Supervisor interrupt for refunds and high-severity issues |
| **LangSmith Observability** | Full trace logging when configured |
| **Docker Support** | One-command deployment with Redis |

---

## 🏗️ Architecture

```
User ──► Streamlit UI ──► LangGraph StateGraph
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
        Sales Agent                      Support Agent
        (Discovery)                      (Resolution)
              │                                 │
   ┌──────────┼──────────┐            ┌─────────┼─────────┐
   │          │          │            │         │         │
search   compare   recommend     track_order cancel  EscalateToHuman
_tool   _products  _products     (shared)   _order        │
   │          │          │                               ▼
structured  analyze    cart_tool                  Human Supervisor
_search    _reviews   view_cart                  (Interrupt Node)
                      track_order
```

### Graph Flow

```
START ──► [route_start] ──► sales_rep ──► [route_sales] ──► sales_tools
                │                                                │
                └──► customer_support ◄── after_sales_tool ◄────┘
                           │
                      [route_support]
                           │
                      support_tools ──► after_support_tool
                                               │
                                        need_human_approval?
                                          ▼         ▼
                                     human_approval  customer_support ──► END
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph 0.4+ |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | ChromaDB (local persistence) |
| Structured Data | Pandas |
| UI | Streamlit |
| Caching | Redis |
| Observability | LangSmith |
| Containerization | Docker + Docker Compose |

---

## ⚡ Quick Start

### Option A: Local Development (Recommended)

```bash
# 1. Clone
git clone https://github.com/clezcano/LangGraph-Retail-Assistant.git
cd LangGraph-Retail-Assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# 3. One-shot setup (installs deps, downloads data, builds vector DB)
python setup.py

# 4. Add your API key
cp .env.example .env
# Edit .env and set: GOOGLE_API_KEY="your-key-here"

# 5. Launch
streamlit run app.py
```

App runs at **http://localhost:8501**

### Option B: Docker

```bash
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY

# First-time: download dataset and build vector DB
python download_dataset.py
python src/build_vector_db.py

# Launch with Docker Compose (app + Redis)
docker-compose up --build
```

---

## 🎯 Example Conversations

### Product Discovery
```
You: "Find me some healthy breakfast options"
Agent: [searches] Here are 5 options: Organic Oats (ID: 1234), ...

You: "Compare the top 3"
Agent: [compare_products] Side-by-side: ratings, price, popularity...

You: "What do other customers think about product 1234?"
Agent: [analyze_reviews] ⭐⭐⭐⭐ 4.2/5 — 😊 Positive sentiment...
```

### Shopping & Checkout
```
You: "Add the oats to my cart"
Agent: ✅ Added 1 × Organic Oats (ID: 1234). Total in cart: 1

You: "What else would go well with this?"
Agent: [recommend_products based_on=cart] You might also like...

You: "Buy everything in my cart"
Agent: ✅ Order ORD-54321 placed! Estimated delivery: Oct 14, 2026
```

### Order Management
```
You: "Where's my order?"
Agent: [track_order] ✅ ORD-54321 | CONFIRMED | Est. Oct 14

You: "Actually, cancel it"
Agent: [cancel_order] ✅ Order ORD-54321 cancelled. Refund in 3-5 days.
```

### Support Escalation
```
You: "I want a refund for my last order"
Agent: [RouteToCustomerSupport] → Support Agent
Support: [EscalateToHuman] 🔴 High severity: refund request
>>> Supervisor panel appears in UI <<<
Supervisor: "Approve — refund $12.50"
Support: "Great news! Your refund of $12.50 has been approved."
```

---

## 📁 Project Structure

```
LangGraph-Retail-Assistant/
├── app.py                      # Streamlit UI
├── setup.py                    # One-shot setup script
├── download_dataset.py         # Dataset downloader
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
│
├── src/
│   ├── __init__.py
│   ├── state.py               # LangGraph State definition
│   ├── graph.py               # StateGraph builder & routing
│   ├── assistants.py          # Agent node functions + LLM setup
│   ├── prompts.py             # System prompts for each agent
│   ├── tools.py               # All tool implementations
│   ├── build_vector_db.py     # ChromaDB indexing script
│   ├── conversation_runner.py # CLI runner
│   └── web_search_mcp.py      # MCP web search integration
│
├── tests/
│   ├── test_new_tools.py      # Tests: compare, recommend, reviews, orders
│   ├── test_graph.py          # Tests: graph routing, state transitions
│   ├── test_cart_and_schema.py
│   ├── test_end_to_end.py
│   ├── test_sales_assistant.py
│   ├── test_structured_search.py
│   ├── test_tool_node.py
│   ├── test_vector_search.py
│   └── test_web_search_mcp.py
│
└── dataset/                   # Downloaded Instacart CSV files
    ├── products.csv
    ├── aisles.csv
    ├── departments.csv
    ├── orders.csv
    └── order_products__prior.csv
```

---

## 🔧 Available Tools

| Tool | Agent | Description |
|---|---|---|
| `search_tool` | Sales | Semantic vector search |
| `structured_search_tool` | Sales | SQL-like filtered search |
| `compare_products` | Sales | Side-by-side product comparison |
| `recommend_products` | Sales | Personalized recommendations |
| `analyze_reviews` | Sales | Review sentiment analysis |
| `cart_tool` | Sales | Add/remove/update/buy |
| `view_cart` | Sales | Show cart contents + prices |
| `track_order` | Sales + Support | Order status tracking |
| `cancel_order` | Support | Cancel pending orders |
| `RouteToCustomerSupport` | Sales | Handoff to Support agent |
| `EscalateToHuman` | Support | Trigger supervisor interrupt |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_new_tools.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

---

## 📊 LangSmith Observability

Add to `.env`:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_key_here
LANGCHAIN_PROJECT=SmartShop-Elite
```

All agent traces, tool calls, and LLM invocations will appear at **smith.langchain.com**.

---

## 📦 Dataset

Uses the [Instacart Online Grocery Shopping Dataset](https://www.instacart.com/datasets/grocery-shopping-2017) (50,000+ products).

Downloaded automatically via `download_dataset.py` from Google Drive.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Run tests (`pytest tests/ -v`)
4. Submit a PR

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.