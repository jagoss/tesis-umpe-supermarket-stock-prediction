"""Application DTOs for the prediction use case.

These are pure data carriers between layers, separate from transport types.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class PredictStockInput:
    """Input data for predicting stock for a time window.

    Attributes:
        product_id: Unique product identifier.
        store_id: Unique store identifier.
        start_date: Inclusive forecast start date.
        end_date: Inclusive forecast end date.
        history: Optional historical time series as (date, quantity) tuples.

    """

    product_id: str
    store_id: str
    start_date: date
    end_date: date
    history: list[tuple[date, float]] | None = None


@dataclass(slots=True)
class PredictionPoint:
    """A predicted quantity for a specific date."""

    date: date
    quantity: int


@dataclass(slots=True)
class PredictStockOutput:
    """Output data representing the forecast results."""

    product_id: str
    store_id: str
    predictions: list[PredictionPoint]
