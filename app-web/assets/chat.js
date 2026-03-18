/* chat.js — Custom Onyx Chat UI (vanilla JS, no dependencies)
   Visual: Editorial Financial Intelligence theme */

// ── Constants ────────────────────────────────────────────────────────────────
const API_BASE = "/api";
const API_KEY = (() => {
  const meta = document.querySelector('meta[name="onyx-api-key"]');
  return meta ? meta.getAttribute("content") : "";
})();

// Number formatters
const numFmt = new Intl.NumberFormat("es-UY", { maximumFractionDigits: 0 });
const numFmtDec = new Intl.NumberFormat("es-UY", { maximumFractionDigits: 2 });

// Chart palette (light, matching page aesthetic)
const CHART = {
  line: "#0D6E6E",       // teal
  lineStroke: "#0A5858",
  dot: "#0D6E6E",
  dotStroke: "#FFFFFF",
  gridLine: "#E7E5E4",
  gridText: "#A8A29E",
  axisLine: "#D6D3D1",
  avgLine: "#D97706",    // amber
  avgText: "#B45309",
  titleColor: "#1C1917",
  tooltipBg: "#0F1729",
  tooltipText: "#FFFFFF",
  tooltipMuted: "rgba(255,255,255,0.6)",
};

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

  document.querySelectorAll(".sidebar__item").forEach((el) => {
    el.classList.toggle(
      "sidebar__item--active",
      el.dataset.sessionId === sessionId
    );
  });

  const msgs = document.getElementById("chatMessages");
  if (msgs) msgs.innerHTML = "";
  clearVizPanel();

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

// ── Date Formatting ──────────────────────────────────────────────────────────
const MONTHS_ES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
const DAYS_ES = ["dom","lun","mar","mié","jue","vie","sáb"];

function formatShortDate(isoStr) {
  const parts = String(isoStr).match(/(\d{4})-(\d{2})-(\d{2})/);
  if (!parts) return String(isoStr);
  const day = parseInt(parts[3], 10);
  const mon = MONTHS_ES[parseInt(parts[2], 10) - 1] || parts[2];
  return `${day} ${mon}`;
}

