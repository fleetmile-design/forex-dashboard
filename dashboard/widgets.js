/**
 * Forex Trader Dashboard - WebSocket Widget Manager
 * Handles WebSocket connection, auto-reconnect, and DOM updates.
 */

const WS_URL = `ws://${location.host}/ws/fast`;
let ws = null;
let reconnectTimer = null;

// ── Connection Management ────────────────────────────────────────────────────

function connect() {
  ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    setConnStatus(true);
    if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      updateDashboard(data);
    } catch (e) {
      console.error("WS parse error:", e);
    }
  };

  ws.onclose = () => {
    setConnStatus(false);
    reconnectTimer = setTimeout(connect, 5000);
  };

  ws.onerror = () => {
    ws.close();
  };
}

function setConnStatus(connected) {
  const el = document.getElementById("conn-status");
  if (connected) {
    el.innerHTML = `<span class="w-2 h-2 rounded-full bg-green-500 inline-block"></span> Connected`;
    el.className = "flex items-center gap-1 text-xs text-green-400";
  } else {
    el.innerHTML = `<span class="w-2 h-2 rounded-full bg-red-500 inline-block"></span> Disconnected`;
    el.className = "flex items-center gap-1 text-xs text-red-400";
  }
}

// ── Dashboard Update ─────────────────────────────────────────────────────────

function updateDashboard(data) {
  updateHeader(data);
  updateBias(data.bias || {});
  updateStrategies(data.strategies || {});
  updateMomentum(data.momentum || {});
  updateMarketState(data.market_state || []);
  updateBB(data.bb || {});
  updatePredictions(data.price_predictions || {});
}

function updateHeader(data) {
  setText("price", data.price ? data.price.toFixed(5) : "–");
  setText("timestamp", formatTime(data.timestamp));

  // Session badge
  const session = data.session || "–";
  const sessEl = document.getElementById("session-badge");
  sessEl.textContent = session;
  sessEl.className = "px-2 py-0.5 rounded text-xs font-bold " + sessionColor(session);

  // News risk badge
  const risk = (data.news_risk || "unknown").toLowerCase();
  const newsEl = document.getElementById("news-badge");
  newsEl.textContent = `📰 News Risk: ${risk.toUpperCase()}`;
  newsEl.className = "px-3 py-1 rounded-full text-xs font-bold " + newsRiskColor(risk);

  // Vol mode
  setText("vol-mode", (data.volatility_state || "normal").toUpperCase());
  colorVolMode(data.volatility_state);
}

function updateBias(bias) {
  const d1 = bias.d1 || "–";
  const conf = bias.confidence || 0;
  const el = document.getElementById("bias-d1");
  el.textContent = d1.toUpperCase();
  el.className = "text-3xl font-bold " + (d1 === "bullish" ? "text-green-400" : d1 === "bearish" ? "text-red-400" : "text-gray-400");

  setWidth("bias-confidence-bar", conf);
  const bar = document.getElementById("bias-confidence-bar");
  bar.className = "progress-bar " + (d1 === "bullish" ? "bg-green-500" : "bg-red-500");
  setText("bias-confidence", `${conf}%`);
}

function updateStrategies(strategies) {
  const bbRev = strategies.bb_reversion || 0;
  const breakout = strategies.breakout || 0;
  const trendCont = strategies.trend_continuation || 0;

  setText("bb-reversion-pct", `${bbRev}%`);
  setWidth("bb-reversion-bar", bbRev);
  setText("breakout-pct", `${breakout}%`);
  setWidth("breakout-bar", breakout);
  setText("trend-cont-pct", `${trendCont}%`);
  setWidth("trend-cont-bar", trendCont);

  // Spike
  const spike = strategies.spike || {};
  const spikeEl = document.getElementById("spike-status");
  if (spike.active) {
    spikeEl.textContent = "ACTIVE";
    spikeEl.className = "ml-2 text-yellow-400 font-bold pulse-glow";
    setText("spike-zone", spike.pullback_zone ? `Pullback: ${spike.pullback_zone}` : "");
  } else {
    spikeEl.textContent = "Inactive";
    spikeEl.className = "ml-2 text-gray-500";
    setText("spike-zone", "");
  }
}

