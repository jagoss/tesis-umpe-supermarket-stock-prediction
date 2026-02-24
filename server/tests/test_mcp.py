"""Tests for MCP endpoint integration.

Verifies that the ``fastapi-mcp`` transport is mounted correctly, exposes
the ``predict_stock`` tool, and returns valid predictions when called
through the JSON-RPC / MCP protocol.

Async tests use ``LifespanManager`` to properly initialize the FastAPI
application lifespan, which is required by the MCP
``StreamableHTTPSessionManager``.

**Implementation note:** The MCP ``StreamableHTTPSessionManager`` cannot be
restarted after shutdown. Each test that needs the MCP transport must reload
the ``api`` module to obtain a fresh ``app`` instance with a fresh MCP
session manager.
"""

from __future__ import annotations

import importlib
import json
import os
from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import patch

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


@pytest.fixture(autouse=True)
def _dummy_env() -> Generator[None, None, None]:
    """Patch environment to use the dummy model backend."""
    with patch.dict(
        os.environ,
        {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "10"},
        clear=False,
    ):
        import server.infrastructure.container as container_mod

        container_mod._singleton_uc = None
        yield
        container_mod._singleton_uc = None


def _create_fresh_app() -> FastAPI:
    """Reload the API module to get a fresh FastAPI app with a new MCP session manager."""
    import server.interface.http.api as api_mod

    importlib.reload(api_mod)
    return api_mod.app


