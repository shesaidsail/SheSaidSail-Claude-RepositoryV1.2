"""
Regime-aware bias engine.

Computes model stats for:
  'ALL'          — global across every regime (always computed)
  <regime_name>  — per-regime, when ≥ 2 paired records exist

Called automatically by settle_daily.py after each settlement.
"""

import sqlite3
import statistics
from datetime import datetime, timezone

from scipy.stats import norm
from models.confidence_engine import compute_confidence


# ---------------------------------------------------------------------------
# Core compute / store
# ---------------------------------------------------------------------------

def compute_and_store_stats(station: str, model: str, conn: sqlite3.Connection) -> dict:
    """
    Fetch all settled (forecast, actual, regime) triples, compute stats for 'ALL'
    and each regime, upsert model_stats.  Returns {regime: stats_dict}.
    """
    rows = conn.execute("""
        SELECT
            ds.settlement_date,
            COALESCE(ds.regime, 'UNKNOWN') AS regime,
            fr.forecast_high,
            ds.official_high,
            ROUND(ds.official_high - fr.forecast_high, 2) AS error
        FROM daily_settlements ds
        JOIN forecast_runs fr
            ON  fr.forecast_date = ds.settlement_date
            AND fr.station_code  = ds.station_code
            AND fr.model_name    = ?
        WHERE ds.station_code = ?
        ORDER BY ds.settlement_date DESC
    """, (model, station)).fetchall()

    if not rows:
        return {}

    all_errors: list[float] = [r["error"] for r in rows]
    by_regime:  dict[str, list[float]] = {}
    for r in rows:
        by_regime.setdefault(r["regime"], []).append(r["error"])

    results: dict = {}

    def _upsert(regime: str, errors: list[float], regime_conf: float = 0.6) -> dict | None:
        if len(errors) < 2:
            return None
        avg  = round(statistics.mean(errors), 4)
        std  = round(statistics.stdev(errors), 4)
        n    = len(errors)
        r7   = round(statistics.mean(errors[:7]),  4) if len(errors[:7])  >= 2 else None
        r30  = round(statistics.mean(errors[:30]), 4) if len(errors[:30]) >= 2 else None
        conf, _ = compute_confidence(n, std, regime, edge=0.0, regime_conf=regime_conf)
        now  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        stats = {
            "station_code": station, "model_name": model, "regime": regime,
            "avg_bias": avg, "std_dev": std, "sample_size": n,
            "rolling_7d_bias": r7, "rolling_30d_bias": r30,
            "confidence": conf, "updated_at": now,
        }
        conn.execute("""
            INSERT INTO model_stats
                (station_code, model_name, regime, avg_bias, std_dev, sample_size,
                 rolling_7d_bias, rolling_30d_bias, confidence, updated_at)
            VALUES
                (:station_code, :model_name, :regime, :avg_bias, :std_dev, :sample_size,
                 :rolling_7d_bias, :rolling_30d_bias, :confidence, :updated_at)
            ON CONFLICT(station_code, model_name, regime) DO UPDATE SET
                avg_bias         = excluded.avg_bias,
                std_dev          = excluded.std_dev,
                sample_size      = excluded.sample_size,
                rolling_7d_bias  = excluded.rolling_7d_bias,
                rolling_30d_bias = excluded.rolling_30d_bias,
                confidence       = excluded.confidence,
                updated_at       = excluded.updated_at
        """, stats)
        conn.commit()
        return stats

    r_all = _upsert("ALL", all_errors)
    if r_all:
        results["ALL"] = r_all
    for regime, errors in by_regime.items():
        r = _upsert(regime, errors)
        if r:
            results[regime] = r

    return results


# ---------------------------------------------------------------------------
# Read helpers
# ---------------------------------------------------------------------------

def get_stats(
    station: str, model: str, regime: str, conn: sqlite3.Connection
) -> dict | None:
    """
    Return regime-specific stats.  Falls back to 'ALL' when regime has < 5 samples.
    The returned dict includes a 'regime_note' key to explain any fallback.
    """
    row = conn.execute(
        "SELECT * FROM model_stats WHERE station_code=? AND model_name=? AND regime=?",
        (station, model, regime),
    ).fetchone()

    if row and (row["sample_size"] or 0) >= 5:
        d = dict(row)
        d["regime_note"] = None
        return d

    row_all = conn.execute(
        "SELECT * FROM model_stats WHERE station_code=? AND model_name=? AND regime='ALL'",
        (station, model),
    ).fetchone()

    if row_all:
        d = dict(row_all)
        n_regime = row["sample_size"] if row else 0
        d["regime_note"] = (
            f"Using global stats — regime '{regime}' has only {n_regime} sample(s) (need ≥ 5)"
        )
        return d
    return None


def all_regime_stats(station: str, model: str, conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT * FROM model_stats
        WHERE station_code = ? AND model_name = ?
        ORDER BY regime
    """, (station, model)).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Probability
# ---------------------------------------------------------------------------

def win_probability(
    adjusted_forecast: float, std_dev: float, threshold: float, side: str
) -> float:
    """
    P(contract wins) with whole-degree settlement correction (T+0.5 cutoff).

    Yes >T wins when actual >= T+1  →  1 - CDF(T+0.5)
    No  >T wins when actual <= T    →  CDF(T+0.5)
    """
    cutoff = threshold + 0.5
    if side.lower() == "yes":
        return 1.0 - norm.cdf(cutoff, loc=adjusted_forecast, scale=std_dev)
    elif side.lower() == "no":
        return norm.cdf(cutoff, loc=adjusted_forecast, scale=std_dev)
    raise ValueError("side must be 'Yes' or 'No'")
