"""Simple dependency container to wire the use case and adapters."""
from __future__ import annotations

from typing import Optional

from ..application.use_cases.predict_stock import PredictStockUseCase
from ..application.ports import ModelPort, PostprocessorPort, PreprocessorPort
from .config import Settings, load_settings
from .models.dummy_model import DummyModel
from .models.sklearn_model import SklearnModel
from .models.torch_model import TorchModel
from .postprocessing.basic_postprocessor import BasicPostprocessor
from .preprocessing.basic_preprocessor import BasicPreprocessor


_singleton_uc: Optional[PredictStockUseCase] = None


def _select_model(settings: Settings) -> ModelPort:
    """Select the model backend based on runtime settings.

    Args:
        settings: Service settings loaded from environment variables.

    Returns:
        A concrete `ModelPort` implementation.
    """
    backend = settings.model_backend
    if backend == "dummy":
        return DummyModel(constant=settings.default_prediction_value)
    if backend == "sklearn":
        # TODO: load model path from env/config when available.
        return SklearnModel(model_path="server/models/sklearn_model.joblib")
    if backend == "torch":
        return TorchModel(model_path="server/models/torch_model.pt")
    raise ValueError(f"Unknown MODEL_BACKEND: {backend}")


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
