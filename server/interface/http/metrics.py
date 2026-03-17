"""Custom Prometheus metrics for the prediction service."""

from __future__ import annotations

from prometheus_client import Histogram

MODEL_INFERENCE_SECONDS = Histogram(
    "model_inference_seconds",
    "Time spent on model inference (use-case execution).",
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
