"""
Interface layer for MCP Prediction Server.

This module contains the external interfaces (HTTP, CLI, etc.) that
expose the application's functionality. It handles request/response
serialization and delegates to the application layer.

Following Clean Architecture principles, this layer adapts external
protocols to internal domain models.
"""

from .controllers import MCPPredictController
from .schemas import PredictionRequestSchema, PredictionResponseSchema

__all__ = [
    "MCPPredictController",
    "PredictionRequestSchema", 
    "PredictionResponseSchema",
]
