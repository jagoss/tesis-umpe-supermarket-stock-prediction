"""Production postprocessor with inverse LocalStandardScaler transform.

Retrieves ``(mean, std)`` from a ``DataRepositoryPort`` and applies the
inverse transform ``pred * std + mean``, then clips to ``>= 0``.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from server.application import DataRepositoryPort, ModelRawPrediction, PredictStockInput
from server.domain import PredictionError, StockForecast, StockForecastPoint

logger = logging.getLogger(__name__)


class ProductionPostprocessor:
    """Inverse-scales raw model predictions and assembles ``StockForecast``."""

    def __init__(self, data_repo: DataRepositoryPort) -> None:
        """Initialise with a data repository for scaler parameter lookups."""
        self._data_repo = data_repo

    def postprocess(self, raw: ModelRawPrediction, original: PredictStockInput) -> StockForecast:
        """Inverse-scale predictions and build the domain forecast entity.

        Args:
            raw: Raw model output values (in scaled space).
            original: Original input used for dates and identifiers.

        Returns:
            ``StockForecast`` with inverse-transformed, non-negative quantities.

        Raises:
            PredictionError: If output length doesn't match horizon or scaler
                params are missing.

        """
        horizon = (original.end_date - original.start_date).days + 1
        if len(raw.values) != horizon:
            raise PredictionError(
                f"Model returned {len(raw.values)} values but horizon is {horizon}"
            )

        scaler = self._data_repo.get_scaler_params(original.store_id, original.product_id)
        if scaler is None:
            raise PredictionError(
                f"No scaler parameters found for store={original.store_id}, "
                f"product={original.product_id}. Cannot inverse-transform predictions."
            )

        mean, std = scaler

        points: list[StockForecastPoint] = []
        for i, scaled_value in enumerate(raw.values):
            # Inverse LocalStandardScaler: value * std + mean
            quantity = scaled_value * std + mean
            # Clip to non-negative (sales can't be negative)
            quantity = max(0.0, quantity)
            points.append(
                StockForecastPoint(
                    date=original.start_date + timedelta(days=i),
                    quantity=quantity,
                )
            )

        return StockForecast(
            product_id=original.product_id,
            store_id=original.store_id,
            points=points,
        )