function formatLongDate(isoStr) {
  const parts = String(isoStr).match(/(\d{4})-(\d{2})-(\d{2})/);
  if (!parts) return String(isoStr);
  const d = new Date(parseInt(parts[1]), parseInt(parts[2], 10) - 1, parseInt(parts[3], 10));
  const dayName = DAYS_ES[d.getDay()];
  const day = parseInt(parts[3], 10);
  const mon = MONTHS_ES[parseInt(parts[2], 10) - 1] || parts[2];
  return `${dayName} ${day} ${mon}`;
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

    const tableWrap = document.createElement("div");
    tableWrap.className = "viz-result__table-wrap";
    tableWrap.appendChild(buildTable(["Fecha", "Unidades"], dates, values));
    result.appendChild(tableWrap);

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
    if (/^\|[\s\-|:]+\|$/.test(trimmed)) continue;

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

// ── Build Table ──────────────────────────────────────────────────────────────
function buildTable(headers, dates, values) {
  const table = document.createElement("table");
  table.className = "chat__table";
  const thead = table.createTHead();
  const hr = thead.insertRow();
  headers.forEach((h) => {
    const th = document.createElement("th");
    th.textContent = h;
    hr.appendChild(th);
  });
  const tbody = table.createTBody();

  dates.forEach((d, i) => {
    const tr = tbody.insertRow();
    tr.className = i % 2 === 0 ? "" : "chat__table-row--alt";

    const tdDate = document.createElement("td");
    tdDate.textContent = formatLongDate(d);
    tr.appendChild(tdDate);

    const tdVal = document.createElement("td");
    const formattedVal = numFmtDec.format(values[i]);
    tdVal.textContent = formattedVal;

    if (i > 0) {
      const badge = document.createElement("span");
      if (values[i] > values[i - 1]) {
        badge.className = "trend-badge trend-badge--up";
        badge.textContent = "\u2191";
      } else if (values[i] < values[i - 1]) {
        badge.className = "trend-badge trend-badge--down";
        badge.textContent = "\u2193";
      } else {
        badge.className = "trend-badge trend-badge--flat";
        badge.textContent = "\u2192";
      }
      tdVal.appendChild(badge);
    }
    tr.appendChild(tdVal);
  });

  const total = values.reduce((a, b) => a + b, 0);
  const trSum = tbody.insertRow();
  trSum.className = "chat__table-row--summary";
  const tdLabel = document.createElement("td");
  tdLabel.textContent = "Total";
  trSum.appendChild(tdLabel);
  const tdTotal = document.createElement("td");
  tdTotal.textContent = numFmtDec.format(total);
  trSum.appendChild(tdTotal);

  return table;
}

// ── Render Prediction Result ─────────────────────────────────────────────────
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
    const predRaw = row.prediction ?? row.prediccion ?? row.yhat;
    const predNum = predRaw != null ? Number(predRaw) : null;
    const pred = predNum != null ? numFmtDec.format(predNum) : "-";

    const tdDate = document.createElement("td");
    tdDate.textContent = formatLongDate(date);
    tr.appendChild(tdDate);

    const tdProd = document.createElement("td");
    tdProd.textContent = product;
    tr.appendChild(tdProd);

    const tdPred = document.createElement("td");
    tdPred.textContent = pred;

    if (i > 0 && predNum != null) {
      const prevRaw = rows[i - 1].prediction ?? rows[i - 1].prediccion ?? rows[i - 1].yhat;
      const prevNum = prevRaw != null ? Number(prevRaw) : null;
      if (prevNum != null) {
        const badge = document.createElement("span");
        if (predNum > prevNum) {
          badge.className = "trend-badge trend-badge--up";
          badge.textContent = "\u2191";
        } else if (predNum < prevNum) {
          badge.className = "trend-badge trend-badge--down";
          badge.textContent = "\u2193";
        } else {
          badge.className = "trend-badge trend-badge--flat";
          badge.textContent = "\u2192";
        }
        tdPred.appendChild(badge);
      }
    }
    tr.appendChild(tdPred);
  });

  const predValues = rows.map((r) => {
    const v = r.prediction ?? r.prediccion ?? r.yhat;
    return v != null ? Number(v) : 0;
  });
  const total = predValues.reduce((a, b) => a + b, 0);
  const trSum = tbody.insertRow();
  trSum.className = "chat__table-row--summary";
  const tdLabel = document.createElement("td");
  tdLabel.textContent = "Total";
  trSum.appendChild(tdLabel);
  const tdEmpty = document.createElement("td");
  tdEmpty.textContent = "";
  trSum.appendChild(tdEmpty);
  const tdTotal = document.createElement("td");
  tdTotal.textContent = numFmtDec.format(total);
  trSum.appendChild(tdTotal);

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

