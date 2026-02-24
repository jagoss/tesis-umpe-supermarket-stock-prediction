# Implementation Plan — Next Phases

> **Audience:** Coding agent (Claude Code, Cursor, etc.)
> **Date:** February 2026
> **Repo:** `tesis-umpe-supermarket-stock-prediction`
> **Branch strategy:** Gitflow — create `feature/*` branches from `develop`, PRs target `develop`, `develop` merges to `main` for releases.

---

## What Already Exists (do NOT rebuild)

The prediction server is **fully implemented** and tested (91 tests pass). Here is what you can rely on:

| Component | Location | Status |
|-----------|----------|--------|
| Domain layer (entities, exceptions) | `server/domain/` | Complete |
| Application layer (use case, DTOs, ports) | `server/application/` | Complete |
| ONNX model adapter | `server/infrastructure/models/onnx_model.py` | Complete |
| Dummy model adapter | `server/infrastructure/models/dummy_model.py` | Complete |
| Pre/post-processing | `server/infrastructure/preprocessing/`, `postprocessing/` | Complete |
| DI container + config | `server/infrastructure/container.py`, `config.py` | Complete |
| FastAPI endpoints (`/health`, `/predict`) | `server/interface/http/api.py` | Complete |
| MCP endpoint (`/mcp`) via `fastapi-mcp` | `server/interface/http/api.py` (bottom) | Complete |
| HTTP schemas (Pydantic) | `server/interface/http/schemas.py` | Complete |
| Test suite | `server/tests/` (15 files, 91 tests) | Complete |
| Onyx integration docs | `.docs/onyx_integration.md` | Complete |

**Architecture:** Clean Architecture with Python Protocols as ports. The `PredictStockUseCase` orchestrates: `PreprocessorPort → ModelPort → PostprocessorPort`. Infrastructure adapters implement these protocols. Config is loaded from environment variables. The app is a single FastAPI instance (`server.interface.http.api:app`).

**Key ports** (in `server/application/ports.py`):
- `PreprocessorPort.preprocess(PredictStockInput) → PreprocessedData`
- `ModelPort.predict(PreprocessedData) → ModelRawPrediction`
- `PostprocessorPort.postprocess(ModelRawPrediction, PredictStockInput) → PredictStockOutput`

**Key DTOs** (in `server/application/dto.py`):
- `PredictStockInput(product_id, store_id, start_date, end_date, history?)`
- `PredictStockOutput(product_id, store_id, predictions: List[PredictionPoint])`

**Stubs that exist but are NOT complete:**
- `server/infrastructure/models/sklearn_model.py` — loads joblib but feature construction is a placeholder
- `server/infrastructure/models/torch_model.py` — returns zeros (stub)

---

## Phase 1: CI/CD — Automated Test Pipeline

**Goal:** Every push and PR runs the test suite automatically.

**Branch:** `feature/ci-test-pipeline`

### Step 1.1: Create GitHub Actions test workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]" || pip install -e .
          pip install pytest

      - name: Run tests
        env:
          MODEL_BACKEND: dummy
          DEFAULT_PREDICTION_VALUE: "10"
        run: pytest server/tests/ -v --tb=short
```

### Step 1.2: Add `[project.optional-dependencies]` for dev tooling

In `pyproject.toml`, add under `[project]`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "httpx>=0.27",
]
```

### Verification
- Push to a branch, confirm the workflow runs and all 91+ tests pass on both Python 3.11 and 3.12.

---

## Phase 2: Containerization (Docker)

**Goal:** Containerize the prediction server for reproducible deployment. Onyx will connect to this container's `/mcp` endpoint.

**Branch:** `feature/docker`

### Step 2.1: Create `Dockerfile`

Create `Dockerfile` at the project root:

