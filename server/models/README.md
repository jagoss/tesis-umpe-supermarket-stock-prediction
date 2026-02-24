# Model Artifacts Directory

This directory stores trained machine learning model artifacts that are deployed for inference by the prediction service.

## Purpose

Following Clean Architecture principles, this folder serves as the **storage location for model binaries**, while the actual inference logic (adapters implementing `ModelPort`) lives in `server/infrastructure/models/`.

```
server/
├── models/                          # ← Model artifacts (this directory)
│   ├── example_model.onnx          # Example ONNX model
│   ├── sklearn_model.joblib        # (optional) Sklearn model
│   └── torch_model.pt              # (optional) PyTorch model
│
└── infrastructure/
    └── models/                      # ← Model adapters (Python code)
        ├── onnx_model.py           # ONNXModel adapter
        ├── sklearn_model.py        # SklearnModel adapter
        └── torch_model.py          # TorchModel adapter
```

## Current Models

### `example_model.onnx`

A simple linear regression model trained on synthetic time series data for demonstration purposes.

**Model Specifications:**
- **Type:** Linear Regression (sklearn → ONNX)
- **Input:** `float32[1, 4]` tensor with features:
  - `[0]` horizon_step: Day ahead being predicted (1 to N)
  - `[1]` day_of_week: Day of week (0=Monday, 6=Sunday)
  - `[2]` month: Month of year (1-12)
  - `[3]` is_weekend: Binary flag (1.0 if Sat/Sun, 0.0 otherwise)
- **Output:** `float32[1, 1]` tensor representing predicted quantity
- **ONNX Opset:** 15

**Usage:**
```bash
export MODEL_BACKEND=onnx
python -m server.main
```

This model is intended as a **starting point**. Replace it with your actual trained model for production use.

## Deploying Your Own Model

### Option 1: ONNX Model (Recommended)

ONNX provides framework-agnostic model deployment with excellent performance.

#### Step 1: Train Your Model

Train your model using any framework (scikit-learn, PyTorch, TensorFlow, etc.):

```python
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Train your model
model = RandomForestRegressor(n_estimators=100)
X_train = ...  # Your training features
y_train = ...  # Your training targets
model.fit(X_train, y_train)
```

#### Step 2: Convert to ONNX

**From scikit-learn:**
```python
from skl2onnx import to_onnx

onnx_model = to_onnx(model, X_train[:1].astype(np.float32), target_opset=15)

with open("server/models/my_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

**From PyTorch:**
```python
import torch

# Export to ONNX
dummy_input = torch.randn(1, 4)
torch.onnx.export(
    model,
    dummy_input,
    "server/models/my_model.onnx",
    export_params=True,
    opset_version=15,
    input_names=["input"],
    output_names=["output"]
)
```

**From TensorFlow/Keras:**
```python
import tf2onnx
import onnx

spec = (tf.TensorSpec((None, 4), tf.float32, name="input"),)
model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec)

with open("server/models/my_model.onnx", "wb") as f:
    f.write(model_proto.SerializeToString())
```

#### Step 3: Update Configuration

Update `server/infrastructure/container.py` to point to your model:

```python
if backend == "onnx":
    return ONNXModel(model_path="server/models/my_model.onnx")
```

Or better yet, use environment variables (see Configuration section below).

#### Step 4: Adjust Feature Engineering

Update `ONNXModel._build_features()` in `server/infrastructure/models/onnx_model.py` to match your model's expected input features.

### Option 2: Scikit-learn Model

If you prefer using joblib-serialized scikit-learn models:

```python
import joblib

# Save your trained sklearn model
joblib.dump(model, "server/models/sklearn_model.joblib")
```

Set environment variable:
```bash
export MODEL_BACKEND=sklearn
```

### Option 3: PyTorch Model

For PyTorch models (TorchScript or state dict):

```python
import torch

