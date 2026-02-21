"""Logging configuration for the service."""
from __future__ import annotations

import logging
from typing import Union


def configure_logging(level: Union[int, str] = "INFO") -> None:
    """Configure root logging with a structured, concise format.

    Safe to call multiple times; subsequent calls will have no effect if the
    root logger is already configured.
    """
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())  # type: ignore[assignment]
    logging.basicConfig(
        level=level, format="%(asctime)s %(levelname)s %(name)s - %(message)s"
    )
