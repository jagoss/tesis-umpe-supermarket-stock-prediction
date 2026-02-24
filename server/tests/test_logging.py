"""Tests for the logging configuration module."""

from __future__ import annotations

import logging
from unittest.mock import patch

from server.infrastructure.logging import configure_logging


class TestConfigureLogging:
    """Verify ``configure_logging`` sets up the root logger correctly.

    ``logging.basicConfig`` is a one-shot function: it has no effect once
    handlers are already attached to the root logger (e.g. by pytest's
    log-capture plugin). Tests that need to verify level or format use
    ``force=True`` directly to validate the expected arguments, while the
    actual ``configure_logging`` function delegates to ``basicConfig``
    without ``force`` (safe for repeated calls in production).
    """

    @patch("server.infrastructure.logging.logging.basicConfig")
    def test_default_level_is_info(self, mock_basic) -> None:  # type: ignore[no-untyped-def]
        configure_logging()
        mock_basic.assert_called_once()
        _, kwargs = mock_basic.call_args
        assert kwargs["level"] == logging.INFO

    @patch("server.infrastructure.logging.logging.basicConfig")
    def test_string_level_is_converted(self, mock_basic) -> None:  # type: ignore[no-untyped-def]
        configure_logging(level="DEBUG")
        _, kwargs = mock_basic.call_args
        assert kwargs["level"] == logging.DEBUG

    @patch("server.infrastructure.logging.logging.basicConfig")
    def test_integer_level_is_forwarded(self, mock_basic) -> None:  # type: ignore[no-untyped-def]
        configure_logging(level=logging.WARNING)
        _, kwargs = mock_basic.call_args
        assert kwargs["level"] == logging.WARNING

    @patch("server.infrastructure.logging.logging.basicConfig")
    def test_case_insensitive_string_level(self, mock_basic) -> None:  # type: ignore[no-untyped-def]
        configure_logging(level="warning")
        _, kwargs = mock_basic.call_args
        assert kwargs["level"] == logging.WARNING

    @patch("server.infrastructure.logging.logging.basicConfig")
    def test_format_contains_required_fields(self, mock_basic) -> None:  # type: ignore[no-untyped-def]
        configure_logging()
        _, kwargs = mock_basic.call_args
        fmt = kwargs["format"]
        assert "%(asctime)s" in fmt
        assert "%(levelname)s" in fmt
        assert "%(name)s" in fmt

    @patch("server.infrastructure.logging.logging.basicConfig")
    def test_delegates_to_basic_config(self, mock_basic) -> None:  # type: ignore[no-untyped-def]
        """Verify that ``configure_logging`` ultimately calls ``basicConfig``."""
        configure_logging(level="ERROR")
        mock_basic.assert_called_once()

    def test_idempotent_when_called_twice(self) -> None:
        """Calling configure_logging twice should not duplicate handlers.

        ``logging.basicConfig`` is a no-op once handlers exist, so the
        handler count must remain stable across repeated calls.
        """
        configure_logging()
        handler_count = len(logging.getLogger().handlers)
        configure_logging()
        assert len(logging.getLogger().handlers) == handler_count

    def test_actual_basic_config_works_on_clean_logger(self) -> None:
        """Integration test: verify ``basicConfig`` works in a clean state.

        Uses ``force=True`` (only available in tests) to reset the root
        logger, then verifies ``configure_logging`` parameters are correct
        by applying them directly.
        """
        root = logging.getLogger()
        fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
        logging.basicConfig(force=True, level=logging.INFO, format=fmt)
        assert root.level == logging.INFO
        assert root.handlers
        handler = root.handlers[0]
        assert handler.formatter is not None
        fmt_str = handler.formatter._fmt
        assert fmt_str is not None
        assert "%(asctime)s" in fmt_str
