# Data Serving Architecture for Production ONNX Model

> **Document Purpose:** Technical design for Phase 2's data-serving layer —
> how the production ONNX model gets access to pre-computed historical features
> at inference time.
>
> **Last Updated:** 2026-03-17

---

## Context

Phase 2 (ML Training Pipeline & Production Model) requires the production ONNX
model to have access to historical data for feature computation. The current toy
model uses only 4 temporal features (`horizon_step, day_of_week, month,
is_weekend`), but the real model (LightGBM via MLForecast, as prototyped in the
notebook) needs lag features (1/7/14/28/90/365 days), rolling means (7/28/365
day windows), promotions, holidays, store metadata, and LocalStandardScaler
inverse transforms.

The Kaggle data is **static** (2013-2017 Ecuador supermarket data, ~125 MB
total). The MCP request stays simple — the server handles all data lookup
internally.

**Scope:** Data serving architecture only. Model training and ONNX export are
handled separately.

---

## Approach: Pre-computed Features in Parquet

### Why this approach

| Approach | Rejected because |
|---|---|
| A: Raw CSVs in memory, compute at request time | Computing lag/rolling features from 3M rows per request is too slow; requires re-running entire MLForecast pipeline |
| B: PostgreSQL | Over-engineering for static data; computing 365-day rolling means in SQL is painful; adds ORM/migration complexity |
| D: Hybrid | No benefit when data never changes |

**Pre-computed Parquet works because:**
- Data is static — pre-compute once, load always
- An offline script runs the same MLForecast pipeline from the notebook,
  producing a Parquet file with all features pre-computed
- At inference time, the preprocessor does an O(1) lookup by
  `(store_nbr, family, date)`
- ~50-100 MB Parquet file fits easily in memory
- Cleanly fits the existing port/adapter pattern

### Future date strategy: pre-computed + buffer

Pre-compute features for the **training window + a 30-90 day forecast buffer**
beyond the training data end date. For dates within the buffer, features are
looked up normally. For dates beyond the buffer, the server returns a clear
`DataNotFoundError` with a message indicating the available date range.

**This is designed for iteration:** When recursive multi-step prediction is
needed later, the same `DataRepositoryPort` interface stays unchanged. The
`ProductionPreprocessor` gets extended to fall back to recursive feature
generation when a date isn't found, instead of raising an error.

---

## Data Flow

```
MCP Request: {product_id: "BEVERAGES", store_id: "1", start: "2017-08-01", end: "2017-08-16"}
  │
  ▼
ProductionPreprocessor.preprocess()
  │── For each date in range: data_repo.get_feature_vector("1", "BEVERAGES", date)
  │── Assembles feature matrix (16 rows × N_features)
  │── Returns PreprocessedData(features=[[...], ...])
  │
  ▼
ONNXModel.predict()
  │── Uses preprocessed.features as numpy input (instead of building toy features)
  │── Runs ONNX session.run()
  │── Returns ModelRawPrediction(values=[scaled_pred_1, ..., scaled_pred_16])
  │
  ▼
ProductionPostprocessor.postprocess()
  │── Gets (mean, std) scaler params from data_repo for this series
  │── Inverse transforms: pred * std + mean
  │── Clips to >= 0
  │── Returns StockForecast
```

---

## New Port: `DataRepositoryPort`

Added to `server/application/ports.py`:

```python
class DataRepositoryPort(Protocol):
    def get_feature_vector(self, store_id: str, product_id: str, target_date: date) -> list[float] | None: ...
    def get_feature_names(self) -> list[str]: ...
    def get_scaler_params(self, store_id: str, product_id: str) -> tuple[float, float] | None: ...
    def get_available_date_range(self) -> tuple[date, date]: ...
```

---

## Files Created

| File | Purpose |
|---|---|
| `server/infrastructure/data/__init__.py` | New package |
| `server/infrastructure/data/parquet_repository.py` | `ParquetDataRepository` — loads Parquet at init, indexes by (store, family, date) for O(1) lookup |
| `server/infrastructure/preprocessing/production_preprocessor.py` | Looks up features from `DataRepositoryPort`, assembles feature matrix, raises `DataNotFoundError` for out-of-range dates |
| `server/infrastructure/postprocessing/production_postprocessor.py` | Inverse-scales predictions using scaler params from `DataRepositoryPort`, clips to >= 0 |
| `scripts/precompute_features.py` | Offline script: loads CSVs, runs feature pipeline, saves features Parquet + scaler params Parquet. Includes forecast buffer. |
| `server/tests/test_parquet_repository.py` | Unit tests with small fixture Parquet |
| `server/tests/test_production_preprocessor.py` | Unit tests (mock DataRepositoryPort) |
| `server/tests/test_production_postprocessor.py` | Unit tests (mock DataRepositoryPort) |

