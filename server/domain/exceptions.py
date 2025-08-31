"""
Domain exceptions for the MCP Prediction Server.

These exceptions represent business rule violations and domain-specific
errors that can occur during prediction operations.
"""


class DomainException(Exception):
    """Base exception for all domain-related errors."""
    
    def __init__(self, message: str, details: str = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class ModelPredictionError(DomainException):
    """Raised when ML model prediction fails."""
    pass


class PreprocessingError(DomainException):
    """Raised when input data preprocessing fails."""
    pass


class PostprocessingError(DomainException):
    """Raised when output data postprocessing fails."""
    pass


class PredictionServiceError(DomainException):
    """Raised when the prediction service encounters an error."""
    pass


class InvalidFeatureError(DomainException):
    """Raised when input features are invalid or malformed."""
    pass


class ModelNotLoadedError(DomainException):
    """Raised when attempting to use a model that hasn't been loaded."""
    pass
