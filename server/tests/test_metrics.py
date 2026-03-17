"""Tests for Prometheus metrics endpoint."""

from __future__ import annotations

import os
from collections.abc import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Create a test client with the dummy model backend."""
    env = {"MODEL_BACKEND": "dummy", "DEFAULT_PREDICTION_VALUE": "10"}
    with patch.dict(os.environ, env, clear=False):
        import server.infrastructure.container as container_mod

        container_mod._singleton_uc = None

        from server.interface.http.api import app

        with TestClient(app) as c:
            yield c

        container_mod._singleton_uc = None


class TestMetricsEndpoint:
    def test_metrics_returns_200(self, client: TestClient) -> None:
        resp = client.get("/metrics")
        assert resp.status_code == 200

    def test_metrics_content_type(self, client: TestClient) -> None:
        resp = client.get("/metrics")
        assert "text/plain" in resp.headers["content-type"]

    def test_metrics_contains_http_metrics(self, client: TestClient) -> None:
        # Make a request first to generate metrics
        client.get("/health")
        resp = client.get("/metrics")
        body = resp.text
        assert "http" in body.lower()

    def test_metrics_contains_model_inference_after_predict(self, client: TestClient) -> None:
        payload = {
            "product_id": "P1",
            "store_id": "S1",
            "start_date": "2026-03-02",
            "end_date": "2026-03-04",
        }
        client.post("/predict", json=payload)
        resp = client.get("/metrics")
        assert "model_inference_seconds" in resp.text

    def test_metrics_not_in_openapi(self, client: TestClient) -> None:
        resp = client.get("/openapi.json")
        schema = resp.json()
        assert "/metrics" not in schema.get("paths", {})
