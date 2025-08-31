"""
HTTP controllers for the MCP Prediction Server API.

This module implements FastAPI controllers that handle HTTP requests,
validate input, delegate to the application layer, and format responses.
"""

import logging
from typing import Dict, Any

from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse

from .schemas import PredictionRequestSchema, PredictionResponseSchema, ErrorResponseSchema
from ..domain import (
    PredictionRequest,
    PredictionService,
    DomainException,
    PreprocessingError,
    PostprocessingError,
    ModelPredictionError,
    PredictionServiceError,
    InvalidFeatureError,
    ModelNotLoadedError,
)


class MCPPredictController:
    """
    FastAPI controller for the /predict endpoint.
    
    This controller handles HTTP prediction requests, validates input,
    delegates to the prediction service, and formats responses.
    
    It follows Clean Architecture by depending on domain interfaces
    rather than concrete implementations.
    """
    
    def __init__(
        self,
        prediction_service: PredictionService,
        logger: logging.Logger = None
    ) -> None:
        """
        Initialize the controller with dependencies.
        
        Args:
            prediction_service: Service to handle prediction logic.
            logger: Optional logger for request tracking.
        """
        self._prediction_service = prediction_service
        self._logger = logger or logging.getLogger(__name__)
    
    async def post_predict(
        self, 
        request: PredictionRequestSchema
    ) -> PredictionResponseSchema:
        """
        Handle POST /predict requests.
        
        This endpoint accepts prediction requests with input features
        and returns predictions with confidence scores and metadata.
        
        Args:
            request: Validated prediction request from the client.
            
        Returns:
            Prediction response with results and metadata.
            
        Raises:
            HTTPException: For various error conditions with appropriate status codes.
        """
        try:
            self._logger.info(
                "Received prediction request",
                extra={
                    "feature_count": len(request.features),
                    "feature_keys": list(request.features.keys())
                }
            )
            
            # Convert HTTP schema to domain entity
            domain_request = PredictionRequest(features=request.features)
            
            # Delegate to application layer
            domain_response = await self._prediction_service.predict(domain_request)
            
            # Convert domain entity to HTTP schema
            response = PredictionResponseSchema(
                prediction=domain_response.prediction,
                confidence=domain_response.confidence,
                model_version=domain_response.model_version
            )
            
            self._logger.info(
                "Prediction request completed successfully",
                extra={
                    "confidence": domain_response.confidence,
                    "model_version": domain_response.model_version
                }
            )
            
            return response
            
        except (PreprocessingError, InvalidFeatureError) as e:
            # 400 Bad Request - Client error in input data
            self._logger.warning(f"Bad request: {e.message}")
            raise HTTPException(
                status_code=400,
                detail=self._format_error_response(e)
            )
            
        except (ModelNotLoadedError, ModelPredictionError) as e:
            # 503 Service Unavailable - Model/service issues
            self._logger.error(f"Service unavailable: {e.message}")
            raise HTTPException(
                status_code=503,
                detail=self._format_error_response(e)
            )
            
        except PostprocessingError as e:
            # 502 Bad Gateway - Internal processing error
            self._logger.error(f"Processing error: {e.message}")
            raise HTTPException(
                status_code=502,
                detail=self._format_error_response(e)
            )
            
        except PredictionServiceError as e:
            # 500 Internal Server Error - General service error
            self._logger.error(f"Service error: {e.message}")
            raise HTTPException(
                status_code=500,
                detail=self._format_error_response(e)
            )
            
        except Exception as e:
            # 500 Internal Server Error - Unexpected error
            self._logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "details": str(e)
                }
            )
    
    def _format_error_response(self, exception: DomainException) -> Dict[str, Any]:
        """
        Format domain exceptions into HTTP error responses.
        
        Args:
            exception: Domain exception to format.
            
        Returns:
            Dictionary suitable for HTTP error response.
        """
        return {
            "error": exception.__class__.__name__,
            "message": exception.message,
            "details": exception.details
        }