```dockerfile
FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ server/
COPY pyproject.toml .

EXPOSE 8000

ENV MODEL_BACKEND=onnx
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "server.interface.http.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2.2: Create `docker-compose.yml`

Create `docker-compose.yml` at the project root. This sets up the prediction server and leaves a placeholder for Onyx:

```yaml
services:
  prediction-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_BACKEND=${MODEL_BACKEND:-onnx}
      - MODEL_PATH=${MODEL_PATH:-server/models/example_model.onnx}
      - DEFAULT_PREDICTION_VALUE=${DEFAULT_PREDICTION_VALUE:-0}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  # Onyx connects to http://prediction-server:8000/mcp
  # See .docs/onyx_integration.md for Onyx setup instructions.
```

### Step 2.3: Create `.dockerignore`

```
.git
.github
.venv
__pycache__
*.pyc
.pytest_cache
.docs
.notebooks
*.md
!requirements.txt
server/tests/
```

### Step 2.4: Create `.env.example`

Create `.env.example` at the project root to document all environment variables:

```bash
# Model configuration
MODEL_BACKEND=onnx          # Options: dummy, onnx, sklearn, torch
MODEL_PATH=server/models/example_model.onnx
DEFAULT_PREDICTION_VALUE=0   # Only used when MODEL_BACKEND=dummy
```

### Verification
```bash
docker compose build
docker compose up -d
curl http://localhost:8000/health          # → {"status": "ok"}
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"product_id":"P1","store_id":"S1","start_date":"2026-03-02","end_date":"2026-03-04"}'
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1}'  # → not 404
docker compose down
```

---

## Phase 3: Inventory Query MCP Tool

**Goal:** Expose a read-only inventory/sales query endpoint as a second MCP tool so Onyx can answer questions like "What is the current stock of product X in store Y?" without needing to predict.

**Branch:** `feature/inventory-tool`

This follows the same Clean Architecture pattern already established.

### Step 3.1: Domain — Add inventory entities

Create `server/domain/inventory.py`:

```python
"""Inventory domain entities."""
from __future__ import annotations

import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InventoryRecord:
    """A snapshot of stock for a product at a store on a specific date."""
    product_id: str
    store_id: str
    date: datetime.date
    quantity_on_hand: int
    quantity_sold: int
```

### Step 3.2: Application — Add inventory port and use case

Create `server/application/use_cases/get_inventory.py`:

```python
"""Use case: query inventory data."""
```

Define a new port `InventoryRepositoryPort` in `server/application/ports.py` (append, don't replace):

```python
class InventoryRepositoryPort(Protocol):
    """Read-only access to inventory/sales data."""

    def get_inventory(
        self, product_id: str, store_id: str,
        start_date: date, end_date: date,
    ) -> list[InventoryRecord]:
        """Return inventory records for the given filters."""
        ...
```

Create `GetInventoryUseCase` that validates input and delegates to the port.

### Step 3.3: Infrastructure — In-memory or CSV-backed adapter

For the first iteration, create `server/infrastructure/repositories/csv_inventory_repository.py` that reads from a CSV file (path configurable via env var `INVENTORY_CSV_PATH`). This is enough to demonstrate the tool to Onyx without needing a database yet.

CSV format: `product_id,store_id,date,quantity_on_hand,quantity_sold`

Include a small example CSV at `server/data/example_inventory.csv` with ~20 rows.

### Step 3.4: Interface — Add `/inventory` endpoint

In `server/interface/http/api.py`, add:

```python
@app.get("/inventory", operation_id="query_inventory", tags=["inventory"])
async def get_inventory(
    product_id: str, store_id: str,
    start_date: datetime.date, end_date: datetime.date,
) -> InventoryResponse:
    """Query current inventory and recent sales for a product at a store.

    Use this tool when the user asks about current stock levels, recent sales
    history, or inventory status. Provide the product ID, store ID, and date
    range to query.
    """
