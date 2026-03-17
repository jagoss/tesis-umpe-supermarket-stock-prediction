"""Tests for infrastructure configuration."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from server.infrastructure.config import (
    Settings,
    _get_default_model_path,
    load_settings,
)


class TestSettings:
    def test_dataclass_fields(self) -> None:
        s = Settings(
            model_backend="dummy",
            model_path="/tmp/m.onnx",
            default_prediction_value=5.0,
            cors_origins=["*"],
            log_format="text",
            log_level="INFO",
            api_key="",
            rate_limit="60/minute",
            max_horizon_days=365,
        )
        assert s.model_backend == "dummy"
        assert s.model_path == "/tmp/m.onnx"
        assert s.default_prediction_value == pytest.approx(5.0)
        assert s.cors_origins == ["*"]


class TestLoadSettings:
    def test_defaults(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            # Remove any existing env vars that could interfere
            for key in ("MODEL_BACKEND", "MODEL_PATH", "DEFAULT_PREDICTION_VALUE"):
                os.environ.pop(key, None)
            s = load_settings()
        assert s.model_backend == "onnx"
        assert s.default_prediction_value == pytest.approx(0.0)
        assert "example_model.onnx" in s.model_path

    def test_backend_from_env(self) -> None:
        with patch.dict(os.environ, {"MODEL_BACKEND": "dummy"}, clear=False):
            s = load_settings()
        assert s.model_backend == "dummy"

    def test_backend_case_insensitive(self) -> None:
        with patch.dict(os.environ, {"MODEL_BACKEND": "  ONNX  "}, clear=False):
            s = load_settings()
        assert s.model_backend == "onnx"

    def test_model_path_from_env_absolute(self) -> None:
        from pathlib import Path

        # Build a truly absolute path (with drive letter on Windows)
        abs_path = str(Path("/custom/path/model.onnx").resolve().parent / "model.onnx")
        with patch.dict(os.environ, {"MODEL_PATH": abs_path}, clear=False):
            s = load_settings()
        assert s.model_path == abs_path

    def test_default_prediction_value_from_env(self) -> None:
        with patch.dict(os.environ, {"DEFAULT_PREDICTION_VALUE": "42.5"}, clear=False):
            s = load_settings()
        assert s.default_prediction_value == pytest.approx(42.5)

    def test_cors_origins_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            for key in ("MODEL_BACKEND", "MODEL_PATH", "DEFAULT_PREDICTION_VALUE", "CORS_ORIGINS"):
                os.environ.pop(key, None)
            s = load_settings()
        assert s.cors_origins == ["*"]

    def test_cors_origins_from_env(self) -> None:
        with patch.dict(
            os.environ,
            {"CORS_ORIGINS": "http://localhost:3000,https://example.com"},
            clear=False,
        ):
            s = load_settings()
        assert s.cors_origins == ["http://localhost:3000", "https://example.com"]


class TestPhase6Settings:
    def test_log_format_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            s = load_settings()
        assert s.log_format == "text"

    def test_log_format_from_env(self) -> None:
        with patch.dict(os.environ, {"LOG_FORMAT": "json"}, clear=False):
            s = load_settings()
        assert s.log_format == "json"

    def test_log_format_case_insensitive(self) -> None:
        with patch.dict(os.environ, {"LOG_FORMAT": "JSON"}, clear=False):
            s = load_settings()
        assert s.log_format == "json"

    def test_log_level_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            s = load_settings()
        assert s.log_level == "INFO"

    def test_log_level_from_env(self) -> None:
        with patch.dict(os.environ, {"LOG_LEVEL": "debug"}, clear=False):
            s = load_settings()
        assert s.log_level == "DEBUG"

    def test_api_key_default_empty(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            s = load_settings()
        assert s.api_key == ""

    def test_api_key_from_env(self) -> None:
        with patch.dict(os.environ, {"API_KEY": "my-secret"}, clear=False):
            s = load_settings()
        assert s.api_key == "my-secret"

    def test_rate_limit_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            s = load_settings()
        assert s.rate_limit == "60/minute"

    def test_rate_limit_from_env(self) -> None:
        with patch.dict(os.environ, {"RATE_LIMIT": "100/hour"}, clear=False):
            s = load_settings()
        assert s.rate_limit == "100/hour"

    def test_max_horizon_days_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            s = load_settings()
        assert s.max_horizon_days == 365

    def test_max_horizon_days_from_env(self) -> None:
        with patch.dict(os.environ, {"MAX_HORIZON_DAYS": "30"}, clear=False):
            s = load_settings()
        assert s.max_horizon_days == 30


class TestGetDefaultModelPath:
    def test_onnx_default(self) -> None:
        path = _get_default_model_path("onnx")
        assert "example_model.onnx" in path

    def test_dummy_empty(self) -> None:
        path = _get_default_model_path("dummy")
        assert path == ""

    def test_unknown_backend_empty(self) -> None:
        path = _get_default_model_path("unknown_backend")
        assert path == ""
