# Project Completion Phases

> **Document Purpose:** Roadmap of remaining work to bring the
> *Supermarket Stock Prediction Server* from its current state to a
> production-ready system integrated with Onyx.
>
> **Last Updated:** 2026-02-23

---

## Current State Summary

### What Is Already Implemented

| Layer / Area | Status | Details |
|---|---|---|
| **Domain** | Complete | `StockForecastPoint`, `StockForecast` entities; `DomainError`, `ValidationError`, `PredictionError` exceptions |
| **Application** | Complete | `PredictStockUseCase`, DTOs (`PredictStockInput`, `PredictStockOutput`, `PredictionPoint`), Ports (`PreprocessorPort`, `ModelPort`, `PostprocessorPort`) |
| **Infrastructure – ONNX Model** | Complete | Lazy loading, 4-feature engineering (`horizon_step`, `day_of_week`, `month`, `is_weekend`), batch inference |
| **Infrastructure – Dummy Model** | Complete | Returns constant values; intended for testing and development |
| **Infrastructure – Sklearn Model** | Stub (to remove) | Placeholder; unnecessary since ONNX is the canonical serving format |
| **Infrastructure – Torch Model** | Stub (to remove) | Placeholder; unnecessary since ONNX is the canonical serving format |
| **Infrastructure – Preprocessing** | Complete (minimal) | Computes horizon and forwards identifiers; no advanced feature engineering |
| **Infrastructure – Postprocessing** | Complete | Maps raw floats to dated `PredictionPoint` objects with rounding |
| **Infrastructure – Config & DI** | Complete | Environment-based settings, DI container with backend selection, singleton |
| **Infrastructure – Logging** | Complete (basic) | `configure_logging` with structured format |
| **Interface – HTTP API** | Complete | FastAPI with `/health` (GET), `/predict` (POST), error mapping |
| **Interface – MCP** | Complete | `fastapi-mcp` mounts at `/mcp`; exposes `predict_stock` tool |
| **Tests** | Good coverage | 13 test files covering domain, DTOs, schemas, config, container, DummyModel, ONNXModel, preprocessor, postprocessor, use case, API, MCP |
| **Documentation** | Partial | Architecture doc, Onyx integration guide, PlantUML diagrams, models README, ONNX integration summary |
| **CI/CD** | Minimal | Claude Code action, PR restriction workflow, Claude code review; **no test/lint/deploy pipelines** |
| **Agent package** | Intentionally minimal | Docstring only; Onyx replaces the custom conversational agent |
| **Docker** | Missing | No Dockerfile, docker-compose, or .dockerignore |
| **Root README** | Missing | Referenced in `pyproject.toml` but does not exist |

### Known Issues in Current Code

1. **Domain entities are dead code** — `StockForecast` and `StockForecastPoint` are defined but never referenced by any other module.
2. **Sklearn and Torch adapters are unnecessary stubs** — ONNX is the canonical model serving format. Models trained in scikit-learn or PyTorch should be *exported to ONNX* (via `skl2onnx` / `torch.onnx.export`) and served through the existing `ONNXModel` adapter. The stub adapters add dead code and maintenance burden.
3. **`history` field is passed through but ignored** — all model adapters discard the optional history data.
4. **Dev/test dependencies are undeclared** — `pytest`, `httpx`, `black`, `ruff`, `mypy` are configured in `pyproject.toml` but not listed as dependencies.
5. **`joblib` inconsistency** — present in `requirements.txt` but missing from `pyproject.toml`.
6. **`ONNXModel._hash_string_to_int()` is dead code** — defined but never called.
7. **No production model artifact** — only a toy `example_model.onnx` (255 bytes) exists.

---

## Phase 1: Foundation & Code Quality Housekeeping

**Goal:** Fix inconsistencies, dead code, and missing project metadata to establish a clean baseline.

### Tasks

1. **Create Root `README.md`**
   - Project description, purpose, and thesis context.
   - Quick start guide (install, configure, run).
   - API documentation summary (endpoints, MCP tools).
   - Architecture overview referencing `.docs/`.
   - Links to Onyx integration guide.

2. **Declare Dev/Test Dependencies**
   - Add `[project.optional-dependencies]` section in `pyproject.toml` with `dev` extras:
     `pytest`, `pytest-cov`, `httpx`, `black`, `ruff`, `mypy`, `isort`.
   - Remove `joblib` and `torch` from dependencies (no longer needed — ONNX is the only serving format).

