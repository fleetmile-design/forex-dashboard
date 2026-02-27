import numpy as np


def calculate_atr(highs: list, lows: list, closes: list, period: int = 14) -> dict:
    """ATR skaičiavimas"""
    tr_list = []
    for i in range(1, len(highs)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
        tr_list.append(tr)

    atr_val = round(np.mean(tr_list[-period:]), 5) if len(tr_list) >= period else 0
    prev_atr = round(np.mean(tr_list[-(period*2):-period]), 5) if len(tr_list) >= period*2 else atr_val
    direction = "rising" if atr_val > prev_atr else "falling"

    return {"atr": atr_val, "direction": direction, "daily_percent": round(atr_val * 10000, 1)}
