"""Tests for BasicPreprocessor."""
from __future__ import annotations

from datetime import date

from server.application.dto import PredictStockInput
from server.infrastructure.preprocessing.basic_preprocessor import BasicPreprocessor


class TestBasicPreprocessor:
    def setup_method(self) -> None:
        self.preprocessor = BasicPreprocessor()

    def test_horizon_calculation(self, sample_input: PredictStockInput) -> None:
        result = self.preprocessor.preprocess(sample_input)
        # March 2 to March 4 inclusive = 3 days
        assert result.horizon == 3

    def test_single_day_horizon(self) -> None:
        data = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 1),
        )
        result = self.preprocessor.preprocess(data)
        assert result.horizon == 1

    def test_forwards_identifiers(self, sample_input: PredictStockInput) -> None:
        result = self.preprocessor.preprocess(sample_input)
        assert result.product_id == "PROD-001"
        assert result.store_id == "STORE-A"
        assert result.start_date == date(2026, 3, 2)
        assert result.end_date == date(2026, 3, 4)

    def test_history_none_forwarded(self, sample_input: PredictStockInput) -> None:
        result = self.preprocessor.preprocess(sample_input)
        assert result.history is None

    def test_history_forwarded(self, sample_input_with_history: PredictStockInput) -> None:
        result = self.preprocessor.preprocess(sample_input_with_history)
        assert result.history is not None
        assert len(result.history) == 3

    def test_long_horizon(self) -> None:
        data = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 31),
        )
        result = self.preprocessor.preprocess(data)
        assert result.horizon == 31
