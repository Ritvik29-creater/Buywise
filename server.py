#!/usr/bin/env python
# server.py — SmartShop Elite · FastAPI Backend for Agentic Retail Assistant

import asyncio
import concurrent.futures
import json
import os
import sys
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Add current directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from langgraph.types import Command
from src.graph import graph

app = FastAPI(title="SmartShop Elite API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_async(coro):
    """Safely run async coroutines across various event loop / thread states."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            def _thread_run():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                return new_loop.run_until_complete(coro)
            return pool.submit(_thread_run).result()
    else:
        return loop.run_until_complete(coro)

def get_product_price(product_id: int) -> float:
    try:
        from src.tools import get_product_price as _tool_price
        return float(_tool_price(int(product_id)))
    except Exception:
        return 0.99

def format_tool_call(tool_call: dict) -> str:
    name = tool_call.get('name', 'unknown')
    args = tool_call.get('args', {})
    parts = [f"{k}={json.dumps(v)}" for k, v in args.items()]
    return f"{name}({', '.join(parts)})"

def serialize_messages(messages: list) -> list:
    """Transform LangChain/LangGraph messages into clean frontend-ready items."""
    output = []
    for msg in messages:
        msg_type = msg.__class__.__name__
        content = getattr(msg, 'content', '')
        if msg_type == 'AIMessage':
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    output.append({
                        'role': 'tool_call',
                        'content': format_tool_call(tc),
                        'tool_name': tc.get('name', 'tool'),
                        'raw_args': tc.get('args', {})
                    })
            elif content:
                output.append({
                    'role': 'assistant',
                    'content': content
                })
        elif msg_type == 'ToolMessage':
            tc_id = getattr(msg, 'tool_call_id', '')
            tool_name = getattr(msg, 'name', '') or 'tool'
            for prev in messages:
                if hasattr(prev, 'tool_calls'):
                    for tc in prev.tool_calls:
                        if tc.get('id') == tc_id:
                            tool_name = tc.get('name', tool_name)
                            break
            output.append({
                'role': 'tool_result',
                'content': content,
                'tool_name': tool_name
            })
    return output

def extract_cart(thread_id: str) -> dict:
    """Fetch live shopping cart state from the session tools."""
    try:
        from src.tools import _product_lookup, get_cart, set_thread_id
        set_thread_id(thread_id)
        cart = get_cart()
        if isinstance(cart, list):
            return {}
        cart_items = {}
        for pid, qty in cart.items():
            title = _product_lookup.get(pid, f"Product #{pid}")
            price = get_product_price(pid)
            cart_items[str(pid)] = {
                'id': str(pid),
                'name': title,
                'quantity': int(qty),
                'price': float(price),
                'subtotal': round(float(price) * int(qty), 2)
            }
        return cart_items
    except Exception as e:
        print(f"Cart extraction note: {e}")
        return {}

class ChatRequest(BaseModel):
    thread_id: str
    message: str

class SupervisorRequest(BaseModel):
    thread_id: str
    response: str

@app.get('/api/new-session')
async def new_session():
    new_id = str(uuid.uuid4())
    return {'thread_id': new_id}

@app.post('/api/chat')
async def chat_endpoint(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    config = {'configurable': {'thread_id': req.thread_id}}
    try:
        from src.tools import set_thread_id
        set_thread_id(req.thread_id)
        
        # Invoke state graph
        graph.invoke({'messages': [('user', req.message)]}, config)
        
        snapshot = graph.get_state(config)
        state = snapshot.values
        dialog_state = state.get('dialog_state', [])
        current_mode = dialog_state[-1] if dialog_state else 'sales_rep'
        
        # Check for supervisor approval interrupts
        interrupt_info = None
        for task in snapshot.tasks:
            if hasattr(task, 'interrupts') and task.interrupts:
                for intr in task.interrupts:
                    if hasattr(intr, 'value') and isinstance(intr.value, dict):
                        interrupt_info = intr.value
                        
        messages = state.get('messages', [])
        new_msgs = serialize_messages(messages)
        cart = extract_cart(req.thread_id)
        
        return {
            'messages': new_msgs,
            'current_mode': current_mode,
            'pending_approval': interrupt_info,
            'cart': cart
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/supervisor')
async def supervisor_endpoint(req: SupervisorRequest):
    if not req.response or not req.response.strip():
        raise HTTPException(status_code=400, detail="Supervisor decision cannot be empty")
        
    config = {'configurable': {'thread_id': req.thread_id}}
    try:
        from src.tools import set_thread_id
        set_thread_id(req.thread_id)
        
        graph.invoke(Command(resume=req.response), config)
        
        snapshot = graph.get_state(config)
        state = snapshot.values
        dialog_state = state.get('dialog_state', [])
        current_mode = dialog_state[-1] if dialog_state else 'sales_rep'
        
        messages = state.get('messages', [])
        new_msgs = serialize_messages(messages)
        cart = extract_cart(req.thread_id)
        
        return {
            'messages': new_msgs,
            'current_mode': current_mode,
            'pending_approval': None,
            'cart': cart
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/cart/{thread_id}')
async def get_cart_endpoint(thread_id: str):
    return {'cart': extract_cart(thread_id)}

# Serve static web folder
static_dir = os.path.join(BASE_DIR, 'web')
if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')

@app.get('/')
async def index_page():
    index_path = os.path.join(BASE_DIR, 'web', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({'status': 'SmartShop Elite Server Running', 'web_ui': 'web/index.html missing'})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', host='0.0.0.0', port=8000, reload=True)
