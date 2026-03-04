# Validación End-to-End (E2E)

## Resumen

Este documento describe los escenarios de prueba para validar la integración completa
entre el servidor de predicción y Onyx. Incluye pruebas automatizadas (script) y
pruebas manuales (checklist para demostración de tesis).

> **Script automatizado:** `scripts/e2e_validate.sh` (Linux/macOS/Git Bash) o
> `scripts/e2e_validate.bat` (Windows CMD).

---

## Prerrequisitos

1. El stack Docker debe estar corriendo: `bash scripts/containers.sh`
2. El prediction server debe pasar el health check: `curl http://localhost:8000/health`
3. Para pruebas con Onyx: la interfaz web debe estar accesible en `http://localhost:3000`

---

## Escenarios de Prueba Automatizados

Estos escenarios son ejecutados por `scripts/e2e_validate.sh`:

### 1. Health Check

**Objetivo:** Verificar que el servidor de predicción está corriendo y responde.

```bash
curl -s http://localhost:8000/health
```

**Resultado esperado:** `{"status":"ok"}` con HTTP 200.

### 2. Predicción Válida (Happy Path)

**Objetivo:** Verificar que una predicción con parámetros válidos retorna resultados.

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-001",
    "store_id": "STORE-A",
    "start_date": "2026-03-02",
    "end_date": "2026-03-04"
  }'
```

**Resultado esperado:**
- HTTP 200
- Respuesta JSON con `product_id`, `store_id`, y array `predictions`
- Cada predicción tiene `date` y `quantity`
- Número de predicciones = días en el rango (3 días)

### 3. Predicción con Datos Históricos

**Objetivo:** Verificar que el campo `history` es aceptado sin errores.

```bash
curl -s -X POST http://localhost:8000/predict \
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
  }'
```

**Resultado esperado:** HTTP 200 con predicciones válidas.

### 4. Endpoint MCP Responde

**Objetivo:** Verificar que el endpoint MCP está activo y sirve contenido.

```bash
curl -s http://localhost:8000/mcp
```

**Resultado esperado:** HTTP 200 (o 405 si solo acepta POST — lo importante es que responda).

### 5. OpenAPI Schema Contiene `predict_stock`

**Objetivo:** Verificar que la operación `predict_stock` está registrada en el schema.

```bash
curl -s http://localhost:8000/openapi.json | grep -q "predict_stock"
```

**Resultado esperado:** La cadena `predict_stock` aparece en el schema OpenAPI.

### 6. Payload Inválido — Producto Faltante

**Objetivo:** Verificar que se retorna un error claro cuando faltan campos requeridos.

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"store_id": "STORE-A", "start_date": "2026-03-02", "end_date": "2026-03-04"}'
```

**Resultado esperado:** HTTP 422 con detalle del campo faltante (`product_id`).

### 7. Rango de Fechas Invertido

**Objetivo:** Verificar manejo de `start_date` posterior a `end_date`.

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-001",
    "store_id": "STORE-A",
    "start_date": "2026-03-10",
    "end_date": "2026-03-02"
  }'
```

**Resultado esperado:** HTTP 400 con mensaje de error de validación.

### 8. Horizonte Largo (30 días)

**Objetivo:** Verificar que el servidor maneja un rango de predicción extenso.

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-001",
    "store_id": "STORE-A",
    "start_date": "2026-03-01",
    "end_date": "2026-03-30"
  }'
```

**Resultado esperado:** HTTP 200 con 30 predicciones.

### 9. CORS Headers Presentes

**Objetivo:** Verificar que los headers CORS están en las respuestas.

```bash
curl -s -I -X OPTIONS http://localhost:8000/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

**Resultado esperado:** Header `access-control-allow-origin` presente en la respuesta.

---

## Escenarios de Prueba Manuales (Onyx)

Estos escenarios requieren interacción con la interfaz de Onyx.

### M1. Happy Path — Conversación Natural

**Pasos:**
1. Abrir http://localhost:3000
2. Seleccionar el agente "Asistente de Inventario"
3. Escribir: *"¿Cuántas unidades del producto PROD-001 debería pedir la tienda STORE-A para la primera semana de marzo 2026?"*

**Resultado esperado:**
- Onyx identifica que debe usar `predict_stock`
- Extrae los parámetros de la pregunta
- Ejecuta la herramienta MCP
- Presenta los resultados en formato legible (tabla o lista con cantidades por día)

### M2. Pregunta Ambigua

**Pasos:**
1. Escribir: *"Necesito saber cuánto pedir"*

**Resultado esperado:**
- El agente solicita los parámetros faltantes (producto, tienda, fechas)
- No intenta ejecutar `predict_stock` sin los datos necesarios

### M3. Producto Inválido

**Pasos:**
1. Escribir: *"Predice el stock del producto XYZ-INVALID en la tienda STORE-A del 1 al 5 de marzo 2026"*

**Resultado esperado:**
- El servidor procesa la solicitud (los IDs son aceptados como strings libres)
- Las predicciones se generan normalmente (el modelo no valida IDs contra una base de datos)

### M4. Error del Servidor

**Pasos:**
1. Detener el prediction server: `docker compose stop prediction_server`
2. Preguntar al agente: *"Predice el stock de PROD-001 en STORE-A para marzo 2026"*

**Resultado esperado:**
- Onyx muestra un mensaje de error indicando que no pudo conectar con la herramienta
- No falla silenciosamente

**Cleanup:** `docker compose start prediction_server`

### M5. Conversación Multi-turno

**Pasos:**
1. Pedir predicción para PROD-001, STORE-A, 1-7 marzo 2026
2. Después preguntar: *"¿Y para la segunda semana?"*
3. Después: *"¿Y para la tienda STORE-B?"*

**Resultado esperado:**
- El agente mantiene contexto entre turnos
- Reutiliza parámetros de turnos anteriores cuando tiene sentido
- Ejecuta nuevas predicciones con los parámetros actualizados

---

## Checklist para Demostración de Tesis

Use este checklist durante la presentación o defensa de tesis:

### Preparación (antes de la demo)

- [ ] Stack Docker corriendo: `bash scripts/containers.sh status`
- [ ] Script E2E pasando: `bash scripts/e2e_validate.sh`
- [ ] Onyx UI accesible: http://localhost:3000
- [ ] Swagger docs accesible: http://localhost:8000/docs
- [ ] Agente "Asistente de Inventario" creado y configurado en Onyx
- [ ] `predict_stock` visible en la lista de herramientas del agente

### Demo en vivo

- [ ] Mostrar arquitectura: docker compose ps (todos los servicios corriendo)
- [ ] Mostrar API docs: abrir Swagger y ejecutar predicción desde la interfaz
- [ ] Mostrar MCP: endpoint /mcp responde
- [ ] Demo conversacional: pregunta natural → Onyx llama predict_stock → respuesta
- [ ] Demo multi-turno: pregunta de seguimiento mantiene contexto
- [ ] Demo de error: mostrar manejo cuando faltan parámetros

### Post-demo

- [ ] Logs disponibles: `bash scripts/containers.sh logs prediction_server`
- [ ] Detener servicios: `bash scripts/containers.sh stop`