3. **Integrate Domain Entities or Remove Them**
   - Option A (recommended): Map `PredictStockOutput` -> `StockForecast` in the use case to properly separate domain from application DTOs.
   - Option B: Remove unused `StockForecastPoint` and `StockForecast` if the DTOs are deemed sufficient.

4. **Remove Unnecessary Model Adapters & Clean Up Dead Code**
   - Remove `sklearn_model.py` and `torch_model.py` (stubs). ONNX is the canonical serving
     format — models trained in any framework are exported to `.onnx` via `skl2onnx` or
     `torch.onnx.export` and served through the existing `ONNXModel` adapter.
   - Update `container.py` to remove sklearn/torch backend options (keep `onnx` and `dummy`).
   - Update `config.py` to remove sklearn/torch default paths.
   - Remove associated test files (if any) and update `test_container.py`.
   - Remove `ONNXModel._hash_string_to_int()` (unused helper method).
   - Remove `scikit-learn`, `skl2onnx`, `joblib` from runtime dependencies (only needed
     at *training* time, not serving time). Keep them in a `training` optional-dependency group.
   - Audit all modules for other unreferenced code.

5. **Synchronize `requirements.txt` with `pyproject.toml`**
   - Ensure both files declare the same dependencies.
   - Consider generating `requirements.txt` from `pyproject.toml` via `pip-compile` or similar.

### Acceptance Criteria

- [ ] Root `README.md` exists and is accurate.
- [ ] `pip install -e ".[dev]"` installs all development tools.
- [ ] `sklearn_model.py`, `torch_model.py`, and related dead code are removed.
- [ ] `container.py` only supports `onnx` and `dummy` backends.
- [ ] Domain entities are either properly used or removed.
- [ ] `requirements.txt` and `pyproject.toml` are in sync (runtime deps are minimal: FastAPI, ONNX Runtime, Pydantic, fastapi-mcp).
- [ ] No dead code remains (`ruff` or manual audit confirms).

---

## Phase 2: ML Training Pipeline & Production Model

**Goal:** Build the data processing and model training pipeline that produces a real ONNX model for supermarket stock forecasting.

### Tasks

1. **Data Collection & Preparation**
   - Define the data source (CSV, database, API) for historical supermarket sales data.
   - Create a data ingestion script or notebook.
   - Implement data cleaning, validation, and exploratory data analysis (EDA).
   - Define train/validation/test split strategy (e.g., time-based split for time series).

2. **Feature Engineering Pipeline**
   - Define the feature set for stock prediction (product metadata, temporal features, lag features, rolling statistics, etc.).
   - Ensure the feature set aligns with the server's `PreprocessorPort` / `ONNXModel` contract.
   - Document the feature schema (input format, expected ranges, encoding).

3. **Model Training**
   - Select and train a forecasting model (e.g., gradient boosting with scikit-learn, or any framework that exports to ONNX).
   - Implement hyperparameter tuning and cross-validation.
   - Track experiments (consider MLflow, Weights & Biases, or a simple log).

4. **Model Export to ONNX**
   - Export the trained model to `.onnx` using the appropriate converter (`skl2onnx`, `torch.onnx.export`, `tf2onnx`, etc.).
   - Validate the exported ONNX model with `onnx.checker.check_model()`.
   - Generate `model_info.json` metadata (version, training date, metrics, feature schema).
   - Place the production model in `server/models/`.

5. **Model Validation**
   - Create a validation script that loads the exported ONNX model via the server's `ONNXModel` adapter and verifies predictions against a test set.
   - Define minimum accuracy/quality thresholds.

6. **History Data Integration**
   - Update `ONNXModel` (or the preprocessor) to actually use the optional `history` field from `PreprocessedData`.
   - Ensure the HTTP schema's `HistoryPoint` data flows through to model inference.

### Acceptance Criteria

- [ ] A reproducible training pipeline exists (script or notebook).
- [ ] At least one production-quality `.onnx` model artifact is generated.
- [ ] Model evaluation metrics are documented (MAE, RMSE, or equivalent).
- [ ] The `history` field is integrated into predictions when provided.
- [ ] `model_info.json` metadata accompanies the model artifact.

---

## Phase 3: CI/CD Pipeline & Automated Quality Gates

**Goal:** Automate testing, linting, and quality checks on every push/PR.

### Tasks

