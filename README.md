# Supermarket Stock Prediction Server

A production-ready stock prediction service built with **Clean Architecture** and
**Domain-Driven Design (DDD)** principles, designed as part of a UMPE thesis project.

The server exposes a REST API and an [MCP](https://modelcontextprotocol.io/) endpoint
for integration with [Onyx](https://onyx.app), an open-source AI assistant platform.
Models trained in any framework (scikit-learn, PyTorch, TensorFlow, etc.) are served
through a single **ONNX Runtime** adapter — *train anywhere, serve with ONNX*.

---

## Quick Start

### Prerequisites

- Python 3.11+
- (Optional) A trained `.onnx` model — the project ships with a toy
  `example_model.onnx` for development.

### Install

```bash
# Runtime dependencies only
pip install -e .

# With development tools (pytest, black, ruff, mypy, …)
pip install -e ".[dev]"

# With training pipeline dependencies (scikit-learn, skl2onnx, …)
pip install -e ".[training]"
```

### Configure

Configuration is driven by environment variables:

| Variable                   | Description                                 | Default               |
|----------------------------|---------------------------------------------|-----------------------|
| `MODEL_BACKEND`            | Model backend — `onnx` or `dummy`           | `onnx`                |
| `MODEL_PATH`               | Path to the `.onnx` model file              | `server/models/example_model.onnx` |
| `DEFAULT_PREDICTION_VALUE` | Constant value for the `dummy` backend      | `0`                   |

### Run

```bash
# Start the server (development mode with hot-reload)
python -m server.main

# Or with uvicorn directly
uvicorn server.interface.http.api:app --reload

# Use the dummy backend (no model file needed)
MODEL_BACKEND=dummy python -m server.main
```

The server starts at `http://127.0.0.1:8000`.

---

## API

### `GET /health`

Liveness probe.

```bash
curl http://127.0.0.1:8000/health
# {"status": "ok"}
```

### `POST /predict`

Predict stock demand for a product at a store over a date range.

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-001",
    "store_id": "STORE-A",
    "start_date": "2026-03-02",
    "end_date": "2026-03-04"
  }'
```

Response:

```json
{
  "product_id": "PROD-001",
  "store_id": "STORE-A",
  "predictions": [
    { "date": "2026-03-02", "quantity": 10 },
    { "date": "2026-03-03", "quantity": 15 },
    { "date": "2026-03-04", "quantity": 8 }
  ]
}
```

Optionally include recent sales history to improve accuracy:

```json
{
  "product_id": "PROD-001",
  "store_id": "STORE-A",
  "start_date": "2026-03-02",
  "end_date": "2026-03-04",
  "history": [
    { "date": "2026-02-27", "quantity": 10.0 },
    { "date": "2026-02-28", "quantity": 12.5 },
    { "date": "2026-03-01", "quantity": 8.0 }
  ]
}
```

### MCP Endpoint

The server exposes an MCP endpoint at `/mcp` for integration with Onyx and other
LLM-based assistants. The `predict_stock` tool is automatically generated from the
`/predict` endpoint.

```bash
curl http://127.0.0.1:8000/mcp
```

---

## Architecture

The project follows **Clean Architecture** with four layers:

```
server/
├── domain/            # Entities, value objects, domain exceptions
├── application/       # Use cases, DTOs, ports (interfaces)
├── infrastructure/    # Adapters: ONNX model, preprocessor, postprocessor, config, DI
└── interface/         # HTTP API (FastAPI), MCP integration, Pydantic schemas
```

**Dependency rule:** inner layers never depend on outer layers.
Infrastructure and interface layers depend inward through ports (dependency inversion).

### Prediction Pipeline

```
PredictStockInput (DTO)
  → BasicPreprocessor   → PreprocessedData
  → ONNXModel / Dummy   → ModelRawPrediction
  → BasicPostprocessor  → StockForecast (domain entity)
  → PredictStockUseCase → PredictStockOutput (DTO, rounded quantities)
```

For detailed architecture documentation and PlantUML diagrams, see
[`.docs/arquitectura_proyecto.md`](.docs/arquitectura_proyecto.md).

---

## Onyx Integration

[Onyx](https://onyx.app) serves as the conversational AI frontend, connecting to this
server via MCP. Onyx provides the chat UI, LLM orchestration, memory, and tool routing.

```
User → Onyx (Chat UI + LLM) → MCP → Prediction Server (/predict) → ONNX Model
```

For the full setup guide (registering the MCP server, creating an agent/persona, and
testing the integration), see
[`.docs/onyx_integration.md`](.docs/onyx_integration.md).

---

## Development

### Run Tests

```bash
pytest
pytest --cov=server --cov-report=term-missing
```

### Lint & Format

```bash
ruff check .
black --check .
isort --check .
mypy server/ --strict
```

### Pre-commit Hooks

The project includes a `.pre-commit-config.yaml` that runs `ruff`, `black`,
`isort`, and `mypy` automatically before each commit.

```bash
# Install hooks (one-time setup)
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

### CI Pipelines

Every push to `develop`/`main` and every pull request triggers three
specialized workflows (path-filtered for efficiency):

| Workflow | File | What it runs |
|---|---|---|
| **Lint** | `.github/workflows/lint.yml` | `ruff check`, `black --check`, `isort --check` |
| **Type Check** | `.github/workflows/typecheck.yml` | `mypy server/ --strict` |
| **Tests** | `.github/workflows/test.yml` | `pytest` with coverage (Python 3.11 + 3.12 matrix) |

Coverage reports are uploaded as GitHub Actions artifacts.

### Project Structure

```
.
├── server/                    # Main application
│   ├── domain/                # Domain entities & exceptions
│   ├── application/           # Use cases, DTOs, ports
│   ├── infrastructure/        # Adapters, config, DI container
│   ├── interface/             # HTTP API & MCP
│   ├── models/                # ONNX model artifacts
│   ├── tests/                 # Test suite
│   └── main.py                # Uvicorn entrypoint
├── agent/                     # Minimal agent package (Onyx replaces custom agent)
├── .docs/                     # Architecture docs, Onyx integration guide
├── pyproject.toml             # Project metadata & tool config
├── requirements.txt           # Pinned runtime dependencies
└── README.md                  # This file
```

---

## License

This project is developed as part of a UMPE thesis.
