# ── Builder stage ─────────────────────────────────────────────────────────────
# Installs runtime dependencies into an isolated prefix so the final image
# does not need build tools (pip, setuptools, wheel).
FROM python:3.11-slim AS builder

WORKDIR /build

RUN pip install --upgrade pip --no-cache-dir

# Install only the runtime dependencies declared in requirements.txt.
# Installed into /install so they can be copied to the runtime stage cleanly.
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy project root marker (required by config.py path resolution) and source
COPY pyproject.toml ./
COPY server/ ./server/

# Create data directory — files are injected via volume mount in docker-compose / production
RUN mkdir -p data

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /app
USER appuser

# Make the server package importable from WORKDIR and set sensible defaults.
# MODEL_PATH is relative to /app — override via environment or volume mount.
ENV PYTHONPATH=/app \
    MODEL_BACKEND=onnx \
    MODEL_PATH=server/models/example_model.onnx \
    DEFAULT_PREDICTION_VALUE=0 \
    PREPROCESSOR_BACKEND=basic \
    DATA_PATH=data/precomputed_features.parquet \
    SCALER_PATH=data/scaler_params.parquet

EXPOSE 8000

# Liveness probe — uses the built-in Python stdlib to avoid curl/wget dependency
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Single worker: the production preprocessor loads a large Parquet dict into
# memory at startup. Multiple workers each load their own copy, multiplying
# RAM usage proportionally. FastAPI + asyncio handles concurrent requests
# efficiently with a single process.
# Override with --workers N in docker-compose / k8s if RAM is not a constraint.
CMD ["uvicorn", "server.interface.http.api:app", \
     "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
