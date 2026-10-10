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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #f8fafc !important;
    color: #0f172a !important;
}

/* ── LUXURY LIGHT MESH CANVAS ── */
.stApp {
    background:
        radial-gradient(1100px circle at 12% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 60%),
        radial-gradient(900px circle at 88% 12%, rgba(245, 158, 11, 0.06) 0%, transparent 55%),
        radial-gradient(1000px circle at 50% 65%, rgba(16, 185, 129, 0.05) 0%, transparent 60%),
        linear-gradient(180deg, #ffffff 0%, #f8fafc 35%, #f1f5f9 100%) !important;
    background-attachment: fixed !important;
}

/* ── LUMINOUS FROSTED SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.94) !important;
    backdrop-filter: blur(28px) saturate(190%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
    border-right: 1px solid rgba(226, 232, 240, 0.95) !important;
    box-shadow: 6px 0 32px rgba(15, 23, 42, 0.04) !important;
}

section[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
    padding-left: 1.15rem;
    padding-right: 1.15rem;
}

.main .block-container {
    padding: 1.4rem 2.2rem 8rem 2.2rem !important;
    max-width: 1020px !important;
}

/* Hide Default Streamlit Chrome */
#MainMenu, footer, header {
    visibility: hidden !important;
    display: none !important;
}
.stDeployButton { display: none !important; }

/* ── ELIMINATE STREAMLIT BOTTOM CONTAINER BACKGROUND ── */
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

/* ── FLOATING LUXURY CHAT INPUT ── */
div[data-testid="stChatInput"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 22px !important;
    box-shadow: 0 12px 36px rgba(15, 23, 42, 0.09), 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #4f46e5 !important;
    box-shadow: 0 14px 44px rgba(79, 70, 229, 0.18), 0 0 0 3.5px rgba(79, 70, 229, 0.14) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stChatInput"] textarea {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: transparent !important;
    background-color: transparent !important;
    font-size: 1.02rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    caret-color: #4f46e5 !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    opacity: 1 !important;
}

div[data-testid="stChatInput"] button {
    color: #4f46e5 !important;
    background: rgba(79, 70, 229, 0.08) !important;
    border-radius: 12px !important;
    padding: 6px !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
div[data-testid="stChatInput"] button:hover {
    color: #ffffff !important;
    background: #4f46e5 !important;
    transform: scale(1.08);
}

/* ── CRISP HIGH-CONTRAST CHAT MESSAGES ── */
div[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 1.35rem 1.6rem !important;
    margin-bottom: 1.2rem !important;
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div[data-testid="stChatMessage"]:hover {
    border-color: #cbd5e1 !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08) !important;
    transform: translateY(-1px) !important;
}

/* High contrast typography for maximum legibility */
div[data-testid="stChatMessage"] *,
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] div,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] td,
div[data-testid="stChatMessage"] th {
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    font-size: 0.985rem !important;
    line-height: 1.72 !important;
}

div[data-testid="stChatMessage"] strong,
div[data-testid="stChatMessage"] b {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-weight: 700 !important;
}

div[data-testid="stChatMessage"] h1,
div[data-testid="stChatMessage"] h2,
div[data-testid="stChatMessage"] h3,
div[data-testid="stChatMessage"] h4 {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    margin-top: 0.9rem !important;
    margin-bottom: 0.45rem !important;
    letter-spacing: -0.3px !important;
}

div[data-testid="stChatMessage"] a {
    color: #4f46e5 !important;
    -webkit-text-fill-color: #4f46e5 !important;
    text-decoration: none !important;
    font-weight: 700 !important;
    border-bottom: 1.5px solid rgba(79, 70, 229, 0.3) !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stChatMessage"] a:hover {
    border-bottom-color: #4f46e5 !important;
}

div[data-testid="stChatMessage"] code {
    color: #4338ca !important;
    -webkit-text-fill-color: #4338ca !important;
    background: #f1f5f9 !important;
    padding: 3px 8px !important;
    border-radius: 7px !important;
    border: 1px solid #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}

/* User Message Bubble — Sleek Indigo to Royal Blue Gradient */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #4338ca 0%, #3b82f6 100%) !important;
    border: 1px solid #3730a3 !important;
    box-shadow: 0 8px 24px rgba(67, 56, 202, 0.24) !important;
    border-radius: 22px 22px 6px 22px !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) p,
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) span,
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 500 !important;
}

/* Assistant Bubble Accent Border */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    border-left: 4.5px solid #4f46e5 !important;
    border-radius: 6px 22px 22px 22px !important;
}

