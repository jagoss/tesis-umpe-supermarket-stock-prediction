"""Tests for the dependency injection container."""
from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from server.application.use_cases import PredictStockUseCase
from server.infrastructure.config import Settings
from server.infrastructure.container import _select_model, build_predict_use_case
from server.infrastructure.models import DummyModel, ONNXModel


class TestSelectModel:
    def test_dummy_backend(self) -> None:
        settings = Settings(model_backend="dummy", model_path="", default_prediction_value=5.0)
        model = _select_model(settings)
        assert isinstance(model, DummyModel)

    def test_onnx_backend(self) -> None:
        # Use the example model path
        from pathlib import Path

        model_path = str(
            Path(__file__).resolve().parent.parent / "models" / "example_model.onnx"
        )
        settings = Settings(model_backend="onnx", model_path=model_path, default_prediction_value=0.0)
        model = _select_model(settings)
        assert isinstance(model, ONNXModel)

    def test_unknown_backend_raises(self) -> None:
        settings = Settings(model_backend="unknown", model_path="", default_prediction_value=0.0)
        with pytest.raises(ValueError, match="Unknown MODEL_BACKEND"):
            _select_model(settings)


class TestBuildPredictUseCase:
    def test_returns_use_case(self) -> None:
        with patch.dict(os.environ, {"MODEL_BACKEND": "dummy"}, clear=False):
            uc = build_predict_use_case()
        assert isinstance(uc, PredictStockUseCase)
