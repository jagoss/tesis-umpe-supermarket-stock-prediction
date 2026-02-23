"""Infrastructure configuration utilities."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """Runtime settings for the prediction service.

    Use `load_settings()` to construct from environment variables.
    """

    model_backend: str
    model_path: str
    default_prediction_value: float


def load_settings() -> Settings:
    """Load settings from environment variables with defaults.

    Environment Variables:
        MODEL_BACKEND: Type of model to use (dummy, onnx, sklearn, torch).
            Defaults to "onnx".
        MODEL_PATH: Path to the model artifact file. If not specified, defaults
            are used based on MODEL_BACKEND.
        DEFAULT_PREDICTION_VALUE: Constant value for dummy backend predictions.

    Returns:
        Settings instance with loaded configuration.

    """
    model_backend = os.getenv("MODEL_BACKEND", "onnx").strip().lower()
    default_prediction_value = float(os.getenv("DEFAULT_PREDICTION_VALUE", "0"))

    # Determine default model path based on backend if not explicitly set
    model_path_default = _get_default_model_path(model_backend)
    model_path_env = os.getenv("MODEL_PATH")
    
    # If MODEL_PATH is set, use it (resolve relative paths from project root)
    if model_path_env:
        model_path = model_path_env
        # If it's a relative path, resolve it from project root
        if not Path(model_path).is_absolute():
            project_root = _get_project_root()
            model_path = str(project_root / model_path)
    else:
        model_path = model_path_default

    return Settings(
        model_backend=model_backend,
        model_path=model_path,
        default_prediction_value=default_prediction_value,
    )


def _get_project_root() -> Path:
    """Find the project root directory (where pyproject.toml is located).

    Returns:
        Path to the project root directory.

    """
    # Start from the current file and walk up to find pyproject.toml
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    # Fallback: assume we're in server/infrastructure, go up 2 levels
    return Path(__file__).resolve().parent.parent.parent


def _get_default_model_path(backend: str) -> str:
    """Get the default model path for a given backend.

    Args:
        backend: The model backend type.

    Returns:
        Absolute path to the model artifact.

    """
    project_root = _get_project_root()
    defaults = {
        "onnx": project_root / "server" / "models" / "example_model.onnx",
        "sklearn": project_root / "server" / "models" / "sklearn_model.joblib",
        "torch": project_root / "server" / "models" / "torch_model.pt",
        "dummy": "",  # Dummy backend doesn't need a model path
    }
    path = defaults.get(backend, "")
    return str(path) if path else ""
