# Forex Trader Dashboard

**Trader Control Dashboard** – gyvasis kontekstinis market state panel'is Docker konteineryje su FastAPI backend'u, WebSocket real-time duomenimis, moduliniu Python kodu ir WebUI dashboard'u.

> **Tai NE auto-trading sistema.** Tai Market State Panel.

---

## Kas rodoma?

| Indikatorius | Aprašymas |
|---|---|
| 📰 News Risk | Naujienų rizika iš forex-news konteinerio |
| 📊 Daily Bias | D1 dienos kryptis (bullish/bearish + confidence %) |
| 🔥 Breakout | BB compression + ATR/ADX kylimo tikimybė |
| 🎯 BB Reversion | Mean Reversion per BB bounce logiką |
| ⚡ Spike | Spike detektavimas (žvakė > 2x ATR) |
| 📈 Momentum | RSI, ADX, ATR, MACD, EMA alignment |
| 🏷️ Market State | Trending/Range/Compression/Expansion klasifikacija |

---

## Architektūra

```
forex-dashboard/
├── core/
│   ├── market_state.py        # Market State klasifikatorius
│   └── scoring_engine.py      # Weighted signals, probability %, confidence
│
├── indicators/
│   ├── bb_module.py           # Bollinger Bands
│   ├── rsi_module.py          # RSI
│   ├── adx_module.py          # ADX su D+/D-
│   ├── atr_module.py          # ATR
│   ├── macd_module.py         # MACD
│   └── ema_module.py          # EMA (multiple periods)
│
├── context/
│   ├── trend_mtf.py           # Multi-timeframe trend (D1/H4/H1)
│   ├── spike_detector.py      # Spike detection
│   ├── breakout_detector.py   # BB compression + ATR/ADX
│   ├── mean_reversion_detector.py  # BB bounce logika
│   └── news_risk.py           # News risk (integruojasi su forex-news)
│
├── api/
│   ├── websocket_server.py    # WebSocket JSON push (kas 1 min)
│   └── rest_api.py            # REST API endpoints
│
├── dashboard/
│   ├── index.html             # WebUI dashboard
│   ├── widgets.js             # WebSocket + DOM updates
│   └── style.css              # Stiliai (gauges, chips, animations)
│
├── main.py                    # FastAPI entry point
├── config.py                  # Konfigūracija
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Paleidimas

```bash
# Klonuoti repozitoriją
cd ~/projects/dashboard
git clone https://github.com/fleetmile-design/forex-dashboard.git
cd forex-dashboard

# Paleisti Docker konteinerį
docker-compose up -d --build

# Dashboard pasiekiamas:
# http://192.168.0.187:8001
```

### Tikrinti statusą

```bash
docker-compose ps
docker-compose logs -f
```

### Sustabdyti

```bash
docker-compose down
```

---

## WebSocket API

### `/ws` – Produkcinis (kas 60 sek)

```
ws://192.168.0.187:8001/ws
```

### `/ws/fast` – Testavimui (kas 5 sek)

```
ws://192.168.0.187:8001/ws/fast
```

### JSON payload pavyzdys

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "symbol": "EURUSD",
  "session": "London",
  "price": 1.08523,
  "bias": {
    "d1": "bullish",
    "confidence": 72
  },
  "strategies": {
    "bb_reversion": 81,
    "breakout": 34,
    "trend_continuation": 67,
    "spike": {
      "active": true,
      "pullback_zone": 1.08450
    }
  },
  "momentum": {
    "rsi": 58.2,
    "adx": 27.4,
    "atr": 0.00120,
    "macd": 0.00040,
    "d_plus": 28.1,
    "d_minus": 15.3
  },
  "market_state": ["trending_up", "expansion"],
  "news_risk": "low",
  "volatility_state": "expansion",
  "bb": {
    "upper": 1.08820,
    "middle": 1.08523,
    "lower": 1.08226,
    "width": 0.0055,
    "percent_b": 0.500
  },
  "ema_aligned": true,
  "price_predictions": {
    "h1_range": {"high": 1.08673, "low": 1.08373},
    "h4_range": {"high": 1.08923, "low": 1.08123}
  }
}
```

---

## REST API

| Endpoint | Metodas | Aprašymas |
|---|---|---|
| `/` | GET | WebUI Dashboard |
| `/api/status` | GET | Sistemos statusas |
| `/api/market-state` | GET | Pilnas rinkos state snapshot |
| `/api/indicators` | GET | Tik momentum indikatoriai |

---

## Modulių aprašymas

### `indicators/` – Techniniai indikatoriai

- **bb_module.py** – Bollinger Bands (upper, middle, lower, width, %B)
- **rsi_module.py** – RSI su oversold/overbought logika
- **adx_module.py** – ADX su D+/D- (trend strength)
- **atr_module.py** – ATR su krypties nustatymu (rising/falling)
- **macd_module.py** – MACD (fast/slow EMA difference)
- **ema_module.py** – EMA skaičiavimas + alignment check (bullish/bearish)

### `context/` – Konteksto analizė

- **trend_mtf.py** – Multi-timeframe analizė (D1/H4/H1 bias)
- **spike_detector.py** – Spike detektavimas (žvakė > 2x ATR)
- **breakout_detector.py** – Breakout tikimybė (BB compression + ATR/ADX)
- **mean_reversion_detector.py** – BB bounce logika (mean reversion score)
- **news_risk.py** – Naujienų rizikos lygis iš forex-news konteinerio

### `core/` – Branduolys

- **market_state.py** – Rinkos būsenos klasifikavimas (Trending/Range/Compression/Expansion)
- **scoring_engine.py** – Bendras scoring (dominant strategy, confidence, action)

---

## Kaip pridėti naują modulį

1. Sukurti failą atitinkamame kataloge (pvz., `indicators/my_indicator.py`)
2. Implementuoti funkciją, grąžinančią `dict`
3. Importuoti į `api/websocket_server.py` → `generate_demo_data()`
4. Pridėti į `dashboard/index.html` ir `dashboard/widgets.js`

---

## Integracija su forex-news konteineriu

`context/news_risk.py` jungiasi prie forex-news konteinerio:

```
http://192.168.0.187:8000/api/news
```

Konfigūracija `config.py`:
```python
NEWS_API_URL = "http://192.168.0.187:8000/api/news"
```

Docker Compose aplinkos kintamasis:
```yaml
environment:
  - NEWS_API_URL=http://192.168.0.187:8000/api/news
```

---

## Licencija

Vidinio naudojimo sistema. © fleetmile-design