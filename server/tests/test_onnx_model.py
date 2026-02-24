"""Tests for ONNXModel adapter."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from server.application import PreprocessedData
from server.domain import PredictionError
from server.infrastructure.models import ONNXModel

# Path to the example ONNX model shipped with the project
_MODEL_PATH = str(
    Path(__file__).resolve().parent.parent / "models" / "example_model.onnx"
)


class TestONNXModelInit:
    def test_missing_model_raises(self, tmp_path: Path) -> None:
        with pytest.raises(PredictionError, match="not found"):
            ONNXModel(model_path=str(tmp_path / "nonexistent.onnx"))

    def test_valid_model_loads(self) -> None:
        model = ONNXModel(model_path=_MODEL_PATH)
        assert model._model_path.exists()


class TestONNXModelPredict:
    def setup_method(self) -> None:
        self.model = ONNXModel(model_path=_MODEL_PATH)

    def test_predict_returns_correct_length(self, sample_preprocessed: PreprocessedData) -> None:
        result = self.model.predict(sample_preprocessed)
        assert len(result.values) == sample_preprocessed.horizon

    def test_predict_returns_floats(self, sample_preprocessed: PreprocessedData) -> None:
        result = self.model.predict(sample_preprocessed)
        for v in result.values:
            assert isinstance(v, float)

    def test_predict_single_day(self) -> None:
        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 1),
            horizon=1,
        )
        result = self.model.predict(data)
        assert len(result.values) == 1

    def test_predict_weekend_features(self) -> None:
        # Saturday March 7, 2026
        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 7),
            end_date=date(2026, 3, 8),  # Sunday
            horizon=2,
        )
        result = self.model.predict(data)
        assert len(result.values) == 2


class TestONNXModelFeatures:
    def setup_method(self) -> None:
        self.model = ONNXModel(model_path=_MODEL_PATH)

    def test_build_features_weekday(self) -> None:
        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 2),  # Monday
            end_date=date(2026, 3, 2),
            horizon=1,
        )
        features = self.model._build_features(data, step=0)
        assert features[0] == 1.0  # horizon_step
        assert features[1] == 0.0  # Monday = 0
        assert features[2] == 3.0  # March
        assert features[3] == 0.0  # not weekend

    def test_build_features_weekend(self) -> None:
        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 7),  # Saturday
            end_date=date(2026, 3, 7),
            horizon=1,
        )
        features = self.model._build_features(data, step=0)
        assert features[1] == 5.0  # Saturday = 5
        assert features[3] == 1.0  # weekend

    def test_feature_vector_length(self) -> None:
        data = PreprocessedData(
            product_id="P1",
            store_id="S1",
            start_date=date(2026, 3, 2),
            end_date=date(2026, 3, 2),
            horizon=1,
        )
        features = self.model._build_features(data, step=0)
        assert len(features) == 4
