"""Sklearn model adapter (stub).

TODO: Implement actual load and predict when sklearn/joblib artifacts are provided.
"""
from __future__ import annotations

from ...application.ports import ModelPort, ModelRawPrediction, PreprocessedData
from ...domain.exceptions import PredictionError


class SklearnModel(ModelPort):
    """Adapter for an sklearn-compatible regression model.

    Assumptions:
    - A fitted model can be loaded from a file path using joblib.
    - The model exposes a `.predict(X)` method returning a 1D array-like.
    """

    def __init__(self, model_path: str) -> None:
        """Initialize the adapter with a path to a serialized sklearn model.

        Args:
            model_path: Filesystem path to the joblib-compatible model file.
        """
        self._model_path = model_path
        # Defer actual loading to avoid dependency at import time.

    def predict(self, data: PreprocessedData) -> ModelRawPrediction:  # pragma: no cover - stub
        """Run prediction using an sklearn model loaded from disk.

        Note: This is a stub implementation; feature construction must be
        aligned to the trained model's expectations.
        """
        try:
            import joblib  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise PredictionError("sklearn backend requires joblib to be installed") from exc
        try:
            model = joblib.load(self._model_path)
            # X would be constructed from `data`. Placeholder uses horizon length.
            X = [[i] for i in range(data.horizon)]
            y = model.predict(X)
            values = [float(v) for v in y]
            return ModelRawPrediction(values=values)
        except Exception as exc:  # noqa: BLE001
            raise PredictionError("failed to run sklearn prediction") from exc
