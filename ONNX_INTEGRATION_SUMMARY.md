# ONNX Model Integration - Implementation Summary

## Overview

Successfully integrated ONNX Runtime support into the supermarket stock prediction service following Clean Architecture and DDD principles.

## What Was Implemented

### 1. Dependencies Added ✓

**Files Modified:**

- `requirements.txt`
- `pyproject.toml`

**New Dependencies:**

- `onnxruntime>=1.18,<2.0` - For ONNX model inference
- `fastapi-mcp>=0.2.0` - For exposing FastAPI endpoints as MCP tools
- `mcp>=1.8.0,<1.26.0` - MCP protocol library (pinned to avoid breaking changes in 1.26.0)
- `scikit-learn>=1.4,<2.0` - For example model generation (training extra)
- `skl2onnx>=1.16,<2.0` - For sklearn to ONNX conversion (training extra)

### 2. Example ONNX Model Created ✓

**File:** `server/models/example_model.onnx`

A simple linear regression model trained on synthetic time series data:

- **Input:** `float32[1, 4]` - [horizon_step, day_of_week, month, is_weekend]
- **Output:** `float32[1, 1]` - predicted quantity
- **Purpose:** Demonstration and testing; ready to be replaced with production models

### 3. ONNX Model Adapter Implemented ✓

**File:** `server/infrastructure/models/onnx_model.py`

**Class:** `ONNXModel` implementing `ModelPort` protocol

**Key Features:**

- Lazy loading of ONNX Runtime session
- Feature engineering from `PreprocessedData` to model input format
- Temporal feature extraction (day of week, month, weekend flag)
- Comprehensive error handling with `PredictionError`
- Batch inference support for multi-step horizons
- Input/output shape validation

**Architecture Compliance:**

- ✓ Implements `ModelPort` (Dependency Inversion Principle)
- ✓ Single Responsibility (only handles ONNX inference)
- ✓ Clean error messages and documentation
- ✓ Implements `ModelPort` alongside `DummyModel`

### 4. Dependency Injection Updated ✓

**File:** `server/infrastructure/container.py`

**Changes:**

- Imported `ONNXModel` adapter
- Added `"onnx"` case to `_select_model()` function
- Integrated with configurable model path from settings

### 5. Configuration Enhanced ✓

**File:** `server/infrastructure/config.py`

**New Features:**

- Added `model_path` field to `Settings` dataclass
- Implemented `_get_default_model_path()` helper function
- Support for `MODEL_PATH` environment variable
- Automatic defaults based on `MODEL_BACKEND` selection

**Configuration Options:**

```bash
# Use ONNX with default path
export MODEL_BACKEND=onnx

# Use ONNX with custom model path
export MODEL_BACKEND=onnx
export MODEL_PATH=/path/to/custom_model.onnx
```

### 6. Documentation Created ✓

**File:** `server/models/README.md`

Comprehensive documentation covering:

- Purpose of the `server/models/` directory
- Model deployment instructions for ONNX, sklearn, and PyTorch
- Step-by-step guide for converting models to ONNX from various frameworks
- Configuration options and environment variables
- Model input/output contract specifications
- Best practices for model versioning and deployment
- Troubleshooting guide
- References and links to external resources

## Architecture Diagram

```txt
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ModelPort (Protocol)                                 │   │
│  │  + predict(PreprocessedData) -> ModelRawPrediction  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ implements
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │ DummyModel   │  │ ONNXModel    │                       │
│  └──────────────┘  └──────────────┘                       │
│                            │                                 │
│                            ▼                                 │
│                    ┌──────────────┐                         │
│                    │ ONNX Runtime │                         │
│                    └──────────────┘                         │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         server/models/example_model.onnx            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Principles Applied

### Clean Architecture ✓

- **Domain Layer:** Untouched (business rules remain pure)
- **Application Layer:** `ModelPort` defines the contract
- **Infrastructure Layer:** `ONNXModel` implements the port
- **Dependency Rule:** Infrastructure depends on abstractions, not vice versa

### Domain-Driven Design ✓

- **Ubiquitous Language:** Uses domain terms (`PreprocessedData`, `ModelRawPrediction`)
- **Bounded Context:** ML inference isolated in infrastructure
- **Anti-Corruption Layer:** Adapter translates between ONNX Runtime API and domain

### Clean Code ✓

- **Single Responsibility:** Each class has one reason to change
- **Dependency Inversion:** Depends on `ModelPort` abstraction
- **Meaningful Names:** Clear, intention-revealing identifiers
- **Error Handling:** Explicit exceptions with helpful messages
- **Documentation:** Comprehensive docstrings and comments

## Usage

### Basic Usage with Default ONNX Model

```bash
# Set environment variable
export MODEL_BACKEND=onnx

# Start the service
python -m server.main
```

### Using Custom ONNX Model

```bash
# Set both backend and custom path
export MODEL_BACKEND=onnx
export MODEL_PATH=/path/to/your/model.onnx

# Start the service
python -m server.main
```

### API Request Example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD123",
    "store_id": "STORE456",
    "start_date": "2024-12-17",
    "end_date": "2024-12-31",
    "horizon": 14
  }'
```

## Files Created/Modified

| File | Status | Purpose |
|------|--------|---------|
| `requirements.txt` | Modified | Added ONNX Runtime, fastapi-mcp, and mcp dependencies |
| `pyproject.toml` | Modified | Added dependencies to project config (including mcp<1.26.0 pin) |
| `server/models/example_model.onnx` | Created | Example ONNX model artifact |
| `server/models/README.md` | Created | Comprehensive model deployment documentation |
| `server/infrastructure/models/onnx_model.py` | Created | ONNX adapter implementing ModelPort |
| `server/infrastructure/container.py` | Modified | Added ONNX backend support |
| `server/infrastructure/config.py` | Modified | Added model_path configuration |

## Testing Recommendations

1. **Unit Tests** (Future):

   ```python
   def test_onnx_model_predict():
       model = ONNXModel(model_path="server/models/example_model.onnx")
       data = PreprocessedData(
           product_id="TEST",
           store_id="STORE1",
           start_date=date(2024, 12, 17),
           end_date=date(2024, 12, 31),
           horizon=14
       )
       result = model.predict(data)
       assert len(result.values) == 14
       assert all(isinstance(v, float) for v in result.values)
   ```

2. **Integration Tests** (Future):
   - Test end-to-end prediction flow with ONNX backend
   - Verify API responses with different horizon values
   - Test error handling for missing model files

3. **Manual Testing**:

   ```bash
   # Test with dummy backend (baseline)
   MODEL_BACKEND=dummy python -m server.main
   
   # Test with ONNX backend
   MODEL_BACKEND=onnx python -m server.main
   ```

## Next Steps

1. **Replace Example Model**: Train and deploy your actual production model
2. **Adjust Feature Engineering**: Update `ONNXModel._build_features()` to match your model's training features
3. **Add Tests**: Implement unit and integration tests for the ONNX adapter
4. **Monitor Performance**: Track inference latency and prediction accuracy
5. **Version Control**: Consider using Git LFS for model artifacts or external storage (S3, Azure Blob)
6. **CI/CD Integration**: Automate model deployment pipeline

## Notes

- The example model is intentionally simple for demonstration purposes
- Feature engineering in `_build_features()` should be customized based on your actual model's training data
- ONNX Runtime provides excellent cross-platform performance without framework dependencies
- ONNX is the canonical serving format; models from any framework are exported to `.onnx`

## References

- [ONNX Documentation](https://onnx.ai/)
- [ONNX Runtime](https://onnxruntime.ai/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- Project Documentation: `server/models/README.md`
