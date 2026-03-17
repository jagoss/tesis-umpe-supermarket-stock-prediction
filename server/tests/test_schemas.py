"""Tests for HTTP Pydantic schemas."""

from __future__ import annotations

import os
from datetime import date, timedelta
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from server.interface.http.schemas import (
    HistoryPoint,
    PredictionPoint,
    PredictionRequest,
    PredictionResponse,
)

# ---------------------------------------------------------------------------
# Shared test constants
# ---------------------------------------------------------------------------
_PRODUCT_ID = "P1"
_STORE_ID = "S1"
_START_DATE = date(2026, 1, 1)
_END_DATE = date(2026, 1, 7)
_MAX_LEN = 101
_MAX_HISTORY = 1001
_SHORT_HORIZON = 30
_LONG_HORIZON_DAYS = 60
_WITHIN_HORIZON_DAYS = 364


class TestHistoryPoint:
    def test_valid(self) -> None:
        hp = HistoryPoint(date=_START_DATE, quantity=10.0)
        assert hp.date == _START_DATE
        assert hp.quantity == pytest.approx(10.0)

    def test_negative_quantity_rejected(self) -> None:
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            HistoryPoint(date=_START_DATE, quantity=-1.0)

    def test_zero_quantity_allowed(self) -> None:
        hp = HistoryPoint(date=_START_DATE, quantity=0.0)
        assert hp.quantity == pytest.approx(0.0)


class TestPredictionRequest:
    def test_valid_minimal(self) -> None:
        req = PredictionRequest(
            product_id=_PRODUCT_ID,
            store_id=_STORE_ID,
            start_date=_START_DATE,
            end_date=_END_DATE,
            history=None,
        )
        assert req.history is None

    def test_valid_with_history(self) -> None:
        req = PredictionRequest(
            product_id=_PRODUCT_ID,
            store_id=_STORE_ID,
            start_date=_START_DATE,
            end_date=_END_DATE,
            history=[HistoryPoint(date=date(2025, 12, 31), quantity=5.0)],
        )
        assert req.history is not None
        assert len(req.history) == 1

    def test_empty_product_id_rejected(self) -> None:
        with pytest.raises(ValidationError, match="at least 1 character"):
            PredictionRequest(
                product_id="",
                store_id=_STORE_ID,
                start_date=_START_DATE,
                end_date=_END_DATE,
                history=None,
            )

    def test_empty_store_id_rejected(self) -> None:
        with pytest.raises(ValidationError, match="at least 1 character"):
            PredictionRequest(
                product_id=_PRODUCT_ID,
                store_id="",
                start_date=_START_DATE,
                end_date=_END_DATE,
                history=None,
            )

    def test_missing_required_fields(self) -> None:
        with pytest.raises(ValidationError, match="Field required"):
            PredictionRequest(product_id=_PRODUCT_ID)  # type: ignore[call-arg]


class TestPredictionPoint:
    def test_valid(self) -> None:
        p = PredictionPoint(date=_START_DATE, quantity=10)
        assert p.quantity == 10

    def test_negative_quantity_rejected(self) -> None:
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            PredictionPoint(date=_START_DATE, quantity=-5)


class TestPredictionResponse:
    def test_valid(self) -> None:
        resp = PredictionResponse(
            product_id=_PRODUCT_ID,
            store_id=_STORE_ID,
            predictions=[PredictionPoint(date=_START_DATE, quantity=10)],
        )
        assert resp.product_id == _PRODUCT_ID
        assert len(resp.predictions) == 1


class TestInputHardening:
    def test_product_id_max_length_rejected(self) -> None:
        with pytest.raises(ValidationError, match="at most 100 characters"):
            PredictionRequest(
                product_id="X" * _MAX_LEN,
                store_id=_STORE_ID,
                start_date=_START_DATE,
                end_date=_END_DATE,
                history=None,
            )

    def test_store_id_max_length_rejected(self) -> None:
        with pytest.raises(ValidationError, match="at most 100 characters"):
            PredictionRequest(
                product_id=_PRODUCT_ID,
                store_id="S" * _MAX_LEN,
                start_date=_START_DATE,
                end_date=_END_DATE,
                history=None,
            )

    def test_history_max_length_rejected(self) -> None:
        history = [HistoryPoint(date=_START_DATE, quantity=1.0)] * _MAX_HISTORY
        with pytest.raises(ValidationError, match="at most 1000 items"):
            PredictionRequest(
                product_id=_PRODUCT_ID,
                store_id=_STORE_ID,
                start_date=_START_DATE,
                end_date=_END_DATE,
                history=history,
            )

    def test_horizon_within_limit_accepted(self) -> None:
        with patch.dict(os.environ, {"MAX_HORIZON_DAYS": "365"}, clear=False):
            req = PredictionRequest(
                product_id=_PRODUCT_ID,
                store_id=_STORE_ID,
                start_date=_START_DATE,
                end_date=_START_DATE + timedelta(days=_WITHIN_HORIZON_DAYS),
                history=None,
            )
            assert req.product_id == _PRODUCT_ID

    def test_horizon_exceeds_limit_rejected(self) -> None:
        with patch.dict(os.environ, {"MAX_HORIZON_DAYS": str(_SHORT_HORIZON)}, clear=False):
            with pytest.raises(ValidationError, match="horizon"):
                PredictionRequest(
                    product_id=_PRODUCT_ID,
                    store_id=_STORE_ID,
                    start_date=_START_DATE,
                    end_date=_START_DATE + timedelta(days=_LONG_HORIZON_DAYS),
                    history=None,
                )
