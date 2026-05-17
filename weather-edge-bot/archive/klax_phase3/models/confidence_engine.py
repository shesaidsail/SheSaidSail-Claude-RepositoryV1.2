"""
Confidence Engine

Combines four factors into a single 0–1 score and a plain-English explanation:

  30%  Sample size     — saturates at n=30
  30%  Variance        — penalizes σ > 4°F; rewards σ < 1.5°F
  25%  Regime clarity  — passes through regime_classification_confidence
  15%  Edge magnitude  — large edges carry more signal

A score ≥ 0.60 is required before a BET recommendation is issued.
"""

from config import MIN_SAMPLE_SIZE, BET_EDGE_THRESHOLD


def compute_confidence(
    sample_size:  int,
    std_dev:      float | None,
    regime:       str,
    edge:         float,
    regime_conf:  float = 0.5,
) -> tuple[float, list[str]]:
    """
    Returns (confidence_score 0-1, reasons list).
    """
    reasons: list[str] = []

    # ---- Sample size (0-1, saturates at 30) ----
    n_score = min(sample_size / 30.0, 1.0)
    if sample_size < MIN_SAMPLE_SIZE:
        reasons.append(
            f"Low sample size (n={sample_size}, target ≥{MIN_SAMPLE_SIZE}) — "
            "treat as provisional; do not size up"
        )
    elif sample_size >= 30:
        reasons.append(f"Strong sample base (n={sample_size})")
    else:
        reasons.append(f"Growing sample base (n={sample_size})")

    # ---- Variance (0-1, σ=0 → 1.0, σ≥4 → 0.0) ----
    if std_dev is not None:
        variance_score = max(1.0 - std_dev / 4.0, 0.0)
        if std_dev < 1.5:
            reasons.append(f"Low variance (σ={std_dev:.2f}°F) — high predictability")
        elif std_dev > 3.0:
            reasons.append(
                f"High variance (σ={std_dev:.2f}°F) — wide uncertainty; "
                "widen confidence intervals and size down"
            )
        else:
            reasons.append(f"Moderate variance (σ={std_dev:.2f}°F)")
    else:
        variance_score = 0.20
        reasons.append("No variance data yet — minimal confidence, do not bet")

    # ---- Regime clarity ----
    regime_score = regime_conf
    if regime == "HIGH_VARIANCE":
        reasons.append("HIGH_VARIANCE regime — ambiguous signals, avoid unless edge is very large")
    elif regime == "OFFSHORE_FLOW":
        reasons.append("OFFSHORE_FLOW — strong consistent bias; regime is well-defined")
    elif regime in ("CLEAR_SKY", "LOW_VARIANCE"):
        reasons.append(f"{regime} — stable conditions, model reliable")

    # ---- Edge magnitude (0-1, saturates at 4× bet threshold) ----
    edge_score = min(abs(edge) / (BET_EDGE_THRESHOLD * 4.0), 1.0)
    if abs(edge) < BET_EDGE_THRESHOLD:
        reasons.append(
            f"Edge {edge:+.1f}¢ is below the {BET_EDGE_THRESHOLD:.0f}¢ bet threshold — "
            "not actionable; PASS or monitor"
        )
    elif abs(edge) >= BET_EDGE_THRESHOLD * 2:
        reasons.append(f"Large edge ({edge:+.1f}¢) — material mispricing detected")
    else:
        reasons.append(f"Marginal edge ({edge:+.1f}¢) — meets threshold, size small")

    # ---- Weighted sum ----
    score = (
        0.30 * n_score
        + 0.30 * variance_score
        + 0.25 * regime_score
        + 0.15 * edge_score
    )
    score = round(min(max(score, 0.0), 1.0), 3)

    if score >= 0.70:
        reasons.append("Confidence: HIGH — full recommended size")
    elif score >= 0.55:
        reasons.append("Confidence: MEDIUM — half size or monitor closely")
    else:
        reasons.append("Confidence: LOW — do not bet; accumulate more data")

    return score, reasons
