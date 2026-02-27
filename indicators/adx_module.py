import numpy as np


def calculate_adx(highs: list, lows: list, closes: list, period: int = 14) -> dict:
    """ADX su D+/D- skaičiavimas"""
    # Supaprastinta implementacija
    tr_list = []
    dm_plus_list = []
    dm_minus_list = []

    for i in range(1, len(highs)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
        tr_list.append(tr)
        dm_plus = highs[i] - highs[i-1] if highs[i] - highs[i-1] > lows[i-1] - lows[i] else 0
        dm_minus = lows[i-1] - lows[i] if lows[i-1] - lows[i] > highs[i] - highs[i-1] else 0
        dm_plus = max(dm_plus, 0)
        dm_minus = max(dm_minus, 0)
        dm_plus_list.append(dm_plus)
        dm_minus_list.append(dm_minus)

    if len(tr_list) < period:
        return {"adx": 0, "d_plus": 0, "d_minus": 0, "trend_strength": "weak"}

    atr = np.mean(tr_list[-period:])
    d_plus = round(100 * np.mean(dm_plus_list[-period:]) / atr, 2) if atr > 0 else 0
    d_minus = round(100 * np.mean(dm_minus_list[-period:]) / atr, 2) if atr > 0 else 0
    dx = abs(d_plus - d_minus) / (d_plus + d_minus) * 100 if (d_plus + d_minus) > 0 else 0
    adx_val = round(dx, 2)

    strength = "strong" if adx_val > 25 else "moderate" if adx_val > 20 else "weak"
    return {"adx": adx_val, "d_plus": d_plus, "d_minus": d_minus, "trend_strength": strength}
