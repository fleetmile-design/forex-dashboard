# Konfigūracija
SYMBOL = "EURUSD"
TIMEFRAMES = ["M1", "M5", "M15", "H1", "H4", "D1"]
WEBSOCKET_INTERVAL = 60  # sekundės
NEWS_API_URL = "http://192.168.0.187:8000/api/news"
PORT = 8001

# Indikatorių parametrai
BB_PERIOD = 20
BB_STD = 2
RSI_PERIOD = 14
ADX_PERIOD = 14
ATR_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
EMA_PERIODS = [9, 21, 50, 200]

# Session times (UTC)
SESSIONS = {
    "asia": {"start": "00:00", "end": "08:00"},
    "london": {"start": "08:00", "end": "16:00"},
    "new_york": {"start": "13:00", "end": "21:00"}
}
