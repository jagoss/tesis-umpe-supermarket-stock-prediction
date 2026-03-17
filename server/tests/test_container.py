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
    def _base_settings(self, **overrides: object) -> Settings:
        defaults: dict[str, object] = dict(
            model_backend="dummy",
            model_path="",
            default_prediction_value=5.0,
            cors_origins=["*"],
            log_format="text",
            log_level="INFO",
            api_key="",
            rate_limit="60/minute",
            max_horizon_days=365,
            preprocessor_backend="basic",
            data_path="",
            scaler_path="",
        )
        defaults.update(overrides)
        return Settings(**defaults)  # type: ignore[arg-type]

    def test_dummy_backend(self) -> None:
        settings = self._base_settings(model_backend="dummy")
        model = _select_model(settings)
        assert isinstance(model, DummyModel)

    def test_onnx_backend(self) -> None:
        from pathlib import Path

        model_path = str(Path(__file__).resolve().parent.parent / "models" / "example_model.onnx")
        settings = self._base_settings(model_backend="onnx", model_path=model_path)
        model = _select_model(settings)
        assert isinstance(model, ONNXModel)

    def test_unknown_backend_raises(self) -> None:
        settings = self._base_settings(model_backend="unknown")
        with pytest.raises(ValueError, match="Unknown MODEL_BACKEND"):
            _select_model(settings)


class TestBuildPredictUseCase:
    def test_returns_use_case(self) -> None:
        with patch.dict(os.environ, {"MODEL_BACKEND": "dummy"}, clear=False):
            uc = build_predict_use_case()
        assert isinstance(uc, PredictStockUseCase)
