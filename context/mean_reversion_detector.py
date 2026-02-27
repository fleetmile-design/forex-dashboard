"""Mean Reversion (BB Bounce) Detection Module"""


def detect_mean_reversion(candle: dict, bb_data: dict, rsi: float, adx: float, news_active: bool = False) -> dict:
    """
    BB Bounce logika:
    - Close > BB_lower IR Low < BB_lower (rejection)
    - RSI < 30 → > 35
    - ADX < 20
    - News = none
    """
    close = candle.get("close", 0)
    low = candle.get("low", 0)
    high = candle.get("high", 0)
    bb_lower = bb_data.get("lower", 0)
    bb_upper = bb_data.get("upper", 0)

    # Lower BB bounce
    lower_rejection = close > bb_lower and low <= bb_lower
    upper_rejection = close < bb_upper and high >= bb_upper

    score = 0
    bounce_type = None

    if lower_rejection:
        bounce_type = "lower_bounce"
        score += 30
    elif upper_rejection:
        bounce_type = "upper_bounce"
        score += 30

    if rsi < 35 and lower_rejection: score += 25
    if rsi > 65 and upper_rejection: score += 25
    if adx < 20: score += 20
    if not news_active: score += 25

    return {
        "bb_bounce_score": min(score, 100),
        "bounce_type": bounce_type,
        "state": "mean_reversion_active" if score > 60 else "neutral",
        "rsi_confirm": (rsi < 35 and lower_rejection) or (rsi > 65 and upper_rejection),
        "adx_filter": adx < 20,
        "news_clear": not news_active
    }
