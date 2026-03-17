"""Tests for HTTP middleware (correlation IDs, auth, rate limiting)."""

from __future__ import annotations

import os
from collections.abc import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def _reset_singleton() -> Generator[None, None, None]:
    import server.infrastructure.container as container_mod

    container_mod._singleton_uc = None
    yield
    container_mod._singleton_uc = None


@pytest.fixture()
def client_no_auth(_reset_singleton: None) -> Generator[TestClient, None, None]:
    """Client with auth disabled (API_KEY empty)."""
    env = {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "10", "API_KEY": ""}
    with patch.dict(os.environ, env, clear=False):
        from server.interface.http.api import app

        with TestClient(app) as c:
            yield c


@pytest.fixture()
def client_with_auth(_reset_singleton: None) -> Generator[TestClient, None, None]:
    """Client with auth enabled (API_KEY=test-secret)."""
    env = {
        "MODEL_BACKEND": "dummy",
        "DEFAULT_PREDICTION_VALUE": "10",
        "API_KEY": "test-secret",
    }
    with patch.dict(os.environ, env, clear=False):
        # Force settings reload by reimporting
        import importlib

        import server.infrastructure.config
        import server.interface.http.api

        importlib.reload(server.infrastructure.config)
        importlib.reload(server.interface.http.api)
        from server.interface.http.api import app

        with TestClient(app) as c:
            yield c

        # Reload back to defaults
        importlib.reload(server.infrastructure.config)
        importlib.reload(server.interface.http.api)


class TestCorrelationIdMiddleware:
    def test_response_contains_correlation_id(self, client_no_auth: TestClient) -> None:
        resp = client_no_auth.get("/health")
        assert "x-correlation-id" in resp.headers

    def test_echoes_provided_correlation_id(self, client_no_auth: TestClient) -> None:
        resp = client_no_auth.get("/health", headers={"X-Correlation-ID": "my-test-id"})
        assert resp.headers["x-correlation-id"] == "my-test-id"

    def test_generates_uuid_when_not_provided(self, client_no_auth: TestClient) -> None:
        resp = client_no_auth.get("/health")
        cid = resp.headers["x-correlation-id"]
        # UUID4 format: 8-4-4-4-12 hex chars
        assert len(cid) == 36
        assert cid.count("-") == 4


class TestApiKeyMiddleware:
    def test_health_bypasses_auth(self, client_with_auth: TestClient) -> None:
        resp = client_with_auth.get("/health")
        assert resp.status_code == 200

    def test_metrics_bypasses_auth(self, client_with_auth: TestClient) -> None:
        resp = client_with_auth.get("/metrics")
        assert resp.status_code == 200

    def test_predict_returns_401_without_key(self, client_with_auth: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client_with_auth.post("/predict", json=payload)
        assert resp.status_code == 401

    def test_predict_200_with_x_api_key(self, client_with_auth: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client_with_auth.post("/predict", json=payload, headers={"X-API-Key": "test-secret"})
        assert resp.status_code == 200

    def test_predict_200_with_bearer_token(self, client_with_auth: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client_with_auth.post(
            "/predict",
            json=payload,
            headers={"Authorization": "Bearer test-secret"},
        )
        assert resp.status_code == 200

    def test_predict_401_with_wrong_key(self, client_with_auth: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client_with_auth.post("/predict", json=payload, headers={"X-API-Key": "wrong-key"})
        assert resp.status_code == 401


class TestRateLimiting:
    def test_rate_limit_returns_429(self, _reset_singleton: None) -> None:
        env = {
            "MODEL_BACKEND": "dummy",
            "DEFAULT_PREDICTION_VALUE": "10",
            "API_KEY": "",
            "RATE_LIMIT": "2/minute",
        }
        with patch.dict(os.environ, env, clear=False):
            import importlib

            import server.infrastructure.config
            import server.interface.http.api

            importlib.reload(server.infrastructure.config)
            importlib.reload(server.interface.http.api)
            from server.interface.http.api import app

            with TestClient(app) as c:
                payload = {
                    "product_id": "P1",
                    "store_id": "S1",
                    "start_date": "2026-03-02",
                    "end_date": "2026-03-04",
                }
                # First two should succeed
                for _ in range(2):
                    resp = c.post("/predict", json=payload)
                    assert resp.status_code == 200

                # Third should be rate limited
                resp = c.post("/predict", json=payload)
                assert resp.status_code == 429

            importlib.reload(server.infrastructure.config)
            importlib.reload(server.interface.http.api)
