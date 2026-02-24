"""Application ports (interfaces) for Clean Architecture.

These define the contracts that infrastructure adapters must implement.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Protocol, Tuple

from .dto import PredictStockInput, PredictStockOutput


@dataclass(slots=True)
class PreprocessedData:
    """Normalized, model-ready features."""

    product_id: str
    store_id: str
    start_date: date
    end_date: date
    horizon: int
    history: Optional[List[Tuple[date, float]]] = None


@dataclass(slots=True)
class ModelRawPrediction:
    """Raw model output vector(s) before post-processing."""

    values: List[float]


class PreprocessorPort(Protocol):
    """Transforms `PredictStockInput` into `PreprocessedData`."""

    def preprocess(self, data: PredictStockInput) -> PreprocessedData:  # pragma: no cover - pure contract
        """Transform application input into model-ready features."""
        ...


class ModelPort(Protocol):
    """Predicts from preprocessed features and returns raw outputs."""

    def predict(self, data: PreprocessedData) -> ModelRawPrediction:  # pragma: no cover - pure contract
        """Produce raw predictions from preprocessed features."""
        ...


class PostprocessorPort(Protocol):
    """Maps raw outputs to the application-level `PredictStockOutput`."""

    def postprocess(self, raw: ModelRawPrediction, original: PredictStockInput) -> PredictStockOutput:  # pragma: no cover - pure contract
        """Convert raw model outputs to the application-level forecast DTO."""
        ...
