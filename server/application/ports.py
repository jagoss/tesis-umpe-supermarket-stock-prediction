"""Application ports (interfaces) for Clean Architecture.

These define the contracts that infrastructure adapters must implement.
The postprocessor returns a domain-level ``StockForecast`` entity; the use case
is responsible for mapping it to the application DTO (``PredictStockOutput``).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

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
    history: list[tuple[date, float]] | None = None
    features: list[list[float]] | None = None


@dataclass(slots=True)
class ModelRawPrediction:
    """Raw model output vector(s) before post-processing."""

    values: list[float]


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

    def postprocess(  # pragma: no cover
        self, raw: ModelRawPrediction, original: PredictStockInput
    ) -> StockForecast:
        """Convert raw model outputs to a domain ``StockForecast`` entity."""
        ...


class DataRepositoryPort(Protocol):
    """Provides pre-computed feature vectors and scaler parameters for inference.

    Implementations load static historical data (e.g. from Parquet files) and
    expose O(1) lookups by ``(store_id, product_id, target_date)``.
    """

    def get_feature_vector(  # pragma: no cover
        self, store_id: str, product_id: str, target_date: date
    ) -> list[float] | None:
        """Return the pre-computed feature vector for a specific series and date.

        Returns ``None`` if the combination is not found.
        """
        ...

    def get_feature_names(self) -> list[str]:  # pragma: no cover
        """Return the ordered list of feature column names."""
        ...

    def get_scaler_params(  # pragma: no cover
        self, store_id: str, product_id: str
    ) -> tuple[float, float] | None:
        """Return ``(mean, std)`` for the LocalStandardScaler of the given series.

        Returns ``None`` if the series is not found.
        """
        ...

    def get_available_date_range(self) -> tuple[date, date]:  # pragma: no cover
        """Return the ``(min_date, max_date)`` available in the dataset."""
        ...