@pytest.fixture()
async def mcp_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client with proper ASGI lifespan management.

    Creates a **fresh** ``app`` instance (via module reload) so the MCP
    ``StreamableHTTPSessionManager`` is properly initialized.
    """
    app = _create_fresh_app()

    async with LifespanManager(app) as manager:
        transport = ASGITransport(app=manager.app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client


async def _mcp_initialize(client: AsyncClient) -> str:
    """Perform MCP ``initialize`` + ``notifications/initialized`` handshake.

    Returns the session ID needed for subsequent requests.
    """
    resp = await client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1,
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"},
            },
        },
        headers=MCP_HEADERS,
    )
    assert resp.status_code == 200
    session_id = resp.headers["mcp-session-id"]

    await client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "method": "notifications/initialized"},
        headers={"Content-Type": "application/json", "Mcp-Session-Id": session_id},
    )
    return session_id


# ---------------------------------------------------------------------------
# Synchronous tests — basic reachability checks (no MCP protocol flow)
# ---------------------------------------------------------------------------
class TestMCPEndpoint:
    """Verify the MCP transport is reachable after mounting."""

    def test_mcp_endpoint_not_404(self) -> None:
        """The /mcp path should be mounted and not return 404."""
        from fastapi.testclient import TestClient

        app = _create_fresh_app()
        with TestClient(app) as client:
            resp = client.post(
                "/mcp",
                json={"jsonrpc": "2.0", "method": "initialize", "id": 1},
            )
            assert resp.status_code != 404


class TestHTTPEndpointsAfterMCPMount:
    """Ensure existing HTTP endpoints still work after MCP is mounted."""

    def test_health_still_works(self) -> None:
        from fastapi.testclient import TestClient

        app = _create_fresh_app()
        with TestClient(app) as client:
            resp = client.get("/health")
            assert resp.status_code == 200
            assert resp.json() == {"status": "ok"}

    def test_predict_still_works(self) -> None:
        from fastapi.testclient import TestClient

        app = _create_fresh_app()
        with TestClient(app) as client:
            payload = {
                "product_id": "PROD-001",
                "store_id": "STORE-A",
                "start_date": "2026-03-02",
                "end_date": "2026-03-04",
            }
            resp = client.post("/predict", json=payload)
            assert resp.status_code == 200
            data = resp.json()
            assert data["product_id"] == "PROD-001"
            assert len(data["predictions"]) == 3


# ---------------------------------------------------------------------------
# Async tests — full MCP protocol flow
# ---------------------------------------------------------------------------
class TestMCPInitialization:
    """Verify the MCP initialize handshake."""

    @pytest.mark.anyio
    async def test_initialize_returns_200(self, mcp_client: AsyncClient) -> None:
        resp = await mcp_client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "id": 1,
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0"},
                },
            },
            headers=MCP_HEADERS,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["result"]["serverInfo"]["name"] == "Supermarket Stock Prediction MCP"

    @pytest.mark.anyio
    async def test_initialize_returns_session_id(self, mcp_client: AsyncClient) -> None:
        resp = await mcp_client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "id": 1,
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0"},
                },
            },
            headers=MCP_HEADERS,
        )
        assert "mcp-session-id" in resp.headers


class TestMCPToolListing:
    """Verify that ``tools/list`` exposes the expected tools."""

    @pytest.mark.anyio
    async def test_tools_list_contains_predict_stock(self, mcp_client: AsyncClient) -> None:
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "method": "tools/list", "id": 2},
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        assert resp.status_code == 200
        tools = resp.json()["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert "predict_stock" in tool_names

    @pytest.mark.anyio
    async def test_health_excluded_from_tools(self, mcp_client: AsyncClient) -> None:
        """The ``check_health`` operation should NOT appear as an MCP tool."""
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "method": "tools/list", "id": 2},
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        tools = resp.json()["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert "check_health" not in tool_names

    @pytest.mark.anyio
    async def test_predict_stock_tool_has_description(self, mcp_client: AsyncClient) -> None:
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "method": "tools/list", "id": 2},
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        tools = resp.json()["result"]["tools"]
        predict_tool = next(t for t in tools if t["name"] == "predict_stock")
        assert len(predict_tool["description"]) > 0

    @pytest.mark.anyio
    async def test_predict_stock_tool_has_input_schema(self, mcp_client: AsyncClient) -> None:
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "method": "tools/list", "id": 2},
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        tools = resp.json()["result"]["tools"]
        predict_tool = next(t for t in tools if t["name"] == "predict_stock")
        schema = predict_tool["inputSchema"]
        assert "product_id" in str(schema)
        assert "store_id" in str(schema)
        assert "start_date" in str(schema)
        assert "end_date" in str(schema)


class TestMCPToolInvocation:
    """Verify calling the ``predict_stock`` tool through the MCP protocol."""

    @pytest.mark.anyio
    async def test_predict_stock_returns_predictions(self, mcp_client: AsyncClient) -> None:
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 3,
                "params": {
                    "name": "predict_stock",
                    "arguments": {
                        "product_id": "PROD-001",
                        "store_id": "STORE-A",
                        "start_date": "2026-03-02",
                        "end_date": "2026-03-04",
                    },
                },
            },
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        assert resp.status_code == 200
        result = resp.json()["result"]
        assert result["isError"] is False

        content_text = result["content"][0]["text"]
        prediction_data: dict[str, Any] = json.loads(content_text)
        assert prediction_data["product_id"] == "PROD-001"
        assert prediction_data["store_id"] == "STORE-A"
        assert len(prediction_data["predictions"]) == 3

    @pytest.mark.anyio
    async def test_predict_stock_returns_correct_dates(self, mcp_client: AsyncClient) -> None:
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 3,
                "params": {
                    "name": "predict_stock",
                    "arguments": {
                        "product_id": "P1",
                        "store_id": "S1",
                        "start_date": "2026-03-02",
                        "end_date": "2026-03-04",
                    },
                },
            },
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        content_text = resp.json()["result"]["content"][0]["text"]
        data: dict[str, Any] = json.loads(content_text)
        dates = [p["date"] for p in data["predictions"]]
        assert dates == ["2026-03-02", "2026-03-03", "2026-03-04"]

    @pytest.mark.anyio
    async def test_predict_stock_quantities_match_dummy(self, mcp_client: AsyncClient) -> None:
        """Dummy backend returns DEFAULT_PREDICTION_VALUE (10) for every point."""
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 3,
                "params": {
                    "name": "predict_stock",
                    "arguments": {
                        "product_id": "P1",
                        "store_id": "S1",
                        "start_date": "2026-03-02",
                        "end_date": "2026-03-02",
                    },
                },
            },
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        content_text = resp.json()["result"]["content"][0]["text"]
        data: dict[str, Any] = json.loads(content_text)
        assert data["predictions"][0]["quantity"] == 10

    @pytest.mark.anyio
    async def test_predict_stock_with_invalid_dates_returns_error(
        self, mcp_client: AsyncClient
    ) -> None:
        """end_date before start_date should propagate as an MCP error response."""
        session_id = await _mcp_initialize(mcp_client)

        resp = await mcp_client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 3,
                "params": {
                    "name": "predict_stock",
                    "arguments": {
                        "product_id": "P1",
                        "store_id": "S1",
                        "start_date": "2026-03-10",
                        "end_date": "2026-03-05",
                    },
                },
            },
            headers={**MCP_HEADERS, "Mcp-Session-Id": session_id},
        )
        assert resp.status_code == 200
        result = resp.json()["result"]
        assert result["isError"] is True
