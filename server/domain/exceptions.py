"""Domain exception hierarchy for the supermarket stock prediction server.

This module defines domain-level exceptions used across the application.
They should represent business/domain errors and be mapped to HTTP errors in the
interface layer.

Assumptions:
- Exceptions are lightweight and carry context in their message.
- Use specific exceptions over generic ones.
"""
from __future__ import annotations

from typing import Optional


class DomainError(Exception):
    """Base class for all domain-specific errors."""

    def __init__(self, message: str, *, cause: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.__cause__ = cause


class ValidationError(DomainError):
    """Raised when input data violates domain invariants."""


class PredictionError(DomainError):
    """Raised when a prediction cannot be produced or post-processed."""
