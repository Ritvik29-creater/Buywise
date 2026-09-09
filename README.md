# BuyWise — Autonomous E-Commerce Shopping Agent

BuyWise is a starter full-stack agentic shopping platform that converts natural-language shopping goals into product discovery, filtering, comparison, recommendation, and cart workflows.

## Current MVP

- FastAPI REST API
- JWT authentication
- Product catalog and search
- Natural-language intent routing
- LangGraph workflow
- Basic local policy retrieval
- Product comparison and recommendations
- In-memory cart demo
- Redis-ready background task
- Automated tests
- Docker / Docker Compose

> This is an educational MVP. External LLM, production PostgreSQL, semantic embeddings, React UI, and LangSmith can be added as the project is expanded.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

Demo login:
- email: demo@buywise.ai
- password: demo123

## Example

POST `/shopping/ask`

```json
{
  "message": "Find me a wireless headphone under 5000 with good battery life"
}
```

## Docker

```bash
docker compose up --build
```