// ── SVG Chart (light style, matching page) ───────────────────────────────────
function buildSVGChart(dates, values) {
  const W = 540, H = 240;
  const PAD = { top: 34, right: 20, bottom: 44, left: 52 };
  const innerW = W - PAD.left - PAD.right;
  const innerH = H - PAD.top - PAD.bottom;

  const nums = values.filter((v) => v !== null);
  const minVal = 0;
  const maxVal = Math.max(...nums);
  const range = maxVal - minVal || 1;
  const avg = nums.reduce((a, b) => a + b, 0) / nums.length;
  const n = values.length;
  const xStep = innerW / Math.max(n - 1, 1);

  const toX = (i) => PAD.left + i * xStep;
  const toY = (v) => PAD.top + innerH - ((v - minVal) / range) * innerH;

  const pointPairs = values
    .map((v, i) => (v !== null ? [toX(i), toY(v)] : null))
    .filter(Boolean);

  const pointsStr = pointPairs.map((p) => p.join(",")).join(" ");

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

  // Defs
  const defs = document.createElementNS(ns, "defs");

  // Area gradient
  const grad = mk("linearGradient", { id: "areaGrad", x1: "0", y1: "0", x2: "0", y2: "1" });
  grad.appendChild(mk("stop", { offset: "0%", "stop-color": CHART.line, "stop-opacity": "0.22" }));
  grad.appendChild(mk("stop", { offset: "100%", "stop-color": CHART.line, "stop-opacity": "0" }));
  defs.appendChild(grad);

  // Drop shadow filter for dots
  const dotFilter = mk("filter", { id: "dotShadow", x: "-50%", y: "-50%", width: "200%", height: "200%" });
  dotFilter.appendChild(mk("feDropShadow", { dx: "0", dy: "1", stdDeviation: "1.5", "flood-color": "rgba(0,0,0,0.12)", "flood-opacity": "1" }));
  defs.appendChild(dotFilter);

  svg.appendChild(defs);

  // Title
  svg.appendChild(txt("Predicción de Demanda", {
    x: W / 2, y: 18,
    "text-anchor": "middle",
    "font-size": "12",
    "font-weight": "600",
    fill: CHART.titleColor,
    "font-family": "'Plus Jakarta Sans', sans-serif",
    "letter-spacing": "0.03em"
  }));

  // Grid + Y labels
  for (let t = 0; t <= 4; t++) {
    const yVal = minVal + (range * t) / 4;
    const y = toY(yVal);
    svg.appendChild(mk("line", {
      x1: PAD.left, y1: y, x2: PAD.left + innerW, y2: y,
      stroke: CHART.gridLine, "stroke-width": "1"
    }));
    svg.appendChild(txt(numFmt.format(Math.round(yVal)), {
      x: PAD.left - 8, y: y + 3.5,
      "text-anchor": "end",
      "font-size": "9.5",
      fill: CHART.gridText,
      "font-family": "'Plus Jakarta Sans', sans-serif"
    }));
  }

  // X labels
  const labelStep = Math.max(1, Math.ceil(n / 6));
  dates.forEach((d, i) => {
    if (i % labelStep !== 0 && i !== n - 1) return;
    svg.appendChild(txt(formatShortDate(d), {
      x: toX(i), y: PAD.top + innerH + 16,
      "text-anchor": "middle",
      "font-size": "9",
      fill: CHART.gridText,
      "font-family": "'Plus Jakarta Sans', sans-serif"
    }));
  });

  // Axes
  svg.appendChild(mk("line", {
    x1: PAD.left, y1: PAD.top, x2: PAD.left, y2: PAD.top + innerH,
    stroke: CHART.axisLine, "stroke-width": "1"
  }));
  svg.appendChild(mk("line", {
    x1: PAD.left, y1: PAD.top + innerH, x2: PAD.left + innerW, y2: PAD.top + innerH,
    stroke: CHART.axisLine, "stroke-width": "1"
  }));

  // Area fill
  if (pointPairs.length >= 2) {
    const first = pointPairs[0];
    const last = pointPairs[pointPairs.length - 1];
    const bottom = PAD.top + innerH;
    const polyPoints =
      `${first[0]},${bottom} ` +
      pointPairs.map((p) => p.join(",")).join(" ") +
      ` ${last[0]},${bottom}`;
    svg.appendChild(mk("polygon", {
      points: polyPoints,
      fill: "url(#areaGrad)"
    }));
  }

  // Average reference line
  const avgY = toY(avg);
  svg.appendChild(mk("line", {
    x1: PAD.left, y1: avgY, x2: PAD.left + innerW, y2: avgY,
    stroke: CHART.avgLine, "stroke-width": "1",
    "stroke-dasharray": "6,4"
  }));
  svg.appendChild(txt(`Promedio: ${numFmt.format(Math.round(avg))}`, {
    x: PAD.left + innerW - 2, y: avgY - 6,
    "text-anchor": "end",
    "font-size": "8.5",
    fill: CHART.avgText,
    "font-family": "'Plus Jakarta Sans', sans-serif",
    "font-weight": "600"
  }));

  // Main line with glow
  if (pointsStr) {
    svg.appendChild(mk("polyline", {
      points: pointsStr,
      fill: "none",
      stroke: CHART.line,
      "stroke-width": "2.5",
      "stroke-linejoin": "round",
      "stroke-linecap": "round",
      class: "chart-line-animated"
    }));
  }

  // Tooltip group
  const tooltipG = document.createElementNS(ns, "g");
  tooltipG.setAttribute("class", "chart-tooltip");
  const tooltipRect = mk("rect", {
    width: "96", height: "38", rx: "6", ry: "6",
    fill: CHART.tooltipBg
  });
  // Shadow for tooltip
  const tooltipShadow = mk("rect", {
    width: "96", height: "38", rx: "6", ry: "6",
    fill: "rgba(0,0,0,0.15)", transform: "translate(0, 2)",
  });
  const tooltipLine1 = txt("", {
    x: "48", y: "14",
    "text-anchor": "middle",
    "font-size": "9.5",
    fill: CHART.tooltipMuted,
    "font-family": "'Plus Jakarta Sans', sans-serif"
  });
  tooltipLine1.setAttribute("class", "tt-date");
  const tooltipLine2 = txt("", {
    x: "48", y: "30",
    "text-anchor": "middle",
    "font-size": "12",
    "font-weight": "700",
    fill: CHART.tooltipText,
    "font-family": "'Plus Jakarta Sans', sans-serif"
  });
  tooltipLine2.setAttribute("class", "tt-val");
  tooltipG.appendChild(tooltipShadow);
  tooltipG.appendChild(tooltipRect);
  tooltipG.appendChild(tooltipLine1);
  tooltipG.appendChild(tooltipLine2);
  svg.appendChild(tooltipG);

  // Dots + hit areas
  values.forEach((v, i) => {
    if (v === null) return;
    const cx = toX(i);
    const cy = toY(v);

    // Visible dot
    svg.appendChild(mk("circle", {
      cx, cy, r: "4",
      fill: CHART.dot,
      stroke: CHART.dotStroke,
      "stroke-width": "2",
      filter: "url(#dotShadow)",
      class: "chart-dot"
    }));

    // Hit area
    const hitArea = mk("circle", {
      cx, cy, r: "14",
      fill: "transparent",
      stroke: "none",
      style: "cursor: pointer"
    });

    hitArea.addEventListener("mouseenter", () => {
      tooltipG.querySelector(".tt-date").textContent = formatShortDate(dates[i]);
      tooltipG.querySelector(".tt-val").textContent = numFmtDec.format(v);

      let tx = cx - 48;
      if (tx < PAD.left) tx = PAD.left;
      if (tx + 96 > W - PAD.right) tx = W - PAD.right - 96;
      let ty = cy - 46;
      if (ty < 4) ty = cy + 12;

      tooltipG.setAttribute("transform", `translate(${tx}, ${ty})`);
      tooltipG.classList.add("visible");
    });

    hitArea.addEventListener("mouseleave", () => {
      tooltipG.classList.remove("visible");
    });

    svg.appendChild(hitArea);
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
  pill.textContent = `\u2699 ${toolName}`;
  bubbleEl.appendChild(pill);
}

function appendErrorToBubble(bubbleEl, msg) {
  const span = document.createElement("span");
  span.className = "chat__error";
  span.textContent = `\u26A0 ${msg}`;
  bubbleEl.appendChild(span);
}

function showWelcomeBubble() {
  const div = appendAssistantBubble();
  setTextContent(div, "\u00A1Hola! Soy el asistente de predicci\u00F3n de stock de la UMPE (Universidad de Montevideo). Puedo ayudarte con predicciones de demanda, tendencias y recomendaciones de reabastecimiento para supermercados de Ecuador.");
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

// ── Service Health Checks ─────────────────────────────────────────────────────
const HEALTH_ENDPOINTS = [
  { id: "statusOnyx",      url: "/api/health",          label: "Onyx" },
  { id: "statusPrediction", url: "/prediction-health",  label: "Predicción" },
];

function setStatusDot(id, state) {
  // state: "checking" | "ok" | "error"
  const container = document.getElementById(id);
  if (!container) return;
  const dot = container.querySelector(".status-dot");
  if (!dot) return;
  dot.className = "status-dot status-dot--" + state;

  const label = container.querySelector(".status-label");
  if (label) {
    container.title =
      state === "ok" ? `${label.textContent}: Operativo` :
      state === "error" ? `${label.textContent}: No disponible` :
      `${label.textContent}: Verificando...`;
  }
}

async function checkServiceHealth(endpoint) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 4000);
    const res = await fetch(endpoint.url, { signal: controller.signal });
    clearTimeout(timeout);
    setStatusDot(endpoint.id, res.ok ? "ok" : "error");
  } catch {
    setStatusDot(endpoint.id, "error");
  }
}

function runHealthChecks() {
  HEALTH_ENDPOINTS.forEach((ep) => checkServiceHealth(ep));
}

// ── Event Listeners ───────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initSession();

  document.getElementById("newChatBtn")?.addEventListener("click", createNewSession);

  // Sidebar collapse / expand
  const appBody = document.querySelector(".app-body");
  document.getElementById("sidebarCollapse")?.addEventListener("click", () => {
    document.getElementById("sidebar")?.classList.add("sidebar--collapsed");
    appBody?.classList.add("app-body--sidebar-collapsed");
  });
  document.getElementById("sidebarToggle")?.addEventListener("click", () => {
    document.getElementById("sidebar")?.classList.remove("sidebar--collapsed");
    appBody?.classList.remove("app-body--sidebar-collapsed");
  });

  document.getElementById("chatForm")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendMessage(text);
  });

  // Health checks: run immediately, then every 30 seconds
  runHealthChecks();
  setInterval(runHealthChecks, 30000);
});
