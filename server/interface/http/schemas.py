"""Pydantic schemas for HTTP transport layer."""

import datetime
from typing import Self

from pydantic import BaseModel, Field, model_validator

from server.infrastructure.config import load_settings


class HistoryPoint(BaseModel):
    """Historical observation used as optional input context.

    Attributes:
        date: The date of the observed quantity.
        quantity: Observed value for that date.

    """

    date: datetime.date = Field(
        ..., description="Date of the historical observation (YYYY-MM-DD)", examples=["2026-03-01"]
    )
    quantity: float = Field(
        ..., ge=0, description="Observed quantity sold on that date", examples=[42.0]
    )


class PredictionRequest(BaseModel):
    """Request payload for /predict endpoint."""

    product_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique product identifier",
        examples=["PROD-001"],
    )
    store_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique store identifier",
        examples=["STORE-A"],
    )
    start_date: datetime.date = Field(
        ...,
        description="First date of the forecast window, inclusive (YYYY-MM-DD)",
        examples=["2026-03-02"],
    )
    end_date: datetime.date = Field(
        ...,
        description="Last date of the forecast window, inclusive (YYYY-MM-DD)",
        examples=["2026-03-04"],
    )
    history: list[HistoryPoint] | None = Field(
        None,
        max_length=1000,
        description="Optional recent sales history to improve prediction accuracy. "
        "Each entry is a date-quantity pair for a past observation.",
    )

    @model_validator(mode="after")
    def _check_horizon(self) -> Self:
        """Reject requests whose date range exceeds ``MAX_HORIZON_DAYS``."""
        horizon = (self.end_date - self.start_date).days + 1
        max_days = load_settings().max_horizon_days
        if horizon > max_days:
            msg = f"Forecast horizon ({horizon} days) exceeds maximum ({max_days} days)"
            raise ValueError(msg)
        return self


class PredictionPoint(BaseModel):
    """A single forecasted quantity for a specific date."""

    date: datetime.date = Field(..., description="Forecasted date (YYYY-MM-DD)")
    quantity: int = Field(..., ge=0, description="Predicted quantity (number of items to stock)")


class PredictionResponse(BaseModel):
    """Response payload for /predict endpoint."""

    product_id: str = Field(..., description="Product identifier echoed from the request")
    store_id: str = Field(..., description="Store identifier echoed from the request")
    predictions: list[PredictionPoint] = Field(
        ..., description="One prediction per day in the requested date range"
    )