# Save TorchScript
scripted_model = torch.jit.script(model)
torch.jit.save(scripted_model, "server/models/torch_model.pt")
```

Set environment variable:
```bash
export MODEL_BACKEND=torch
```

## Configuration

### Environment Variables

The service supports the following environment variables for model configuration:

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `MODEL_BACKEND` | `dummy`, `onnx`, `sklearn`, `torch` | `dummy` | Which model adapter to use |
| `MODEL_PATH` | File path | (varies by backend) | Path to model artifact (future enhancement) |
| `DEFAULT_PREDICTION_VALUE` | Float | `0` | Constant value for `dummy` backend |

**Example:**
```bash
# Use ONNX model
export MODEL_BACKEND=onnx

# Start the service
python -m server.main
```

### Making Model Path Configurable

For production deployments, consider making the model path configurable via environment variables.

Update `server/infrastructure/config.py`:
```python
@dataclass(slots=True)
class Settings:
    model_backend: str
    model_path: str  # Add this
    default_prediction_value: float

def load_settings() -> Settings:
    model_backend = os.getenv("MODEL_BACKEND", "dummy").strip().lower()
    model_path = os.getenv("MODEL_PATH", f"server/models/{model_backend}_model.onnx")
    default_prediction_value = float(os.getenv("DEFAULT_PREDICTION_VALUE", "0"))
    return Settings(
        model_backend=model_backend,
        model_path=model_path,
        default_prediction_value=default_prediction_value
    )
```

Then update `container.py` to use `settings.model_path` instead of hardcoded paths.

## Model Input/Output Contract

All models must adhere to the `ModelPort` protocol defined in `server/application/ports.py`:

```python
class ModelPort(Protocol):
    def predict(self, data: PreprocessedData) -> ModelRawPrediction:
        """Produce raw predictions from preprocessed features."""
```

### Input: `PreprocessedData`

```python
@dataclass
class PreprocessedData:
    product_id: str          # Product identifier
    store_id: str            # Store identifier
    start_date: date         # Start of prediction period
    end_date: date           # End of prediction period
    horizon: int             # Number of days to predict
    history: Optional[List[Tuple[date, float]]]  # Historical data (if available)
```

### Output: `ModelRawPrediction`

```python
@dataclass
class ModelRawPrediction:
    values: List[float]      # Predicted values (length = horizon)
```

**Important:** The model adapter is responsible for:
1. Feature engineering from `PreprocessedData` to model-specific format
2. Running inference
3. Converting model output to `List[float]` with length equal to `horizon`

## Best Practices

1. **Version Control:** Use Git LFS for large model files or store them externally (S3, Azure Blob, etc.)
2. **Model Metadata:** Consider adding a `model_info.json` with metadata:
   ```json
   {
     "model_name": "supermarket_stock_predictor_v1",
     "version": "1.0.0",
     "trained_date": "2024-12-16",
     "framework": "sklearn",
     "metrics": {
       "mae": 5.2,
       "rmse": 8.1
     },
     "features": ["horizon_step", "day_of_week", "month", "is_weekend"]
   }
   ```
3. **Testing:** Always test your model with the service before deploying to production
4. **Monitoring:** Track prediction latency and accuracy in production
5. **Rollback Plan:** Keep previous model versions for quick rollback if needed

## Troubleshooting

### Error: "ONNX model file not found"

- Ensure your `.onnx` file is present in `server/models/`
- Check that the path in `container.py` is correct
- Verify file permissions

### Error: "onnxruntime not installed"

Install ONNX Runtime:
```bash
pip install onnxruntime
```

For GPU support:
```bash
pip install onnxruntime-gpu
```

### Error: "Output shape mismatch"

Your model's output doesn't match the requested horizon. Check:
- Feature engineering in `_build_features()`
- Model expects batch input (shape `[N, features]` not `[features]`)
- Output tensor shape matches `(horizon, 1)` or `(horizon,)`

### Poor Prediction Quality

- Verify feature engineering matches your training pipeline
- Check data preprocessing (scaling, normalization)
- Ensure date features are calculated correctly
- Review model performance metrics from training

## References

- [ONNX Documentation](https://onnx.ai/)
- [ONNX Runtime Documentation](https://onnxruntime.ai/)
- [skl2onnx](https://github.com/onnx/sklearn-onnx)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

