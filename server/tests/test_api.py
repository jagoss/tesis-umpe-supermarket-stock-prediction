"""Tests for the FastAPI HTTP endpoints."""

from __future__ import annotations

import os
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Create a test client with the dummy model backend."""
    env = {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "10"}
    with patch.dict(os.environ, env, clear=False):
        # Reset the singleton so it picks up our env vars
        import server.infrastructure.container as container_mod

        container_mod._singleton_uc = None

        from server.interface.http.api import app

        with TestClient(app) as c:
            yield c

        # Clean up singleton after test
        container_mod._singleton_uc = None


class TestHealthEndpoint:
    def test_health_ok(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestPredictEndpoint:
    def test_valid_request(self, client: TestClient) -> None:
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
        assert data["store_id"] == "STORE-A"
        assert len(data["predictions"]) == 3

    def test_valid_request_with_history(self, client: TestClient) -> None:
        payload = {
            "product_id": "PROD-001",
            "store_id": "STORE-A",
            "start_date": "2026-03-02",
            "end_date": "2026-03-02",
            "history": [
                {"date": "2026-03-01", "quantity": 5.0},
            ],
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 200
        assert len(resp.json()["predictions"]) == 1

    def test_end_before_start_returns_400(self, client: TestClient) -> None:
        payload = {
            "product_id": "PROD-001",
            "store_id": "STORE-A",
            "start_date": "2026-03-10",
            "end_date": "2026-03-05",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 400

    def test_missing_product_id_returns_422(self, client: TestClient) -> None:
        payload = {
            "store_id": "STORE-A",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 422

    def test_empty_product_id_returns_422(self, client: TestClient) -> None:
        payload = {
            "product_id": "",
            "store_id": "STORE-A",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 422

    def test_predictions_have_dates(self, client: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client.post("/predict", json=payload)
        data = resp.json()
        dates = [p["date"] for p in data["predictions"]]
        assert dates == ["2026-03-02", "2026-03-03", "2026-03-04"]

    def test_predictions_quantities_are_integers(self, client: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        resp = client.post("/predict", json=payload)
        data = resp.json()
        for p in data["predictions"]:
            assert isinstance(p["quantity"], int)

    def test_domain_error_returns_422(self, client: TestClient) -> None:
        from server.domain import DomainError

        with patch(
            "server.interface.http.api.get_predict_use_case_singleton"
        ) as mock_uc_factory:
            mock_uc = MagicMock()
            mock_uc.execute.side_effect = DomainError("model failed")
            mock_uc_factory.return_value = mock_uc

            payload = {
                "product_id": "P1",
                "store_id": "S1",
                "start_date": "2026-03-02",
                "end_date": "2026-03-04",
            }
            resp = client.post("/predict", json=payload)

        assert resp.status_code == 422
        assert "model failed" in resp.json()["detail"]

    def test_unexpected_exception_returns_500(self, client: TestClient) -> None:
        with patch(
            "server.interface.http.api.get_predict_use_case_singleton"
        ) as mock_uc_factory:
            mock_uc = MagicMock()
            mock_uc.execute.side_effect = RuntimeError("unexpected boom")
            mock_uc_factory.return_value = mock_uc

            payload = {
                "product_id": "P1",
                "store_id": "S1",
                "start_date": "2026-03-02",
                "end_date": "2026-03-04",
            }
            resp = client.post("/predict", json=payload)

        assert resp.status_code == 500
        assert resp.json()["detail"] == "internal server error"


class TestRateLimitHandler:
    def test_rate_limit_exceeded_handler_returns_429(self) -> None:
        from server.interface.http.api import _rate_limit_exceeded_handler

        mock_request = MagicMock(spec=Request)
        mock_exc = MagicMock(spec=RateLimitExceeded)

        response = _rate_limit_exceeded_handler(mock_request, mock_exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 429
        import json
        body = json.loads(response.body)
        assert body == {"detail": "Rate limit exceeded"}


class TestLifespan:
    def test_lifespan_initializes_use_case(self) -> None:
        """Lifespan startup calls get_predict_use_case_singleton to warm up the DI container."""
        import os

        env = {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "0"}
        with patch.dict(os.environ, env, clear=False):
            import server.infrastructure.container as container_mod

            container_mod._singleton_uc = None

            with patch(
                "server.interface.http.api.get_predict_use_case_singleton"
            ) as mock_factory, patch(
                "server.interface.http.api.configure_logging"
            ):
                mock_factory.return_value = MagicMock()

                from server.interface.http.api import app

                with TestClient(app):
                    mock_factory.assert_called()

            container_mod._singleton_uc = None
