"""Basic postprocessor implementation.

Maps raw numeric predictions to dated ``StockForecastPoint`` domain entities,
producing a ``StockForecast`` aggregate.  The use case layer is responsible for
converting the domain entity into an application DTO with any final rounding.
"""
from __future__ import annotations

from datetime import timedelta

from server.application import ModelRawPrediction, PredictStockInput
from server.domain import PredictionError, StockForecast, StockForecastPoint


class BasicPostprocessor:
    """Converts raw model outputs into a ``StockForecast`` domain entity."""

    def postprocess(
        self, raw: ModelRawPrediction, original: PredictStockInput
    ) -> StockForecast:
        """Map raw model values to a domain forecast across the requested window.

        Each raw prediction value is paired with its corresponding date to
        create ``StockForecastPoint`` value objects.  The resulting
        ``StockForecast`` aggregate carries the full prediction as a
        domain-level concept.

        Args:
            raw: Values returned by the model backend.
            original: Original input, used to compute dates and identifiers.

        Returns:
            A ``StockForecast`` domain entity with one point per day.

        Raises:
            PredictionError: If the number of predictions doesn't match the horizon.

        """
        horizon = (original.end_date - original.start_date).days + 1
        if len(raw.values) != horizon:
            raise PredictionError(
                f"Model returned {len(raw.values)} values but horizon is {horizon}"
            )

        points: list[StockForecastPoint] = [
            StockForecastPoint(
                date=original.start_date + timedelta(days=i),
                quantity=float(value),
            )
            for i, value in enumerate(raw.values)
        ]

        return StockForecast(
            product_id=original.product_id,
            store_id=original.store_id,
            points=points,
        )
