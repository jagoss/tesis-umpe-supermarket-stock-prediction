# Container Management Guide

> Supermarket Stock Prediction Server + Self-Hosted Onyx

---

## Prerequisites

| Requirement | Minimum version | Check |
|---|---|---|
| Docker Engine | 24+ | `docker --version` |
| Docker Compose plugin | v2 | `docker compose version` |
| Free RAM | 12 GB | — |
| Free disk | 32 GB | — |

> **Windows users:** Docker Desktop with WSL 2 backend is recommended.

---

## First-Time Setup

1. **Copy the example environment file and fill in your values:**

   ```bash
   cp .env.example .env
   ```

   Open `.env` and set at minimum:

   | Variable | What to change |
   |---|---|
   | `POSTGRES_PASSWORD` | Any strong password |
   | `ENCRYPTION_KEY_SECRET` | Run `python -c "import secrets; print(secrets.token_hex(32))"` |
   | `GEN_AI_API_KEY` | Your OpenAI / Anthropic / etc. key |
   | `GEN_AI_MODEL_PROVIDER` | `openai`, `anthropic`, `ollama`, … |
   | `GEN_AI_MODEL_VERSION` | e.g. `gpt-4o-mini` |

2. **Run the management script — it creates and starts everything automatically:**

   ```bash
   # Linux / macOS / WSL
   bash scripts/containers.sh

   # Windows CMD / PowerShell
   scripts\containers.bat
   ```

   On first run the script will:
   - Verify Docker is running.
   - Verify `.env` exists (it aborts with instructions if it does not).
   - Pull all required images.
   - Create and start all containers.

---

## Services & Ports

| Service | URL | Description |
|---|---|---|
| **Prediction Server** | http://localhost:8000 | FastAPI prediction API |
| **Prediction API docs** | http://localhost:8000/docs | OpenAPI / Swagger UI |
| **MCP endpoint** | http://localhost:8000/mcp | Used by Onyx internally |
| **Onyx UI** | http://localhost:3000 | Onyx conversational frontend |
| **Onyx API** | http://localhost:8080 | Onyx backend (internal) |

---

## Management Script Reference

Both `scripts/containers.sh` and `scripts/containers.bat` accept the same subcommands:

```
containers [COMMAND]
```

| Command | Action |
|---|---|
| *(no argument)* | Create containers if they do not exist, then start them |
| `start` | Same as above |
| `stop` | Stop all running containers (preserves data) |
| `restart` | Stop then start all containers |
| `status` | Show the current state of every container |
| `logs [service]` | Stream logs (all services, or a specific one) |
| `down` | Stop and **remove** containers (volumes are preserved) |
| `destroy` | Stop and remove containers **and all volumes** (⚠ deletes DB data) |
| `help` | Print usage |

### Examples

```bash
# Start everything (safe to run repeatedly)
bash scripts/containers.sh

# Check what is running
bash scripts/containers.sh status

# Stream logs for all services
bash scripts/containers.sh logs

# Stream logs for the prediction server only
bash scripts/containers.sh logs prediction_server

# Stop everything without losing data
bash scripts/containers.sh stop

# Restart after changing .env
bash scripts/containers.sh restart

# Remove containers (keeps database volume)
bash scripts/containers.sh down

# Full teardown — WARNING: deletes the Postgres volume
bash scripts/containers.sh destroy
```

---

## Registering the MCP Server in Onyx

After `docker compose up` completes and all services are healthy:

1. Open the Onyx UI at **http://localhost:3000**.
2. Sign in (or skip if `AUTH_TYPE=disabled`).
3. Go to **Admin Panel → Tools → Add Tool → From MCP server**.
4. Enter the internal URL:
   ```
   http://prediction_server:8000/mcp
   ```
5. Onyx will discover the `predict_stock` tool automatically.
6. Create or edit an **Assistant**, enable the `predict_stock` tool, and set your system prompt.

---

## Swapping the Production Model

The model file is **volume-mounted** — no image rebuild is needed:

```bash
# 1. Place your new model file on the host
cp /path/to/new_model.onnx ./server/models/production_model.onnx

# 2. Update MODEL_PATH in .env
#    MODEL_PATH=server/models/production_model.onnx

# 3. Restart only the prediction server
docker compose restart prediction_server
```

---

## Updating Onyx

```bash
# Pull the latest images and recreate affected containers
docker compose pull
bash scripts/containers.sh restart
```

To pin to a specific Onyx version, set `ONYX_VERSION=v0.x.y` in `.env` before pulling.

---

## Troubleshooting

### Containers exit immediately after start

Check the logs for the failing service:

```bash
bash scripts/containers.sh logs api_server
bash scripts/containers.sh logs prediction_server
```

Common causes:
- `.env` is missing or has an empty `ENCRYPTION_KEY_SECRET` / `POSTGRES_PASSWORD`.
- A port is already in use — change the host port mapping in `docker-compose.yml`.

### `prediction_server` cannot connect to the model file

Verify that `MODEL_ARTIFACTS_PATH` in `.env` points to a directory that exists on the host and contains the expected `.onnx` file.

### Onyx UI is blank or shows a connection error

The `web_server` depends on `api_server`, which depends on `relational_db`. Wait ~60 seconds on first start for migrations to complete, then refresh.

### Reset everything and start fresh

```bash
bash scripts/containers.sh destroy
bash scripts/containers.sh start
```