1. **Create CI Workflow (`.github/workflows/ci.yml`)**
   - Trigger on push to `develop` and on pull requests.
   - Steps:
     - Install Python 3.11+.
     - Install dependencies (`pip install -e ".[dev]"`).
     - Run linting: `ruff check .`, `black --check .`, `isort --check .`.
     - Run type checking: `mypy server/`.
     - Run tests: `pytest --cov=server --cov-report=xml`.
     - Upload coverage report (e.g., Codecov or GitHub Actions artifact).

2. **Add Pre-commit Hooks (optional but recommended)**
   - Create `.pre-commit-config.yaml` with `ruff`, `black`, `isort`, `mypy`.
   - Document in README how to install hooks.

3. **Verify Current Tests Pass**
   - Run the full test suite locally and fix any failures.
   - Ensure all tests run in CI without requiring model files or external services.

4. **Add Missing Tests**
   - `test_logging.py`: test `configure_logging` function.
   - `test_main.py`: test `run()` function (mock `uvicorn.run`).
   - Enhance `test_mcp.py`: test actual MCP tool listing and invocation.
   - Integration test: full request lifecycle through the API with the dummy backend.

### Acceptance Criteria

- [ ] CI workflow runs on every PR and push to `develop`.
- [ ] Linting (`ruff`, `black`, `isort`), type checking (`mypy`), and tests (`pytest`) all pass.
- [ ] Code coverage is tracked and reported.
- [ ] No test depends on external services or production model files.

---

## Phase 4: Containerization & Deployment

**Goal:** Package the prediction server for reproducible deployment and set up the Onyx integration environment.

### Tasks

1. **Create `Dockerfile`**
   - Multi-stage build: builder (install deps) + runtime (slim image).
   - Copy only necessary files (server/, models/, pyproject.toml).
   - Set `CMD` to run `uvicorn server.interface.http.api:app`.
   - Add health check instruction.
   - Configure for production (no reload, appropriate workers).

2. **Create `.dockerignore`**
   - Exclude `.git`, `__pycache__`, `.docs`, `agent/`, `tests/`, notebooks, etc.

3. **Create `docker-compose.yml`**
   - Service: `prediction-server` (build from Dockerfile).
   - Environment variables: `MODEL_BACKEND`, `MODEL_PATH`, `DEFAULT_PREDICTION_VALUE`.
   - Port mapping: `8000:8000`.
   - Volume mount for model artifacts.
   - Optional: Onyx service (if self-hosted) with MCP server URL configured.

4. **Create Deployment Workflow (`.github/workflows/deploy.yml`)**
   - Trigger on push to `main` (after PR merge).
   - Build Docker image.
   - Push to container registry (GitHub Container Registry, Docker Hub, or cloud provider).
   - Optionally deploy to target environment (cloud VM, Kubernetes, etc.).

5. **Environment Configuration**
   - Document all environment variables and their defaults.
   - Create `.env.example` file.
   - Ensure `config.py` handles production settings (disable debug, set proper log levels).

### Acceptance Criteria

- [ ] `docker build -t prediction-server .` produces a working image.
- [ ] `docker-compose up` starts the server and it passes `/health` check.
- [ ] Model artifacts can be mounted as a volume (not baked into the image).
- [ ] `.env.example` documents all configuration options.
- [ ] Deploy workflow pushes image to a container registry.

---

## Phase 5: Onyx Integration & End-to-End Validation

**Goal:** Complete the integration with Onyx as the conversational AI frontend, validated end-to-end.

### Tasks

1. **Onyx Instance Setup**
   - Deploy or access an Onyx instance (self-hosted or cloud).
   - Document the Onyx version and configuration used.

2. **Register MCP Server in Onyx**
   - Follow the steps in `onyx_integration.md`:
     - Admin Panel → Actions → "From MCP server".
     - URL: `http://<prediction-server-host>:8000/mcp`.
     - Verify `predict_stock` tool appears.

3. **Create Onyx Agent/Persona**
   - Configure the supermarket inventory assistant persona.
   - Set up the system prompt (as documented in `onyx_integration.md`).
   - Enable the `predict_stock` tool.

4. **End-to-End Testing**
   - Test conversational flow: user asks in natural language → Onyx calls MCP → server returns prediction → Onyx presents results.
   - Test edge cases: invalid product IDs, date ranges in the past, very long horizons.
   - Test error handling: server down, invalid responses, timeouts.
   - Document test scenarios and results.

5. **Network & Security Configuration**
   - Ensure Onyx can reach the prediction server (firewall rules, DNS, etc.).
   - Consider adding API key authentication to the prediction server if exposed beyond the local network.
   - Add CORS configuration if needed.

