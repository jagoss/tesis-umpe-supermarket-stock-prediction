"""
Main application entry point for the MCP Prediction Server.

This module creates and configures the FastAPI application with all
dependencies properly injected following Clean Architecture principles.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings, setup_logging, create_prediction_service, create_controller
from .interface.schemas import PredictionRequestSchema, PredictionResponseSchema, ErrorResponseSchema


# Global variables for dependency injection
prediction_controller = None
logger = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    
    This function handles:
    - Dependency injection and service initialization on startup
    - Resource cleanup on shutdown
    """
    global prediction_controller, logger
    
    # Startup
    settings = get_settings()
    logger = setup_logging(settings)
    
    try:
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        
        # Initialize dependencies
        prediction_service = create_prediction_service(settings, logger)
        prediction_controller = create_controller(prediction_service, logger)
        
        logger.info("Application startup completed successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Application shutdown completed")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="MCP Server for Machine Learning Predictions in Supermarket Stock Management",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health", summary="Health Check")
    async def health_check():
        """Simple health check endpoint."""
        return {"status": "healthy", "service": settings.app_name}
    
    # Main prediction endpoint
    @app.post(
        "/predict",
        response_model=PredictionResponseSchema,
        responses={
            400: {"model": ErrorResponseSchema, "description": "Bad Request"},
            500: {"model": ErrorResponseSchema, "description": "Internal Server Error"},
            502: {"model": ErrorResponseSchema, "description": "Bad Gateway"},
            503: {"model": ErrorResponseSchema, "description": "Service Unavailable"},
        },
        summary="Make Prediction",
        description="Execute machine learning prediction using the configured model"
    )
    async def predict(request: PredictionRequestSchema) -> PredictionResponseSchema:
        """
        Make a prediction using the configured ML model.
        
        This endpoint accepts input features and returns predictions
        with confidence scores and model metadata.
        """
        if prediction_controller is None:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "ServiceUnavailable",
                    "message": "Prediction service not initialized",
                    "details": "Server is starting up or encountered initialization error"
                }
            )
        
        return await prediction_controller.post_predict(request)
    
    return app


# Create the FastAPI application
app = create_app()


if __name__ == "__main__":
    """
    Development server entry point.
    
    For production deployment, use a proper ASGI server like uvicorn:
    uvicorn server.main:app --host 0.0.0.0 --port 8000
    """
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
