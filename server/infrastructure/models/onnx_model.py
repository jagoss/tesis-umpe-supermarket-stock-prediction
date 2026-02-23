"""ONNX Runtime model adapter for inference.

This adapter loads an ONNX model and runs inference using ONNX Runtime.
ONNX is the canonical serving format — models trained in any framework
(scikit-learn, PyTorch, TensorFlow, etc.) are exported to .onnx and served
through this single adapter.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

from ...application.ports import ModelPort, ModelRawPrediction, PreprocessedData
from ...domain.exceptions import PredictionError


class ONNXModel(ModelPort):
    """Adapter for ONNX Runtime-based prediction models.

    This adapter loads an ONNX model from disk and provides inference capabilities
    through the ModelPort interface. It handles feature engineering from PreprocessedData
    to the model's expected input format.

    The current implementation assumes:
    - Model input: float32 array with shape (N, 4) where features are
      [horizon_step, day_of_week, month, is_weekend]
    - Model output: float32 array with shape (N, 1) representing predicted quantities

    For custom models with different input/output specifications, adjust the
    _build_features() and predict() methods accordingly.
    """

    def __init__(self, model_path: str) -> None:
        """Initialize the ONNX model adapter.

        Args:
            model_path: Filesystem path to the .onnx model file (absolute or relative).

        Raises:
            PredictionError: If onnxruntime is not installed or model file not found.
            
        """
        # Resolve to absolute path
        model_path_obj = Path(model_path)
        if not model_path_obj.is_absolute():
            # If relative, resolve from current working directory first
            # Then try from project root if that fails
            resolved = model_path_obj.resolve()
            if not resolved.exists():
                # Try resolving from project root (where pyproject.toml is)
                current = Path(__file__).resolve()
                while current.parent != current:
                    if (current / "pyproject.toml").exists():
                        resolved = (current / model_path).resolve()
                        break
                    current = current.parent
            model_path_obj = resolved
        
        self._model_path = model_path_obj
        self._session: Any = None  # onnxruntime.InferenceSession, lazily loaded

        # Validate that the model file exists
        if not self._model_path.exists():
            raise PredictionError(
                f"ONNX model file not found: {self._model_path}. "
                f"Resolved from: {model_path}. "
                "Ensure the model artifact is present in server/models/"
            )

    def _ensure_session_loaded(self) -> Any:
        """Lazily load the ONNX Runtime session.

        Returns:
            The loaded InferenceSession.

        Raises:
            PredictionError: If onnxruntime is not installed or model loading fails.
            
        """
        if self._session is not None:
            return self._session

        try:
            import onnxruntime as ort  # type: ignore
        except ImportError as exc:
            raise PredictionError(
                "ONNX backend requires onnxruntime to be installed. "
                "Install it with: pip install onnxruntime"
            ) from exc

        try:
            # Create inference session with CPU execution provider
            self._session = ort.InferenceSession(
                str(self._model_path),
                providers=["CPUExecutionProvider"]
            )
            return self._session
        except Exception as exc:
            raise PredictionError(
                f"Failed to load ONNX model from {self._model_path}: {exc}"
            ) from exc

    def _build_features(self, data: PreprocessedData, step: int) -> list[float]:
        """Extract features from PreprocessedData for a single horizon step.

        This method constructs the feature vector expected by the ONNX model.
        Adjust this if your model expects different features.

        Current features:
        - horizon_step: Which day ahead we're predicting (1 to horizon)
        - day_of_week: Day of week for the prediction date (0-6)
        - month: Month for the prediction date (1-12)
        - is_weekend: 1.0 if weekend (Sat/Sun), 0.0 otherwise

        Args:
            data: Preprocessed input data containing product, store, dates, etc.
            step: The horizon step (0-indexed, where 0 is the first prediction day).

        Returns:
            List of float features matching model input expectations.
            
        """
        from datetime import timedelta

        # Calculate the prediction date for this step
        prediction_date = data.start_date + timedelta(days=step)

        # Extract temporal features
        day_of_week = prediction_date.weekday()  # Monday=0, Sunday=6
        month = prediction_date.month
        is_weekend = 1.0 if day_of_week >= 5 else 0.0

        # horizon_step is 1-indexed (first day = 1, second day = 2, ...)
        horizon_step = step + 1

        return [
            float(horizon_step),
            float(day_of_week),
            float(month),
            float(is_weekend),
        ]

    def predict(self, data: PreprocessedData) -> ModelRawPrediction:
        """Run ONNX inference to produce predictions for the requested horizon.

        This method:
        1. Loads the ONNX Runtime session (if not already loaded)
        2. Constructs feature vectors for each step in the horizon
        3. Runs batch inference via ONNX Runtime
        4. Extracts and returns the predicted values

        Args:
            data: Preprocessed input containing product_id, store_id, dates, horizon.

        Returns:
            ModelRawPrediction containing a list of predicted values (one per horizon step).

        Raises:
            PredictionError: If inference fails or output shape is unexpected.
            
        """
        session = self._ensure_session_loaded()

        try:
            # Build feature matrix: one row per horizon step
            x_features: list[list[float]] = [
                self._build_features(data, step) for step in range(data.horizon)
            ]
            x: npt.NDArray[np.float32] = np.array(x_features, dtype=np.float32)

            # Get input name from the ONNX model metadata
            input_name = session.get_inputs()[0].name

            # Run inference
            outputs = session.run(None, {input_name: x})

            # Extract predictions from the output
            # Most sklearn-derived ONNX models output shape (N, 1) or (N,)
            predictions = outputs[0]

            # Flatten if needed and convert to list
            if predictions.ndim == 2:
                # Shape (N, 1) -> flatten to (N,)
                predictions = predictions.flatten()

            values: list[float] = [float(v) for v in predictions]

            # Validate output length matches horizon
            if len(values) != data.horizon:
                raise PredictionError(
                    f"ONNX model output length ({len(values)}) does not match "
                    f"requested horizon ({data.horizon})"
                )

            return ModelRawPrediction(values=values)

        except PredictionError:
            # Re-raise our own exceptions as-is
            raise
        except Exception as exc:
            raise PredictionError(f"ONNX inference failed: {exc}") from exc

