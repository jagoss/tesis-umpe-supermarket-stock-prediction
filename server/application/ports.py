"""Application ports (interfaces) for Clean Architecture.

These define the contracts that infrastructure adapters must implement.
The postprocessor returns a domain-level ``StockForecast`` entity; the use case
is responsible for mapping it to the application DTO (``PredictStockOutput``).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Protocol, Tuple

from server.application.dto import PredictStockInput
from server.domain import StockForecast


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
    """Transforms ``PredictStockInput`` into ``PreprocessedData``."""

    def preprocess(self, data: PredictStockInput) -> PreprocessedData:  # pragma: no cover
        """Transform application input into model-ready features."""
        ...


class ModelPort(Protocol):
    """Predicts from preprocessed features and returns raw outputs."""

    def predict(self, data: PreprocessedData) -> ModelRawPrediction:  # pragma: no cover
        """Produce raw predictions from preprocessed features."""
        ...


class PostprocessorPort(Protocol):
    """Maps raw model outputs to a domain-level ``StockForecast`` entity.

    The use case is responsible for converting the resulting ``StockForecast``
    into the application DTO (``PredictStockOutput``).
    """

    def postprocess(self, raw: ModelRawPrediction, original: PredictStockInput) -> StockForecast:  # pragma: no cover
        """Convert raw model outputs to a domain ``StockForecast`` entity."""
        ...
