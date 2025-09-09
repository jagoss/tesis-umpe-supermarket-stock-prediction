"""
Application layer for MCP Prediction Server.

This module contains the use cases and application services that orchestrate
domain operations. It depends on domain interfaces but not on infrastructure.

Following Clean Architecture principles, this layer coordinates between
the domain and infrastructure layers.
"""

from .services import PredictionServiceImpl

__all__ = [
    "PredictionServiceImpl",
]
