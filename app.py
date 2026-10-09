#!/usr/bin/env python
# app.py — SmartShop Elite  ·  Premium AI Shopping Assistant

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st
from langgraph.types import Command

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.graph import graph

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartShop Elite — AI Concierge",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Ultra-Premium Design System & CSS ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background: #060814 !important;
    color: #f8fafc !important;
}

/* Ambient Radial Glows (Deep Obsidian + Vivid Violet + Cyan Accents) */
.stApp {
    background:
        radial-gradient(circle at 10% 12%, rgba(99,102,241,0.22) 0%, transparent 42%),
        radial-gradient(circle at 90% 70%, rgba(168,85,247,0.20) 0%, transparent 45%),
        radial-gradient(circle at 50% 45%, rgba(6,182,212,0.08) 0%, transparent 55%),
        radial-gradient(circle at 75% 15%, rgba(236,72,153,0.08) 0%, transparent 35%),
        linear-gradient(135deg, #060814 0%, #0b0f24 50%, #080d1e 100%) !important;
    background-attachment: fixed !important;
}

/* Glassmorphism Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(11, 15, 36, 0.78) !important;
    backdrop-filter: blur(32px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(32px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 8px 0 36px rgba(0,0,0,0.55), inset -1px 0 0 rgba(255,255,255,0.06) !important;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
    padding-left: 1.15rem;
    padding-right: 1.15rem;
}

.main .block-container {
    padding: 1.5rem 2rem 7.5rem 2rem !important;
    max-width: 980px !important;
}

/* Hide Streamlit Chrome & Headers */
#MainMenu, footer, header {
    visibility: hidden !important;
    display: none !important;
}
.stDeployButton { display: none !important; }

/* ── CRITICAL: ELIMINATE STREAMLIT WHITE RECTANGLE AT BOTTOM ── */
div[data-testid="stBottom"],
div[data-testid="stBottom"] > div,
div[data-testid="stBottom"] footer,
div[data-testid="stChatFloatingInputContainer"],
.stChatFloatingInputContainer,
.stBottom {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* ── ULTRA-PREMIUM CHAT INPUT WITH GLASSMORPHISM ── */
div[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.85) !important;
    background-color: rgba(15, 23, 42, 0.85) !important;
    border: 1.5px solid rgba(99, 102, 241, 0.5) !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.7), 0 0 24px rgba(99,102,241,0.25), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    backdrop-filter: blur(28px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #a855f7 !important;
    box-shadow: 0 12px 48px rgba(0,0,0,0.85), 0 0 32px rgba(168,85,247,0.45), inset 0 1px 0 rgba(255,255,255,0.25) !important;
}

div[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: transparent !important;
    background-color: transparent !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    caret-color: #a855f7 !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    opacity: 1 !important;
}

div[data-testid="stChatInput"] button {
    color: #a855f7 !important;
    background: transparent !important;
    transition: transform 0.2s, color 0.2s;
}
div[data-testid="stChatInput"] button:hover {
    color: #c084fc !important;
    transform: scale(1.1);
}

/* ── READABLE GLASS CHAT MESSAGES ── */
div[data-testid="stChatMessage"] {
    background: rgba(14, 20, 44, 0.72) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-top: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 18px !important;
    padding: 1.15rem 1.4rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(24px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(160%) !important;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stChatMessage"]:hover {
    border-color: rgba(99,102,241,0.45) !important;
    box-shadow: 0 10px 36px rgba(0,0,0,0.45), 0 0 20px rgba(99,102,241,0.15) !important;
}

/* Force all text in messages to be crisp, bright, and legible */
div[data-testid="stChatMessage"] *,
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] div,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] td,
div[data-testid="stChatMessage"] th {
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
    font-size: 0.97rem !important;
    line-height: 1.65 !important;
}

div[data-testid="stChatMessage"] strong,
div[data-testid="stChatMessage"] b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 700 !important;
}

div[data-testid="stChatMessage"] h1,
div[data-testid="stChatMessage"] h2,
div[data-testid="stChatMessage"] h3,
div[data-testid="stChatMessage"] h4 {
    color: #a5b4fc !important;
    -webkit-text-fill-color: #a5b4fc !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    margin-top: 0.8rem !important;
    margin-bottom: 0.4rem !important;
}

