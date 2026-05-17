"""
4-factor confidence scoring engine.

Score = 0.30 × sample_score
      + 0.30 × variance_score
      + 0.25 × regime_score
      + 0.15 × edge_score

Returns (score: float, reasons: list[str])
"""

import math


def _sample_score(n: int) -> float:
    if n <= 0:
        return 0.0
    return min(1.0, 1 - math.exp(-n / 20))


def _variance_score(std_dev: float | None) -> float:
    if std_dev is None or std_dev <= 0:
        return 0.1
    return max(0.0, 1 - std_dev / 6.0)


def _regime_score(regime: str, regime_conf: float) -> float:
    penalty = {"UNKNOWN": 0.3, "HIGH_VARIANCE": 0.5, "STORM_RISK": 0.5,
               "RAIN_RISK": 0.6, "HEAT_SPIKE_RISK": 0.6}
    base = penalty.get(regime, regime_conf)
    return max(0.0, min(1.0, base))


def _edge_score(edge: float) -> float:
    if edge <= 0:
        return 0.0
    return min(1.0, edge / 30.0)


def compute_confidence(
    sample_size:  int,
    std_dev:      float | None,
    regime:       str,
    edge:         float,
    regime_conf:  float = 0.6,
) -> tuple[float, list[str]]:
    """Returns (confidence_score 0-1, list_of_reason_strings)."""
    ss = _sample_score(sample_size)
    vs = _variance_score(std_dev)
    rs = _regime_score(regime, regime_conf)
    es = _edge_score(abs(edge))

    score = round(0.30 * ss + 0.30 * vs + 0.25 * rs + 0.15 * es, 4)
    score = max(0.0, min(1.0, score))

    reasons = [
        f"Sample size n={sample_size}: score={ss:.2f} (weight 30%)",
        f"Std dev σ={std_dev or 'N/A'}: score={vs:.2f} (weight 30%)",
        f"Regime={regime} conf={regime_conf:.2f}: score={rs:.2f} (weight 25%)",
        f"Edge={edge:+.1f}¢: score={es:.2f} (weight 15%)",
        f"→ Composite confidence: {score:.2%}",
    ]

    if regime in ("OFFSHORE_FLOW", "DRY_HEAT", "HEAT_SPIKE_RISK"):
        reasons.append(f"Note: {regime} can produce large swings — verify with live METAR")
    if sample_size < 10:
        reasons.append("Warning: low sample size — results may not be stable yet")
    if std_dev and std_dev > 4:
        reasons.append("Warning: high historical variance — wide probability distribution")

    return score, reasons
