"""Tests for PredictStockUseCase."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from server.application.dto import PredictStockInput, PredictStockOutput, PredictionPoint
from server.application.ports import ModelRawPrediction, PreprocessedData
from server.application.use_cases.predict_stock import PredictStockUseCase
from server.domain.exceptions import PredictionError, ValidationError


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
        postprocessor.postprocess.return_value = PredictStockOutput(
            product_id="P1",
            store_id="S1",
            predictions=[PredictionPoint(date=date(2026, 3, 5), quantity=10)],
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
        output = PredictStockOutput(
            product_id="PROD-001",
            store_id="STORE-A",
            predictions=[
                PredictionPoint(date=date(2026, 3, 2), quantity=10),
                PredictionPoint(date=date(2026, 3, 3), quantity=20),
                PredictionPoint(date=date(2026, 3, 4), quantity=30),
            ],
        )

        preprocessor.preprocess.return_value = pre_data
        model.predict.return_value = raw
        postprocessor.postprocess.return_value = output

        uc = _build_use_case(preprocessor, model, postprocessor)
        result = uc.execute(sample_input)

        preprocessor.preprocess.assert_called_once_with(sample_input)
        model.predict.assert_called_once_with(pre_data)
        postprocessor.postprocess.assert_called_once_with(raw, sample_input)
        assert result is output

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
