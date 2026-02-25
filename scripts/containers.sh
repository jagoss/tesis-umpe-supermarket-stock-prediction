#!/usr/bin/env bash
# containers.sh — Create, start, and manage Docker Compose services
#
# Usage: bash scripts/containers.sh [COMMAND]
#
# Commands:
#   (none) | start   Create containers if they do not exist, then start them
#   stop             Stop all running containers (data is preserved)
#   restart          Stop then start all containers
#   status           Show the current state of every container
#   logs [service]   Stream logs (all services, or one specific service)
#   down             Stop and remove containers (volumes are preserved)
#   destroy          Stop and remove containers AND all volumes  ⚠ deletes DB data
#   help             Print this help message

set -euo pipefail

# ── Helpers ───────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
die()     { error "$*"; exit 1; }

# ── Resolve project root (parent of scripts/) ─────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# ── Preflight checks ─────────────────────────────────────────────────────────

check_docker() {
    if ! command -v docker &>/dev/null; then
        die "Docker is not installed or not in PATH. See https://docs.docker.com/get-docker/"
    fi

    if ! docker info &>/dev/null; then
        die "Docker daemon is not running. Start Docker Desktop (Windows/macOS) or 'sudo systemctl start docker' (Linux)."
    fi

    if ! docker compose version &>/dev/null; then
        die "Docker Compose plugin (v2) is not available. Update Docker Desktop or install the plugin."
    fi
}

check_env() {
    if [[ ! -f ".env" ]]; then
        warn ".env file not found."
        if [[ -f ".env.example" ]]; then
            echo ""
            echo -e "  Run the following to create it from the example:"
            echo -e "  ${BOLD}  cp .env.example .env${NC}"
            echo -e "  Then edit ${BOLD}.env${NC} and set POSTGRES_PASSWORD, ENCRYPTION_KEY_SECRET, and GEN_AI_API_KEY."
        fi
        echo ""
        die "Aborting. Create .env before starting the containers."
    fi
}

# ── Container helpers ─────────────────────────────────────────────────────────

# Returns 0 if at least one service container has been created (running or stopped)
containers_exist() {
    local count
    count=$(docker compose ps -a --quiet 2>/dev/null | wc -l)
    [[ "$count" -gt 0 ]]
}

# ── Commands ─────────────────────────────────────────────────────────────────

cmd_start() {
    check_docker
    check_env

    if containers_exist; then
        info "Containers already exist — starting any that are stopped..."
        docker compose start
    else
        info "No containers found — pulling images and creating containers..."
        docker compose up -d --pull missing
    fi

    echo ""
    success "All services started."
    echo ""
    cmd_status
    echo ""
    info "Prediction API : http://localhost:8000"
    info "API docs       : http://localhost:8000/docs"
    info "Onyx UI        : http://localhost:3000"
    info "MCP endpoint   : http://localhost:8000/mcp  (internal: http://prediction_server:8000/mcp)"
}

cmd_stop() {
    check_docker
    info "Stopping containers (data is preserved)..."
    docker compose stop
    success "Containers stopped."
}

cmd_restart() {
    check_docker
    check_env
    info "Restarting all containers..."
    docker compose stop
    docker compose start
    success "All containers restarted."
    echo ""
    cmd_status
}

cmd_status() {
    check_docker
    docker compose ps
}

cmd_logs() {
    check_docker
    local service="${1:-}"
    if [[ -n "$service" ]]; then
        info "Streaming logs for '${service}' (Ctrl+C to stop)..."
        docker compose logs -f "$service"
    else
        info "Streaming logs for all services (Ctrl+C to stop)..."
        docker compose logs -f
    fi
}

cmd_down() {
    check_docker
    warn "Removing containers (volumes are preserved — data is safe)..."
    docker compose down
    success "Containers removed."
}

cmd_destroy() {
    check_docker
    echo ""
    warn "This will remove ALL containers AND volumes, including the Postgres database."
    echo -n "  Type 'yes' to confirm: "
    read -r confirm
    if [[ "$confirm" != "yes" ]]; then
        info "Aborted."
        exit 0
    fi
    docker compose down -v
    success "Containers and volumes removed."
}

cmd_help() {
    grep '^#' "$0" | grep -v '#!/' | sed 's/^# \{0,1\}//'
}

# ── Entrypoint ────────────────────────────────────────────────────────────────

COMMAND="${1:-start}"
shift || true   # consume first arg so "$@" contains remaining args (e.g. service name for logs)

case "$COMMAND" in
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    restart) cmd_restart ;;
    status)  cmd_status ;;
    logs)    cmd_logs "${1:-}" ;;
    down)    cmd_down ;;
    destroy) cmd_destroy ;;
    help|-h|--help) cmd_help ;;
    *)
        error "Unknown command: '$COMMAND'"
        echo ""
        cmd_help
        exit 1
        ;;
esac
