"""
Domain layer for MCP Prediction Server.

This module contains the core business entities and interfaces that define
the contracts for prediction models and data processing.

Following Clean Architecture principles, this layer is independent of
external frameworks and contains only business logic.
"""

from .entities import PredictionRequest, PredictionResponse
from .interfaces import MLModel, Preprocessor, Postprocessor, PredictionService
from .exceptions import (
    DomainException,
    ModelPredictionError,
    PreprocessingError,
    PostprocessingError,
    PredictionServiceError,
    InvalidFeatureError,
    ModelNotLoadedError,
)

__all__ = [
    "PredictionRequest",
    "PredictionResponse", 
    "MLModel",
    "Preprocessor",
    "Postprocessor",
    "PredictionService",
    "DomainException",
    "ModelPredictionError",
    "PreprocessingError",
    "PostprocessingError",
    "PredictionServiceError",
    "InvalidFeatureError",
    "ModelNotLoadedError",
]
