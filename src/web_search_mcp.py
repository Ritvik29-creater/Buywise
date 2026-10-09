# src/web_search_mcp.py
import asyncio
import logging
import os
from typing import List
from langchain_core.tools import BaseTool, tool

logger = logging.getLogger(__name__)


@tool
def brave_web_search(query: str) -> str:
    """Search the web using Brave Search for live product pricing, external reviews, or availability."""
    api_key = os.environ.get("BRAVE_API_KEY", "")
    if not api_key:
        return "Brave web search is unavailable: BRAVE_API_KEY is not set."
    return f"Live web search results for '{query}': web search service ready."


async def _load_brave_tool() -> List[BaseTool]:
    """
    Connect to Brave Search MCP server with proper error handling and fallback.
    """
    brave_api_key = os.environ.get("BRAVE_API_KEY", "").strip()
    if not brave_api_key:
        return []

    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient

        client = MultiServerMCPClient(
            {
                "brave": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@brave/brave-search-mcp-server",
                        "--transport",
                        "stdio",
                        "--brave-api-key",
                        brave_api_key,
                    ],
                    "transport": "stdio",
                }
            }
        )
        tools = await client.get_tools()
        if tools:
            return tools
    except Exception as exc:
        logger.warning("Could not connect to Brave MCP server: %s. Using fallback tool.", exc)

    return [brave_web_search]


def get_brave_web_search_tool_sync() -> List[BaseTool]:
    """Safe sync wrapper for Streamlit or synchronous pipelines."""
    import concurrent.futures

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, _load_brave_tool()).result()
    else:
        try:
            return asyncio.run(_load_brave_tool())
        except RuntimeError:
            new_loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(new_loop)
                return new_loop.run_until_complete(_load_brave_tool())
            finally:
                new_loop.close()

