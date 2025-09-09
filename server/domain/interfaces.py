"""
Domain interfaces for the MCP Prediction Server.

These interfaces define the contracts that must be implemented by
infrastructure components. They represent the domain's requirements
without coupling to specific implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from .entities import PredictionRequest, PredictionResponse


class MLModel(ABC):
    """
    Interface for machine learning models.
    
    This contract defines the operations that any ML model implementation
    must provide. It abstracts away the specific ML framework (PyTorch,
    scikit-learn, etc.) used for the actual model.
    """
    
    @abstractmethod
    def predict(self, input_data: Any) -> Any:
        """
        Make a prediction using the loaded model.
        
        Args:
            input_data: Preprocessed input data ready for model inference.
                       Format depends on the specific model implementation.
        
        Returns:
            Raw prediction output from the model.
            
        Raises:
            ModelPredictionError: If prediction fails.
        """
        pass
    
    @abstractmethod
    def version(self) -> str:
        """
        Get the version identifier of the model.
        
        Returns:
            Version string identifying the model version.
        """
        pass


class Preprocessor(ABC):
    """
    Interface for data preprocessing before model inference.
    
    Implementations transform raw input features into the format
    expected by the ML model.
    """
    
    @abstractmethod
    def transform(self, features: Dict[str, Any]) -> Any:
        """
        Transform input features for model consumption.
        
        Args:
            features: Raw input features from the prediction request.
        
        Returns:
            Transformed data ready for model input.
            
        Raises:
            PreprocessingError: If transformation fails.
        """
        pass


class Postprocessor(ABC):
    """
    Interface for processing model outputs.
    
    Implementations transform raw model outputs into business-friendly
    format for the prediction response.
    """
    
    @abstractmethod
    def transform(self, raw_output: Any) -> Dict[str, Any]:
        """
        Transform raw model output into response format.
        
        Args:
            raw_output: Raw output from the ML model.
        
        Returns:
            Processed prediction data for the response.
            
        Raises:
            PostprocessingError: If transformation fails.
        """
        pass


class PredictionService(ABC):
    """
    Interface for the core prediction service.
    
    This represents the main use case of the application layer,
    orchestrating the prediction pipeline.
    """
    
    @abstractmethod
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Execute a complete prediction pipeline.
        
        Args:
            request: The prediction request with input features.
        
        Returns:
            Complete prediction response with results and metadata.
            
        Raises:
            PredictionServiceError: If prediction pipeline fails.
        """
        pass
