"""Shared fixtures for server tests."""
from __future__ import annotations

from datetime import date
from typing import List, Tuple

import pytest

from server.application.dto import PredictStockInput, PredictStockOutput, PredictionPoint
from server.application.ports import ModelRawPrediction, PreprocessedData


@pytest.fixture()
def sample_input() -> PredictStockInput:
    """A 3-day prediction input."""
    return PredictStockInput(
        product_id="PROD-001",
        store_id="STORE-A",
        start_date=date(2026, 3, 2),  # Monday
        end_date=date(2026, 3, 4),  # Wednesday
    )


@pytest.fixture()
def sample_input_with_history() -> PredictStockInput:
    """A 3-day prediction input with historical data."""
    history: List[Tuple[date, float]] = [
        (date(2026, 2, 27), 10.0),
        (date(2026, 2, 28), 12.5),
        (date(2026, 3, 1), 8.0),
    ]
    return PredictStockInput(
        product_id="PROD-001",
        store_id="STORE-A",
        start_date=date(2026, 3, 2),
        end_date=date(2026, 3, 4),
        history=history,
    )


@pytest.fixture()
def sample_preprocessed() -> PreprocessedData:
    """Preprocessed data with horizon=3."""
    return PreprocessedData(
        product_id="PROD-001",
        store_id="STORE-A",
        start_date=date(2026, 3, 2),
        end_date=date(2026, 3, 4),
        horizon=3,
    )


@pytest.fixture()
def sample_raw_prediction() -> ModelRawPrediction:
    """Raw model output with 3 values."""
    return ModelRawPrediction(values=[10.3, 15.7, 8.1])
