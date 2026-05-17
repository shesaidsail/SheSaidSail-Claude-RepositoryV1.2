"""
Signal quality ranking engine.

Grades each edge calculation as:
  A+  — high edge, high confidence, clean data, tight spread, good regime n
  B   — good edge, medium confidence, acceptable conditions
  Watchlist — possible edge but not enough proof
  Avoid — bad data, stale, low confidence, wide spread

Only A+ and B signals should be paper-traded or acted on.
Watchlist items are tracked but not traded.
Avoid items are logged but suppressed from the main view.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MIN_EDGE, MIN_CONFIDENCE, MAX_SPREAD, MIN_REGIME_N

# ── Grade thresholds ──────────────────────────────────────────────────────────
GRADE_A_PLUS = {
    "min_edge":          10.0,
    "min_confidence":    0.70,
    "max_spread":        5.0,
    "min_regime_n":      5,
    "max_metar_age_min": 30,
}

GRADE_B = {
    "min_edge":          5.0,
    "min_confidence":    0.55,
    "max_spread":        8.0,
    "min_regime_n":      3,
    "max_metar_age_min": 90,
}

WATCHLIST = {
    "min_edge":          2.0,
    "min_confidence":    0.40,
    "max_spread":        15.0,
    "min_regime_n":      1,
    "max_metar_age_min": 360,
}


def _metar_age_minutes(station_code: str, conn) -> float | None:
    row = conn.execute("""
        SELECT MAX(timestamp_utc) AS ts FROM official_observations
        WHERE station_code=?
    """, (station_code,)).fetchone()
    if not row or not row["ts"]:
        return None
    try:
        ts = datetime.strptime(row["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - ts).total_seconds() / 60
    except Exception:
        return None


def _regime_n(station_code: str, model: str, regime: str, conn) -> int:
    row = conn.execute("""
        SELECT sample_size FROM model_stats
        WHERE station_code=? AND model_name=? AND regime=?
    """, (station_code, model, regime)).fetchone()
    return (row["sample_size"] or 0) if row else 0


def _forecast_distance(forecast_high: float | None, threshold: float) -> float | None:
    """How far is the forecast from the threshold? Signals close to threshold are most meaningful."""
    if forecast_high is None:
        return None
    return abs(forecast_high - threshold)


def grade_signal(edge_result: dict, conn, model: str = "OpenMeteo") -> dict:
    """
    Grade an edge_result dict.

    Adds 'grade', 'grade_reasons', 'quality_flags' to the result and returns it.
    """
    edge       = abs(edge_result.get("edge") or 0)
    confidence = edge_result.get("confidence") or 0
    spread     = edge_result.get("spread")
    station    = edge_result.get("station_code")
    regime     = edge_result.get("regime", "UNKNOWN")
    threshold  = edge_result.get("threshold_f", 0)
    fc_high    = edge_result.get("forecast_high")

    metar_age = _metar_age_minutes(station, conn) if station else None
    regime_n  = _regime_n(station, model, regime, conn) if station else 0
    fc_dist   = _forecast_distance(fc_high, threshold)

    quality_flags = []
    reasons       = []

    # Check data freshness
    if metar_age is None:
        quality_flags.append("NO_METAR")
        reasons.append("No METAR observations — data quality unknown")
    elif metar_age > 120:
        quality_flags.append("STALE_METAR")
        reasons.append(f"METAR is {metar_age:.0f} min old (>120 min threshold)")

    if edge_result.get("forecast_high") is None:
        quality_flags.append("NO_FORECAST")
        reasons.append("No Open-Meteo forecast available")

    # Check regime quality
    if regime == "UNKNOWN":
        quality_flags.append("UNKNOWN_REGIME")
        reasons.append("Regime unclassified — confidence penalised")
    if regime_n == 0:
        quality_flags.append("NO_REGIME_DATA")
        reasons.append(f"No historical data for regime {regime}")

    # Check spread
    if spread is not None and spread > MAX_SPREAD:
        quality_flags.append("WIDE_SPREAD")
        reasons.append(f"Bid/ask spread {spread:.1f}¢ is too wide")

    # Check forecast distance from threshold
    if fc_dist is not None and fc_dist > 8:
        quality_flags.append("FAR_FROM_THRESHOLD")
        reasons.append(f"Forecast {fc_high:.1f}°F is {fc_dist:.1f}°F from threshold — lower probability leverage")

    # Hard stops for Avoid
    hard_stops = {"NO_METAR", "NO_FORECAST", "WIDE_SPREAD"}
    if quality_flags and hard_stops.intersection(set(quality_flags)):
        if "NO_FORECAST" in quality_flags or edge < WATCHLIST["min_edge"]:
            grade = "Avoid"
            reasons.insert(0, "Hard stop: missing critical data")
        else:
            grade = "Watchlist"
            reasons.insert(0, "Quality issue: borderline data")

    # Grade by thresholds
    elif (edge >= GRADE_A_PLUS["min_edge"]
          and confidence >= GRADE_A_PLUS["min_confidence"]
          and (spread is None or spread <= GRADE_A_PLUS["max_spread"])
          and regime_n >= GRADE_A_PLUS["min_regime_n"]
          and (metar_age is None or metar_age <= GRADE_A_PLUS["max_metar_age_min"])):
        grade = "A+"
        reasons.insert(0, "A+ signal: high edge, high confidence, clean data")

    elif (edge >= GRADE_B["min_edge"]
          and confidence >= GRADE_B["min_confidence"]
          and (spread is None or spread <= GRADE_B["max_spread"])
          and regime_n >= GRADE_B["min_regime_n"]
          and (metar_age is None or metar_age <= GRADE_B["max_metar_age_min"])):
        grade = "B"
        reasons.insert(0, "B signal: good edge and confidence, acceptable data")

    elif (edge >= WATCHLIST["min_edge"]
          and confidence >= WATCHLIST["min_confidence"]):
        grade = "Watchlist"
        reasons.insert(0, "Watchlist: edge present but conditions not ideal")

    else:
        grade = "Avoid"
        reasons.insert(0, f"Avoid: edge {edge:.1f}¢ or confidence {confidence:.0%} below minimum")

    edge_result["grade"]         = grade
    edge_result["grade_reasons"] = reasons
    edge_result["quality_flags"] = quality_flags
    edge_result["regime_n"]      = regime_n
    edge_result["metar_age_min"] = metar_age

    return edge_result


def grade_all(results: list[dict], conn, model: str = "OpenMeteo") -> list[dict]:
    """Grade a list of edge results, sort A+ → B → Watchlist → Avoid."""
    graded = [grade_signal(r, conn, model) for r in results]
    order  = {"A+": 0, "B": 1, "Watchlist": 2, "Avoid": 3}
    graded.sort(key=lambda r: (order.get(r.get("grade"), 3), -(abs(r.get("edge") or 0))))
    return graded
