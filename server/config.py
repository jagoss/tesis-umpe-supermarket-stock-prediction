"""
Configuration and dependency injection for the MCP Prediction Server.

This module provides environment-based configuration and dependency injection
setup following Clean Architecture principles.
"""

import logging
import os
from typing import Optional
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field

from .domain import PredictionService
from .application import PredictionServiceImpl
from .infrastructure import TorchModel, SklearnModel, DefaultPreprocessor, DefaultPostprocessor
from .interface import MCPPredictController


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This configuration follows the 12-factor app methodology,
    allowing easy deployment across different environments.
    """
    
    # Server Configuration
    app_name: str = Field(default="MCP Prediction Server", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Model Configuration
    model_type: str = Field(default="sklearn", env="MODEL_TYPE")  # "torch" or "sklearn"
    model_path: str = Field(default="./models/model.pkl", env="MODEL_PATH")
    model_version: str = Field(default="v1.0.0", env="MODEL_VERSION")
    
    # PyTorch specific settings
    torch_device: str = Field(default="cpu", env="TORCH_DEVICE")
    
    # Processing Configuration
    feature_mapping_file: Optional[str] = Field(default=None, env="FEATURE_MAPPING_FILE")
    output_format: str = Field(default="json", env="OUTPUT_FORMAT")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns:
        Application settings loaded from environment.
    """
    return Settings()


def setup_logging(settings: Settings) -> logging.Logger:
    """
    Configure application logging.
    
    Args:
        settings: Application settings containing log configuration.
        
    Returns:
        Configured logger instance.
    """
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(),
            # TODO: Add file handler for production
            # logging.FileHandler("app.log")
        ]
    )
    
    logger = logging.getLogger("mcp_server")
    logger.info(f"Logging configured at {settings.log_level} level")
    
    return logger


def create_model(settings: Settings, logger: logging.Logger):
    """
    Create ML model instance based on configuration.
    
    Args:
        settings: Application settings.
        logger: Logger instance.
        
    Returns:
        Configured ML model instance.
        
    Raises:
        ValueError: If model type is not supported.
    """
    model_path = Path(settings.model_path)
    
    if settings.model_type.lower() == "torch":
        logger.info(f"Creating PyTorch model from {model_path}")
        return TorchModel(
            model_path=str(model_path),
            version=settings.model_version,
            device=settings.torch_device,
            logger=logger
        )
    elif settings.model_type.lower() == "sklearn":
        logger.info(f"Creating scikit-learn model from {model_path}")
        return SklearnModel(
            model_path=str(model_path),
            version=settings.model_version,
            logger=logger
        )
    else:
        raise ValueError(f"Unsupported model type: {settings.model_type}")


def create_preprocessor(settings: Settings, logger: logging.Logger):
    """
    Create data preprocessor instance.
    
    Args:
        settings: Application settings.
        logger: Logger instance.
        
    Returns:
        Configured preprocessor instance.
    """
    feature_mapping = None
    
    if settings.feature_mapping_file:
        # TODO: Load feature mapping from file
        logger.info(f"Loading feature mapping from {settings.feature_mapping_file}")
        # feature_mapping = load_json(settings.feature_mapping_file)
    
    logger.info("Creating default preprocessor")
    return DefaultPreprocessor(
        feature_mapping=feature_mapping,
        logger=logger
    )


def create_postprocessor(settings: Settings, logger: logging.Logger):
    """
    Create data postprocessor instance.
    
    Args:
        settings: Application settings.
        logger: Logger instance.
        
    Returns:
        Configured postprocessor instance.
    """
    logger.info(f"Creating postprocessor with {settings.output_format} format")
    return DefaultPostprocessor(
        output_format=settings.output_format,
        logger=logger
    )


def create_prediction_service(settings: Settings, logger: logging.Logger) -> PredictionService:
    """
    Create prediction service with all dependencies.
    
    This function implements dependency injection by creating and wiring
    all required components for the prediction service.
    
    Args:
        settings: Application settings.
        logger: Logger instance.
        
    Returns:
        Fully configured prediction service.
    """
    logger.info("Initializing prediction service dependencies")
    
    # Create dependencies
    model = create_model(settings, logger)
    preprocessor = create_preprocessor(settings, logger)
    postprocessor = create_postprocessor(settings, logger)
    
    # Create and return service
    service = PredictionServiceImpl(
        model=model,
        preprocessor=preprocessor,
        postprocessor=postprocessor,
        logger=logger
    )
    
    logger.info("Prediction service initialized successfully")
    return service


def create_controller(prediction_service: PredictionService, logger: logging.Logger) -> MCPPredictController:
    """
    Create HTTP controller with dependencies.
    
    Args:
        prediction_service: Configured prediction service.
        logger: Logger instance.
        
    Returns:
        Configured HTTP controller.
    """
    logger.info("Creating HTTP controller")
    return MCPPredictController(
        prediction_service=prediction_service,
        logger=logger
    )
