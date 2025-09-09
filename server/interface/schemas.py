"""
Request/Response schemas for the MCP Prediction Server API.

This module defines Pydantic models for HTTP request and response serialization,
providing automatic validation, documentation, and type safety for the API.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field, validator


class PredictionRequestSchema(BaseModel):
    """
    HTTP request schema for prediction endpoint.
    
    This schema validates incoming prediction requests and provides
    automatic OpenAPI documentation for the /predict endpoint.
    
    Attributes:
        features: Dictionary of input features for prediction.
                 Keys are feature names, values can be any JSON-compatible type.
    
    Examples:
        ```json
        {
            "features": {
                "product_id": "ABC123",
                "historical_sales": [100, 120, 95, 110],
                "season": "winter",
                "store_location": "downtown"
            }
        }
        ```
    """
    
    features: Dict[str, Any] = Field(
        ...,
        description="Input features for prediction",
        example={
            "product_id": "ABC123",
            "historical_sales": [100, 120, 95, 110],
            "season": "winter",
            "store_location": "downtown"
        }
    )
    
    @validator("features")
    def validate_features_not_empty(cls, v):
        """Ensure features dictionary is not empty."""
        if not v:
            raise ValueError("Features dictionary cannot be empty")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "features": {
                    "product_id": "ABC123",
                    "historical_sales": [100, 120, 95, 110],
                    "season": "winter",
                    "store_location": "downtown"
                }
            }
        }


class PredictionResponseSchema(BaseModel):
    """
    HTTP response schema for prediction endpoint.
    
    This schema structures the prediction response and provides
    automatic OpenAPI documentation.
    
    Attributes:
        prediction: The prediction result (format depends on model).
        confidence: Confidence score between 0.0 and 1.0.
        model_version: Version identifier of the model used.
        
    Examples:
        ```json
        {
            "prediction": {
                "stock_forecast": [150, 180, 200, 175]
            },
            "confidence": 0.85,
            "model_version": "v1.2.0"
        }
        ```
    """
    
    prediction: Any = Field(
        ...,
        description="Prediction result from the model",
        example={"stock_forecast": [150, 180, 200, 175]}
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0",
        example=0.85
    )
    
    model_version: str = Field(
        ...,
        description="Version of the model used for prediction",
        example="v1.2.0"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "prediction": {"stock_forecast": [150, 180, 200, 175]},
                "confidence": 0.85,
                "model_version": "v1.2.0"
            }
        }


class ErrorResponseSchema(BaseModel):
    """
    HTTP error response schema.
    
    This schema provides consistent error formatting across
    all API endpoints.
    
    Attributes:
        error: Error type or category.
        message: Human-readable error message.
        details: Optional additional error details.
    """
    
    error: str = Field(
        ...,
        description="Error type or category",
        example="PreprocessingError"
    )
    
    message: str = Field(
        ...,
        description="Human-readable error message",
        example="Failed to preprocess input features"
    )
    
    details: str = Field(
        None,
        description="Optional additional error details",
        example="Required feature 'product_id' is missing"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "error": "PreprocessingError",
                "message": "Failed to preprocess input features",
                "details": "Required feature 'product_id' is missing"
            }
        }
