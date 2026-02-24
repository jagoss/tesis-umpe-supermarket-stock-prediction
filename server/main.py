"""Entrypoint to run the FastAPI app with Uvicorn.

Usage (recommended):
    uvicorn server.interface.http.api:app --reload

This module allows running via `python -m server.main` as well.
"""

from __future__ import annotations

import uvicorn


def run() -> None:
    """Run the FastAPI application using Uvicorn in development mode.

    Host: 127.0.0.1
    Port: 8000
    Reload: enabled
    """
    uvicorn.run("server.interface.http.api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":  # pragma: no cover - runtime entry
    run()