div[data-testid="stChatMessage"] a {
    color: #38bdf8 !important;
    -webkit-text-fill-color: #38bdf8 !important;
    text-decoration: underline !important;
}

div[data-testid="stChatMessage"] code {
    color: #38bdf8 !important;
    -webkit-text-fill-color: #38bdf8 !important;
    background: rgba(255,255,255,0.08) !important;
    padding: 2px 6px !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* User Message Bubble — Sleek Floating Purple-Indigo Glass */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(99,102,241,0.35) 0%, rgba(168,85,247,0.25) 100%) !important;
    border: 1px solid rgba(168,85,247,0.5) !important;
    border-top: 1px solid rgba(255,255,255,0.3) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.25), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    border-radius: 20px 20px 6px 20px !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) p,
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) span,
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 500 !important;
}

/* Assistant Bubble Corner */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    border-radius: 6px 20px 20px 20px !important;
}

/* ── Glassmorphism Live Status Widget (st.status) ── */
div[data-testid="stStatusWidget"] {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1.5px solid rgba(168, 85, 247, 0.45) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    box-shadow: 0 8px 32px rgba(168, 85, 247, 0.22), inset 0 1px 0 rgba(255,255,255,0.12) !important;
    margin-bottom: 14px !important;
    padding: 12px 16px !important;
}

div[data-testid="stStatusWidget"] * {
    color: #e2e8f0 !important;
    font-size: 0.92rem !important;
}

div[data-testid="stStatusWidget"] summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: #d8b4fe !important;
}

/* ── Top Header ── */
.ss-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 1.4rem;
    padding-bottom: 1.1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.ss-logo-icon {
    width: 54px;
    height: 54px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #38bdf8 100%);
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 0 32px rgba(99,102,241,0.55), 0 4px 14px rgba(0,0,0,0.5);
    flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.2);
}

.ss-logo-text { display: flex; flex-direction: column; }
.ss-logo-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    letter-spacing: -0.4px;
}

.ss-logo-sub {
    font-size: 0.75rem;
    color: #94a3b8;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 2px;
}

.ss-mode-badge {
    margin-left: auto;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    backdrop-filter: blur(16px);
}

.ss-mode-badge::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}

.ss-mode-badge.sales {
    background: rgba(99,102,241,0.22);
    border: 1px solid rgba(99,102,241,0.5);
    color: #c7d2fe;
    box-shadow: 0 0 16px rgba(99,102,241,0.25);
}
.ss-mode-badge.sales::before {
    background: #818cf8;
    box-shadow: 0 0 10px #818cf8;
}

.ss-mode-badge.support {
    background: rgba(249,115,22,0.22);
    border: 1px solid rgba(249,115,22,0.5);
    color: #fed7aa;
    box-shadow: 0 0 16px rgba(249,115,22,0.25);
}
.ss-mode-badge.support::before {
    background: #fb923c;
    box-shadow: 0 0 10px #fb923c;
}

.agent-badge-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.agent-badge-pill.sales {
    background: rgba(99,102,241,0.28);
    color: #c7d2fe;
    border: 1px solid rgba(99,102,241,0.5);
    box-shadow: 0 0 12px rgba(99,102,241,0.2);
}
.agent-badge-pill.support {
    background: rgba(249,115,22,0.28);
    color: #fed7aa;
    border: 1px solid rgba(249,115,22,0.5);
    box-shadow: 0 0 12px rgba(249,115,22,0.2);
}
.agent-badge-pill.supervisor {
    background: rgba(168,85,247,0.28);
    color: #e9d5ff;
    border: 1px solid rgba(168,85,247,0.5);
    box-shadow: 0 0 12px rgba(168,85,247,0.2);
}

