"""WebSocket server - JSON push kas 1 min"""
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
from datetime import datetime

# Demo data generator (vėliau pakeis tikri MT5 duomenys)
import random


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                pass


manager = ConnectionManager()


def generate_demo_data() -> dict:
    """Generuoja demo duomenis testavimui"""
    base_price = 1.0850
    price = base_price + random.uniform(-0.005, 0.005)

    return {
        "timestamp": datetime.now().isoformat(),
        "symbol": "EURUSD",
        "session": _get_current_session(),
        "price": round(price, 5),
        "bias": {
            "d1": random.choice(["bullish", "bearish"]),
            "confidence": random.randint(40, 90)
        },
        "strategies": {
            "bb_reversion": random.randint(10, 95),
            "breakout": random.randint(10, 95),
            "trend_continuation": random.randint(10, 95),
            "spike": {
                "active": random.choice([True, False]),
                "pullback_zone": round(price - 0.001, 5)
            }
        },
        "momentum": {
            "rsi": round(random.uniform(20, 80), 2),
            "adx": round(random.uniform(10, 45), 2),
            "atr": round(random.uniform(0.0005, 0.002), 5),
            "macd": round(random.uniform(-0.001, 0.001), 5),
            "d_plus": round(random.uniform(10, 35), 2),
            "d_minus": round(random.uniform(10, 35), 2)
        },
        "market_state": random.sample(["trending_up", "expansion", "range", "compression"], k=random.randint(1, 2)),
        "news_risk": random.choice(["low", "medium", "high"]),
        "volatility_state": random.choice(["expansion", "contraction", "normal"]),
        "bb": {
            "upper": round(price + 0.003, 5),
            "middle": round(price, 5),
            "lower": round(price - 0.003, 5),
            "width": round(random.uniform(0.001, 0.006), 4),
            "percent_b": round(random.uniform(0, 1), 3)
        },
        "ema_aligned": random.choice([True, False]),
        "price_predictions": {
            "h1_range": {"high": round(price + 0.0015, 5), "low": round(price - 0.0015, 5)},
            "h4_range": {"high": round(price + 0.004, 5), "low": round(price - 0.004, 5)},
        }
    }


def _get_current_session():
    hour = datetime.utcnow().hour
    if 0 <= hour < 8:
        return "Asia"
    elif 8 <= hour < 16:
        return "London"
    else:
        return "New York"
