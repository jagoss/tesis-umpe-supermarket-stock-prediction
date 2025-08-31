"""
Domain entities for the MCP Prediction Server.

These entities represent the core data structures used in the prediction domain.
They are independent of external frameworks and contain only business logic.
"""

from typing import Any, Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionRequest:
    """
    Represents a prediction request with input features.
    
    This immutable value object encapsulates the features required
    for making a prediction. Features are provided as a flexible
    dictionary to accommodate different model input schemas.
    
    Attributes:
        features: Dictionary mapping feature names to their values.
                 Structure depends on the specific model requirements.
    
    Examples:
        >>> request = PredictionRequest({
        ...     "product_id": "ABC123",
        ...     "historical_sales": [100, 120, 95],
        ...     "season": "winter"
        ... })
    """
    features: Dict[str, Any]
    
    def __post_init__(self) -> None:
        """Validate that features is not empty."""
        if not self.features:
            raise ValueError("Features dictionary cannot be empty")


@dataclass(frozen=True)
class PredictionResponse:
    """
    Represents the result of a prediction operation.
    
    This immutable value object encapsulates the prediction result,
    confidence score, and model metadata.
    
    Attributes:
        prediction: The prediction result. Can be scalar, list, or complex object.
        confidence: Confidence score between 0.0 and 1.0.
        model_version: Version identifier of the model used for prediction.
    
    Examples:
        >>> response = PredictionResponse(
        ...     prediction={"stock_forecast": [150, 180, 200]},
        ...     confidence=0.85,
        ...     model_version="v1.2.0"
        ... )
    """
    prediction: Any
    confidence: float
    model_version: str
    
    def __post_init__(self) -> None:
        """Validate confidence score is within valid range."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if not self.model_version:
            raise ValueError("Model version cannot be empty")
