"""Spike Detection Module"""


def detect_spike(candle: dict, atr: float, multiplier: float = 2.0) -> dict:
    """
    Spike = žvakė > 2x ATR
    Tikrina lokaciją (BB edge, S/R)
    """
    candle_range = abs(candle.get("high", 0) - candle.get("low", 0))
    is_spike = candle_range > (multiplier * atr) if atr > 0 else False

    result = {
        "spike_detected": is_spike,
        "candle_range": round(candle_range, 5),
        "atr_ratio": round(candle_range / atr, 2) if atr > 0 else 0,
        "direction": "up" if candle.get("close", 0) > candle.get("open", 0) else "down",
        "pullback_zone": None,
        "reaction_type": None
    }

    if is_spike:
        mid = (candle["high"] + candle["low"]) / 2
        if result["direction"] == "up":
            result["pullback_zone"] = round(mid, 5)
            result["reaction_type"] = "pullback_to_mid"
        else:
            result["pullback_zone"] = round(mid, 5)
            result["reaction_type"] = "mean_reversal"

    return result
