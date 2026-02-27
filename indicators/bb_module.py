import numpy as np


def calculate_bb(closes: list, period: int = 20, std_dev: float = 2.0) -> dict:
    """Bollinger Bands skaičiavimas"""
    closes_arr = np.array(closes[-period:])
    middle = np.mean(closes_arr)
    std = np.std(closes_arr)
    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)
    width = (upper - lower) / middle  # BB width normalized
    return {
        "upper": round(upper, 5),
        "middle": round(middle, 5),
        "lower": round(lower, 5),
        "width": round(width, 5),
        "percent_b": round((closes[-1] - lower) / (upper - lower), 3) if upper != lower else 0.5
    }
