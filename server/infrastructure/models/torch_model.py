"""Torch model adapter (stub).

TODO: Implement actual load and inference when a Torch script or state dict is provided.
"""
from __future__ import annotations

from ...application.ports import ModelPort, ModelRawPrediction, PreprocessedData
from ...domain.exceptions import PredictionError


class TorchModel(ModelPort):
    """Adapter for a PyTorch model (stub)."""

    def __init__(self, model_path: str, device: str | None = None) -> None:
        """Initialize the adapter with model path and optional device.

        Args:
            model_path: Filesystem path to a TorchScript or state dict file.
            device: Optional device string (e.g., "cpu", "cuda").
        """
        self._model_path = model_path
        self._device = device

    def predict(self, data: PreprocessedData) -> ModelRawPrediction:  # pragma: no cover - stub
        """Run inference with a PyTorch model.

        Note: This is a stub implementation. It currently returns zeros with
        length equal to the requested horizon.
        """
        try:
            import torch  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise PredictionError("torch backend requires torch to be installed") from exc
        try:
            # Placeholder: implement torch model loading and inference here.
            # For now, return zeros to match horizon.
            values = [0.0 for _ in range(data.horizon)]
            return ModelRawPrediction(values=values)
        except Exception as exc:  # noqa: BLE001
            raise PredictionError("failed to run torch prediction") from exc
