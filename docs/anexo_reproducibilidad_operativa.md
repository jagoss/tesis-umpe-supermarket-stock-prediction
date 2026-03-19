# Anexo técnico: reejecución y validación operativa

## Objetivo

Este anexo resume los prerequisitos mínimos y los comandos de referencia para reinstalar el entorno, levantar el servicio y ejecutar las validaciones técnicas documentadas en el repositorio. Su propósito es complementar la sección [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md) con una guía operativa breve y trazable.

## 1. Prerequisitos mínimos

### 1.1 Entorno Python

- `Python >= 3.11`
- Instalación editable del proyecto:

```bash
pip install -e .
pip install -e ".[dev]"
```

- Dependencias relevantes observables en [pyproject.toml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/pyproject.toml):
  - runtime: `fastapi`, `uvicorn`, `onnxruntime`, `fastapi-mcp`, `mcp`, `pandas`, `pyarrow`
  - desarrollo: `pytest`, `pytest-cov`, `pytest-anyio`, `httpx`, `asgi-lifespan`
  - entrenamiento: `scikit-learn`, `skl2onnx`, `onnx`

### 1.2 Entorno Docker

Para el stack completo documentado en el repositorio:

- `Docker Engine 24+`
- `Docker Compose v2`
- memoria libre recomendada: `12 GB`
- disco libre recomendado: `32 GB`

Fuente: [containers.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.docs/containers.md).

## 2. Configuración mínima

### 2.1 Archivo `.env`

Crear el archivo a partir de [.env.example](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.env.example):

```bash
cp .env.example .env
```

Variables mínimas observables para levantar el stack:

- `POSTGRES_PASSWORD`
- `ENCRYPTION_KEY_SECRET`
- `GEN_AI_MODEL_PROVIDER`
- `GEN_AI_MODEL_VERSION`
- `GEN_AI_API_KEY` o configuración alternativa posterior en Onyx
- `MODEL_BACKEND`
- `MODEL_PATH`
- `PREPROCESSOR_BACKEND`
- `DATA_PATH`
- `SCALER_PATH`

### 2.2 Modos de operación del servidor

Modo liviano para validación funcional:

```bash
MODEL_BACKEND=dummy python -m server.main
```

Modo productivo documentado:

```bash
MODEL_BACKEND=onnx \
PREPROCESSOR_BACKEND=production \
DATA_PATH=data/precomputed_features.parquet \
SCALER_PATH=data/scaler_params.parquet \
python -m server.main
```

Observación: la presente auditoría no reejecutó este segundo modo en el workspace actual.

## 3. Comandos de validación técnica

### 3.1 Suite de pruebas

Comando declarado en CI:

```bash
pytest server/tests/ -v --tb=short --cov=server --cov-report=xml --cov-report=term-missing
```

Estado en esta auditoría:

- `python3 -m pytest --version` falla porque `pytest` no está instalado en este entorno local.
- Por tanto, este anexo documenta el procedimiento, pero no agrega una nueva corrida local como evidencia.

### 3.2 Smoke test del contenedor

Procedimiento equivalente al workflow [container-smoke-test.yml](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/.github/workflows/container-smoke-test.yml):

```bash
docker build -t prediction-server:test .

docker run -d \
  --name prediction_server_test \
  -p 8000:8000 \
  -e MODEL_BACKEND=dummy \
  -e DEFAULT_PREDICTION_VALUE=10 \
  prediction-server:test

curl http://localhost:8000/health
curl http://localhost:8000/docs
curl http://localhost:8000/openapi.json
```

### 3.3 Validación E2E del servidor

Script disponible:

```bash
bash scripts/e2e_validate.sh
```

Chequeos principales documentados:

- `GET /health`
- `POST /predict` válido
- `POST /predict` con `history`
- respuesta del endpoint `/mcp`
- presencia de operaciones en `/openapi.json`
- manejo de errores `400` y `422`
- horizonte largo
- cabeceras CORS

## 4. Comandos de operación del stack Docker

Script de referencia:

```bash
bash scripts/containers.sh start
bash scripts/containers.sh status
bash scripts/containers.sh logs prediction_server
bash scripts/containers.sh stop
```

Servicios principales esperados:

- `prediction_server`
- `api_server`
- `web_server`
- `background`
- `model_server`
- `index`
- `relational_db`
- `cache`
- `app_web`

## 5. Límites conocidos

- No hay lockfile estricto con versiones exactas para todas las dependencias.
- La validación continua fuerte se apoya en `MODEL_BACKEND=dummy`, no en una corrida productiva completa.
- La integración total con Onyx requiere recursos de hardware significativamente mayores que una corrida local simple.
- En este workspace no fue posible reejecutar `pytest` por ausencia de la dependencia.

## 6. Uso recomendado dentro de la tesis

Este anexo puede citarse como respaldo operativo de:

- la sección [validacion_reproducibilidad.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/validacion_reproducibilidad.md)
- la sección [arquitectura_implementacion.md](/mnt/c/Users/juana/PycharmProjects/tesis-umpe-supermarket-stock-prediction/docs/arquitectura_implementacion.md)

No debe utilizarse como evidencia de calidad predictiva del modelo, sino como evidencia de reproducibilidad operativa y de procedimientos de validación técnica.
