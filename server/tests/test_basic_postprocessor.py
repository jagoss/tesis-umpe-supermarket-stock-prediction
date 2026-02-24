"""Tests for BasicPostprocessor.

The postprocessor now returns a ``StockForecast`` domain entity with float
quantities.  Rounding to integer is the use case's responsibility.
"""
from __future__ import annotations

from datetime import date

import pytest

from server.application import ModelRawPrediction, PredictStockInput
from server.domain import PredictionError, StockForecast
from server.infrastructure.postprocessing import BasicPostprocessor


class TestBasicPostprocessor:
    def setup_method(self) -> None:
        self.postprocessor = BasicPostprocessor()

    def test_returns_stock_forecast(
        self,
        sample_raw_prediction: ModelRawPrediction,
        sample_input: PredictStockInput,
    ) -> None:
        result = self.postprocessor.postprocess(sample_raw_prediction, sample_input)
        assert isinstance(result, StockForecast)
        assert result.product_id == "PROD-001"
        assert result.store_id == "STORE-A"
        assert len(result.points) == 3

    def test_dates_are_sequential(
        self,
        sample_raw_prediction: ModelRawPrediction,
        sample_input: PredictStockInput,
    ) -> None:
        result = self.postprocessor.postprocess(sample_raw_prediction, sample_input)
        assert result.points[0].date == date(2026, 3, 2)
        assert result.points[1].date == date(2026, 3, 3)
        assert result.points[2].date == date(2026, 3, 4)

    def test_quantities_are_float(self, sample_input: PredictStockInput) -> None:
        raw = ModelRawPrediction(values=[10.3, 15.7, 8.5])
        result = self.postprocessor.postprocess(raw, sample_input)
        assert result.points[0].quantity == pytest.approx(10.3)
        assert result.points[1].quantity == pytest.approx(15.7)
        assert result.points[2].quantity == pytest.approx(8.5)

    def test_mismatch_raises(self, sample_input: PredictStockInput) -> None:
        raw = ModelRawPrediction(values=[1.0, 2.0])  # 2 values but horizon is 3
        with pytest.raises(PredictionError, match="horizon"):
            self.postprocessor.postprocess(raw, sample_input)

    def test_single_day(self) -> None:
        inp = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 6, 15),
            end_date=date(2026, 6, 15),
        )
        raw = ModelRawPrediction(values=[42.9])
        result = self.postprocessor.postprocess(raw, inp)
        assert len(result.points) == 1
        assert result.points[0].date == date(2026, 6, 15)
        assert result.points[0].quantity == pytest.approx(42.9)

    def test_zero_values(self, sample_input: PredictStockInput) -> None:
        raw = ModelRawPrediction(values=[0.0, 0.0, 0.0])
        result = self.postprocessor.postprocess(raw, sample_input)
        for p in result.points:
            assert p.quantity == 0.0

    def test_forecast_is_frozen(
        self,
        sample_raw_prediction: ModelRawPrediction,
        sample_input: PredictStockInput,
    ) -> None:
        result = self.postprocessor.postprocess(sample_raw_prediction, sample_input)
        with pytest.raises(AttributeError):
            result.product_id = "CHANGED"  # type: ignore[misc]
