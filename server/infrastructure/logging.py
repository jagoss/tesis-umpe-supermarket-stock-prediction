"""Logging configuration for the service."""

from __future__ import annotations

import logging
from contextvars import ContextVar

_correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


def get_correlation_id() -> str:
    """Return the current correlation ID for the active request context."""
    return _correlation_id_var.get()


def set_correlation_id(cid: str) -> None:
    """Set the correlation ID for the active request context."""
    _correlation_id_var.set(cid)


class _CorrelationIdFilter(logging.Filter):
    """Inject ``correlation_id`` into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        record.correlation_id = get_correlation_id()  # type: ignore[attr-defined]
        return True


def configure_logging(level: int | str = "INFO", fmt: str = "text") -> None:
    """Configure root logging with a structured, concise format.

    Args:
        level: Log level (string name or int constant).
        fmt: ``"text"`` for human-readable output, ``"json"`` for structured
            JSON lines suitable for production log aggregation.

    """
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())

    correlation_filter = _CorrelationIdFilter()

    if fmt == "json":
        from pythonjsonlogger.jsonlogger import JsonFormatter  # type: ignore[import-untyped]

        handler = logging.StreamHandler()
        handler.setFormatter(
            JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s",
            )
        )
        handler.addFilter(correlation_filter)
        root = logging.getLogger()
        root.setLevel(level)
        root.handlers.clear()
        root.addHandler(handler)
    else:
        logging.basicConfig(
            level=level, format="%(asctime)s %(levelname)s %(name)s - %(message)s"
        )
        # Add correlation filter to all existing handlers
        for handler in logging.getLogger().handlers:
            handler.addFilter(correlation_filter)
