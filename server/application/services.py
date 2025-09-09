"""
Application services for the MCP Prediction Server.

This module contains the concrete implementation of application use cases,
orchestrating domain operations through dependency injection.
"""

import logging
from typing import Any

from ..domain import (
    PredictionRequest,
    PredictionResponse,
    PredictionService,
    MLModel,
    Preprocessor,
    Postprocessor,
    PredictionServiceError,
    PreprocessingError,
    PostprocessingError,
    ModelPredictionError,
)


class PredictionServiceImpl(PredictionService):
    """
    Concrete implementation of the prediction service.
    
    This service orchestrates the complete prediction pipeline:
    1. Preprocessing input features
    2. Running model inference
    3. Postprocessing model outputs
    4. Building the response
    
    All dependencies are injected following the Dependency Inversion Principle.
    """
    
    def __init__(
        self,
        model: MLModel,
        preprocessor: Preprocessor,
        postprocessor: Postprocessor,
        logger: logging.Logger = None,
    ) -> None:
        """
        Initialize the prediction service with required dependencies.
        
        Args:
            model: ML model implementation for inference.
            preprocessor: Data preprocessor for input transformation.
            postprocessor: Data postprocessor for output transformation.
            logger: Optional logger for operation tracking.
        """
        self._model = model
        self._preprocessor = preprocessor
        self._postprocessor = postprocessor
        self._logger = logger or logging.getLogger(__name__)
    
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Execute the complete prediction pipeline.
        
        This method orchestrates the full prediction flow:
        1. Log the incoming request
        2. Preprocess input features
        3. Execute model inference
        4. Postprocess model outputs
        5. Build and return response
        
        Args:
            request: The prediction request with input features.
            
        Returns:
            Complete prediction response with results and metadata.
            
        Raises:
            PredictionServiceError: If any step in the pipeline fails.
        """
        try:
            self._logger.info(
                "Starting prediction pipeline",
                extra={"feature_count": len(request.features)}
            )
            
            # Step 1: Preprocess input features
            try:
                processed_input = self._preprocessor.transform(request.features)
                self._logger.debug("Input preprocessing completed successfully")
            except Exception as e:
                self._logger.error(f"Preprocessing failed: {e}")
                raise PreprocessingError(
                    "Failed to preprocess input features",
                    details=str(e)
                ) from e
            
            # Step 2: Execute model inference
            try:
                raw_prediction = self._model.predict(processed_input)
                model_version = self._model.version()
                self._logger.debug(
                    "Model inference completed successfully",
                    extra={"model_version": model_version}
                )
            except Exception as e:
                self._logger.error(f"Model prediction failed: {e}")
                raise ModelPredictionError(
                    "Failed to execute model prediction",
                    details=str(e)
                ) from e
            
            # Step 3: Postprocess model outputs
            try:
                processed_output = self._postprocessor.transform(raw_prediction)
                self._logger.debug("Output postprocessing completed successfully")
            except Exception as e:
                self._logger.error(f"Postprocessing failed: {e}")
                raise PostprocessingError(
                    "Failed to postprocess model output",
                    details=str(e)
                ) from e
            
            # Step 4: Calculate confidence score (domain-specific logic)
            confidence = self._calculate_confidence(raw_prediction, processed_output)
            
            # Step 5: Build response
            response = PredictionResponse(
                prediction=processed_output,
                confidence=confidence,
                model_version=model_version
            )
            
            self._logger.info(
                "Prediction pipeline completed successfully",
                extra={
                    "confidence": confidence,
                    "model_version": model_version
                }
            )
            
            return response
            
        except (PreprocessingError, ModelPredictionError, PostprocessingError):
            # Re-raise domain exceptions as-is
            raise
        except Exception as e:
            # Catch any unexpected errors and wrap them
            self._logger.error(f"Unexpected error in prediction pipeline: {e}")
            raise PredictionServiceError(
                "Unexpected error during prediction",
                details=str(e)
            ) from e
    
    def _calculate_confidence(
        self, 
        raw_prediction: Any, 
        processed_output: Any
    ) -> float:
        """
        Calculate confidence score for the prediction.
        
        This is domain-specific logic that can be customized based on
        the type of model and prediction requirements.
        
        Args:
            raw_prediction: Raw output from the model.
            processed_output: Processed prediction output.
            
        Returns:
            Confidence score between 0.0 and 1.0.
        """
        # TODO: Implement domain-specific confidence calculation
        # This is a placeholder that should be customized based on:
        # - Model type (classification vs regression)
        # - Output structure (probabilities, variance, etc.)
        # - Business requirements for confidence scoring
        
        # For now, return a default confidence
        # In practice, this would analyze the prediction characteristics
        return 0.8