```

Add corresponding Pydantic schemas in `server/interface/http/schemas.py`.

**Important:** The existing `FastApiMCP` instance auto-discovers new endpoints. Since it uses `exclude_operations=["check_health"]`, the new `query_inventory` operation will automatically appear as an MCP tool. No MCP code changes needed.

### Step 3.5: Wire in the DI container

In `server/infrastructure/container.py`, construct the `GetInventoryUseCase` with the CSV adapter and make it available.

### Step 3.6: Tests

Create `server/tests/test_inventory.py`:
- Test valid inventory query returns data
- Test empty result when no matching records
- Test date validation (end < start → 400)
- Test that `/inventory` appears as MCP tool (not excluded)

### Verification
```bash
MODEL_BACKEND=dummy python -m server.main
# HTTP query:
curl "http://localhost:8000/inventory?product_id=PROD-001&store_id=STORE-A&start_date=2026-02-01&end_date=2026-02-28"
# MCP: connect Onyx → verify both predict_stock AND query_inventory appear
pytest server/tests/ -v  # all tests pass
```

---

## Phase 4: Database Integration (PostgreSQL)

**Goal:** Replace the CSV inventory adapter with PostgreSQL. Add a sales history table that both the inventory tool and (optionally) the prediction endpoint can use.

**Branch:** `feature/database`

### Step 4.1: Add dependencies

In `pyproject.toml` and `requirements.txt`:
```
sqlalchemy>=2.0,<3.0
asyncpg>=0.30
alembic>=1.14
```

### Step 4.2: Define SQLAlchemy models

Create `server/infrastructure/database/models.py` with tables:
- `products` (id, name, category, sku)
- `stores` (id, name, location)
- `inventory_snapshots` (product_id, store_id, date, quantity_on_hand, quantity_sold)

### Step 4.3: Create Alembic migration setup

```bash
alembic init server/infrastructure/database/migrations
```

Configure `alembic.ini` and `env.py` to use the `DATABASE_URL` environment variable.

Create the initial migration for the three tables.

### Step 4.4: Implement PostgreSQL repository adapter

Create `server/infrastructure/repositories/pg_inventory_repository.py` implementing `InventoryRepositoryPort` using SQLAlchemy async queries.

### Step 4.5: Update DI container

In `server/infrastructure/container.py`:
- Add `DATABASE_URL` to `Settings`
- Create DB engine/session at startup
- Wire `PgInventoryRepository` when `DATABASE_URL` is set, fall back to CSV adapter when not set

### Step 4.6: Update Docker Compose

Add a `postgres` service to `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: supermarket
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-localdev}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  prediction-server:
    # ... existing config ...
    environment:
      - DATABASE_URL=postgresql+asyncpg://app:${POSTGRES_PASSWORD:-localdev}@postgres:5432/supermarket
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```

### Step 4.7: Seed script

Create `server/infrastructure/database/seed.py` that loads example inventory data into the database for development/demo purposes.

### Step 4.8: Tests

- Test `PgInventoryRepository` against a SQLite in-memory database (SQLAlchemy makes this easy)
- Test container selects correct adapter based on `DATABASE_URL` presence
- Existing tests must still pass (they don't use the database)

### Verification
```bash
docker compose up -d
alembic upgrade head
python server/infrastructure/database/seed.py
curl "http://localhost:8000/inventory?product_id=PROD-001&store_id=STORE-A&start_date=2026-02-01&end_date=2026-02-28"
pytest server/tests/ -v
```

---

## Phase 5: Product Catalog MCP Tool

**Goal:** Expose a product search endpoint so Onyx can answer "What products do you have in the dairy category?" or help users discover valid product/store IDs before making predictions.

**Branch:** `feature/product-catalog`

### Step 5.1: Application port

Add to `server/application/ports.py`:

```python
class ProductCatalogPort(Protocol):
    """Read-only access to the product/store catalog."""

    def search_products(self, query: str, category: str | None = None, limit: int = 20) -> list[Product]: ...
    def list_stores(self) -> list[Store]: ...
    def get_product(self, product_id: str) -> Product | None: ...
```

### Step 5.2: Endpoints

Add two new endpoints to `api.py`:

```python
@app.get("/products", operation_id="search_products", tags=["catalog"])
async def search_products(q: str = "", category: str | None = None, limit: int = 20) -> ProductListResponse:
    """Search the product catalog by name or category.

    Use this tool when the user asks what products are available, searches by
    name, or needs to find a product ID before requesting a prediction.
    """