6. **Update Documentation**
   - Update `onyx_integration.md` with any changes discovered during actual setup.
   - Add screenshots or logs of successful integration.
   - Document troubleshooting steps encountered.

### Acceptance Criteria

- [ ] Onyx lists `predict_stock` as an available tool.
- [ ] A natural-language conversation produces a correct stock prediction.
- [ ] Error scenarios are handled gracefully (meaningful error messages to the user).
- [ ] Network/security configuration is documented and applied.

---

## Phase 6: Hardening & Production Readiness

**Goal:** Prepare the system for production use with observability, security, and resilience.

### Tasks

1. **Observability & Monitoring**
   - Add structured logging (JSON format) for production.
   - Expose Prometheus metrics endpoint (request count, latency, error rate, model inference time).
   - Create Grafana dashboard or alerting rules (optional, depends on infrastructure).
   - Add request tracing (correlation IDs).

2. **Security Hardening**
   - Add API key authentication to the prediction server (middleware or dependency injection).
   - Rate limiting for the `/predict` endpoint.
   - Input validation hardening (max horizon length, allowed product/store ID patterns).
   - Dependency vulnerability scanning (`pip-audit` or `safety` in CI).

3. **Performance & Resilience**
   - Load testing: verify the server handles expected concurrent request volume.
   - Configure Uvicorn workers for production (multi-process or use Gunicorn as process manager).
   - Add request timeout middleware.
   - Consider model warm-up on startup (currently the singleton loads lazily).

4. **Advanced Preprocessing (optional)**
   - Enhance `BasicPreprocessor` with feature scaling/normalization if the production model requires it.
   - Add support for additional input features (promotions, holidays, weather, etc.).

5. **Model Versioning & A/B Testing (optional)**
   - Support loading multiple model versions simultaneously.
   - Add model version to the prediction response.
   - Enable A/B testing between model versions.

### Acceptance Criteria

- [ ] Structured logs are emitted in production mode.
- [ ] Prometheus metrics are available at `/metrics`.
- [ ] API key authentication is enforced.
- [ ] The server handles at least N concurrent requests without degradation (define N based on requirements).
- [ ] Dependency vulnerabilities are scanned in CI.

---

## Phase Summary & Recommended Priority

| Phase | Priority | Effort Estimate | Dependencies |
|---|---|---|---|
| **Phase 1:** Foundation & Housekeeping | High | Small (1–2 days) | None |
| **Phase 2:** ML Training Pipeline | High | Large (1–2 weeks) | Phase 1 |
| **Phase 3:** CI/CD Pipeline | High | Small (1–2 days) | Phase 1 |
| **Phase 4:** Containerization & Deployment | High | Medium (2–3 days) | Phase 3 |
| **Phase 5:** Onyx Integration & E2E | High | Medium (2–3 days) | Phase 4 |
| **Phase 6:** Hardening & Production Readiness | Medium | Medium (3–5 days) | Phase 5 |

### Recommended Execution Order

```
             ┌──► Phase 2 (ML Pipeline) ──┐
Phase 1 ─────┤                             ├──► Phase 4 ──► Phase 5 ──► Phase 6
             └──► Phase 3 (CI/CD) ─────────┘
```

**Phase 1** is the prerequisite for everything — it cleans up dead code (including the unnecessary sklearn/torch adapters) and establishes the project baseline.

**Phases 2 and 3** can run in parallel after Phase 1: Phase 2 builds the training pipeline and production model, while Phase 3 sets up automated quality gates.

**Phase 4** (Docker) depends on both having CI working and a production model available.

**Phase 5** (Onyx) depends on having a deployable server.

**Phase 6** (hardening) is the final layer before production launch.

---

## Architectural Decision: ONNX as the Single Serving Format

The original codebase included stub adapters for scikit-learn (`sklearn_model.py`) and
PyTorch (`torch_model.py`). These are removed in Phase 1 because **ONNX is the canonical
model serving format**:

- **ONNX Runtime** is optimized for production inference (faster, lower memory, hardware acceleration).
- Models trained in *any* framework (scikit-learn, PyTorch, TensorFlow, XGBoost, etc.)
  can be exported to `.onnx` using standard converters (`skl2onnx`, `torch.onnx.export`, `tf2onnx`).
- Maintaining a single inference adapter eliminates feature-engineering divergence, reduces
  test surface, and simplifies the DI container.
- Training-time dependencies (`scikit-learn`, `skl2onnx`, `torch`) belong in the training
  pipeline (Phase 2), not in the serving application.

This follows the principle: **train anywhere, serve with ONNX**.
