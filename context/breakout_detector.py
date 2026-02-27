"""Breakout Detection Module"""


def detect_breakout(bb_data: dict, atr_data: dict, adx_data: dict, news_minutes: int = 999) -> dict:
    """
    Breakout probability:
    - BB width susiaurėja (compression)
    - ATR kyla
    - ADX kyla
    - News < 60 min → higher probability
    """
    score = 0
    compression = bb_data.get("width", 1) < 0.002  # Narrow BB
    atr_rising = atr_data.get("direction") == "rising"
    adx_rising = adx_data.get("adx", 0) > 20
    news_catalyst = news_minutes < 60

    if compression: score += 30
    if atr_rising: score += 25
    if adx_rising: score += 25
    if news_catalyst: score += 20

    return {
        "breakout_probability": min(score, 100),
        "compression": compression,
        "atr_rising": atr_rising,
        "adx_rising": adx_rising,
        "news_catalyst": news_catalyst
    }