## Files Modified

| File | Change |
|---|---|
| `server/application/ports.py` | Added `DataRepositoryPort` protocol; added `features: list[list[float]] \| None` field to `PreprocessedData` |
| `server/application/__init__.py` | Export `DataRepositoryPort` |
| `server/domain/exceptions.py` | Added `DataNotFoundError(DomainError)` |
| `server/domain/__init__.py` | Export `DataNotFoundError` |
| `server/infrastructure/config.py` | Added `preprocessor_backend`, `data_path`, `scaler_path` settings + env vars |
| `server/infrastructure/container.py` | Wire `ParquetDataRepository` (singleton), select production vs basic preprocessor/postprocessor |
| `server/infrastructure/models/onnx_model.py` | Use `data.features` when available; fallback to current toy-feature logic for backwards compat |
| `server/infrastructure/preprocessing/__init__.py` | Export `ProductionPreprocessor` |
| `server/infrastructure/postprocessing/__init__.py` | Export `ProductionPostprocessor` |
| `requirements.txt` / `pyproject.toml` | Added `pandas>=2.0,<3.0`, `pyarrow>=14.0,<19.0` |
| `Dockerfile` | COPY `data/*.parquet` into image; added env vars |
| `docker-compose.yml` | Mount data volume, added `PREPROCESSOR_BACKEND` / `DATA_PATH` / `SCALER_PATH` env vars |
| `.env.example` | Documented new env vars |

---

## Container Wiring

```python
def build_predict_use_case() -> PredictStockUseCase:
    settings = load_settings()
    model = _select_model(settings)

    if settings.preprocessor_backend == "production":
        data_repo = ParquetDataRepository(settings.data_path, settings.scaler_path)
        pre = ProductionPreprocessor(data_repo)
        post = ProductionPostprocessor(data_repo)
    else:
        pre = BasicPreprocessor()
        post = BasicPostprocessor()

    return PredictStockUseCase(preprocessor=pre, model=model, postprocessor=post)
```

---

## Implementation Sequence

1. **Ports & domain** — `DataRepositoryPort` in `ports.py`, `features` field in `PreprocessedData`, `DataNotFoundError` in `exceptions.py`
2. **ParquetDataRepository** — loads Parquet, builds index, O(1) lookup + tests
3. **ProductionPreprocessor** — calls data_repo for each date, assembles feature matrix + tests
4. **ProductionPostprocessor** — inverse LocalStandardScaler, clip >= 0 + tests
5. **Precompute script** — `scripts/precompute_features.py` (loads CSVs, builds features, saves Parquet)
6. **Wiring** — Update `config.py`, `container.py`, `ONNXModel.predict()` to use `data.features`
7. **Deployment** — Update `Dockerfile`, `docker-compose.yml`, `.env.example`
8. **Backwards compatibility check** — `PREPROCESSOR_BACKEND=basic` still works with toy model

---

## Verification

1. `scripts/precompute_features.py` produces valid Parquet files from CSVs
2. `pytest server/tests/` — all existing + new tests pass
3. Start server with `PREPROCESSOR_BACKEND=production`, `DATA_PATH=data/precomputed_features.parquet`
4. `POST /predict` with valid (store_nbr, family, date range within buffer) returns predictions
5. `POST /predict` with date range beyond buffer returns clear error with available range
6. MCP tool via Onyx returns predictions for a valid request
7. `PREPROCESSOR_BACKEND=basic` still works (backwards compatibility with toy model)

---

## Pre-computed Feature Columns

The feature matrix produced by `scripts/precompute_features.py` contains:

| Category | Features |
|---|---|
| Calendar | `day_of_week`, `month`, `day_of_month`, `is_weekend`, `week_of_year` |
| Promotions | `onpromotion` |
| External | `oil_price` |
| Holidays | `is_holiday` (national holidays only) |
| Store metadata | `store_city_enc`, `store_state_enc`, `store_type_enc`, `cluster` |
| Lag features | `lag_1`, `lag_7`, `lag_14`, `lag_28`, `lag_90`, `lag_365` |
| Rolling means | `rolling_mean_7`, `rolling_mean_28`, `rolling_mean_365` |

All lag/rolling features are computed on **scaled** sales (after
LocalStandardScaler) to match what MLForecast produces during training.