function updateMomentum(momentum) {
  const rsi = momentum.rsi || 50;
  const adx = momentum.adx || 0;

  // RSI gauge
  setText("rsi-value", rsi.toFixed(1));
  const rsiArc = document.getElementById("rsi-arc");
  const totalLen = 141.37;
  const offset = totalLen - (rsi / 100) * totalLen;
  rsiArc.style.strokeDashoffset = offset;
  rsiArc.style.stroke = rsiColor(rsi);
  const rsiEl = document.getElementById("rsi-value");
  rsiEl.className = "rsi-center text-lg font-bold " + (rsi < 30 ? "text-green-300" : rsi > 70 ? "text-red-300" : "text-yellow-300");
  setText("rsi-label", rsiLabel(rsi));

  // ADX
  setText("adx-value", adx.toFixed(1));
  setText("adx-strength", adxStrength(adx));
  setText("d-plus", (momentum.d_plus || 0).toFixed(1));
  setText("d-minus", (momentum.d_minus || 0).toFixed(1));

  // ATR
  setText("atr-value", (momentum.atr || 0).toFixed(5));
  setText("atr-dir", "");

  // MACD
  const macd = momentum.macd || 0;
  setText("macd-value", macd >= 0 ? `+${macd.toFixed(5)}` : macd.toFixed(5));
  const macdEl = document.getElementById("macd-value");
  macdEl.className = "text-xl font-bold " + (macd >= 0 ? "text-green-400" : "text-red-400");
  setText("macd-label", macd >= 0 ? "Bullish" : "Bearish");

  // EMA aligned (from top-level data – handled in updateHeader)
}

function updateMarketState(states) {
  const allStates = ["trending_up", "trending_down", "range", "compression", "expansion", "neutral"];
  allStates.forEach(s => {
    const el = document.getElementById(`state-${s}`);
    if (!el) return;
    if (states.includes(s)) {
      el.classList.add("state-chip-active");
    } else {
      el.classList.remove("state-chip-active");
    }
  });
}

function updateBB(bb) {
  setText("bb-upper", bb.upper ? bb.upper.toFixed(5) : "–");
  setText("bb-middle", bb.middle ? bb.middle.toFixed(5) : "–");
  setText("bb-lower", bb.lower ? bb.lower.toFixed(5) : "–");
  setText("bb-width", bb.width ? bb.width.toFixed(4) : "–");
  const pctB = bb.percent_b || 0.5;
  setText("bb-pct-val", pctB.toFixed(3));
  setWidth("bb-pct-bar", pctB * 100);
}

function updatePredictions(pred) {
  const h1 = pred.h1_range || {};
  const h4 = pred.h4_range || {};
  setText("h1-low", h1.low ? h1.low.toFixed(5) : "–");
  setText("h1-high", h1.high ? h1.high.toFixed(5) : "–");
  setText("h4-low", h4.low ? h4.low.toFixed(5) : "–");
  setText("h4-high", h4.high ? h4.high.toFixed(5) : "–");
  setWidth("h1-range-bar", 100);
  setWidth("h4-range-bar", 100);
}

// Also update EMA aligned from top-level
const _origUpdate = updateDashboard;
// Override to handle ema_aligned at top level
window.updateDashboard = function(data) {
  _origUpdate(data);
  const emaEl = document.getElementById("ema-aligned");
  if (data.ema_aligned === true) {
    emaEl.textContent = "✅ YES";
    emaEl.className = "text-lg font-bold text-green-400";
  } else if (data.ema_aligned === false) {
    emaEl.textContent = "❌ NO";
    emaEl.className = "text-lg font-bold text-red-400";
  } else {
    emaEl.textContent = "–";
    emaEl.className = "text-lg font-bold text-gray-400";
  }
};

// ── Helpers ──────────────────────────────────────────────────────────────────

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function setWidth(id, pct) {
  const el = document.getElementById(id);
  if (el) el.style.width = `${Math.min(Math.max(pct, 0), 100)}%`;
}

function formatTime(iso) {
  if (!iso) return "–";
  const d = new Date(iso);
  return d.toLocaleTimeString();
}

function sessionColor(session) {
  if (session === "Asia") return "bg-blue-800 text-blue-200";
  if (session === "London") return "bg-green-800 text-green-200";
  if (session === "New York") return "bg-orange-800 text-orange-200";
  return "bg-gray-700 text-gray-300";
}

function newsRiskColor(risk) {
  if (risk === "low") return "bg-green-900 text-green-300";
  if (risk === "medium") return "bg-yellow-900 text-yellow-300 animate-pulse";
  if (risk === "high") return "bg-red-900 text-red-300 animate-pulse";
  return "bg-gray-800 text-gray-400";
}

function rsiColor(rsi) {
  if (rsi < 30) return "#22c55e";
  if (rsi > 70) return "#ef4444";
  return "#eab308";
}

function rsiLabel(rsi) {
  if (rsi < 30) return "Oversold";
  if (rsi > 70) return "Overbought";
  return "Neutral";
}

function adxStrength(adx) {
  if (adx > 25) return "Strong";
  if (adx > 20) return "Moderate";
  return "Weak";
}

function colorVolMode(state) {
  const el = document.getElementById("vol-mode");
  if (!el) return;
  if (state === "expansion") el.className = "text-xl font-bold text-orange-400";
  else if (state === "contraction") el.className = "text-xl font-bold text-blue-400";
  else el.className = "text-xl font-bold text-yellow-400";
}

// ── Init ─────────────────────────────────────────────────────────────────────
connect();
