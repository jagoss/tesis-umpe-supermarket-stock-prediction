"""Tests for the application entry point (``server.main``)."""

from __future__ import annotations

from unittest.mock import patch

from server.main import run


class TestRun:
    """Verify that ``run()`` delegates to ``uvicorn.run`` with the correct settings."""

    @patch("server.main.uvicorn")
    def test_calls_uvicorn_run(self, mock_uvicorn) -> None:  # type: ignore[no-untyped-def]
        run()
        mock_uvicorn.run.assert_called_once()

    @patch("server.main.uvicorn")
    def test_passes_app_import_string(self, mock_uvicorn) -> None:  # type: ignore[no-untyped-def]
        run()
        args, _ = mock_uvicorn.run.call_args
        assert args[0] == "server.interface.http.api:app"

    @patch("server.main.uvicorn")
    def test_uses_localhost_and_port_8000(self, mock_uvicorn) -> None:  # type: ignore[no-untyped-def]
        run()
        _, kwargs = mock_uvicorn.run.call_args
        assert kwargs["host"] == "127.0.0.1"
        assert kwargs["port"] == 8000

    @patch("server.main.uvicorn")
    def test_enables_reload_for_development(self, mock_uvicorn) -> None:  # type: ignore[no-untyped-def]
        run()
        _, kwargs = mock_uvicorn.run.call_args
        assert kwargs["reload"] is True
