"""Dummy model implementation for quick testing and scaffolding.

This model returns a constant value for each step of the requested horizon.
"""
from __future__ import annotations

from typing import List

from ...application.ports import ModelPort, ModelRawPrediction, PreprocessedData


class DummyModel(ModelPort):
    """A simple constant predictor used as a placeholder."""

    def __init__(self, *, constant: float = 0.0) -> None:
        """Create a constant-output predictor.

        Args:
            constant: The value to repeat for each step in the horizon.
        """
        self._constant = float(constant)

    def predict(self, data: PreprocessedData) -> ModelRawPrediction:
        """Return a constant vector with length equal to the requested horizon."""
        values: List[float] = [self._constant for _ in range(max(0, data.horizon))]
        return ModelRawPrediction(values=values)
