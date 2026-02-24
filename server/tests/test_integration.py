"""Integration tests: full request lifecycle through the API with the dummy backend.

These tests exercise the entire stack — from the HTTP interface down to the
model adapter and back — using the ``dummy`` backend so they run without
any external model artifacts or services.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a ``TestClient`` wired to the dummy backend (constant=10)."""
    with patch.dict(
        os.environ,
        {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "10"},
        clear=False,
    ):
        import server.infrastructure.container as container_mod

        container_mod._singleton_uc = None

        from server.interface.http.api import app

        with TestClient(app) as c:
            yield c

        container_mod._singleton_uc = None


class TestFullPredictionLifecycle:
    """End-to-end request from HTTP to model and back."""

    def test_predict_single_day(self, client: TestClient) -> None:
        payload = {
            "product_id": "PROD-X",
            "store_id": "STORE-1",
            "start_date": "2026-04-01",
            "end_date": "2026-04-01",
        }
        resp = client.post("/predict", json=payload)

        assert resp.status_code == 200
        data: dict[str, Any] = resp.json()
        assert data["product_id"] == "PROD-X"
        assert data["store_id"] == "STORE-1"
        assert len(data["predictions"]) == 1
        assert data["predictions"][0]["date"] == "2026-04-01"
        assert data["predictions"][0]["quantity"] == 10

    def test_predict_multi_day_range(self, client: TestClient) -> None:
        payload = {
            "product_id": "PROD-Y",
            "store_id": "STORE-2",
            "start_date": "2026-04-01",
            "end_date": "2026-04-07",
        }
        resp = client.post("/predict", json=payload)

        assert resp.status_code == 200
        data: dict[str, Any] = resp.json()
        assert len(data["predictions"]) == 7
        dates = [p["date"] for p in data["predictions"]]
        assert dates == [
            "2026-04-01",
            "2026-04-02",
            "2026-04-03",
            "2026-04-04",
            "2026-04-05",
            "2026-04-06",
            "2026-04-07",
        ]
        for point in data["predictions"]:
            assert point["quantity"] == 10

    def test_predict_with_history(self, client: TestClient) -> None:
        """History is accepted and forwarded (dummy backend ignores it)."""
        payload = {
            "product_id": "PROD-Z",
            "store_id": "STORE-3",
            "start_date": "2026-04-01",
            "end_date": "2026-04-03",
            "history": [
                {"date": "2026-03-30", "quantity": 20.5},
                {"date": "2026-03-31", "quantity": 18.0},
            ],
        }
        resp = client.post("/predict", json=payload)

        assert resp.status_code == 200
        data: dict[str, Any] = resp.json()
        assert data["product_id"] == "PROD-Z"
        assert len(data["predictions"]) == 3

    def test_quantities_are_non_negative_integers(self, client: TestClient) -> None:
        payload = {
            "product_id": "P",
            "store_id": "S",
            "start_date": "2026-04-01",
            "end_date": "2026-04-05",
        }
        resp = client.post("/predict", json=payload)
        data: dict[str, Any] = resp.json()
        for point in data["predictions"]:
            assert isinstance(point["quantity"], int)
            assert point["quantity"] >= 0

    def test_response_schema_matches_prediction_response(self, client: TestClient) -> None:
        """Verify the response JSON matches the ``PredictionResponse`` schema."""
        payload = {
            "product_id": "PROD-001",
            "store_id": "STORE-A",
            "start_date": "2026-04-01",
            "end_date": "2026-04-02",
        }
        resp = client.post("/predict", json=payload)
        data: dict[str, Any] = resp.json()
        assert "product_id" in data
        assert "store_id" in data
        assert "predictions" in data
        for point in data["predictions"]:
            assert "date" in point
            assert "quantity" in point


class TestErrorHandling:
    """Verify error scenarios return appropriate HTTP status codes."""

    def test_end_date_before_start_date_returns_400(self, client: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-04-10",
            "end_date": "2026-04-05",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 400
        assert "end_date" in resp.json()["detail"].lower()

    def test_missing_required_field_returns_422(self, client: TestClient) -> None:
        payload = {
            "store_id": "S1",
            "start_date": "2026-04-01",
            "end_date": "2026-04-02",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 422

    def test_empty_product_id_returns_422(self, client: TestClient) -> None:
        payload = {
            "product_id": "",
            "store_id": "S1",
            "start_date": "2026-04-01",
            "end_date": "2026-04-02",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 422

    def test_invalid_date_format_returns_422(self, client: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "not-a-date",
            "end_date": "2026-04-02",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 422

    def test_empty_body_returns_422(self, client: TestClient) -> None:
        resp = client.post("/predict", json={})
        assert resp.status_code == 422


class TestHealthEndpointIntegration:
    """Verify the health endpoint works end-to-end."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_health_is_idempotent(self, client: TestClient) -> None:
        for _ in range(5):
            resp = client.get("/health")
            assert resp.status_code == 200

    def test_predict_after_health_works(self, client: TestClient) -> None:
        """Verify that health checks don't interfere with predictions."""
        client.get("/health")
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-04-01",
            "end_date": "2026-04-01",
        }
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 200
