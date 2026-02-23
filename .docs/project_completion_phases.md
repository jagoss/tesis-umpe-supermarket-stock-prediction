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
| **Infrastructure – Sklearn Model** | Stub | Placeholder feature construction (`[[i] for i in range(horizon)]`); reloads model on every call; explicit `TODO` |
| **Infrastructure – Torch Model** | Stub | Returns zeros; never loads or uses the model file; explicit `TODO` |
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
2. **`sklearn_model.py` feature construction is a placeholder** — does not match the 4-feature format used by the ONNX adapter.
3. **`torch_model.py` is entirely non-functional** — returns zeros without loading any model.
4. **`history` field is passed through but ignored** — all model adapters discard the optional history data.
5. **Dev/test dependencies are undeclared** — `pytest`, `httpx`, `black`, `ruff`, `mypy` are configured in `pyproject.toml` but not listed as dependencies.
6. **`joblib` inconsistency** — present in `requirements.txt` but missing from `pyproject.toml`.
7. **`ONNXModel._hash_string_to_int()` is dead code** — defined but never called.
8. **No production model artifact** — only a toy `example_model.onnx` (255 bytes) exists.

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
   - Add `joblib` to `pyproject.toml` main dependencies (currently only in `requirements.txt`).
   - Add `torch` as an optional dependency group (e.g., `[project.optional-dependencies] torch`).

3. **Integrate Domain Entities or Remove Them**
   - Option A (recommended): Map `PredictStockOutput` -> `StockForecast` in the use case to properly separate domain from application DTOs.
   - Option B: Remove unused `StockForecastPoint` and `StockForecast` if the DTOs are deemed sufficient.

4. **Clean Up Dead Code**
   - Remove `ONNXModel._hash_string_to_int()` (unused helper method).
   - Audit all modules for other unreferenced code.

5. **Synchronize `requirements.txt` with `pyproject.toml`**
   - Ensure both files declare the same dependencies.
   - Consider generating `requirements.txt` from `pyproject.toml` via `pip-compile` or similar.

### Acceptance Criteria

- [ ] Root `README.md` exists and is accurate.
- [ ] `pip install -e ".[dev]"` installs all development tools.
- [ ] No dead code remains (`ruff` or manual audit confirms).
- [ ] Domain entities are either properly used or removed.
- [ ] `requirements.txt` and `pyproject.toml` are in sync.

---

## Phase 2: Complete Model Adapter Implementations

**Goal:** Make `SklearnModel` and `TorchModel` adapters fully functional and consistent with `ONNXModel`.

### Tasks

1. **Implement `SklearnModel` Adapter**
   - Add lazy model loading (load once, cache in memory) matching the ONNX adapter pattern.
   - Implement proper feature engineering: build the same 4-feature vector (`horizon_step`, `day_of_week`, `month`, `is_weekend`) used by the ONNX adapter, or define a consistent feature contract across adapters.
   - Validate model file existence at initialization.
   - Add proper error handling (`PredictionError` wrapping, import checks).
   - Remove `# pragma: no cover - stub` markers.

2. **Implement `TorchModel` Adapter**
   - Implement actual model loading (`torch.load()` or `torch.jit.load()`).
   - Implement inference with proper tensor construction.
   - Support device selection (CPU/CUDA).
   - Add lazy loading, path validation, and error handling.
   - Remove `# pragma: no cover - stub` markers.

3. **Standardize Feature Engineering Across Adapters**
   - Extract shared feature-building logic into a common utility or move it into the preprocessor.
   - Consider making `BasicPreprocessor` responsible for building the feature matrix so model adapters receive ready-to-use input.

4. **Write Tests for New Adapters**
   - `test_sklearn_model.py`: loading, predict happy path, missing model file, feature shape validation.
   - `test_torch_model.py`: loading, predict happy path, missing model file, device selection.
   - Update `test_container.py` to cover sklearn and torch backend selection.

5. **Create Example Model Artifacts**
   - Generate a small `example_sklearn_model.joblib` for testing.
   - Generate a small `example_torch_model.pt` for testing.
   - Update `server/models/README.md` if needed.

