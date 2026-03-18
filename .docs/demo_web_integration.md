# Demo Web Page — Integración del Chat UI Custom

## Descripción

Página web estática con branding UMPE que embebe un chat UI custom (HTML + CSS + vanilla JS)
que llama directamente a la API REST de Onyx. Servida por nginx en Docker como un
servicio adicional del stack (`demo_web`).

El chat UI reemplaza el antiguo `<onyx-chat-widget>` del CDN por una interfaz completamente
controlada que permite visualizar tool calls y renderizar resultados de predicción
(tablas + gráficos SVG inline).

## Arquitectura

```
[Browser] → :80 nginx (demo_web)
               ├── index.html  (landing con branding + chat UI markup)
               └── assets/
                     ├── style.css   (estilos BEM del chat)
                     ├── chat.js     (lógica de chat, SSE parsing, SVG charts)
                     └── logo.png    (logo UMPE)

[chat.js fetch()] → :80/api → nginx proxy → :8080 (Onyx api_server)
                                                ↕ MCP
                                             :8000 (Prediction Server)
```

Sin dependencia de CDN externo. Todo el código del chat corre en el navegador.

## Endpoints de la API de Onyx utilizados

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/chat/create-chat-session` | Crea sesión de chat → `{chat_session_id}` |
| POST | `/api/chat/send-message` | Envía mensaje → SSE stream |

Autenticación: header `Authorization: Bearer <api_key>`.

### Eventos SSE de `/api/chat/send-message`

| Campo | Descripción |
|-------|-------------|
| `answer_piece` | Fragmento de texto del LLM (streaming token a token) |
| `tool_name` | Nombre de la tool que Onyx está ejecutando |
| `tool_result` | JSON con el resultado de la tool (e.g. predicciones) |
| `message_id` | ID del mensaje asistente (usado como `parent_message_id` en el siguiente turno) |
| `error` | Mensaje de error del servidor |

## Configurar la API Key

1. Acceder al panel de administración de Onyx en `http://localhost:3000`.
2. Ir a **Settings → API Keys**.
3. Crear una nueva API key de tipo **Limited** (solo permisos de chat).
4. Copiar la key generada.
5. Agregarla en `.env`:
   ```env
   ONYX_WIDGET_API_KEY=onyx_...
   ```

La API key se inyecta en runtime mediante `envsubst` en el Dockerfile:
- `index.html` se copia como `index.html.template` con el placeholder `${ONYX_WIDGET_API_KEY}`
- Al arrancar el contenedor, `envsubst` reemplaza el placeholder y genera el `index.html` final
- El valor queda en un `<meta name="onyx-api-key">` que `chat.js` lee al inicializar

## Build y ejecución

```bash
# Levantar solo la demo (requiere que el resto del stack esté corriendo)
docker compose up -d demo_web

# Rebuild después de cambios en los archivos estáticos
docker compose build demo_web && docker compose up -d demo_web
```

Abrir `http://localhost:3003` en el navegador.

## Verificar el reemplazo de la API key

```bash
curl http://localhost:3003/ | grep onyx-api-key
# → <meta name="onyx-api-key" content="onyx_...">
# El placeholder ${ONYX_WIDGET_API_KEY} NO debe aparecer en la respuesta.
```

## Personalización

### Colores

Editar las CSS custom properties en `demo/assets/style.css`:

```css
:root {
    --color-primary: #4F46E5;   /* Color principal (header, burbujas usuario, botón enviar) */
    --color-bg: #F9FAFB;        /* Fondo de la página */
    --color-surface: #FFFFFF;    /* Fondo del chat */
}
```

### Logo

Reemplazar `demo/assets/logo.png` con el logo real de UMPE. Tamaño recomendado:
altura de 96px (se muestra a 48px para soporte retina).

### Visualización de predicciones

Cuando Onyx llama a la tool `predict_stock` (o cualquier tool), `chat.js` recibe el evento
`tool_result` y llama a `renderPredictionResult()`, que acepta:

- Array de objetos con campos `date`/`fecha`/`ds`, `product`/`producto`/`item`, `prediction`/`prediccion`/`yhat`
- Objeto con clave `predictions` que contiene el array anterior

Renderiza:
1. **Tabla HTML** con columnas Fecha / Producto / Predicción
2. **Gráfico SVG inline** de líneas con dots, grid y labels de ejes (sin librerías externas)

## Notas

- `proxy_buffering off` en nginx es crítico para que el streaming SSE funcione correctamente.
- `chat.js` usa `fetch()` + `ReadableStream` (no `EventSource`) porque necesita POST + headers custom.
- El threading de conversación se mantiene guardando el `message_id` de cada respuesta y enviándolo
  como `parent_message_id` en el siguiente mensaje.
- El servicio `demo_web` no modifica ningún componente existente del stack.
