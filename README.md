# Supermarket Stock Prediction

Sistema de predicción de demanda para supermercados desarrollado como proyecto de tesis en UMPE.

Expone una **REST API** y un endpoint **MCP** que permite integrar predicciones de stock en asistentes de IA (como [Onyx](https://onyx.app)). Los modelos se entrenan en cualquier framework (scikit-learn, PyTorch, TensorFlow) y se sirven mediante **ONNX Runtime**.

```
Usuario → Onyx (chat + LLM) → MCP → Servidor de predicción (/predict) → Modelo ONNX
```

---

## Ejecutar localmente con Docker

### Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) o Docker Engine + Compose v2 (Linux)
- Al menos **4 vCPU, 10 GB RAM, 32 GB de disco** (por los servicios de Onyx)

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd tesis-umpe-supermarket-stock-prediction

# 2. Configurar variables de entorno
cp .env.example .env
```

Editar `.env` y completar los valores obligatorios:

| Variable | Descripción |
|---|---|
| `ENCRYPTION_KEY_SECRET` | Exactamente 32 caracteres. Generar con: `python -c "import secrets; print(secrets.token_urlsafe(24))"` |
| `GEN_AI_API_KEY` | Clave de API del proveedor LLM (OpenAI, Anthropic, etc.) |
| `POSTGRES_PASSWORD` | Contraseña para la base de datos |

```bash
# 3. Levantar todos los servicios
docker compose up -d

# 4. Verificar que todo esté corriendo
docker compose ps
curl http://localhost:8000/health    # {"status": "ok"}
```

### URLs disponibles

| Servicio | URL |
|---|---|
| API de predicción | `http://localhost:8000` |
| Onyx (chat UI) | `http://localhost:3000` |
| App web (demo) | `http://localhost:3003` |
| Endpoint MCP | `http://localhost:8000/mcp` |

### Detener

```bash
docker compose down        # detener contenedores
docker compose down -v     # detener y eliminar volúmenes (reset completo)
```

> **Nota:** Para usar el backend `dummy` (sin modelo ONNX), establecer `MODEL_BACKEND=dummy` en `.env`.

---

## API

### `GET /health`

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

### `POST /predict`

Predice la demanda de un producto en una tienda para un rango de fechas.

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-001",
    "store_id": "STORE-A",
    "start_date": "2026-03-02",
    "end_date": "2026-03-04"
  }'
```

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

Opcionalmente se puede incluir historial de ventas reciente en el campo `history` para mejorar la precisión.

---

## Arquitectura

El proyecto sigue **Clean Architecture** con cuatro capas:

```
server/
├── domain/            # Entidades, value objects, excepciones de dominio
├── application/       # Casos de uso, DTOs, puertos (interfaces)
├── infrastructure/    # Adaptadores: modelo ONNX, preprocesador, config, DI
└── interface/         # API HTTP (FastAPI), integración MCP, schemas Pydantic
```

Pipeline de predicción:

```
PredictStockInput → Preprocesador → Modelo ONNX → Postprocesador → PredictStockOutput
```

---

## Desarrollo

### Instalación local (sin Docker)

```bash
pip install -e ".[dev]"
python -m server.main          # servidor en http://127.0.0.1:8000
```

### Tests y linting

```bash
pytest
ruff check . && black --check . && mypy server/ --strict
```

### Pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

## Licencia

Proyecto de tesis — UMPE.
