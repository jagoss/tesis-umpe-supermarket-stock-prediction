"""Tests for PredictStockUseCase.

The use case receives a ``StockForecast`` domain entity from the postprocessor
and maps it to a ``PredictStockOutput`` application DTO with rounded quantities.
"""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from server.application import (
    ModelRawPrediction,
    PredictStockInput,
    PredictStockOutput,
    PreprocessedData,
)
from server.application.use_cases import PredictStockUseCase
from server.domain import (
    PredictionError,
    StockForecast,
    StockForecastPoint,
    ValidationError,
)


def _build_use_case(
    preprocessor: MagicMock | None = None,
    model: MagicMock | None = None,
    postprocessor: MagicMock | None = None,
) -> PredictStockUseCase:
    """Helper to build a use case with mocked dependencies."""
    pre = preprocessor or MagicMock()
    mod = model or MagicMock()
    post = postprocessor or MagicMock()
    return PredictStockUseCase(preprocessor=pre, model=mod, postprocessor=post)


def _make_forecast(
    product_id: str = "PROD-001",
    store_id: str = "STORE-A",
    start: date = date(2026, 3, 2),
    values: list[float] | None = None,
) -> StockForecast:
    """Build a ``StockForecast`` domain entity for testing."""
    from datetime import timedelta

    values = values or [10.0, 20.0, 30.0]
    return StockForecast(
        product_id=product_id,
        store_id=store_id,
        points=[
            StockForecastPoint(date=start + timedelta(days=i), quantity=v)
            for i, v in enumerate(values)
        ],
    )


class TestValidation:
    def test_end_before_start_raises(self) -> None:
        uc = _build_use_case()
        data = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 10),
            end_date=date(2026, 3, 5),
        )
        with pytest.raises(ValidationError, match="end_date must be greater"):
            uc.execute(data)

    def test_same_start_and_end_ok(self) -> None:
        preprocessor = MagicMock()
        model = MagicMock()
        postprocessor = MagicMock()

        pre_data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 5),
            end_date=date(2026, 3, 5),
            horizon=1,
        )
        preprocessor.preprocess.return_value = pre_data
        model.predict.return_value = ModelRawPrediction(values=[10.0])
        postprocessor.postprocess.return_value = _make_forecast(
            product_id="P1",
            store_id="S1",
            start=date(2026, 3, 5),
            values=[10.0],
        )

        uc = _build_use_case(preprocessor, model, postprocessor)
        data = PredictStockInput(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 5),
            end_date=date(2026, 3, 5),
        )
        result = uc.execute(data)
        assert len(result.predictions) == 1
        assert result.predictions[0].quantity == 10


class TestOrchestration:
    def test_calls_pipeline_in_order(self, sample_input: PredictStockInput) -> None:
        preprocessor = MagicMock()
        model = MagicMock()
        postprocessor = MagicMock()

        pre_data = PreprocessedData(
            product_id="PROD-001",
            store_id="STORE-A",
            start_date=date(2026, 3, 2),
            end_date=date(2026, 3, 4),
            horizon=3,
        )
        raw = ModelRawPrediction(values=[10.0, 20.0, 30.0])
        forecast = _make_forecast()

        preprocessor.preprocess.return_value = pre_data
        model.predict.return_value = raw
        postprocessor.postprocess.return_value = forecast

        uc = _build_use_case(preprocessor, model, postprocessor)
        result = uc.execute(sample_input)

        preprocessor.preprocess.assert_called_once_with(sample_input)
        model.predict.assert_called_once_with(pre_data)
        postprocessor.postprocess.assert_called_once_with(raw, sample_input)
        assert isinstance(result, PredictStockOutput)
        assert result.product_id == "PROD-001"
        assert result.store_id == "STORE-A"
        assert len(result.predictions) == 3

    def test_rounding_applied(self, sample_input: PredictStockInput) -> None:
        """The use case rounds float quantities to int for the DTO."""
        preprocessor = MagicMock()
        model = MagicMock()
        postprocessor = MagicMock()

        preprocessor.preprocess.return_value = MagicMock()
        model.predict.return_value = MagicMock()
        postprocessor.postprocess.return_value = _make_forecast(values=[10.3, 15.7, 8.5])

        uc = _build_use_case(preprocessor, model, postprocessor)
        result = uc.execute(sample_input)
        assert result.predictions[0].quantity == 10
        assert result.predictions[1].quantity == 16
        assert result.predictions[2].quantity == 8  # Python banker's rounding

    def test_preprocessor_error_propagates(self, sample_input: PredictStockInput) -> None:
        preprocessor = MagicMock()
        preprocessor.preprocess.side_effect = RuntimeError("preprocess failed")

        uc = _build_use_case(preprocessor=preprocessor)
        with pytest.raises(RuntimeError, match="preprocess failed"):
            uc.execute(sample_input)

    def test_model_error_propagates(self, sample_input: PredictStockInput) -> None:
        preprocessor = MagicMock()
        model = MagicMock()
        preprocessor.preprocess.return_value = MagicMock()
        model.predict.side_effect = PredictionError("model broke")

        uc = _build_use_case(preprocessor=preprocessor, model=model)
        with pytest.raises(PredictionError, match="model broke"):
            uc.execute(sample_input)

    def test_postprocessor_error_propagates(self, sample_input: PredictStockInput) -> None:
        preprocessor = MagicMock()
        model = MagicMock()
        postprocessor = MagicMock()
        preprocessor.preprocess.return_value = MagicMock()
        model.predict.return_value = MagicMock()
        postprocessor.postprocess.side_effect = PredictionError("post failed")

        uc = _build_use_case(preprocessor=preprocessor, model=model, postprocessor=postprocessor)
        with pytest.raises(PredictionError, match="post failed"):
            uc.execute(sample_input)
