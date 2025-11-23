"""Basic postprocessor implementation.

Maps raw numeric predictions to dated points across the requested window.
"""
from __future__ import annotations

from datetime import timedelta
from typing import List

from ...application.dto import PredictStockInput, PredictStockOutput, PredictionPoint
from ...application.ports import ModelRawPrediction
from ...domain.exceptions import PredictionError


class BasicPostprocessor:
    """Converts model outputs into `PredictStockOutput`."""

    def postprocess(self, raw: ModelRawPrediction, original: PredictStockInput) -> PredictStockOutput:
        """Map raw model values to dated predictions for the requested window.

        Args:
            raw: Values returned by the model backend.
            original: Original input, used to compute dates and identifiers.

        Returns:
            Application-level `PredictStockOutput` with one point per day.

        Raises:
            PredictionError: If the number of predictions doesn't match the horizon.
        """
        horizon = (original.end_date - original.start_date).days + 1
        if len(raw.values) != horizon:
            raise PredictionError(
                f"Model returned {len(raw.values)} values but horizon is {horizon}"
            )

        predictions: List[PredictionPoint] = []
        for i, value in enumerate(raw.values):
            day = original.start_date + timedelta(days=i)
            predictions.append(PredictionPoint(date=day, quantity=float(value)))

        return PredictStockOutput(
            product_id=original.product_id,
            store_id=original.store_id,
            predictions=predictions,
        )
