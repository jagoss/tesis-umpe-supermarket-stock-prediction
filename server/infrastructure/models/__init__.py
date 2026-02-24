"""Model adapters implementing ``ModelPort``.

Public API
----------
ONNXModel
    ONNX Runtime adapter — canonical serving format.
DummyModel
    Constant-value predictor for testing and development.
"""

from server.infrastructure.models.dummy_model import DummyModel
from server.infrastructure.models.onnx_model import ONNXModel

__all__ = [
    "ONNXModel",
    "DummyModel",
]