### Acceptance Criteria

- [ ] `MODEL_BACKEND=sklearn` loads a real model and produces valid predictions.
- [ ] `MODEL_BACKEND=torch` loads a real model and produces valid predictions.
- [ ] All adapters share a consistent feature contract.
- [ ] Test coverage for all model adapters reaches >90%.
- [ ] Example models exist for all three backends.

---

## Phase 3: ML Training Pipeline & Production Model

**Goal:** Build the data processing and model training pipeline that produces a real predictive model for supermarket stock forecasting.

### Tasks

1. **Data Collection & Preparation**
   - Define the data source (CSV, database, API) for historical supermarket sales data.
   - Create a data ingestion script or notebook.
   - Implement data cleaning, validation, and exploratory data analysis (EDA).
   - Define train/validation/test split strategy (e.g., time-based split for time series).

2. **Feature Engineering Pipeline**
   - Define the feature set for stock prediction (product metadata, temporal features, lag features, rolling statistics, etc.).
   - Ensure the feature set aligns with the server's `PreprocessorPort` contract.
   - Document the feature schema (input format, expected ranges, encoding).

3. **Model Training**
   - Select and train a forecasting model (e.g., gradient boosting, LSTM, or time series model).
   - Implement hyperparameter tuning and cross-validation.
   - Track experiments (consider MLflow, Weights & Biases, or a simple log).

4. **Model Export**
   - Export the trained model to ONNX format (primary backend).
   - Optionally export to sklearn joblib and/or PyTorch formats.
   - Generate `model_info.json` metadata (version, training date, metrics, feature schema).

5. **Model Validation**
   - Create a validation script that loads the exported model via the server's adapter and verifies predictions against a test set.
   - Define minimum accuracy/quality thresholds.

6. **History Data Integration**
   - Update model adapters (or the preprocessor) to actually use the optional `history` field from `PreprocessedData`.
   - Ensure the HTTP schema's `HistoryPoint` data flows through to model inference.

### Acceptance Criteria

- [ ] A reproducible training pipeline exists (script or notebook).
- [ ] At least one production-quality model artifact is generated.
- [ ] Model evaluation metrics are documented (MAE, RMSE, or equivalent).
- [ ] The `history` field is integrated into predictions when provided.
- [ ] `model_info.json` metadata accompanies every model artifact.

---

## Phase 4: CI/CD Pipeline & Automated Quality Gates

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

## Phase 5: Containerization & Deployment

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

## Phase 6: Onyx Integration & End-to-End Validation

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

## Phase 7: Hardening & Production Readiness

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
| **Phase 2:** Model Adapters Completion | Medium | Medium (2–3 days) | Phase 1 |
| **Phase 3:** ML Training Pipeline | High | Large (1–2 weeks) | Phase 2 |
| **Phase 4:** CI/CD Pipeline | High | Small (1–2 days) | Phase 1 |
| **Phase 5:** Containerization & Deployment | High | Medium (2–3 days) | Phase 4 |
| **Phase 6:** Onyx Integration & E2E | High | Medium (2–3 days) | Phase 5 |
| **Phase 7:** Hardening & Production Readiness | Medium | Medium (3–5 days) | Phase 6 |

### Recommended Execution Order

```
Phase 1 ──► Phase 4 ──► Phase 2 ──► Phase 3
                │                      │
                ▼                      ▼
             Phase 5 ◄─────────── Phase 3
                │
                ▼
             Phase 6
                │
                ▼
             Phase 7
```

**Phases 1 and 4** can be done in parallel and should be tackled first — they establish the quality baseline and automation that everything else builds on.

**Phase 2** (model adapters) and **Phase 3** (training pipeline) can partially overlap: the adapter work defines the interface that the training pipeline must produce models for.

**Phase 5** (Docker) depends on having CI working, and **Phase 6** (Onyx) depends on having a deployable server.

**Phase 7** (hardening) is the final layer before production launch.