/* ── STATUS WIDGET (Agent Thinking Status) ── */
div[data-testid="stStatusWidget"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 18px !important;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05) !important;
    margin-bottom: 16px !important;
    padding: 14px 18px !important;
}

div[data-testid="stStatusWidget"] * {
    color: #334155 !important;
    font-size: 0.92rem !important;
}

div[data-testid="stStatusWidget"] summary {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    color: #4338ca !important;
}

/* ── HEADER BANNER ── */
.ss-header {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 1.1rem;
    padding-bottom: 1.2rem;
    border-bottom: 1.5px solid #e2e8f0;
}

.ss-logo-icon {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #f59e0b 100%);
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.28);
    flex-shrink: 0;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.ss-logo-icon:hover { transform: scale(1.05) rotate(3deg); }

.ss-logo-text { display: flex; flex-direction: column; }
.ss-logo-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    letter-spacing: -0.6px;
}

.ss-logo-sub {
    font-size: 0.78rem;
    color: #64748b;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: 3px;
}

.ss-mode-badge {
    margin-left: auto;
    padding: 7px 18px;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.ss-mode-badge::before {
    content: '';
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px currentColor;
    animation: pulseBeacon 2s infinite;
}

@keyframes pulseBeacon {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.8; }
}

.ss-mode-badge.sales {
    background: #eef2ff;
    border: 1.5px solid #c7d2fe;
    color: #4338ca;
}
.ss-mode-badge.sales::before { background: #4f46e5; }

.ss-mode-badge.support {
    background: #fff7ed;
    border: 1.5px solid #fed7aa;
    color: #c2410c;
}
.ss-mode-badge.support::before { background: #ea580c; }

/* ── QUICK FEATURE STRIP ── */
.feature-pill-strip {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.feature-pill-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 9999px;
    padding: 5px 14px;
    font-size: 0.76rem;
    font-weight: 600;
    color: #475569;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
}
.feature-pill-item:hover {
    border-color: #cbd5e1;
    color: #0f172a;
    transform: translateY(-1px);
}

.agent-badge-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.agent-badge-pill.sales {
    background: #eef2ff;
    color: #4338ca;
    border: 1px solid #c7d2fe;
}
.agent-badge-pill.support {
    background: #fff7ed;
    color: #c2410c;
    border: 1px solid #fed7aa;
}
.agent-badge-pill.supervisor {
    background: #faf5ff;
    color: #7e22ce;
    border: 1px solid #e9d5ff;
}

/* ── MODERN EXPANDERS ── */
details[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 18px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.03) !important;
    overflow: hidden !important;
}
details[data-testid="stExpander"] summary {
    color: #0f172a !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    padding: 12px 18px !important;
    font-size: 0.95rem !important;
}
details[data-testid="stExpander"] summary:hover {
    color: #4f46e5 !important;
    background: #f8fafc !important;
}
details[data-testid="stExpander"] * {
    color: #334155 !important;
}

/* ── WELCOME HERO ── */
.welcome-hero {
    text-align: center;
    padding: 2.6rem 2rem 2rem;
    background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
    border: 1.5px solid #e2e8f0;
    border-radius: 28px;
    margin-bottom: 1.8rem;
    box-shadow: 0 10px 32px rgba(15, 23, 42, 0.05);
    position: relative;
    overflow: hidden;
}
.welcome-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed, #10b981, #f59e0b);
}
.welcome-icon { font-size: 3.2rem; margin-bottom: 12px; }
.welcome-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.95rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.welcome-subtitle {
    font-size: 0.98rem;
    color: #475569;
    max-width: 660px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── CART DRAWER (Sidebar) ── */
.cart-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 11px 14px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.cart-card:hover {
    background: #f8fafc;
    border-color: #cbd5e1;
    transform: translateY(-1.5px);
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
}
.cart-card-name {
    font-size: 0.88rem;
    color: #0f172a;
    font-weight: 700;
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
    background: #eef2ff;
    color: #4338ca;
    border-radius: 8px;
    padding: 3px 8px;
    font-size: 0.76rem;
    font-weight: 800;
}
.cart-price {
    color: #059669;
    font-size: 0.92rem;
    font-weight: 800;
}
.cart-total-box {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 1.5px solid #a7f3d0;
    border-radius: 16px;
    padding: 14px 16px;
    margin: 14px 0 12px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.08);
}
.cart-total-label { font-size: 0.88rem; color: #047857; font-weight: 700; }
.cart-total-val { font-size: 1.35rem; font-weight: 900; color: #059669; font-family: 'Outfit', sans-serif; }

/* ── APPROVAL PANEL ── */
.approval-panel {
    background: #fdf4ff;
    border: 1.5px solid #f0abfc;
    border-radius: 20px;
    padding: 22px 26px;
    margin: 20px 0;
    box-shadow: 0 6px 22px rgba(168, 85, 247, 0.1);
}
.approval-panel h4 {
    color: #86198f;
    font-family: 'Outfit', sans-serif;
    font-size: 1.15rem;
    margin: 0 0 14px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.approval-row { display: flex; gap: 12px; margin-bottom: 7px; font-size: 0.9rem; }
.approval-row .label { color: #64748b; min-width: 90px; font-weight: 600; }
.approval-row .value { color: #0f172a; font-weight: 500; }
.sev-pill {
    padding: 3px 12px;
    border-radius: 8px;
    font-weight: 800;
    font-size: 0.74rem;
    text-transform: uppercase;
}
.sev-high { background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }
.sev-medium { background: #fef3c7; color: #d97706; border: 1px solid #fde68a; }
.sev-low { background: #dcfce7; color: #16a34a; border: 1px solid #bbf7d0; }

/* ── SLEEK SPECULAR BUTTONS ── */
.stButton > button {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
    border-color: #4338ca !important;
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.25) !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
}

/* Sidebar Section Headers */
.sb-brand {
    font-family: 'Outfit', sans-serif;
    font-size: 1.45rem;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
    letter-spacing: -0.4px;
}
.sb-section-title {
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 12px;
    padding-bottom: 4px;
    border-bottom: 1px solid #e2e8f0;
}
.session-pill {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 0.86rem;
    color: #334155;
    margin-bottom: 7px;
}
.session-pill strong { color: #0f172a; font-weight: 700; }

/* ── PRODUCT DETAIL VIEW & SPEC GRID ── */
.prod-page-container {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 28px !important;
    padding: 32px !important;
    box-shadow: 0 16px 44px rgba(15, 23, 42, 0.06) !important;
    margin-bottom: 26px !important;
}

.prod-page-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    border-radius: 9999px;
    padding: 5px 16px;
    font-size: 0.8rem;
    font-weight: 800;
    color: #4338ca;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.prod-page-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    line-height: 1.3 !important;
    margin: 14px 0 !important;
    letter-spacing: -0.4px !important;
}

.prod-page-price {
    font-family: 'Outfit', sans-serif;
    font-size: 2.3rem;
    font-weight: 900;
    color: #059669;
    margin-right: 20px;
}

.prod-spec-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
    margin: 24px 0;
}

.prod-spec-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 14px 16px;
    transition: all 0.2s ease;
}
.prod-spec-card:hover {
    background: #ffffff;
    border-color: #cbd5e1;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
}
.prod-spec-label {
    font-size: 0.74rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
    margin-bottom: 5px;
}
.prod-spec-val {
    font-size: 0.98rem;
    font-weight: 700;
    color: #0f172a;
}

.order-celebrate-box {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 1.5px solid #34d399;
    border-radius: 20px;
    padding: 22px 26px;
    box-shadow: 0 10px 28px rgba(16, 185, 129, 0.12);
    margin-bottom: 24px;
}

.prod-tap-header {
    margin-top: 18px;
    margin-bottom: 10px;
    font-size: 0.88rem;
    color: #4338ca;
    letter-spacing: 0.5px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Chat Product Card */
.chat-prod-card-preview {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}
.chat-prod-card-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #0f172a;
}
.chat-prod-card-sub {
    font-size: 0.78rem;
    color: #64748b;
}

hr { border-color: #e2e8f0 !important; margin: 18px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers & Catalog Access ─────────────────────────────────────────────────
@st.cache_data
def get_catalog_data():
    try:
        prods = pd.read_csv("./dataset/products.csv", engine="python")
        depts = pd.read_csv("./dataset/departments.csv", engine="python")
        aisles = pd.read_csv("./dataset/aisles.csv", engine="python")
        merged = prods.merge(depts, on="department_id", how="left").merge(aisles, on="aisle_id", how="left")
        return merged
    except Exception:
        return pd.DataFrame()


def get_product_details(product_id: int):
    df = get_catalog_data()
    if df.empty:
        return None
    try:
        matches = df[df["product_id"] == int(product_id)]
        if not matches.empty:
            return matches.iloc[0].to_dict()
    except Exception:
        pass
    return None


def extract_product_ids_from_text(text: str) -> list:
    if not text:
        return []
    import re
    pattern = r"(?:\(ID:\s*|ID:\s*|ID\s+)(\d+)\)?"
    matches = re.findall(pattern, text, re.IGNORECASE)
    seen = set()
    result = []
    df = get_catalog_data()
    valid_ids = set(df["product_id"].tolist()) if not df.empty else set()
    for m in matches:
        try:
            pid = int(m)
            if pid not in seen and (not valid_ids or pid in valid_ids):
                seen.add(pid)
                result.append(pid)
        except Exception:
            pass
    return result


def instant_buy_product(product_id: int):
    try:
        import random
        from src.tools import set_thread_id, _order_storage, _product_lookup, get_product_price
        tid = st.session_state.thread_id
        set_thread_id(tid)
        order_num = random.randint(10000, 99999)
        order_id = f"ORD-{order_num}"
        p_info = get_product_details(product_id)
        name = p_info["product_name"] if p_info else _product_lookup.get(product_id, f"Product #{product_id}")
        price = float(p_info.get("price", get_product_price(product_id))) if p_info else get_product_price(product_id)
        
        now = datetime.now()
        order_record = {
            "order_id": order_id,
            "status": "delivered",
            "placed_at": now.strftime("%Y-%m-%d %H:%M"),
            "estimated_delivery": now.strftime("%Y-%m-%d") + " (Delivered · Auto-Satisfied)",
            "items": [{"product_id": product_id, "name": name, "quantity": 1, "price": price}],
            "total": round(price, 2),
            "cancellable": True,
            "refund_eligible": True,
        }
        
        thread_orders = _order_storage.setdefault(tid, [])
        thread_orders.append(order_record)
        
        st.session_state.last_instant_order = {
            "order_id": order_id,
            "product_id": product_id,
            "product_name": name,
            "price": price,
            "time": now.strftime("%H:%M:%S"),
        }
        st.toast(f"🎉 Order {order_id} placed and auto-satisfied! (${price:.2f})", icon="✅")
    except Exception as e:
        st.error(f"Error completing instant purchase: {e}")


def add_product_to_cart_direct(product_id: int):
    try:
        from src.tools import set_thread_id, get_cart, _product_lookup, get_product_price
        tid = st.session_state.thread_id
        set_thread_id(tid)
        cart = get_cart()
        if isinstance(cart, dict):
            cart[product_id] = cart.get(product_id, 0) + 1
        direct_cart_update()
        p_info = get_product_details(product_id)
        pname = p_info.get("product_name", f"Product #{product_id}") if p_info else f"Product #{product_id}"
        st.toast(f"🛒 Added '{pname[:30]}' to your cart!", icon="🛍️")
    except Exception as e:
        st.error(f"Error adding to cart: {e}")


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
        "active_product_id": None,
        "last_instant_order": None,
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
    st.session_state.active_product_id = None
    st.session_state.last_instant_order = None


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


def render_product_page(product_id: int):
    p_info = get_product_details(product_id)
    if not p_info:
        st.error("Product not found in store catalog.")
        if st.button("⬅️ Back to Chat Concierge", key="err_back_chat"):
            st.session_state.active_product_id = None
            st.rerun()
        return

    p_name = p_info.get("product_name", f"Product #{product_id}")
    p_price = float(p_info.get("price", 0.0))
    p_brand = p_info.get("brand", "SmartShop Elite")
    p_rating = float(p_info.get("rating", 4.8))
    p_reviews = int(p_info.get("review_count", 120))
    p_desc = p_info.get("description", "Premium catalog item.")
    p_dept = p_info.get("department", "General")
    p_aisle = p_info.get("aisle", "General")

    # Navigation header
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("⬅️ Back to Chat Concierge", key="btn_back_chat_top", use_container_width=True):
            st.session_state.active_product_id = None
            st.rerun()
    with col_nav2:
        if st.session_state.get("last_instant_order") and st.session_state.last_instant_order.get("product_id") == product_id:
            oid = st.session_state.last_instant_order["order_id"]
            if st.button(f"📦 Ask Concierge to Track Order {oid}", key="btn_track_this_order", use_container_width=True):
                st.session_state.active_product_id = None
                send_user_message(f"Can you track my order {oid}?")
                st.rerun()

    # Celebratory Banner if recently ordered
    if st.session_state.get("last_instant_order") and st.session_state.last_instant_order.get("product_id") == product_id:
        lo = st.session_state.last_instant_order
        st.markdown(f"""
        <div class="order-celebrate-box">
            <div style="font-size:1.18rem;font-weight:800;color:#065f46;margin-bottom:6px;font-family:'Outfit',sans-serif;">
                🎉 Order Placed & Auto-Satisfied for Testing!
            </div>
            <div style="font-size:0.94rem;color:#064e3b;line-height:1.7;">
                • <strong>Order ID:</strong> <code style="color:#0369a1;background:#e0f2fe;font-weight:700;">{lo['order_id']}</code><br>
                • <strong>Product:</strong> {lo['product_name']}<br>
                • <strong>Total Paid:</strong> ${lo['price']:.2f}<br>
                • <strong>Status:</strong> <span style="color:#059669;font-weight:800;">Delivered Immediately · Auto-Satisfied Self-Test Mode</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main Product Detail Hero
    st.markdown(f"""
    <div class="prod-page-container">
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
            <span class="prod-page-badge">🏪 {p_dept}</span>
            <span class="prod-page-badge" style="background:#faf5ff;border-color:#e9d5ff;color:#7e22ce;">🏷️ {p_brand}</span>
            <span class="prod-page-badge" style="background:#ecfdf5;border-color:#a7f3d0;color:#047857;">🟢 In Stock · Immediate Delivery</span>
        </div>
        <div class="prod-page-title">{p_name}</div>
        <div style="display:flex;align-items:baseline;margin-bottom:20px;">
            <span class="prod-page-price">${p_price:.2f}</span>
            <span style="font-size:0.95rem;color:#475569;">⭐ <strong>{p_rating:.1f}/5.0</strong> ({p_reviews:,} verified buyer reviews)</span>
        </div>
        <div style="font-size:1.02rem;color:#334155;line-height:1.75;margin-bottom:24px;background:#f8fafc;padding:16px 20px;border-radius:16px;border:1px solid #e2e8f0;">
            {p_desc}
        </div>
        <div class="prod-spec-grid">
            <div class="prod-spec-card">
                <div class="prod-spec-label">Product ID</div>
                <div class="prod-spec-val">#{product_id}</div>
            </div>
            <div class="prod-spec-card">
                <div class="prod-spec-label">Department</div>
                <div class="prod-spec-val">{p_dept}</div>
            </div>
            <div class="prod-spec-card">
                <div class="prod-spec-label">Aisle Category</div>
                <div class="prod-spec-val">{p_aisle}</div>
            </div>
            <div class="prod-spec-card">
                <div class="prod-spec-label">Customer Rating</div>
                <div class="prod-spec-val">{p_rating:.1f} / 5.0 (98% Positive)</div>
            </div>
            <div class="prod-spec-card">
                <div class="prod-spec-label">Guarantee</div>
                <div class="prod-spec-val">30-Day Money Back</div>
            </div>
            <div class="prod-spec-card">
                <div class="prod-spec-label">Shipping</div>
                <div class="prod-spec-val">Free Next-Day Delivery</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action Buttons
    st.markdown('<div style="font-size:0.8rem;font-weight:800;letter-spacing:1.2px;color:#4f46e5;text-transform:uppercase;margin-bottom:12px;">⚡ Product Actions & Instant Testing</div>', unsafe_allow_html=True)
    btn_c1, btn_c2, btn_c3 = st.columns([2, 2, 2])
    with btn_c1:
        if st.button("⚡ Buy Now (Auto-Satisfied)", key="btn_page_buy_now", use_container_width=True):
            instant_buy_product(product_id)
            st.rerun()
    with btn_c2:
        if st.button("🛒 Add to Cart", key="btn_page_add_cart", use_container_width=True):
            add_product_to_cart_direct(product_id)
            st.rerun()
    with btn_c3:
        if st.button("💬 Ask Concierge About Item", key="btn_page_ask_agent", use_container_width=True):
            st.session_state.active_product_id = None
            send_user_message(f"Tell me more about {p_name} and customer review highlights.")
            st.rerun()

    # Also provide collapsible chat preview so context isn't lost
    with st.expander("💬 View Conversation History with Concierge", expanded=False):
        for h_msg in st.session_state.chat_history:
            h_role = h_msg.get("role", "assistant")
            h_text = h_msg.get("content", "")
            if h_role in ["user", "assistant"]:
                with st.chat_message(h_role):
                    st.markdown(h_text)


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

    # ── Direct Product Page Explorer ──
    df_cat = get_catalog_data()
    if not df_cat.empty:
        with st.expander(f"🛍️ Direct Product Explorer ({len(df_cat)} Items)", expanded=False):
            prod_options = {
                int(row["product_id"]): f"#{int(row['product_id'])} · {str(row['product_name'])[:28]}... (${float(row.get('price', 0.0)):.2f})"
                for _, row in df_cat.iterrows()
            }
            sel_pid = st.selectbox(
                "Pick a product to view:",
                options=list(prod_options.keys()),
                format_func=lambda x: prod_options[x],
                key="sb_select_prod_picker",
            )
            if st.button("📄 Open Product Page", key="sb_btn_open_prod", use_container_width=True):
                st.session_state.active_product_id = sel_pid
                st.rerun()

    with st.expander("📁 Department Catalog (10 Categories)", expanded=False):
        st.markdown("""
        * **📱 Electronics & Mobile**: Flagship smartphones, tablets, smartwatches, fast chargers
        * **💻 Computers & Gaming**: M3 Max MacBooks, OLED displays, PS5 Pro, custom keyboards
        * **🎧 Audio & Sound**: Noise-cancelling headphones, waterproof Bluetooth speakers
        * **👟 Footwear & Athletic**: Road & trail marathon shoes, waterproof hiking boots
        * **🧥 Fashion & Outerwear**: GORE-TEX alpine shells, 800-fill down parkas, travel bags
        * **☕ Home & Kitchen**: Touchscreen espresso machines, commercial blenders, cast iron
        * **🏃 Sports & Outdoors**: Percussive therapy, adjustable dumbbells, ultralight tents
        * **✨ Beauty, Skincare & Sun Care**: Wet-skin sunscreens, mineral zinc, targeted serums
        * **🍫 Gourmet & Nutrition**: Whey isolate, ceremonial Uji matcha, zero-sugar electrolytes
        * **📚 Books & Stationery**: Sci-fi masterpieces, productivity classics, luxury fountain pens
        """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.75rem;color:#64748b;text-align:center;line-height:1.8;">
        LangGraph &nbsp;·&nbsp; Gemini &nbsp;·&nbsp; ChromaDB<br>
        <span style="color:#4f46e5;font-weight:700;">SmartShop Elite v2.5 · Classic Edition</span>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN — HEADER & VIEW ROUTING
# ═══════════════════════════════════════════════════════════════════════════════
is_sales = st.session_state.current_mode == "sales_rep"
mode_class = "sales" if is_sales else "support"
mode_label = "Sales Representative" if is_sales else "Customer Support"

st.markdown(f"""
<div class="ss-header">
    <div class="ss-logo-icon">🛒</div>
    <div class="ss-logo-text">
        <div class="ss-logo-title">SmartShop Elite</div>
        <div class="ss-logo-sub">Autonomous Retail Concierge · Multi-Agent RAG</div>
    </div>
    <span class="ss-mode-badge {mode_class}">{mode_label}</span>
</div>
<div class="feature-pill-strip">
    <span class="feature-pill-item">📦 <strong>325+ Catalog Items</strong></span>
    <span class="feature-pill-item">🔬 <strong>Deep Spec & Chemical Analysis</strong></span>
    <span class="feature-pill-item">⚡ <strong>One-Click Test Purchase</strong></span>
    <span class="feature-pill-item">🤖 <strong>LangGraph Multi-Agent Engine</strong></span>
</div>""", unsafe_allow_html=True)

# ── CONDITIONAL VIEW: PRODUCT PAGE OR CONCIERGE CHAT ──
if st.session_state.get("active_product_id"):
    render_product_page(st.session_state.active_product_id)
else:
    # ── Permanent Catalog & Questions Guide ──
    with st.expander("💡 What Products Can I Ask About? (Browse 325+ Items Across 10 Departments)", expanded=not bool(st.session_state.chat_history)):
        st.markdown("""
        You can ask me to **recommend**, **search**, **compare**, or **check specifications & reviews** for products across our catalog:
        
        * **✨ Beauty, Skincare & Sun Care**: *Neutrogena Wet Skin Kids Spray SPF 70+ (cuts through water), Neutrogena Wet Skin Stick SPF 70+, Shiseido SynchroShield WetForce SPF 50+, La Roche-Posay Anthelios Melt-in Milk SPF 60, EltaMD UV Clear SPF 46, Supergoop! Unseen SPF 40, Biore UV Aqua Rich Watery Essence, Skin1004 Centella Sun Serum, Beauty of Joseon Relief Sun*
        * **📱 Electronics & Mobile**: *Apple iPhone 16 Pro Max, Samsung Galaxy S24 Ultra, Google Pixel 9 Pro XL, OnePlus 12, iPad Pro 13" M4 OLED, Apple Watch Ultra 2, Garmin Fenix 8, Anker Prime 27650mAh*
        * **💻 Computers & Gaming**: *MacBook Pro 16" M3 Max, Dell XPS 16 OLED, ASUS ROG Zephyrus G16, PS5 Pro 2TB, Steam Deck OLED 1TB, Keychron Q1 Pro, Logitech MX Master 3S*
        * **🎧 Audio & Sound**: *Sony WH-1000XM5, Bose QuietComfort Ultra, Apple AirPods Max, AirPods Pro 2 USB-C, Sonos Arc Soundbar, JBL Charge 5 Waterproof*
        * **👟 Footwear**: *Nike Alphafly 3 Marathon Shoes, Hoka Bondi 8 Max Cushion, Brooks Ghost 16, Salomon Speedcross 6 GORE-TEX, New Balance 990v6, Merrell Moab 3*
        * **🧥 Fashion & Apparel**: *Arc'teryx Beta AR GORE-TEX Pro, Patagonia Down Sweater Hoody, The North Face 1996 Nuptse, Bellroy Classic Backpack Plus*
        * **☕ Home & Kitchen**: *Breville Barista Touch Impress, Fellow Ode Gen 2 Grinder, Vitamix A3500 Ascent, Roborock S8 Pro Ultra, Dyson V15 Detect, Le Creuset Dutch Oven*
        * **🏃 Sports & Outdoors**: *Theragun PRO Plus 6-in-1, Bowflex SelectTech 552 Dumbbells, Manduka PRO Yoga Mat, MSR Hubba Hubba 2-Person Tent, Hydro Flask 32oz*
        * **🍫 Gourmet & Nutrition**: *Optimum Nutrition Gold Standard Whey, Stumptown Hair Bender Coffee, Ippodo Sayaka Ceremonial Matcha, LMNT Electrolyte Variety Pack*
        * **📚 Books & Stationery**: *Project Hail Mary, Dune Deluxe Hardcover, Atomic Habits, Pilot Custom 823 Fountain Pen, Leuchtturm1919 Journal*
        """)

    # ── WELCOME HERO & QUICK-START CARDS (When chat is empty) ──
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-hero">
            <div class="welcome-icon">✨</div>
            <div class="welcome-title">Welcome to SmartShop Elite</div>
            <div class="welcome-subtitle">
                Your personal retail concierge powered by <strong>LangGraph Multi-Agent architecture</strong> and <strong>Google Gemini RAG</strong>.<br>
                Discover 325+ curated products with semantic vector search, analyze chemical and technical specifications, compare items, and enjoy seamless one-click ordering.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="text-align:center;font-size:0.75rem;font-weight:800;letter-spacing:1.5px;color:#4f46e5;text-transform:uppercase;margin-bottom:14px;">Curated Suggestions & Prompts</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("☀️ Sunscreens with wet skin application technology", key="hero_sug_sunscreen", use_container_width=True):
                send_user_message("Suggest sunscreens with wet skin technology and analyze their specifications.")
                st.rerun()
            if st.button("🎧 Compare Sony WH-1000XM5 & Bose Ultra", key="hero_sug_audio", use_container_width=True):
                send_user_message("Compare Sony WH-1000XM5 and Bose QuietComfort Ultra headphones.")
                st.rerun()
            if st.button("👟 Find top-rated running shoes with maximum cushioning", key="hero_sug_shoes", use_container_width=True):
                send_user_message("Find top-rated running shoes with maximum cushioning.")
                st.rerun()
        with col2:
            if st.button("💻 Find Apple MacBook & pro creator laptops", key="hero_sug_laptop", use_container_width=True):
                send_user_message("Find Apple MacBook and high-performance creator laptops.")
                st.rerun()
            if st.button("☕ Recommend the best home barista espresso machines", key="hero_sug_coffee", use_container_width=True):
                send_user_message("Recommend the best home barista espresso machines.")
                st.rerun()
            if st.button("📦 Track my recent orders and delivery status", key="hero_sug_orders", use_container_width=True):
                send_user_message("Can you track my recent orders?")
                st.rerun()

    # ── CHAT MESSAGES DISPLAY (Rich Native Markdown + Glass Cards) ──
    for msg_idx, msg in enumerate(st.session_state.chat_history):
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

                # Interactive Product Badges / Tap to view product page
                detected_pids = extract_product_ids_from_text(content)
                if detected_pids:
                    st.markdown('<div class="prod-tap-header">🔍 <strong>Featured Product Matches</strong> · Tap to inspect specs or one-click buy:</div>', unsafe_allow_html=True)
                    for idx_p, pid in enumerate(detected_pids):
                        p_info = get_product_details(pid)
                        if p_info:
                            p_name = p_info.get("product_name", f"Product #{pid}")
                            p_price = float(p_info.get("price", 0.0))
                            p_brand = p_info.get("brand", "")
                            p_dept = p_info.get("department", "Store Item")
                            p_aisle = p_info.get("aisle", "General")
                            b_prefix = f"[{p_brand}] " if p_brand else ""
                            st.markdown(f"""
                            <div class="chat-prod-card-preview">
                                <div>
                                    <div class="chat-prod-card-title">🏷️ {b_prefix}{p_name}</div>
                                    <div class="chat-prod-card-sub">Department: {p_dept} · Aisle: {p_aisle} · ID #{pid}</div>
                                </div>
                                <div style="text-align:right;">
                                    <span style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.18rem;color:#059669;">${p_price:.2f}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            col_card_a, col_card_b = st.columns([3, 2])
                            with col_card_a:
                                if st.button(f"📄 View Product Details & Specs", key=f"chat_tap_prod_{msg_idx}_{pid}_{idx_p}", use_container_width=True):
                                    st.session_state.active_product_id = pid
                                    st.rerun()
                            with col_card_b:
                                if st.button(f"⚡ Instant Buy (${p_price:.2f})", key=f"chat_fast_buy_{msg_idx}_{pid}_{idx_p}", use_container_width=True):
                                    instant_buy_product(pid)
                                    st.rerun()

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
                        live_pids = extract_product_ids_from_text(reply_text)
                        if live_pids:
                            st.markdown('<div class="prod-tap-header">🔍 <strong>Featured Product Matches</strong> · Tap to inspect specs or one-click buy:</div>', unsafe_allow_html=True)
                            for idx_p, pid in enumerate(live_pids):
                                p_info = get_product_details(pid)
                                if p_info:
                                    p_name = p_info.get("product_name", f"Product #{pid}")
                                    p_price = float(p_info.get("price", 0.0))
                                    p_brand = p_info.get("brand", "")
                                    p_dept = p_info.get("department", "Store Item")
                                    p_aisle = p_info.get("aisle", "General")
                                    b_prefix = f"[{p_brand}] " if p_brand else ""
                                    st.markdown(f"""
                                    <div class="chat-prod-card-preview">
                                        <div>
                                            <div class="chat-prod-card-title">🏷️ {b_prefix}{p_name}</div>
                                            <div class="chat-prod-card-sub">Department: {p_dept} · Aisle: {p_aisle} · ID #{pid}</div>
                                        </div>
                                        <div style="text-align:right;">
                                            <span style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.18rem;color:#059669;">${p_price:.2f}</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    col_card_a, col_card_b = st.columns([3, 2])
                                    with col_card_a:
                                        if st.button(f"📄 View Product Details & Specs", key=f"chat_tap_prod_live_{pid}_{idx_p}", use_container_width=True):
                                            st.session_state.active_product_id = pid
                                            st.rerun()
                                    with col_card_b:
                                        if st.button(f"⚡ Instant Buy (${p_price:.2f})", key=f"chat_fast_buy_live_{pid}_{idx_p}", use_container_width=True):
                                            instant_buy_product(pid)
                                            st.rerun()
                except Exception as err:
                    status_box.update(label="⚠️ **Request failed**", state="error", expanded=True)
                    st.error(f"Error: {err}")
                    st.session_state.chat_history.append({"role": "error", "content": str(err)})

        st.rerun()

    # ── HUMAN APPROVAL INTERRUPT PANEL ──
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

    # ── PERSISTENT QUICK SUGGESTIONS & PINNED CHAT INPUT ──
    st.markdown('<div style="margin-top:20px;margin-bottom:10px;font-size:0.76rem;font-weight:800;letter-spacing:1.2px;color:#4f46e5;text-transform:uppercase;">⚡ Quick Suggestions & Direct Testing Queries</div>', unsafe_allow_html=True)
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

