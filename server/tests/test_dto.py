"""Tests for application DTOs."""
from __future__ import annotations

from datetime import date

from server.application.dto import PredictStockInput, PredictStockOutput, PredictionPoint


class TestPredictStockInput:
    def test_creation_minimal(self) -> None:
        dto = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 7),
        )
        assert dto.product_id == "P1"
        assert dto.store_id == "S1"
        assert dto.start_date == date(2026, 1, 1)
        assert dto.end_date == date(2026, 1, 7)
        assert dto.history is None

    def test_creation_with_history(self) -> None:
        history = [(date(2025, 12, 30), 5.0), (date(2025, 12, 31), 6.0)]
        dto = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 7),
            history=history,
        )
        assert dto.history is not None
        assert len(dto.history) == 2
        assert dto.history[0] == (date(2025, 12, 30), 5.0)


class TestPredictionPoint:
    def test_creation(self) -> None:
        p = PredictionPoint(date=date(2026, 1, 1), quantity=42)
        assert p.date == date(2026, 1, 1)
        assert p.quantity == 42


class TestPredictStockOutput:
    def test_creation(self) -> None:
        points = [
            PredictionPoint(date=date(2026, 1, 1), quantity=10),
            PredictionPoint(date=date(2026, 1, 2), quantity=20),
        ]
        out = PredictStockOutput(product_id="P1", store_id="S1", predictions=points)
        assert out.product_id == "P1"
        assert out.store_id == "S1"
        assert len(out.predictions) == 2

    def test_empty_predictions(self) -> None:
        out = PredictStockOutput(product_id="P1", store_id="S1", predictions=[])
        assert out.predictions == []