/* ── Modern Expanders ── */
details[data-testid="stExpander"] {
    background: rgba(14, 20, 44, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
details[data-testid="stExpander"] summary {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}
details[data-testid="stExpander"] summary:hover {
    color: #818cf8 !important;
}
details[data-testid="stExpander"] * {
    color: #e2e8f0 !important;
}

/* ── Welcome Hero ── */
.welcome-hero {
    text-align: center;
    padding: 2.2rem 1.8rem 1.4rem;
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255,255,255,0.12);
    border-top: 1px solid rgba(255,255,255,0.25);
    border-radius: 24px;
    margin-bottom: 1.6rem;
    backdrop-filter: blur(28px) saturate(180%);
    box-shadow: 0 12px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.15);
}
.welcome-icon { font-size: 3rem; margin-bottom: 10px; }
.welcome-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}
.welcome-subtitle {
    font-size: 0.92rem;
    color: #cbd5e1;
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Cart Drawer (Sidebar) ── */
.cart-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    transition: background 0.2s, border-color 0.2s, transform 0.2s;
}
.cart-card:hover {
    background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.4);
    transform: translateY(-1px);
}
.cart-card-name {
    font-size: 0.85rem;
    color: #f1f5f9;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}
.cart-card-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}
.cart-qty {
    background: rgba(99,102,241,0.25);
    color: #c7d2fe;
    border-radius: 8px;
    padding: 2px 7px;
    font-size: 0.75rem;
    font-weight: 700;
}
.cart-price {
    color: #34d399;
    font-size: 0.86rem;
    font-weight: 700;
}
.cart-total-box {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 14px;
    padding: 12px 14px;
    margin: 12px 0 10px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 16px rgba(16,185,129,0.15);
}
.cart-total-label { font-size: 0.85rem; color: #a7f3d0; font-weight: 600; }
.cart-total-val { font-size: 1.25rem; font-weight: 800; color: #34d399; }

/* ── Approval Panel ── */
.approval-panel {
    background: rgba(168,85,247,0.1);
    border: 1.5px solid rgba(168,85,247,0.45);
    border-radius: 18px;
    padding: 20px 24px;
    margin: 18px 0;
    box-shadow: 0 0 36px rgba(168,85,247,0.18), inset 0 1px 0 rgba(255,255,255,0.1);
    backdrop-filter: blur(24px);
}
.approval-panel h4 {
    color: #e9d5ff;
    font-family: 'Space Grotesk',sans-serif;
    font-size: 1.1rem;
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.approval-row { display: flex; gap: 10px; margin-bottom: 6px; font-size: 0.88rem; }
.approval-row .label { color: #94a3b8; min-width: 85px; font-weight: 600; }
.approval-row .value { color: #f1f5f9; }
.sev-pill {
    padding: 2px 10px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.72rem;
    text-transform: uppercase;
}
.sev-high { background: rgba(239,68,68,0.25); color: #f87171; border: 1px solid rgba(239,68,68,0.5); }
.sev-medium { background: rgba(245,158,11,0.25); color: #fbbf24; border: 1px solid rgba(245,158,11,0.5); }
.sev-low { background: rgba(16,185,129,0.25); color: #34d399; border: 1px solid rgba(16,185,129,0.5); }

/* ── Modern Buttons with Specular Lift ── */
.stButton > button {
    background: rgba(15, 23, 42, 0.65) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
    padding: 9px 16px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.35) 0%, rgba(168, 85, 247, 0.28) 100%) !important;
    border-color: rgba(168, 85, 247, 0.6) !important;
    box-shadow: 0 8px 28px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
}

/* Sidebar Section Headers */
.sb-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sb-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.session-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 0.82rem;
    color: #cbd5e1;
    margin-bottom: 6px;
}
.session-pill strong { color: #f8fafc; font-weight: 600; }

hr { border-color: rgba(255,255,255,0.08) !important; margin: 16px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_product_price(product_id):
    try:
        from src.tools import get_product_price as _tool_price
        return _tool_price(int(product_id))
    except Exception:
        return 0.99


def format_tool_call(tool_call):
    name = tool_call.get("name", "unknown")
    args = tool_call.get("args", {})
    parts = [f"{k}={repr(v)}" for k, v in args.items()]
    return f"{name}({', '.join(parts)})"


def get_current_state():
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    snapshot = graph.get_state(config).values
    dialog_state = snapshot.get("dialog_state", [])
    current_mode = dialog_state[-1] if dialog_state else "sales_rep"
    return snapshot, current_mode


def direct_cart_update():
    try:
        from src.tools import _product_lookup, get_cart, set_thread_id
        set_thread_id(st.session_state.thread_id)
        cart = get_cart()
        if isinstance(cart, list) and len(cart) > 0 and "Session error" in cart[0]:
            return
        cart_items = {}
        for pid, qty in cart.items():
            title = _product_lookup.get(pid, f"Product #{pid}")
            price = get_product_price(pid)
            cart_items[str(pid)] = {"name": title, "quantity": qty, "price": price}
        st.session_state.cart_items = cart_items
    except Exception:
        pass


def parse_cart_from_tool_message(content):
    cart_items = {}
    if not content or "Your cart contains:" not in content:
        return cart_items
    for line in content.split("\n"):
        if line.strip().startswith("- ") and "(ID:" in line:
            try:
                product_name = line.split("(ID:")[0].strip("- ").strip()
                id_part = line.split("(ID: ")[1].split(")")[0].strip()
                quantity = 1
                if "×" in line:
                    quantity = int(line.split("×")[1].strip().split()[0])
                elif "x" in line.lower():
                    quantity = int(line.lower().split("x")[1].strip().split()[0])
                price = get_product_price(int(id_part))
                cart_items[id_part] = {"name": product_name, "quantity": quantity, "price": price}
            except Exception:
                pass
    return cart_items


def get_cart_totals():
    total_items, total_price = 0, 0.0
    for item_data in st.session_state.cart_items.values():
        qty = item_data.get("quantity", 0)
        price = item_data.get("price", 0.0)
        total_items += qty
        total_price += qty * price
    return total_items, total_price


# ── Session Initialization ───────────────────────────────────────────────────
def init_session():
    defaults = {
        "thread_id": str(uuid.uuid4()),
        "messages": [],
        "chat_history": [],
        "pending_approval": None,
        "pending_user_query": None,
        "debug_mode": False,
        "current_mode": "sales_rep",
        "cart_items": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Core Graph Execution Logic ───────────────────────────────────────────────
def _process_graph_output(state, snapshot):
    messages = state["messages"]
    new_messages = [m for m in messages if m not in st.session_state.messages]
    last_assistant_content = ""
    for msg in new_messages:
        msg_type = msg.__class__.__name__
        content = getattr(msg, "content", "")
        if msg_type == "AIMessage":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    st.session_state.chat_history.append({
                        "role": "tool_call",
                        "content": format_tool_call(tc),
                        "tool_name": tc.get("name", "tool"),
                    })
            elif content:
                last_assistant_content = content
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": content,
                    "mode": st.session_state.current_mode,
                })
        elif msg_type == "ToolMessage":
            tc_id = getattr(msg, "tool_call_id", "")
            tool_name = "tool"
            for prev in messages:
                if hasattr(prev, "tool_calls"):
                    for tc in prev.tool_calls:
                        if tc.get("id") == tc_id:
                            tool_name = tc.get("name", "tool")
                            break
            st.session_state.chat_history.append({
                "role": "tool_result",
                "content": content,
                "tool_name": tool_name
            })
            if tool_name == "view_cart":
                parsed = parse_cart_from_tool_message(content)
                if parsed:
                    st.session_state.cart_items = parsed
    st.session_state.messages = messages
    direct_cart_update()
    return last_assistant_content


def execute_user_turn(user_input: str) -> str:
    """Executes a user turn with the LangGraph agent and returns the assistant reply content."""
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    graph.invoke({"messages": [("user", user_input)]}, config)
    snapshot = graph.get_state(config)
    state = snapshot.values
    dialog_state = state.get("dialog_state", [])
    st.session_state.current_mode = dialog_state[-1] if dialog_state else "sales_rep"
    
    interrupt_info = None
    for task in snapshot.tasks:
        if hasattr(task, "interrupts") and task.interrupts:
            for intr in task.interrupts:
                if hasattr(intr, "value") and isinstance(intr.value, dict):
                    interrupt_info = intr.value
                    
    last_content = _process_graph_output(state, snapshot)
    if interrupt_info:
        st.session_state.pending_approval = {
            "severity": interrupt_info.get("severity", "unknown"),
            "summary": interrupt_info.get("summary", "Approval required"),
            "message": interrupt_info.get("message", ""),
        }
    return last_content


def send_user_message(user_input: str):
    """Fallback / programmatic query sender."""
    if not user_input or not user_input.strip():
        return
    st.session_state.pending_user_query = user_input


def send_supervisor_decision(decision: str):
    if not decision or not decision.strip():
        return
    st.session_state.chat_history.append({"role": "supervisor", "content": decision})
    st.session_state.pending_approval = None
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    try:
        graph.invoke(Command(resume=decision), config)
        snapshot = graph.get_state(config)
        state = snapshot.values
        dialog_state = state.get("dialog_state", [])
        st.session_state.current_mode = dialog_state[-1] if dialog_state else "sales_rep"
        _process_graph_output(state, snapshot)
    except Exception as e:
        st.session_state.chat_history.append({"role": "error", "content": str(e)})


def reset_conversation():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.pending_approval = None
    st.session_state.pending_user_query = None
    st.session_state.current_mode = "sales_rep"
    st.session_state.cart_items = {}


def clear_cart_items():
    try:
        from src.tools import get_cart, set_thread_id
        set_thread_id(st.session_state.thread_id)
        cart = get_cart()
        if isinstance(cart, dict):
            cart.clear()
        st.session_state.cart_items = {}
    except Exception:
        st.session_state.cart_items = {}


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-brand"><span style="font-size:1.45rem;">🛒</span> SmartShop Elite</div>', unsafe_allow_html=True)

    # ── Cart Section ──
    total_items, total_price = get_cart_totals()
    cart_label = f"Shopping Cart ({total_items})" if total_items > 0 else "Shopping Cart (Empty)"
    st.markdown(f'<div class="sb-section-title">{cart_label}</div>', unsafe_allow_html=True)

    if st.session_state.cart_items:
        for item_id, item_data in st.session_state.cart_items.items():
            qty = item_data.get("quantity", 0)
            price = item_data.get("price", 0.0)
            name = item_data.get("name", "Product")
            st.markdown(f"""
            <div class="cart-card">
                <div class="cart-card-name" title="{name}">{name}</div>
                <div class="cart-card-meta">
                    <span class="cart-price">${price:.2f}</span>
                    <span class="cart-qty">x{qty}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            
        st.markdown(f"""
        <div class="cart-total-box">
            <span class="cart-total-label">Subtotal ({total_items} items)</span>
            <span class="cart-total-val">${total_price:.2f}</span>
        </div>""", unsafe_allow_html=True)
        
        c_col1, c_col2 = st.columns([2, 1])
        with c_col1:
            if st.button("🛍️ Checkout", use_container_width=True):
                send_user_message("I would like to checkout and place my order for the items in my cart.")
                st.rerun()
        with c_col2:
            if st.button("Clear", use_container_width=True):
                clear_cart_items()
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 10px;color:#64748b;font-size:0.83rem;line-height:1.5;">
            Your cart is empty.<br>
            <span style="font-size:0.75rem;color:#475569;">Ask to find and add products!</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Agent State ──
    st.markdown('<div class="sb-section-title">Agent State</div>', unsafe_allow_html=True)
    mode_display = "Sales Representative" if st.session_state.current_mode == "sales_rep" else "Customer Support"
    st.markdown(f"""
    <div class="session-pill">Active Agent: <strong>{mode_display}</strong></div>
    <div class="session-pill">Thread: <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">{st.session_state.thread_id[:16]}...</span></div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Actions ──
    st.markdown('<div class="sb-section-title">Actions</div>', unsafe_allow_html=True)
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        if st.button("↺ New Chat", use_container_width=True):
            reset_conversation()
            st.rerun()
    with act_col2:
        btn_dbg_text = "Hide Debug" if st.session_state.debug_mode else "🐞 Debug"
        if st.button(btn_dbg_text, use_container_width=True):
            st.session_state.debug_mode = not st.session_state.debug_mode
            st.rerun()

    if st.session_state.debug_mode:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="sb-section-title">Debug Inspector</div>', unsafe_allow_html=True)
        snapshot, _ = get_current_state()
        st.caption("Dialog State Stack:")
        st.json(snapshot.get("dialog_state", []))
        st.caption("Raw Cart Items:")
        st.json(st.session_state.cart_items)

    with st.expander("📁 Department Catalog (10)", expanded=False):
        st.markdown("""
        * **📱 Electronics**: 16 items
        * **💻 Computers**: 15 items
        * **🎧 Audio & Sound**: 10 items
        * **👟 Footwear**: 11 items
        * **🧥 Fashion**: 11 items
        * **☕ Home & Kitchen**: 13 items
        * **🏃 Sports**: 9 items
        * **✨ Beauty**: 11 items
        * **🍫 Gourmet**: 10 items
        * **📚 Books**: 10 items
        """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem;color:#475569;text-align:center;line-height:1.8;">
        LangGraph &nbsp;·&nbsp; Gemini &nbsp;·&nbsp; ChromaDB<br>
        <span style="color:#6366f1;font-weight:600;">SmartShop Elite v2.5</span>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN — HEADER
# ═══════════════════════════════════════════════════════════════════════════════
is_sales = st.session_state.current_mode == "sales_rep"
mode_class = "sales" if is_sales else "support"
mode_label = "Sales Representative" if is_sales else "Customer Support"

st.markdown(f"""
<div class="ss-header">
    <div class="ss-logo-icon">🛒</div>
    <div class="ss-logo-text">
        <div class="ss-logo-title">SmartShop Elite</div>
        <div class="ss-logo-sub">Autonomous Retail Concierge</div>
    </div>
    <span class="ss-mode-badge {mode_class}">{mode_label}</span>
</div>""", unsafe_allow_html=True)

# ── Permanent Catalog & Questions Guide ──
with st.expander("💡 What Products Can I Ask About? (Browse 116 Items Across 10 Departments)", expanded=not bool(st.session_state.chat_history)):
    st.markdown("""
    You can ask me to **recommend**, **search**, **compare**, or **check reviews & specs** for products across our catalog:
    
    * **📱 Electronics**: *Apple iPhone 16 Pro Max, Samsung Galaxy S24 Ultra, Google Pixel 9 Pro, OnePlus 12, iPad Pro M4, Apple Watch Ultra 2, Kindle Paperwhite*
    * **💻 Computers & Gaming**: *MacBook Pro 16" M3 Max, MacBook Air 15" M3, Dell XPS 14 OLED, Razer Blade 16, Logitech MX Master 3S, Keychron Q1 Pro*
    * **🎧 Audio & Sound**: *Sony WH-1000XM5, Bose QuietComfort Ultra, Apple AirPods Max, Sonos Move 2, JBL Charge 5, Sennheiser Momentum 4*
    * **👟 Footwear**: *Nike Air Zoom Pegasus 41, Hoka Clifton 9, Brooks Ghost 16, On Cloudmonster 2, Asics Gel-Kayano 31, Adidas Ultraboost Light*
    * **🧥 Fashion & Apparel**: *The North Face 1996 Retro Nuptse, Arc'teryx Beta LT GORE-TEX, Patagonia Nano Puff, Lululemon Scuba Hoodie*
    * **☕ Home & Kitchen**: *Breville Barista Touch Impress, Nespresso VertuoPlus, Fellow Ode Gen 2 Burr Grinder, Ninja Air Fryer Max XL, Le Creuset Dutch Oven*
    * **🏃 Sports & Outdoors**: *WHOOP 4.0 Health Tracker, Oura Ring Gen3 Horizon, Manduka PRO Yoga Mat, Bowflex SelectTech Dumbbells*
    * **✨ Beauty & Skincare**: *The Ordinary Niacinamide + Zinc, CeraVe Hydrating Cleanser, Paula's Choice 2% BHA Salicylic Acid, Dyson Supersonic Hair Dryer*
    * **🍫 Gourmet & Snacks**: *RXBAR Protein Variety Pack, Barebells Creamy Crisp 20g, Blue Bottle Bella Donovan Beans, Compartes Luxury Truffles*
    * **📚 Books & Stationery**: *Project Hail Mary, Dune Deluxe Edition, Tomorrow and Tomorrow and Tomorrow, Leuchtturm1917 Hardcover Notebook*
    """)


# ═══════════════════════════════════════════════════════════════════════════════
#  WELCOME HERO & QUICK-START CARDS (When chat is empty)
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-hero">
        <div class="welcome-icon">✨</div>
        <div class="welcome-title">Welcome to SmartShop Elite</div>
        <div class="welcome-subtitle">
            Your personal retail concierge powered by LangGraph multi-agent architecture and Google Gemini.
            Discover products with vector search, compare specs, analyze review sentiment, and manage your cart seamlessly.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;font-size:0.75rem;font-weight:700;letter-spacing:1.4px;color:#818cf8;text-transform:uppercase;margin-bottom:14px;">Quick Start Suggestions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎧 Compare Sony WH-1000XM5 & Bose Ultra", key="hero_sug_audio", use_container_width=True):
            send_user_message("Compare Sony WH-1000XM5 and Bose QuietComfort Ultra headphones.")
            st.rerun()
        if st.button("👟 Find top-rated running shoes with good cushioning", key="hero_sug_shoes", use_container_width=True):
            send_user_message("Find top-rated running shoes with good cushioning under $200.")
            st.rerun()
        if st.button("☕ Recommend the best home espresso machines", key="hero_sug_coffee", use_container_width=True):
            send_user_message("Recommend the best home espresso machines.")
            st.rerun()
    with col2:
        if st.button("💻 Find Apple MacBook & premium ultrabooks", key="hero_sug_laptop", use_container_width=True):
            send_user_message("Find Apple MacBook and high-performance ultrabooks.")
            st.rerun()
        if st.button("📦 Track my recent order status", key="hero_sug_orders", use_container_width=True):
            send_user_message("Can you track my recent orders?")
            st.rerun()
        if st.button("🛒 What's currently in my cart?", key="hero_sug_cart", use_container_width=True):
            direct_cart_update()
            send_user_message("What is currently in my shopping cart?")
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAT MESSAGES DISPLAY (Rich Native Markdown + Glass Cards)
# ═══════════════════════════════════════════════════════════════════════════════
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)

    elif role == "assistant":
        mode = msg.get("mode", "sales_rep")
        is_agent_sales = mode == "sales_rep"
        avatar_icon = "🛍️" if is_agent_sales else "🎧"
        agent_title = "Sales Specialist" if is_agent_sales else "Support Agent"
        pill_class = "sales" if is_agent_sales else "support"
        
        with st.chat_message("assistant", avatar=avatar_icon):
            st.markdown(f'<span class="agent-badge-pill {pill_class}">{agent_title}</span>', unsafe_allow_html=True)
            st.markdown(content)

    elif role == "supervisor":
        with st.chat_message("assistant", avatar="🛡️"):
            st.markdown('<span class="agent-badge-pill supervisor">Supervisor Decision</span>', unsafe_allow_html=True)
            st.markdown(content)

    elif role == "tool_call":
        if st.session_state.debug_mode:
            with st.expander(f"🛠️ Calling {msg.get('tool_name', 'tool')}", expanded=False):
                st.code(content, language="python")

    elif role == "tool_result":
        if st.session_state.debug_mode:
            with st.expander(f"📋 Result from {msg.get('tool_name', 'tool')}", expanded=False):
                st.code(content, language="markdown")

    elif role == "error":
        st.error(f"**Error**: {content}", icon="⚠️")

# ── REACTIVE TURN: RENDER USER QUERY IMMEDIATELY + LIVE ASSISTANT STATUS ──
if st.session_state.get("pending_user_query"):
    incoming_query = st.session_state.pop("pending_user_query")
    
    # 1. Add user message to history and render IMMEDIATELY
    st.session_state.chat_history.append({"role": "user", "content": incoming_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(incoming_query)

    # 2. Render assistant with live glassmorphic animated thinking status
    is_agent_sales = st.session_state.current_mode == "sales_rep"
    avatar_icon = "🛍️" if is_agent_sales else "🎧"
    agent_title = "Sales Specialist" if is_agent_sales else "Support Agent"
    pill_class = "sales" if is_agent_sales else "support"

    with st.chat_message("assistant", avatar=avatar_icon):
        st.markdown(f'<span class="agent-badge-pill {pill_class}">{agent_title}</span>', unsafe_allow_html=True)
        with st.status("🔮 **SmartShop Concierge is finding the best products...**", expanded=True) as status_box:
            st.write("🔍 Searching vector database & catalog inventory...")
            try:
                reply_text = execute_user_turn(incoming_query)
                st.write("⚡ Analyzing specs, pricing & customer sentiment...")
                status_box.update(label="✨ **Recommendations Ready!**", state="complete", expanded=False)
                if reply_text:
                    st.markdown(reply_text)
            except Exception as err:
                status_box.update(label="⚠️ **Request failed**", state="error", expanded=True)
                st.error(f"Error: {err}")
                st.session_state.chat_history.append({"role": "error", "content": str(err)})

    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  HUMAN APPROVAL INTERRUPT PANEL
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.pending_approval:
    approval = st.session_state.pending_approval
    sev = approval.get("severity", "unknown").lower()
    sev_class = "sev-high" if sev == "high" else ("sev-medium" if sev == "medium" else "sev-low")
    
    st.markdown(f"""
    <div class="approval-panel">
        <h4>🛡️ Human Supervisor Authorization Required</h4>
        <div class="approval-row"><span class="label">Summary</span><span class="value">{approval.get('summary', 'Action requires approval')}</span></div>
        <div class="approval-row"><span class="label">Severity</span><span class="value"><span class="sev-pill {sev_class}">{sev.upper()}</span></span></div>
        <div class="approval-row"><span class="label">Details</span><span class="value">{approval.get('message', '')}</span></div>
    </div>""", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("✅ Approve Request", key="btn_appr_fast", use_container_width=True):
            send_supervisor_decision("Approved. Please proceed with processing the request.")
            st.rerun()
    with col_b:
        if st.button("❌ Deny Request", key="btn_deny_fast", use_container_width=True):
            send_supervisor_decision("Denied. Unable to approve request per store policy.")
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  PERSISTENT QUICK SUGGESTIONS & PINNED CHAT INPUT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:16px;margin-bottom:8px;font-size:0.75rem;font-weight:700;letter-spacing:1px;color:#818cf8;text-transform:uppercase;">⚡ Quick Suggestions & Sample Queries</div>', unsafe_allow_html=True)
s_cols1 = st.columns(4)
with s_cols1[0]:
    if st.button("👟 Running Shoes", key="sug_shoes", use_container_width=True):
        send_user_message("Show me top-rated running shoes with good cushioning under $200.")
        st.rerun()
with s_cols1[1]:
    if st.button("📱 iPhone vs S24", key="sug_phones", use_container_width=True):
        send_user_message("Compare Apple iPhone 16 Pro Max and Samsung Galaxy S24 Ultra.")
        st.rerun()
with s_cols1[2]:
    if st.button("🎧 Sony XM5 vs Bose", key="sug_audio", use_container_width=True):
        send_user_message("Compare Sony WH-1000XM5 and Bose QuietComfort Ultra headphones.")
        st.rerun()
with s_cols1[3]:
    if st.button("💻 MacBook Pro M3", key="sug_laptop", use_container_width=True):
        send_user_message("Find Apple MacBook Pro and high-performance gaming laptops.")
        st.rerun()

s_cols2 = st.columns(4)
with s_cols2[0]:
    if st.button("☕ Espresso Machines", key="sug_coffee", use_container_width=True):
        send_user_message("Recommend the best home espresso machines.")
        st.rerun()
with s_cols2[1]:
    if st.button("🧥 Winter Jackets", key="sug_jacket", use_container_width=True):
        send_user_message("Recommend warm winter jackets like North Face or Patagonia.")
        st.rerun()
with s_cols2[2]:
    if st.button("📦 Order Status", key="sug_orders", use_container_width=True):
        send_user_message("Can you track my recent orders?")
        st.rerun()
with s_cols2[3]:
    if st.button("🛒 View Cart", key="sug_cart", use_container_width=True):
        direct_cart_update()
        send_user_message("What is currently in my shopping cart?")
        st.rerun()

input_placeholder = (
    "Provide supervisor instructions or approval decision..."
    if st.session_state.pending_approval
    else "Ask me to find products, compare items, track orders, or checkout..."
)

if user_query := st.chat_input(input_placeholder):
    if st.session_state.pending_approval:
        send_supervisor_decision(user_query)
    else:
        st.session_state.pending_user_query = user_query
    st.rerun()
