"""Tests for domain entities."""
from __future__ import annotations

from datetime import date

import pytest

from server.domain.entities import StockForecast, StockForecastPoint


class TestStockForecastPoint:
    def test_creation(self) -> None:
        point = StockForecastPoint(date=date(2026, 1, 1), quantity=42.5)
        assert point.date == date(2026, 1, 1)
        assert point.quantity == 42.5

    def test_frozen(self) -> None:
        point = StockForecastPoint(date=date(2026, 1, 1), quantity=10.0)
        with pytest.raises(AttributeError):
            point.quantity = 20.0  # type: ignore[misc]

    def test_equality(self) -> None:
        a = StockForecastPoint(date=date(2026, 1, 1), quantity=5.0)
        b = StockForecastPoint(date=date(2026, 1, 1), quantity=5.0)
        assert a == b

    def test_inequality(self) -> None:
        a = StockForecastPoint(date=date(2026, 1, 1), quantity=5.0)
        b = StockForecastPoint(date=date(2026, 1, 2), quantity=5.0)
        assert a != b


class TestStockForecast:
    def test_creation(self) -> None:
        points = [
            StockForecastPoint(date=date(2026, 1, 1), quantity=10.0),
            StockForecastPoint(date=date(2026, 1, 2), quantity=20.0),
        ]
        forecast = StockForecast(product_id="P1", store_id="S1", points=points)
        assert forecast.product_id == "P1"
        assert forecast.store_id == "S1"
        assert len(forecast.points) == 2

    def test_frozen(self) -> None:
        forecast = StockForecast(product_id="P1", store_id="S1", points=[])
        with pytest.raises(AttributeError):
            forecast.product_id = "P2"  # type: ignore[misc]

    def test_empty_points(self) -> None:
        forecast = StockForecast(product_id="P1", store_id="S1", points=[])
        assert forecast.points == []
