#!/usr/bin/env bash
# e2e_validate.sh — End-to-end validation against the live Docker stack
#
# Usage: bash scripts/e2e_validate.sh [BASE_URL]
#
# Runs a suite of checks against the prediction server and reports pass/fail
# for each. Exits with code 0 if all checks pass, 1 otherwise.
#
# Arguments:
#   BASE_URL   Base URL of the prediction server (default: http://localhost:8000)

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────

BASE_URL="${1:-http://localhost:8000}"
PASSED=0
FAILED=0
TOTAL=0

# ── Helpers ───────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

pass() {
    PASSED=$((PASSED + 1))
    TOTAL=$((TOTAL + 1))
    echo -e "  ${GREEN}PASS${NC}  $1"
}

fail() {
    FAILED=$((FAILED + 1))
    TOTAL=$((TOTAL + 1))
    echo -e "  ${RED}FAIL${NC}  $1"
    if [[ -n "${2:-}" ]]; then
        echo -e "        ${RED}$2${NC}"
    fi
}

section() {
    echo ""
    echo -e "${CYAN}── $1 ──${NC}"
}

# ── Checks ────────────────────────────────────────────────────────────────

section "Health Check"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health" 2>/dev/null || echo "000")
if [[ "$HTTP_CODE" == "200" ]]; then
    pass "GET /health returns 200"
else
    fail "GET /health returns 200" "Got HTTP $HTTP_CODE"
fi

HEALTH_BODY=$(curl -s "${BASE_URL}/health" 2>/dev/null || echo "")
if echo "$HEALTH_BODY" | grep -q '"status"'; then
    pass "Health response contains 'status' field"
else
    fail "Health response contains 'status' field" "Body: $HEALTH_BODY"
fi

# ──────────────────────────────────────────────────────────────────────────

section "Valid Prediction (Happy Path)"

PREDICT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "product_id": "PROD-001",
        "store_id": "STORE-A",
        "start_date": "2026-03-02",
        "end_date": "2026-03-04"
    }' 2>/dev/null || echo -e "\n000")

PREDICT_BODY=$(echo "$PREDICT_RESPONSE" | head -n -1)
PREDICT_CODE=$(echo "$PREDICT_RESPONSE" | tail -n 1)

if [[ "$PREDICT_CODE" == "200" ]]; then
    pass "POST /predict returns 200 for valid payload"
else
    fail "POST /predict returns 200 for valid payload" "Got HTTP $PREDICT_CODE"
fi

if echo "$PREDICT_BODY" | grep -q '"predictions"'; then
    pass "Response contains 'predictions' array"
else
    fail "Response contains 'predictions' array" "Body: $PREDICT_BODY"
fi

if echo "$PREDICT_BODY" | grep -q '"product_id"'; then
    pass "Response echoes product_id"
else
    fail "Response echoes product_id" "Body: $PREDICT_BODY"
fi

# ──────────────────────────────────────────────────────────────────────────

section "Prediction with History"

HIST_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "product_id": "PROD-001",
        "store_id": "STORE-A",
        "start_date": "2026-03-02",
        "end_date": "2026-03-04",
        "history": [
            {"date": "2026-02-28", "quantity": 100},
            {"date": "2026-03-01", "quantity": 120}
        ]
    }' 2>/dev/null || echo "000")

if [[ "$HIST_CODE" == "200" ]]; then
    pass "POST /predict with history returns 200"
else
    fail "POST /predict with history returns 200" "Got HTTP $HIST_CODE"
fi

# ──────────────────────────────────────────────────────────────────────────

section "MCP Endpoint"

MCP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/mcp" 2>/dev/null || echo "000")
if [[ "$MCP_CODE" != "000" ]]; then
    pass "MCP endpoint responds (HTTP $MCP_CODE)"
else
    fail "MCP endpoint responds" "Connection refused or timeout"
fi

# ──────────────────────────────────────────────────────────────────────────

section "OpenAPI Schema"

SCHEMA=$(curl -s "${BASE_URL}/openapi.json" 2>/dev/null || echo "")

if echo "$SCHEMA" | grep -q "predict_stock"; then
    pass "OpenAPI schema contains 'predict_stock' operation"
else
    fail "OpenAPI schema contains 'predict_stock' operation"
fi

if echo "$SCHEMA" | grep -q "check_health"; then
    pass "OpenAPI schema contains 'check_health' operation"
else
    fail "OpenAPI schema contains 'check_health' operation"
fi

# ──────────────────────────────────────────────────────────────────────────

section "Error Handling — Missing Required Field"

ERR_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{"store_id": "STORE-A", "start_date": "2026-03-02", "end_date": "2026-03-04"}' \
    2>/dev/null || echo "000")

if [[ "$ERR_CODE" == "422" ]]; then
    pass "Missing product_id returns 422"
else
    fail "Missing product_id returns 422" "Got HTTP $ERR_CODE"
fi

# ──────────────────────────────────────────────────────────────────────────

section "Error Handling — Inverted Date Range"

INV_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "product_id": "PROD-001",
        "store_id": "STORE-A",
        "start_date": "2026-03-10",
        "end_date": "2026-03-02"
    }' 2>/dev/null || echo "000")

if [[ "$INV_CODE" == "400" ]]; then
    pass "Inverted date range returns 400"
else
    fail "Inverted date range returns 400" "Got HTTP $INV_CODE"
fi

# ──────────────────────────────────────────────────────────────────────────

section "Long Horizon (30 days)"

LONG_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "product_id": "PROD-001",
        "store_id": "STORE-A",
        "start_date": "2026-03-01",
        "end_date": "2026-03-30"
    }' 2>/dev/null || echo "000")

if [[ "$LONG_CODE" == "200" ]]; then
    pass "30-day prediction returns 200"
else
    fail "30-day prediction returns 200" "Got HTTP $LONG_CODE"
fi

# ──────────────────────────────────────────────────────────────────────────

section "CORS Headers"

CORS_HEADERS=$(curl -s -I -X OPTIONS "${BASE_URL}/health" \
    -H "Origin: http://localhost:3000" \
    -H "Access-Control-Request-Method: GET" 2>/dev/null || echo "")

if echo "$CORS_HEADERS" | grep -qi "access-control-allow-origin"; then
    pass "CORS access-control-allow-origin header present"
else
    fail "CORS access-control-allow-origin header present"
fi

# ── Summary ───────────────────────────────────────────────────────────────

echo ""
echo -e "${BOLD}══════════════════════════════════════${NC}"
echo -e "${BOLD}  Results: ${GREEN}${PASSED} passed${NC}, ${RED}${FAILED} failed${NC} ${BOLD}/ ${TOTAL} total${NC}"
echo -e "${BOLD}══════════════════════════════════════${NC}"
echo ""

if [[ "$FAILED" -gt 0 ]]; then
    echo -e "${RED}Some checks failed.${NC} See details above."
    exit 1
else
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
fi
