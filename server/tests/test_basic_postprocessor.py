"""Tests for BasicPostprocessor."""
from __future__ import annotations

from datetime import date

import pytest

from server.application.dto import PredictStockInput
from server.application.ports import ModelRawPrediction
from server.domain.exceptions import PredictionError
from server.infrastructure.postprocessing.basic_postprocessor import BasicPostprocessor


class TestBasicPostprocessor:
    def setup_method(self) -> None:
        self.postprocessor = BasicPostprocessor()

    def test_happy_path(
        self,
        sample_raw_prediction: ModelRawPrediction,
        sample_input: PredictStockInput,
    ) -> None:
        result = self.postprocessor.postprocess(sample_raw_prediction, sample_input)
        assert result.product_id == "PROD-001"
        assert result.store_id == "STORE-A"
        assert len(result.predictions) == 3

    def test_dates_are_sequential(
        self,
        sample_raw_prediction: ModelRawPrediction,
        sample_input: PredictStockInput,
    ) -> None:
        result = self.postprocessor.postprocess(sample_raw_prediction, sample_input)
        assert result.predictions[0].date == date(2026, 3, 2)
        assert result.predictions[1].date == date(2026, 3, 3)
        assert result.predictions[2].date == date(2026, 3, 4)

    def test_rounding(self, sample_input: PredictStockInput) -> None:
        raw = ModelRawPrediction(values=[10.3, 15.7, 8.5])
        result = self.postprocessor.postprocess(raw, sample_input)
        assert result.predictions[0].quantity == 10
        assert result.predictions[1].quantity == 16
        assert result.predictions[2].quantity == 8  # Python banker's rounding: round(8.5) = 8

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
        assert len(result.predictions) == 1
        assert result.predictions[0].date == date(2026, 6, 15)
        assert result.predictions[0].quantity == 43

    def test_zero_values(self, sample_input: PredictStockInput) -> None:
        raw = ModelRawPrediction(values=[0.0, 0.0, 0.0])
        result = self.postprocessor.postprocess(raw, sample_input)
        for p in result.predictions:
            assert p.quantity == 0
