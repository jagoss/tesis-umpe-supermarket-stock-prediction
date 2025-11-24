"""Pydantic schemas for HTTP transport layer."""
from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class HistoryPoint(BaseModel):
    """Historical observation used as optional input context.

    Attributes:
        date: The date of the observed quantity.
        quantity: Observed value for that date.
    """
    date: datetime.date = Field(..., description="Date of the historical observation")
    quantity: float = Field(..., ge=0, description="Observed quantity")


class PredictionRequest(BaseModel):
    """Request payload for /predict endpoint."""

    product_id: str = Field(..., min_length=1)
    store_id: str = Field(..., min_length=1)
    start_date: datetime.date
    end_date: datetime.date
    history: Optional[List[HistoryPoint]] = None


class PredictionPoint(BaseModel):
    """A single forecasted quantity for a specific date."""
    date: datetime.date
    quantity: float


class PredictionResponse(BaseModel):
    """Response payload for /predict endpoint."""
    product_id: str
    store_id: str
    predictions: List[PredictionPoint]
