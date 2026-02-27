import numpy as np


def calculate_macd(closes: list, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """MACD skaičiavimas"""
    def ema(data, period):
        multiplier = 2 / (period + 1)
        ema_val = data[0]
        for price in data[1:]:
            ema_val = (price - ema_val) * multiplier + ema_val
        return ema_val

    if len(closes) < slow + signal:
        return {"macd": 0, "signal": 0, "histogram": 0}

    ema_fast = ema(closes[-fast:], fast)
    ema_slow = ema(closes[-slow:], slow)
    macd_val = round(ema_fast - ema_slow, 5)

    return {"macd": macd_val, "signal": 0, "histogram": macd_val}
