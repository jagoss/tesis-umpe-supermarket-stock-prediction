"""Basic preprocessor implementation.

Converts application input DTO into model-ready features.
"""
from __future__ import annotations

from server.application import PreprocessedData, PreprocessorPort, PredictStockInput


class BasicPreprocessor(PreprocessorPort):
    """Computes a simple horizon and forwards history if provided."""

    def preprocess(self, data: PredictStockInput) -> PreprocessedData:
        """Compute horizon from dates and pass through optional history.

        Args:
            data: Application-level input DTO.

        Returns:
            PreprocessedData with computed `horizon` and forwarded identifiers.
        """
        horizon = (data.end_date - data.start_date).days + 1
        # Ensure non-negative horizon; validation already ensures end >= start.
        horizon = max(0, horizon)
        return PreprocessedData(
            product_id=data.product_id,
            store_id=data.store_id,
            start_date=data.start_date,
            end_date=data.end_date,
            horizon=horizon,
            history=data.history,
        )
