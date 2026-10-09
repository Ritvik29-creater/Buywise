# ─────────────────────────────────────────────────────────────────────────────
# SmartShop Elite — Dockerfile
# Multi-stage build: deps → runtime
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim AS base

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Install Python dependencies ────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Copy source code ───────────────────────────────────────────────────────
COPY . .

# ── Create required directories ───────────────────────────────────────────
RUN mkdir -p dataset vector_db

# ── Expose Streamlit port ──────────────────────────────────────────────────
EXPOSE 8501

# ── Health check ──────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Default command: launch Streamlit ────────────────────────────────────
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