@app.get("/stores", operation_id="list_stores", tags=["catalog"])
async def list_stores() -> StoreListResponse:
    """List all stores in the system.

    Use this tool when the user asks which stores exist or needs a store ID.
    """
```

### Step 5.3: Infrastructure adapter

If Phase 4 (database) is done: implement against the `products` and `stores` tables.
If Phase 4 is NOT done: implement a CSV/JSON-backed adapter (same pattern as Phase 3).

### Step 5.4: Tests

- Test product search with and without category filter
- Test store listing
- Test product lookup by ID (found and not found)
- Verify both operations appear as MCP tools

### Verification
After this phase, Onyx will have **four** tools:
1. `predict_stock` — forecast demand
2. `query_inventory` — check current stock
3. `search_products` — find products
4. `list_stores` — list stores

---

## Phase 6: Structured Logging & Prediction Tracking

**Goal:** Add structured JSON logging and a prediction audit log so each prediction can be traced and later used to evaluate model accuracy.

**Branch:** `feature/observability`

### Step 6.1: Structured logging

Replace the current `server/infrastructure/logging.py` with structured JSON logging:

- Use Python's `logging` with a JSON formatter (e.g., `python-json-logger`)
- Add `pyproject.toml` dependency: `python-json-logger>=3.0`
- Log each prediction request with: `product_id`, `store_id`, `date_range`, `latency_ms`, `horizon`
- Log level configurable via `LOG_LEVEL` environment variable

### Step 6.2: Prediction audit log

Create `server/infrastructure/audit.py`:

- Define an `AuditPort` protocol in `server/application/ports.py`:
  ```python
  class AuditPort(Protocol):
      def log_prediction(self, input: PredictStockInput, output: PredictStockOutput, latency_ms: float) -> None: ...
  ```
- First implementation: `JsonFileAuditLogger` that appends JSON lines to a file (`AUDIT_LOG_PATH` env var, default `logs/predictions.jsonl`)
- Later (after Phase 4): `PgAuditLogger` that writes to a `prediction_audit` database table

### Step 6.3: Wire into use case

The `PredictStockUseCase` should accept an optional `AuditPort`. After a successful prediction, call `audit.log_prediction(...)`. Do NOT make audit failures block the response — wrap in try/except and log a warning.

### Step 6.4: Tests

- Test `JsonFileAuditLogger` writes valid JSONL
- Test use case still works when audit is None
- Test use case still returns successfully when audit raises an exception

---

## Phase 7: API Security

**Goal:** Add API key authentication to protect the prediction server endpoints. Onyx will send the API key in requests.

**Branch:** `feature/api-auth`

### Step 7.1: API key middleware

Create `server/interface/http/middleware.py`:

- Read `API_KEY` from environment variable
- If `API_KEY` is set: require `Authorization: Bearer <key>` header on all endpoints except `/health`
- If `API_KEY` is not set: allow all requests (backward compatible for development)
- Return 401 for missing/invalid keys

Implement as a FastAPI dependency or Starlette middleware.

### Step 7.2: Update schemas

Add `401` response to the OpenAPI spec for protected endpoints:

```python
@app.post("/predict", ..., responses={401: {"description": "Invalid or missing API key"}})
```

### Step 7.3: Update Docker Compose

Add `API_KEY` to the environment section:
```yaml
environment:
  - API_KEY=${API_KEY:-}  # empty = no auth (dev mode)
