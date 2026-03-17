"""HTTP middleware for correlation IDs, authentication, and timeouts."""

from __future__ import annotations

import asyncio
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from server.infrastructure.logging import set_correlation_id

_SKIP_PATHS = {"/health", "/metrics"}


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Read or generate a correlation ID and echo it in the response."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Inject or propagate the correlation ID for each request."""
        cid = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        set_correlation_id(cid)
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Enforce API key authentication when configured.

    When ``api_key`` is empty the middleware is a no-op (auth disabled).
    ``/health`` and ``/metrics`` are always exempt.
    """

    def __init__(self, app: object, api_key: str = "") -> None:  # noqa: D107
        super().__init__(app)  # type: ignore[arg-type]
        self._api_key = api_key

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Reject requests missing a valid API key, unless the path is exempt."""
        if not self._api_key or request.url.path in _SKIP_PATHS:
            return await call_next(request)

        key = request.headers.get("x-api-key") or ""
        if not key:
            auth = request.headers.get("authorization") or ""
            if auth.lower().startswith("bearer "):
                key = auth[7:]

        if key != self._api_key:
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing API key"})

        return await call_next(request)


class TimeoutMiddleware(BaseHTTPMiddleware):
    """Return 504 if the downstream handler exceeds *timeout_seconds*."""

    def __init__(self, app: object, timeout_seconds: float = 30) -> None:  # noqa: D107
        super().__init__(app)  # type: ignore[arg-type]
        self._timeout = timeout_seconds

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Return 504 if the handler does not respond within the configured timeout."""
        if request.url.path in _SKIP_PATHS:
            return await call_next(request)
        try:
            return await asyncio.wait_for(call_next(request), timeout=self._timeout)
        except TimeoutError:
            return JSONResponse(status_code=504, content={"detail": "Request timed out"})
