"""Agent package — Onyx chat integration.

The conversational agent layer is handled by `Onyx <https://onyx.app>`_, an
open-source AI assistant platform.  Onyx provides the chat UI, LLM
orchestration, conversational memory, and tool routing.  It connects to the
prediction server via the **Model Context Protocol (MCP)**, consuming the
``/mcp`` endpoint exposed by ``fastapi-mcp``.

This package is intentionally minimal because Onyx replaces the need for a
custom LangChain agent.  See ``.docs/onyx_integration.md`` for the full setup
guide.
"""
