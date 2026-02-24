"""Simple dependency container to wire the use case and adapters.

Supported model backends:
- ``onnx`` (default): ONNX Runtime — canonical serving format.
- ``dummy``: constant-value predictor for testing and development.

Models trained in any framework (scikit-learn, PyTorch, TensorFlow, etc.)
should be exported to ``.onnx`` and served through the ONNX adapter.
"""

from __future__ import annotations

from server.application import ModelPort, PostprocessorPort, PreprocessorPort
from server.application.use_cases import PredictStockUseCase
from server.infrastructure.config import Settings, load_settings
from server.infrastructure.models import DummyModel, ONNXModel
from server.infrastructure.postprocessing import BasicPostprocessor
from server.infrastructure.preprocessing import BasicPreprocessor

_singleton_uc: PredictStockUseCase | None = None


def _select_model(settings: Settings) -> ModelPort:
    """Select the model backend based on runtime settings.

    Only ``onnx`` and ``dummy`` are supported. Models trained in other
    frameworks must be exported to ONNX (via ``skl2onnx``, ``torch.onnx.export``,
    ``tf2onnx``, etc.) and served through the ONNX adapter.

    Args:
        settings: Service settings loaded from environment variables.

    Returns:
        A concrete ``ModelPort`` implementation.

    Raises:
        ValueError: If ``settings.model_backend`` is not ``onnx`` or ``dummy``.

    """
    backend = settings.model_backend
    if backend == "dummy":
        return DummyModel(constant=settings.default_prediction_value)
    if backend == "onnx":
        return ONNXModel(model_path=settings.model_path)
    raise ValueError(f"Unknown MODEL_BACKEND: '{backend}'. Supported backends: 'onnx', 'dummy'.")


def build_predict_use_case() -> PredictStockUseCase:
    """Create a new instance of the use case with configured adapters."""
    settings = load_settings()
    pre: PreprocessorPort = BasicPreprocessor()
    model: ModelPort = _select_model(settings)
    post: PostprocessorPort = BasicPostprocessor()
    return PredictStockUseCase(preprocessor=pre, model=model, postprocessor=post)


def get_predict_use_case_singleton() -> PredictStockUseCase:
    """Return a process-wide singleton instance of the use case."""
    global _singleton_uc
    if _singleton_uc is None:
        _singleton_uc = build_predict_use_case()
    return _singleton_uc
