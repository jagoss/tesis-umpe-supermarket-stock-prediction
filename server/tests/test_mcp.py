"""Tests for MCP endpoint integration."""
from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> TestClient:
    """Create a test client with the dummy model backend."""
    with patch.dict(os.environ, {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "10"}, clear=False):
        import server.infrastructure.container as container_mod

        container_mod._singleton_uc = None

        from server.interface.http.api import app

        with TestClient(app) as c:
            yield c

        container_mod._singleton_uc = None


class TestMCPEndpoint:
    """Verify the MCP transport is reachable after mounting."""

    def test_mcp_endpoint_not_404(self, client: TestClient) -> None:
        """The /mcp path should be mounted and not return 404."""
        resp = client.post("/mcp", json={"jsonrpc": "2.0", "method": "initialize", "id": 1})
        assert resp.status_code != 404


class TestHTTPEndpointsAfterMCPMount:
    """Ensure existing HTTP endpoints still work after MCP is mounted."""

    def test_health_still_works(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_predict_still_works(self, client: TestClient) -> None:
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
