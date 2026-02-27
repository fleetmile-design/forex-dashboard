"""Scoring Engine - Weighted Signals, Probability, Confidence"""


def calculate_overall_score(
    bias: dict,
    bb_reversion: dict,
    breakout: dict,
    spike: dict,
    market_state: dict,
    momentum: dict
) -> dict:
    """
    Apskaičiuoja bendrą scoring'ą pagal visus modulius
    """
    trend_score = bias.get("confidence", 0)
    reversion_score = bb_reversion.get("bb_bounce_score", 0)
    breakout_score = breakout.get("breakout_probability", 0)

    # Nustatom dominant strategy
    scores = {
        "trend_continuation": trend_score,
        "mean_reversion": reversion_score,
        "breakout": breakout_score
    }

    dominant = max(scores, key=scores.get)
    confidence = scores[dominant]

    return {
        "dominant_strategy": dominant,
        "confidence": confidence,
        "scores": scores,
        "action": "watch" if confidence < 50 else "prepare" if confidence < 70 else "ready"
    }
