"""Tests for DummyModel."""
from __future__ import annotations

from server.application import PreprocessedData
from server.infrastructure.models import DummyModel


class TestDummyModel:
    def test_returns_constant(self, sample_preprocessed: PreprocessedData) -> None:
        model = DummyModel(constant=5.0)
        result = model.predict(sample_preprocessed)
        assert result.values == [5.0, 5.0, 5.0]

    def test_default_constant_zero(self, sample_preprocessed: PreprocessedData) -> None:
        model = DummyModel()
        result = model.predict(sample_preprocessed)
        assert result.values == [0.0, 0.0, 0.0]

    def test_horizon_one(self) -> None:
        from datetime import date

        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 1),
            horizon=1,
        )
        model = DummyModel(constant=99.0)
        result = model.predict(data)
        assert result.values == [99.0]

    def test_horizon_zero(self) -> None:
        from datetime import date

        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 1),
            horizon=0,
        )
        model = DummyModel(constant=10.0)
        result = model.predict(data)
        assert result.values == []
