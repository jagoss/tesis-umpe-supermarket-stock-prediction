"""Infrastructure configuration utilities."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    """Runtime settings for the prediction service.

    Use `load_settings()` to construct from environment variables.
    """

    model_backend: str
    default_prediction_value: float


def load_settings() -> Settings:
    """Load settings from environment variables with defaults."""
    model_backend = os.getenv("MODEL_BACKEND", "dummy").strip().lower()
    default_prediction_value = float(os.getenv("DEFAULT_PREDICTION_VALUE", "0"))
    return Settings(model_backend=model_backend, default_prediction_value=default_prediction_value)
