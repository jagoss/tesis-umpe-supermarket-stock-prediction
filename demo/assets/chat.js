/* chat.js — Custom Onyx Chat UI (vanilla JS, no dependencies) */

// ── Constants ────────────────────────────────────────────────────────────────
const API_BASE = "/api";
const API_KEY = (() => {
  const meta = document.querySelector('meta[name="onyx-api-key"]');
  return meta ? meta.getAttribute("content") : "";
})();

// ── State ─────────────────────────────────────────────────────────────────────
let chatSessionId = null;
let parentMessageId = null;
let isStreaming = false;

// ── Session Init ──────────────────────────────────────────────────────────────
async function initSession() {
  try {
    const res = await fetch(`${API_BASE}/chat/create-chat-session`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({ persona_id: 1, description: "" }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    chatSessionId = data.chat_session_id;
    showWelcomeBubble();
    await loadSessionList();
  } catch (err) {
    showErrorBubble(
      "No se pudo conectar con el asistente. Verifica que el servidor esté activo."
    );
    console.error("[chat] initSession error:", err);
  }
}

// ── Session List ──────────────────────────────────────────────────────────────
async function loadSessionList() {
  try {
    const res = await fetch(`${API_BASE}/chat/get-user-chat-sessions`, {
      headers: { Authorization: `Bearer ${API_KEY}` },
    });
    if (!res.ok) return;
    const raw = await res.json();
    const sessions = Array.isArray(raw) ? raw : raw.sessions ?? [];
    renderSessionList(sessions);
  } catch (err) {
    console.error("[chat] loadSessionList error:", err);
  }
}

function renderSessionList(sessions) {
  const list = document.getElementById("sessionList");
  if (!list) return;
  list.innerHTML = "";

  if (!sessions.length) {
    list.innerHTML = '<p class="sidebar__empty">Sin conversaciones previas</p>';
    return;
  }

  sessions
    .slice()
    .sort((a, b) => new Date(b.time_created ?? 0) - new Date(a.time_created ?? 0))
    .forEach((s) => {
      const id = s.id ?? s.chat_session_id;
      const label = s.description?.trim() || formatDate(s.time_created);
      const dateStr = formatDate(s.time_created);

      const btn = document.createElement("button");
      btn.className =
        "sidebar__item" + (id === chatSessionId ? " sidebar__item--active" : "");
      btn.dataset.sessionId = id;

      const labelEl = document.createElement("span");
      labelEl.className = "sidebar__item-label";
      labelEl.textContent = label;

      const dateEl = document.createElement("span");
      dateEl.className = "sidebar__item-date";
      dateEl.textContent = dateStr;

      btn.appendChild(labelEl);
      btn.appendChild(dateEl);
      btn.addEventListener("click", () => switchToSession(id));
      list.appendChild(btn);
    });
}

async function switchToSession(sessionId) {
  if (sessionId === chatSessionId) return;

  chatSessionId = sessionId;
  parentMessageId = null;

  // Mark active in sidebar
  document.querySelectorAll(".sidebar__item").forEach((el) => {
    el.classList.toggle(
      "sidebar__item--active",
      el.dataset.sessionId === sessionId
    );
  });

  // Clear UI
  const msgs = document.getElementById("chatMessages");
  if (msgs) msgs.innerHTML = "";
  clearVizPanel();

  // Load history
  await loadSessionHistory(sessionId);
}

async function loadSessionHistory(sessionId) {
  try {
    const res = await fetch(`${API_BASE}/chat/get-chat-session/${sessionId}`, {
      headers: { Authorization: `Bearer ${API_KEY}` },
    });
    if (!res.ok) return;
    const data = await res.json();
    const messages = data.messages ?? [];

    messages.forEach((msg) => {
      const type = msg.message_type ?? msg.type;
      const text = msg.message ?? msg.content ?? msg.text ?? "";
      if (!text) return;

      if (type === "user") {
        appendUserBubble(text);
      } else if (type === "assistant") {
        const bubble = appendAssistantBubble();
        setTextContent(bubble, text);
        if (msg.message_id != null) parentMessageId = msg.message_id;
      }
    });

    scrollToBottom();
  } catch (err) {
    console.error("[chat] loadSessionHistory error:", err);
  }
}

async function createNewSession() {
  try {
    const res = await fetch(`${API_BASE}/chat/create-chat-session`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({ persona_id: 1, description: "" }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    chatSessionId = data.chat_session_id;
    parentMessageId = null;

    const msgs = document.getElementById("chatMessages");
    if (msgs) msgs.innerHTML = "";
    clearVizPanel();
    showWelcomeBubble();

    await loadSessionList();
  } catch (err) {
    console.error("[chat] createNewSession error:", err);
  }
}

// ── Send Message ─────────────────────────────────────────────────────────────
async function sendMessage(text) {
  if (isStreaming || !text.trim()) return;
  if (!chatSessionId) {
    showErrorBubble("Sesión no inicializada. Recarga la página.");
    return;
  }

  isStreaming = true;
  setSendDisabled(true);

  appendUserBubble(text);
  const assistantBubble = appendAssistantBubble();
  showStatus("Escribiendo...");

  try {
    const res = await fetch(`${API_BASE}/chat/send-message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        chat_session_id: chatSessionId,
        parent_message_id: parentMessageId,
        message: text,
        prompt_id: 0,
        search_doc_ids: [],
        retrieval_options: null,
      }),
    });

    if (!res.ok) {
      const body = await res.text();
      console.error("[chat] send-message error body:", body);
      throw new Error(`HTTP ${res.status}`);
    }
    await parseSSEStream(res, assistantBubble);
    // Refresh session list so description updates after first message
    loadSessionList();
  } catch (err) {
    appendErrorToBubble(assistantBubble, "Error al obtener respuesta.");
    console.error("[chat] sendMessage error:", err);
  } finally {
    isStreaming = false;
    setSendDisabled(false);
    hideStatus();
    scrollToBottom();
  }
}

// ── SSE Parsing ───────────────────────────────────────────────────────────────
// Onyx streams raw JSON lines (no "data:" prefix).
// First line: {"user_message_id": N, "reserved_assistant_message_id": M}
// Subsequent: {"placement": {...}, "obj": {"type": "...", ...}}
async function parseSSEStream(response, bubbleEl) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let textContent = "";
  let seenFirstLine = false;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop();

    for (const line of lines) {
      const raw = line.trim();
      if (!raw) continue;

      let packet;
      try {
        packet = JSON.parse(raw);
      } catch {
        continue;
      }

      // First line: message IDs
      if (!seenFirstLine) {
        seenFirstLine = true;
        if (packet.reserved_assistant_message_id != null) {
          parentMessageId = packet.reserved_assistant_message_id;
        }
        continue;
      }

      const obj = packet.obj;
      if (!obj) continue;

      if (obj.type === "message_delta" && obj.content != null) {
        textContent += obj.content;
        setTextContent(bubbleEl, textContent);
        scrollToBottom();
      } else if (obj.type === "tool_call") {
        const name = obj.tool_name ?? obj.tool_call?.name ?? "tool";
        showToolPill(bubbleEl, name);
        showStatus("Consultando predicción...");
      } else if (obj.type === "tool_result") {
        const vizContainer = document.createElement("div");
        appendToVizPanel(vizContainer);
        renderPredictionResult(obj.tool_result ?? obj.result, vizContainer);
      } else if (obj.type === "stop") {
        if (textContent) renderMarkdownTables(textContent);
        return;
      } else if (obj.type === "error") {
        appendErrorToBubble(bubbleEl, obj.error || "Error desconocido");
      }
    }
  }
}

// ── Viz Panel Helpers ─────────────────────────────────────────────────────────
function appendToVizPanel(el) {
  const empty = document.getElementById("vizEmpty");
  const content = document.getElementById("vizContent");
  if (empty) empty.hidden = true;
  if (content) {
    content.innerHTML = "";
    content.classList.add("has-data");
    content.appendChild(el);
  }
}

function clearVizPanel() {
  const empty = document.getElementById("vizEmpty");
  const content = document.getElementById("vizContent");
  if (empty) empty.hidden = false;
  if (content) {
    content.classList.remove("has-data");
    content.innerHTML = "";
  }
}

// ── Markdown Table Parser ─────────────────────────────────────────────────────
function renderMarkdownTables(text) {
  const lines = text.split("\n");
  let inTable = false;
  let headerCols = [];
  let dataRows = [];

  const flush = () => {
    if (dataRows.length < 2) { dataRows = []; headerCols = []; return; }

    const dateColIdx = headerCols.findIndex((h) =>
      /fecha|date|día|dia/i.test(h)
    );
    let numColIdx = -1;
    for (let i = headerCols.length - 1; i >= 0; i--) {
      if (/\d/.test(dataRows[0][i] ?? "")) { numColIdx = i; break; }
    }
    if (numColIdx === -1) { dataRows = []; headerCols = []; return; }

    const dates = [];
    const values = [];
    dataRows.forEach((cells) => {
      let dateVal = dateColIdx >= 0 ? cells[dateColIdx] : null;
      if (!dateVal) dateVal = cells.find((c) => /\d{4}-\d{2}-\d{2}/.test(c)) ?? "";
      const match = dateVal.match(/\d{4}-\d{2}-\d{2}/);
      const numStr = (cells[numColIdx] ?? "").replace(/[^\d.]/g, "");
      if (match && numStr) {
        dates.push(match[0]);
        values.push(parseFloat(numStr));
      }
    });

    if (dates.length < 2) { dataRows = []; headerCols = []; return; }

    const result = document.createElement("div");
    result.className = "viz-result";

    // Table
    const tableWrap = document.createElement("div");
    tableWrap.className = "viz-result__table-wrap";
    const table = document.createElement("table");
    table.className = "chat__table";
    const thead = table.createTHead();
    const hr = thead.insertRow();
    ["Fecha", "Unidades"].forEach((h) => {
      const th = document.createElement("th");
      th.textContent = h;
      hr.appendChild(th);
    });
    const tbody = table.createTBody();
    dates.forEach((d, i) => {
      const tr = tbody.insertRow();
      tr.className = i % 2 === 0 ? "" : "chat__table-row--alt";
      [d, values[i]].forEach((v) => {
        const td = document.createElement("td");
        td.textContent = v;
        tr.appendChild(td);
      });
    });
    tableWrap.appendChild(table);
    result.appendChild(tableWrap);

    // Chart
    const chartWrapper = document.createElement("div");
    chartWrapper.className = "viz-result__chart";
    chartWrapper.appendChild(buildSVGChart(dates, values));
    result.appendChild(chartWrapper);

    appendToVizPanel(result);
    dataRows = [];
    headerCols = [];
  };

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed.startsWith("|")) {
      if (inTable) { flush(); inTable = false; }
      continue;
    }
    if (/^\|[\s\-|:]+\|$/.test(trimmed)) continue; // separator row

    const cells = trimmed
      .split("|")
      .map((c) => c.trim())
      .filter((_, i, a) => i > 0 && i < a.length - 1);

    if (!inTable) {
      inTable = true;
      headerCols = cells;
    } else {
      dataRows.push(cells);
    }
  }
  if (inTable) flush();
}

// ── Render Prediction Result (from tool_result event) ────────────────────────
function renderPredictionResult(toolResult, container) {
  let data = toolResult;
  if (typeof toolResult === "string") {
    try { data = JSON.parse(toolResult); } catch { return; }
  }

  let rows = [];
  if (Array.isArray(data)) {
    rows = data;
  } else if (data && Array.isArray(data.predictions)) {
    rows = data.predictions;
  } else if (data && typeof data === "object") {
    const arr = Object.values(data).find((v) => Array.isArray(v));
    if (arr) rows = arr;
  }
  if (!rows.length) return;

  const result = document.createElement("div");
  result.className = "viz-result";

  const tableWrap = document.createElement("div");
  tableWrap.className = "viz-result__table-wrap";
  const table = document.createElement("table");
  table.className = "chat__table";
  const thead = table.createTHead();
  const hr = thead.insertRow();
  ["Fecha", "Producto", "Predicción"].forEach((h) => {
    const th = document.createElement("th");
    th.textContent = h;
    hr.appendChild(th);
  });
  const tbody = table.createTBody();
  rows.forEach((row, i) => {
    const tr = tbody.insertRow();
    tr.className = i % 2 === 0 ? "" : "chat__table-row--alt";
    const date = row.date ?? row.fecha ?? row.ds ?? "-";
    const product = row.product ?? row.producto ?? row.item ?? "-";
    const pred =
      row.prediction != null ? Number(row.prediction).toFixed(2)
      : row.prediccion != null ? Number(row.prediccion).toFixed(2)
      : row.yhat != null ? Number(row.yhat).toFixed(2)
      : "-";
    [date, product, pred].forEach((val) => {
      const td = document.createElement("td");
      td.textContent = val;
      tr.appendChild(td);
    });
  });
  tableWrap.appendChild(table);
  result.appendChild(tableWrap);

  const dates = rows.map((r) => r.date ?? r.fecha ?? r.ds ?? "");
  const values = rows.map((r) => {
    const v = r.prediction ?? r.prediccion ?? r.yhat;
    return v != null ? Number(v) : null;
  });
  if (values.filter((v) => v !== null).length >= 2) {
    const chartWrapper = document.createElement("div");
    chartWrapper.className = "viz-result__chart";
    chartWrapper.appendChild(buildSVGChart(dates, values));
    result.appendChild(chartWrapper);
  }
  container.appendChild(result);
}

// ── SVG Chart ─────────────────────────────────────────────────────────────────
function buildSVGChart(dates, values) {
  const W = 540, H = 220;
  const PAD = { top: 16, right: 16, bottom: 44, left: 48 };
  const innerW = W - PAD.left - PAD.right;
  const innerH = H - PAD.top - PAD.bottom;

  const nums = values.filter((v) => v !== null);
  const minVal = Math.min(...nums);
  const maxVal = Math.max(...nums);
  const range = maxVal - minVal || 1;
  const n = values.length;
  const xStep = innerW / Math.max(n - 1, 1);

  const toX = (i) => PAD.left + i * xStep;
  const toY = (v) => PAD.top + innerH - ((v - minVal) / range) * innerH;

  const points = values
    .map((v, i) => (v !== null ? `${toX(i)},${toY(v)}` : null))
    .filter(Boolean)
    .join(" ");

  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);

  const mk = (tag, attrs) => {
    const el = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  };
  const txt = (content, attrs) => {
    const el = mk("text", attrs);
    el.textContent = content;
    return el;
  };

  // Grid + Y labels
  for (let t = 0; t <= 4; t++) {
    const yVal = minVal + (range * t) / 4;
    const y = toY(yVal);
    svg.appendChild(mk("line", { x1: PAD.left, y1: y, x2: PAD.left + innerW, y2: y, stroke: "#E5E7EB", "stroke-width": "1" }));
    svg.appendChild(txt(Math.round(yVal), { x: PAD.left - 6, y: y + 4, "text-anchor": "end", "font-size": "10", fill: "#6B7280", "font-family": "sans-serif" }));
  }

  // X labels (max 6)
  const labelStep = Math.max(1, Math.ceil(n / 6));
  dates.forEach((d, i) => {
    if (i % labelStep !== 0 && i !== n - 1) return;
    const label = String(d).length > 8 ? String(d).slice(5) : String(d);
    svg.appendChild(txt(label, { x: toX(i), y: PAD.top + innerH + 14, "text-anchor": "middle", "font-size": "9", fill: "#6B7280", "font-family": "sans-serif" }));
  });

  // Axes
  svg.appendChild(mk("line", { x1: PAD.left, y1: PAD.top, x2: PAD.left, y2: PAD.top + innerH, stroke: "#D1D5DB", "stroke-width": "1" }));
  svg.appendChild(mk("line", { x1: PAD.left, y1: PAD.top + innerH, x2: PAD.left + innerW, y2: PAD.top + innerH, stroke: "#D1D5DB", "stroke-width": "1" }));

  // Line
  if (points) {
    svg.appendChild(mk("polyline", { points, fill: "none", stroke: "var(--color-primary, #4F46E5)", "stroke-width": "2", "stroke-linejoin": "round", "stroke-linecap": "round" }));
  }

  // Dots
  values.forEach((v, i) => {
    if (v === null) return;
    svg.appendChild(mk("circle", { cx: toX(i), cy: toY(v), r: "3", fill: "var(--color-primary, #4F46E5)", stroke: "white", "stroke-width": "1.5" }));
  });

  return svg;
}

// ── DOM Helpers ───────────────────────────────────────────────────────────────
function messagesEl() { return document.getElementById("chatMessages"); }

function appendUserBubble(text) {
  const div = document.createElement("div");
  div.className = "chat__bubble chat__bubble--user";
  div.textContent = text;
  messagesEl().appendChild(div);
  scrollToBottom();
}

function appendAssistantBubble() {
  const div = document.createElement("div");
  div.className = "chat__bubble chat__bubble--assistant";
  messagesEl().appendChild(div);
  scrollToBottom();
  return div;
}

function setTextContent(bubbleEl, text) {
  let node = bubbleEl._textNode;
  if (!node) {
    node = document.createTextNode(text);
    bubbleEl.insertBefore(node, bubbleEl.firstChild);
    bubbleEl._textNode = node;
  } else {
    node.textContent = text;
  }
}

function showToolPill(bubbleEl, toolName) {
  const existing = bubbleEl.querySelector(".chat__tool");
  if (existing) existing.remove();
  const pill = document.createElement("span");
  pill.className = "chat__tool";
  pill.textContent = `⚙ ${toolName}`;
  bubbleEl.appendChild(pill);
}

function appendErrorToBubble(bubbleEl, msg) {
  const span = document.createElement("span");
  span.className = "chat__error";
  span.textContent = `⚠ ${msg}`;
  bubbleEl.appendChild(span);
}

function showWelcomeBubble() {
  const div = appendAssistantBubble();
  setTextContent(div, "¡Hola! Soy el asistente de inventario de UMPE. Puedes preguntarme sobre predicciones de stock, tendencias de demanda o recomendaciones de reabastecimiento.");
}

function showErrorBubble(msg) {
  const div = appendAssistantBubble();
  appendErrorToBubble(div, msg);
}

function showStatus(text) {
  const s = document.getElementById("chatStatus");
  const t = document.getElementById("chatStatusText");
  if (s) s.hidden = false;
  if (t) t.textContent = text;
}

function hideStatus() {
  const s = document.getElementById("chatStatus");
  if (s) s.hidden = true;
}

function scrollToBottom() {
  const el = messagesEl();
  if (el) el.scrollTop = el.scrollHeight;
}

function setSendDisabled(disabled) {
  const btn = document.getElementById("chatSend");
  const input = document.getElementById("chatInput");
  if (btn) btn.disabled = disabled;
  if (input) input.disabled = disabled;
}

function formatDate(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  return d.toLocaleDateString("es-EC", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

// ── Event Listeners ───────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initSession();

  document.getElementById("newChatBtn")?.addEventListener("click", createNewSession);

  document.getElementById("chatForm")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendMessage(text);
  });
});
