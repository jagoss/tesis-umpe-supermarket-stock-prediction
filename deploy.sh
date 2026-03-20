#!/usr/bin/env bash
# deploy.sh — Script de despliegue productivo del stack de predicción de demanda.
#
# Uso:
#   bash scripts/deploy.sh [start|stop|restart|status|logs|health]
#
# Requiere:
#   - Docker Engine 24+ y Docker Compose v2
#   - Archivo .env configurado (ver .env.example)
#   - Artefactos de modelo: server/models/lightgbm_model.onnx
#   - Artefactos de datos: data/precomputed_features.parquet, data/scaler_params.parquet

set -euo pipefail

COMPOSE_FILES="-f docker-compose.yml -f docker-compose.prod.yml"
PROJECT_NAME="prediction-stack"

# ── Colores ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── Verificaciones previas ──
preflight_check() {
    log_info "Ejecutando verificaciones previas..."

    # Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker no está instalado."
        exit 1
    fi

    # Docker Compose
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose v2 no está disponible."
        exit 1
    fi

    # .env
    if [ ! -f .env ]; then
        log_error "Archivo .env no encontrado. Copiar desde .env.example:"
        log_error "  cp .env.example .env"
        exit 1
    fi

    # Artefactos del modelo
    if [ ! -f server/models/lightgbm_model.onnx ]; then
        log_warn "Artefacto ONNX no encontrado. El servidor usará MODEL_BACKEND=dummy si no se configura."
    fi

    if [ ! -f data/precomputed_features.parquet ]; then
        log_warn "Artefacto de features precomputadas no encontrado."
    fi

    log_info "Verificaciones completadas."
}

# ── Comandos ──
cmd_start() {
    preflight_check
    log_info "Iniciando stack productivo..."
    docker compose $COMPOSE_FILES -p $PROJECT_NAME up -d --build
    log_info "Stack iniciado. Ejecutando health check..."
    sleep 10
    cmd_health
}

cmd_stop() {
    log_info "Deteniendo stack..."
    docker compose $COMPOSE_FILES -p $PROJECT_NAME down
    log_info "Stack detenido."
}

cmd_restart() {
    log_info "Reiniciando stack..."
    cmd_stop
    cmd_start
}

cmd_status() {
    log_info "Estado de los servicios:"
    docker compose $COMPOSE_FILES -p $PROJECT_NAME ps
}

cmd_logs() {
    local service="${2:-}"
    if [ -n "$service" ]; then
        docker compose $COMPOSE_FILES -p $PROJECT_NAME logs -f --tail=100 "$service"
    else
        docker compose $COMPOSE_FILES -p $PROJECT_NAME logs -f --tail=50
    fi
}

cmd_health() {
    log_info "Verificando salud del servidor de predicción..."

    local max_retries=5
    local retry=0

    while [ $retry -lt $max_retries ]; do
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_info "Prediction server: ${GREEN}OK${NC}"

            # Verificar predicción básica
            local response
            response=$(curl -sf -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d '{"store_id":"1","product_id":"BEVERAGES","start_date":"2026-03-20","end_date":"2026-03-22"}' \
                2>/dev/null) || true

            if [ -n "$response" ]; then
                log_info "Predicción de prueba: ${GREEN}OK${NC}"
            else
                log_warn "Predicción de prueba: sin respuesta (puede requerir API key)."
            fi
            return 0
        fi

        retry=$((retry + 1))
        log_warn "Intento $retry/$max_retries - servidor no disponible aún. Esperando 5s..."
        sleep 15
    done

    log_error "El servidor de predicción no respondió después de $max_retries intentos."
    return 1
}

# ── Main ──
case "${1:-help}" in
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    restart) cmd_restart ;;
    status)  cmd_status ;;
    logs)    cmd_logs "$@" ;;
    health)  cmd_health ;;
    *)
        echo "Uso: $0 {start|stop|restart|status|logs [servicio]|health}"
        echo ""
        echo "Comandos:"
        echo "  start    Inicia el stack productivo completo"
        echo "  stop     Detiene todos los servicios"
        echo "  restart  Reinicia el stack completo"
        echo "  status   Muestra el estado de los servicios"
        echo "  logs     Muestra logs (opcional: nombre del servicio)"
        echo "  health   Verifica salud del servidor de predicción"
        exit 1
        ;;
esac
