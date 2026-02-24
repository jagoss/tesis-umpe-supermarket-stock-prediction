"""Tests for HTTP Pydantic schemas."""

from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from server.interface.http.schemas import (
    HistoryPoint,
    PredictionPoint,
    PredictionRequest,
    PredictionResponse,
)


class TestHistoryPoint:
    def test_valid(self) -> None:
        hp = HistoryPoint(date=date(2026, 1, 1), quantity=10.0)
        assert hp.date == date(2026, 1, 1)
        assert hp.quantity == 10.0

    def test_negative_quantity_rejected(self) -> None:
        with pytest.raises(ValidationError):
            HistoryPoint(date=date(2026, 1, 1), quantity=-1.0)

    def test_zero_quantity_allowed(self) -> None:
        hp = HistoryPoint(date=date(2026, 1, 1), quantity=0.0)
        assert hp.quantity == 0.0


class TestPredictionRequest:
    def test_valid_minimal(self) -> None:
        req = PredictionRequest(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 7),
        )
        assert req.history is None

    def test_valid_with_history(self) -> None:
        req = PredictionRequest(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 7),
            history=[HistoryPoint(date=date(2025, 12, 31), quantity=5.0)],
        )
        assert len(req.history) == 1

    def test_empty_product_id_rejected(self) -> None:
        with pytest.raises(ValidationError):
            PredictionRequest(
                product_id="",
                store_id="S1",
                start_date=date(2026, 1, 1),
                end_date=date(2026, 1, 7),
            )

    def test_empty_store_id_rejected(self) -> None:
        with pytest.raises(ValidationError):
            PredictionRequest(
                product_id="P1",
                store_id="",
                start_date=date(2026, 1, 1),
                end_date=date(2026, 1, 7),
            )

    def test_missing_required_fields(self) -> None:
        with pytest.raises(ValidationError):
            PredictionRequest(product_id="P1")  # type: ignore[call-arg]


class TestPredictionPoint:
    def test_valid(self) -> None:
        p = PredictionPoint(date=date(2026, 1, 1), quantity=10)
        assert p.quantity == 10

    def test_negative_quantity_rejected(self) -> None:
        with pytest.raises(ValidationError):
            PredictionPoint(date=date(2026, 1, 1), quantity=-5)


class TestPredictionResponse:
    def test_valid(self) -> None:
        resp = PredictionResponse(
            product_id="P1",
            store_id="S1",
            predictions=[PredictionPoint(date=date(2026, 1, 1), quantity=10)],
        )
        assert resp.product_id == "P1"
        assert len(resp.predictions) == 1
