"""FastAPI application exposing the prediction endpoint."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP  # type: ignore[import-untyped]
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from server.application import PredictStockInput
from server.domain import DomainError, ValidationError
from server.infrastructure.config import load_settings
from server.infrastructure.container import get_predict_use_case_singleton
from server.infrastructure.logging import configure_logging
from server.interface.http.metrics import MODEL_INFERENCE_SECONDS
from server.interface.http.middleware import (
    ApiKeyMiddleware,
    CorrelationIdMiddleware,
    TimeoutMiddleware,
)
from server.interface.http.schemas import PredictionPoint as HttpPredictionPoint
from server.interface.http.schemas import (
    PredictionRequest,
    PredictionResponse,
)

logger = logging.getLogger(__name__)

_settings = load_settings()

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
_limiter = Limiter(key_func=get_remote_address, default_limits=[])

_REQUEST_TIMEOUT_SECONDS = 30


def _rate_limit_exceeded_handler(_request: Request, _exc: RateLimitExceeded) -> JSONResponse:
    """Return a 429 JSON response when the rate limit is exceeded."""
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def _lifespan(_application: FastAPI) -> AsyncIterator[None]:
    """Initialize logging and warm up the DI container at startup."""
    configure_logging(level=_settings.log_level, fmt=_settings.log_format)
    get_predict_use_case_singleton()
    logger.info("Prediction service started and ready")
    yield


app = FastAPI(title="Supermarket Stock Prediction Server", version="0.1.0", lifespan=_lifespan)

app.state.limiter = _limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# ---------------------------------------------------------------------------
# Middleware stack (Starlette applies in reverse registration order)
# Register: Timeout → ApiKey → CorrelationId → CORS (last = outermost)
# Execution order for requests: CORS → CorrelationId → ApiKey → Timeout
# ---------------------------------------------------------------------------
app.add_middleware(TimeoutMiddleware, timeout_seconds=_REQUEST_TIMEOUT_SECONDS)
app.add_middleware(ApiKeyMiddleware, api_key=_settings.api_key)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Prometheus metrics (auto-instruments all routes)
# ---------------------------------------------------------------------------
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


@app.get("/health", operation_id="check_health", tags=["monitoring"])
async def health() -> dict[str, str]:
    """Simple liveness probe returning service status."""
    return {"status": "ok"}


@app.post(
    "/predict",
    operation_id="predict_stock",
    tags=["prediction"],
    responses={
        400: {"description": "Validation error (e.g. end date before start date)"},
        401: {"description": "Missing or invalid API key"},
        422: {"description": "Domain error during prediction"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    },
)
@_limiter.limit(_settings.rate_limit)
async def predict(
    request: Request, payload: PredictionRequest
) -> PredictionResponse:  # noqa: ARG001
    """Predict stock for a product and store over a date range.

    Use this tool when the user asks about future stock needs, demand forecasts,
    or how many units of a product a store should order.  Provide the product ID,
    store ID, and the date range to forecast.  Optionally include recent sales
    history to improve accuracy.

    Args:
        request: The incoming HTTP request (required by the rate-limiter decorator).
        payload: The prediction request with identifiers, date range, and optional history.

    Returns:
        The predicted quantities for each day in the requested window.

    """
    try:
        history = (
            [(hp.date, hp.quantity) for hp in payload.history]
            if payload.history is not None
            else None
        )
        uc = get_predict_use_case_singleton()
        with MODEL_INFERENCE_SECONDS.time():
            result = uc.execute(
                PredictStockInput(
                    product_id=payload.product_id,
                    store_id=payload.store_id,
                    start_date=payload.start_date,
                    end_date=payload.end_date,
                    history=history,
                )
            )
        points: list[HttpPredictionPoint] = [
            HttpPredictionPoint(date=p.date, quantity=p.quantity) for p in result.predictions
        ]
        return PredictionResponse(
            product_id=result.product_id, store_id=result.store_id, predictions=points
        )
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except DomainError as de:
        logger.exception("Domain error during prediction")
        raise HTTPException(status_code=422, detail=str(de)) from de
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during prediction")
        raise HTTPException(status_code=500, detail="internal server error") from exc


# ---------------------------------------------------------------------------
# MCP (Model Context Protocol) – exposes prediction tools for Onyx / LLMs
# ---------------------------------------------------------------------------
mcp = FastApiMCP(
    app,
    name="Supermarket Stock Prediction MCP",
    description=(
        "MCP server that exposes supermarket stock-prediction capabilities. "
        "An LLM-based assistant (e.g. Onyx) can call these tools to forecast "
        "product demand for a given store and date range."
    ),
    describe_full_response_schema=True,
    exclude_operations=["check_health", "metrics"],
)
mcp.mount_http()
