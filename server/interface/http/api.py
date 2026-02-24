"""FastAPI application exposing the prediction endpoint."""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP

from server.application import PredictStockInput
from server.domain import DomainError, ValidationError
from server.infrastructure.container import get_predict_use_case_singleton
from server.infrastructure.logging import configure_logging
from server.interface.http.schemas import PredictionPoint as HttpPredictionPoint
from server.interface.http.schemas import (
    PredictionRequest,
    PredictionResponse,
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Supermarket Stock Prediction Server", version="0.1.0")


@app.on_event("startup")
async def _startup() -> None:
    """Initialize logging and warm up DI container.

    This reduces first-request latency by constructing the use case singleton
    and configuring the logging pipeline at process start.
    """
    configure_logging()
    # Touch singleton to initialize dependencies at startup for faster first request.
    _ = get_predict_use_case_singleton()
    logger.info("Prediction service started and ready")


@app.get("/health", operation_id="check_health", tags=["monitoring"])
async def health() -> dict[str, str]:
    """Simple liveness probe returning service status."""
    return {"status": "ok"}


@app.post(
    "/predict",
    response_model=PredictionResponse,
    operation_id="predict_stock",
    tags=["prediction"],
)
async def predict(payload: PredictionRequest) -> PredictionResponse:
    """Predict stock for a product and store over a date range.

    Use this tool when the user asks about future stock needs, demand forecasts,
    or how many units of a product a store should order.  Provide the product ID,
    store ID, and the date range to forecast.  Optionally include recent sales
    history to improve accuracy.

    Args:
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
    except ValidationError as ve:  # map to 400
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
    exclude_operations=["check_health"],
)
mcp.mount_http()
