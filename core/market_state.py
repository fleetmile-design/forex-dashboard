"""Market State Classifier"""


def classify_market_state(bb_data: dict, atr_data: dict, adx_data: dict, trend_data: dict) -> dict:
    """
    Klasifikuoja rinkos būseną:
    - Trending (Up/Down)
    - Range
    - Compression
    - Expansion
    - News Risk
    """
    states = []

    # Trending
    if adx_data.get("adx", 0) > 25:
        direction = "up" if adx_data.get("d_plus", 0) > adx_data.get("d_minus", 0) else "down"
        states.append(f"trending_{direction}")

    # Range
    if adx_data.get("adx", 0) < 20 and bb_data.get("width", 0) > 0.003:
        states.append("range")

    # Compression
    if bb_data.get("width", 0) < 0.002:
        states.append("compression")

    # Expansion
    if atr_data.get("direction") == "rising" and bb_data.get("width", 0) > 0.004:
        states.append("expansion")

    if not states:
        states.append("neutral")

    return {
        "active_states": states,
        "primary_state": states[0] if states else "neutral",
        "trending": any("trending" in s for s in states),
        "range": "range" in states,
        "compression": "compression" in states,
        "expansion": "expansion" in states
    }