```

Update `.env.example` to document `API_KEY`.

### Step 7.4: Update Onyx docs

In `.docs/onyx_integration.md`, add a section explaining how to configure the API key in Onyx's MCP server connection settings.

### Step 7.5: Tests

- Test that requests without key get 401 when `API_KEY` is set
- Test that requests with correct key succeed
- Test that `/health` is always accessible (no auth)
- Test that when `API_KEY` is empty/unset, all requests succeed (dev mode)
- All existing tests must still pass (they don't set `API_KEY`)

---

## Phase 8: Production ML Model Training Notebook

**Goal:** Create a Jupyter notebook that trains a real stock prediction model on supermarket data and exports it as ONNX, ready to replace `example_model.onnx`.

**Branch:** `feature/training-notebook`

### Step 8.1: Create training notebook

Create `.notebooks/train_stock_model.ipynb` with these sections:

1. **Data Loading** — Load sales history CSV (provide an example synthetic dataset)
2. **EDA** — Basic exploratory plots (sales by day of week, trends, seasonality)
3. **Feature Engineering** — Must produce the same features that `ONNXModel._build_features()` expects:
   - `horizon_step` (day ahead index)
   - `day_of_week` (0-6)
   - `month` (1-12)
   - `is_weekend` (0/1)
   - Document clearly if you add new features — the ONNX adapter must be updated to match
4. **Model Training** — Train a `RandomForestRegressor` or `GradientBoostingRegressor` from sklearn
5. **Evaluation** — MAE, RMSE, and a plot of predicted vs actual
6. **Export to ONNX** — Use `skl2onnx.to_onnx()` and save to `server/models/stock_model_v1.onnx`
7. **Validation** — Load the exported ONNX model with `onnxruntime` and verify predictions match sklearn

### Step 8.2: Create synthetic training dataset

Create `.notebooks/data/synthetic_sales.csv` with ~1 year of daily synthetic sales data for 5 products across 3 stores. Include:
- Weekly seasonality (weekends have different sales)
- Monthly seasonality
- Random noise
- A few missing days (to test robustness)

### Step 8.3: Add notebook dependencies

Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
notebooks = [
    "jupyter>=1.0",
    "matplotlib>=3.8",
    "pandas>=2.1",
]
```

### Verification
- Run all notebook cells top to bottom
- Verify `server/models/stock_model_v1.onnx` is produced
- Start server with `MODEL_BACKEND=onnx MODEL_PATH=server/models/stock_model_v1.onnx python -m server.main`
- Send a prediction request and verify non-trivial (non-constant) results

---

## Phase Summary & Dependency Graph

```
Phase 1: CI/CD Pipeline           ← Do first (protects all future work)
Phase 2: Docker                   ← Do second (deployment foundation)
Phase 3: Inventory Tool           ← Independent (enriches Onyx capabilities)
Phase 4: Database                 ← After Phase 3 (upgrades CSV to PostgreSQL)
Phase 5: Product Catalog          ← After Phase 3 (same pattern)
Phase 6: Observability            ← Independent (can be done anytime)
Phase 7: API Security             ← After Phase 2 (needs deployment context)
Phase 8: Training Notebook        ← Independent (can be done anytime)
```

Recommended order: **1 → 2 → 3 → 5 → 4 → 6 → 7 → 8**

Phases 6 and 8 are fully independent and can be done in parallel with anything.

---

## Architecture Rules (MUST follow)

1. **Clean Architecture:** Domain layer has zero framework imports. Application layer depends only on domain. Infrastructure implements application ports.
2. **Ports as Protocols:** New capabilities are defined as `typing.Protocol` classes in `server/application/ports.py`.
3. **DI via container:** All wiring happens in `server/infrastructure/container.py`. Endpoints never construct infrastructure objects directly.
4. **MCP auto-discovery:** The existing `FastApiMCP` instance at the bottom of `api.py` auto-discovers new FastAPI endpoints. New tools only need `operation_id` and `tags` on their decorator. Do NOT modify the MCP setup unless you need to exclude an operation.
5. **Test patterns:** Follow `server/tests/test_api.py` for test fixtures (patch `MODEL_BACKEND=dummy`, reset singleton). Tests must pass with `pytest server/tests/ -v`.
6. **Config via env vars:** All new settings go through `server/infrastructure/config.py`'s `Settings` dataclass, loaded from environment variables with sensible defaults.
7. **Docstrings for MCP tools:** Any endpoint exposed as an MCP tool MUST have a docstring starting with "Use this tool when..." to guide the LLM.
8. **No breaking changes:** Existing endpoints, schemas, and test contracts must not break. Additions only.
