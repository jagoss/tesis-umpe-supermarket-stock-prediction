"""Domain entities and value objects for stock forecasting."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass(frozen=True, slots=True)
class StockForecastPoint:
    """Single forecasted point for a specific date."""

    date: date
    quantity: float


@dataclass(frozen=True, slots=True)
class StockForecast:
    """Forecast for a product at a store across a time window."""

    product_id: str
    store_id: str
    points: List[StockForecastPoint]
