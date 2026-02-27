import numpy as np


def calculate_ema(closes: list, period: int = 21) -> float:
    """EMA skaičiavimas"""
    multiplier = 2 / (period + 1)
    ema_val = closes[0]
    for price in closes[1:]:
        ema_val = (price - ema_val) * multiplier + ema_val
    return round(ema_val, 5)


def check_ema_alignment(closes: list, periods: list = [9, 21, 50, 200]) -> dict:
    """Tikrina ar EMA'os išsirikiavusios (bullish/bearish)"""
    emas = {}
    for p in periods:
        if len(closes) >= p:
            emas[f"ema_{p}"] = calculate_ema(closes, p)
        else:
            emas[f"ema_{p}"] = None

    valid_emas = [v for v in emas.values() if v is not None]
    if len(valid_emas) < 2:
        return {"aligned": False, "direction": "unknown", "emas": emas}

    bullish = all(valid_emas[i] >= valid_emas[i+1] for i in range(len(valid_emas)-1))
    bearish = all(valid_emas[i] <= valid_emas[i+1] for i in range(len(valid_emas)-1))

    direction = "bullish" if bullish else "bearish" if bearish else "mixed"
    return {"aligned": bullish or bearish, "direction": direction, "emas": emas}
