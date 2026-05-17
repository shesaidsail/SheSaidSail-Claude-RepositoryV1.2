"""
Blended bias engine.

For each station + regime pair, computes:
  - global bias (ALL records for this station)
  - regime bias (records for this station in this regime)
  - blended bias: weighted average based on regime sample size

Blending weights:
  n < 5   → 90% global / 10% regime
  5–20    → linear ramp from 10% to 90% regime weight
  > 20    → 90% regime / 10% global
"""

import sqlite3
import statistics
from datetime import datetime, timezone


def _blend_weight(n: int) -> float:
    """Regime weight (0-1) given sample size n."""
    if n < 5:
        return 0.10
    if n > 20:
        return 0.90
    return 0.10 + (n - 5) / 15 * 0.80


def compute_and_store_stats(
    station: str, model: str, conn: sqlite3.Connection
) -> dict:
    """
    Recompute bias stats for all regimes of a station.
    Returns {regime: stats_dict}.
    """
    rows = conn.execute("""
        SELECT
            ds.settlement_date,
            COALESCE(ds.regime, 'UNKNOWN') AS regime,
            fr.temp_max                     AS forecast_high,
            ds.official_high,
            ROUND(ds.official_high - fr.temp_max, 2) AS error
        FROM daily_settlements ds
        JOIN forecast_runs fr
            ON  fr.forecast_date = ds.settlement_date
            AND fr.station_code  = ds.station_code
            AND fr.model_name    = ?
        WHERE ds.station_code = ?
          AND ds.official_high IS NOT NULL
          AND fr.temp_max       IS NOT NULL
        ORDER BY ds.settlement_date DESC
    """, (model, station)).fetchall()

    if not rows:
        return {}

    all_errors: list[float] = [r["error"] for r in rows]
    by_regime:  dict[str, list[float]] = {}
    for r in rows:
        by_regime.setdefault(r["regime"], []).append(r["error"])

    results: dict = {}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _upsert(regime: str, errors: list[float]) -> dict | None:
        if len(errors) < 2:
            return None
        avg  = round(statistics.mean(errors), 4)
        std  = round(statistics.stdev(errors), 4)
        n    = len(errors)
        r7   = round(statistics.mean(errors[:7]),  4) if len(errors) >= 2 else None
        r30  = round(statistics.mean(errors[:30]), 4) if len(errors) >= 2 else None
        conn.execute("""
            INSERT INTO model_stats
                (station_code, model_name, regime, avg_bias, std_dev, sample_size,
                 rolling_7d_bias, rolling_30d_bias, confidence, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(station_code, model_name, regime) DO UPDATE SET
                avg_bias        = excluded.avg_bias,
                std_dev         = excluded.std_dev,
                sample_size     = excluded.sample_size,
                rolling_7d_bias = excluded.rolling_7d_bias,
                rolling_30d_bias= excluded.rolling_30d_bias,
                updated_at      = excluded.updated_at
        """, (station, model, regime, avg, std, n, r7, r30, None, now))
        conn.commit()
        return {"station_code": station, "model_name": model, "regime": regime,
                "avg_bias": avg, "std_dev": std, "sample_size": n,
                "rolling_7d_bias": r7, "rolling_30d_bias": r30, "updated_at": now}

    r_all = _upsert("ALL", all_errors)
    if r_all:
        results["ALL"] = r_all
    for regime, errors in by_regime.items():
        r = _upsert(regime, errors)
        if r:
            results[regime] = r

    return results


def get_stats(
    station: str, model: str, regime: str, conn: sqlite3.Connection
) -> dict | None:
    """
    Return stats for this station/model/regime.
    Falls back to ALL if regime has < 5 samples.
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
            f"Using global stats — '{regime}' has only {n_regime} sample(s) (need ≥ 5)"
        )
        return d
    return None


def blended_bias(
    station: str, model: str, regime: str, conn: sqlite3.Connection
) -> tuple[float, float, str]:
    """
    Returns (bias, std_dev, note).
    Blends global + regime stats per the weight schedule.
    """
    global_row = conn.execute(
        "SELECT * FROM model_stats WHERE station_code=? AND model_name=? AND regime='ALL'",
        (station, model),
    ).fetchone()

    regime_row = conn.execute(
        "SELECT * FROM model_stats WHERE station_code=? AND model_name=? AND regime=?",
        (station, model, regime),
    ).fetchone()

    g_bias = global_row["avg_bias"] if global_row else 0.0
    g_std  = global_row["std_dev"]  if global_row else 3.0
    g_n    = global_row["sample_size"] if global_row else 0

    r_bias = regime_row["avg_bias"] if regime_row else g_bias
    r_std  = regime_row["std_dev"]  if regime_row else g_std
    r_n    = regime_row["sample_size"] if regime_row else 0

    w = _blend_weight(r_n)
    bias = round(w * r_bias + (1 - w) * g_bias, 3)
    std  = round(w * r_std  + (1 - w) * g_std,  3)
    std  = max(std, 0.5)   # floor to prevent degenerate probs

    if r_n == 0:
        note = f"Global only (no regime data): bias={g_bias:+.2f}°F, σ={g_std:.2f}°F (n={g_n})"
    elif r_n < 5:
        note = (f"Mostly global ({100*(1-w):.0f}%): global={g_bias:+.2f}°F "
                f"regime={r_bias:+.2f}°F (n={r_n})")
    elif r_n <= 20:
        note = (f"Blended {100*w:.0f}% regime / {100*(1-w):.0f}% global: "
                f"bias={bias:+.2f}°F (n={r_n})")
    else:
        note = f"Mostly regime ({100*w:.0f}%): bias={r_bias:+.2f}°F, σ={r_std:.2f}°F (n={r_n})"

    return bias, std, note


def all_regime_stats(
    station: str, model: str, conn: sqlite3.Connection
) -> list[dict]:
    rows = conn.execute("""
        SELECT * FROM model_stats
        WHERE station_code=? AND model_name=?
        ORDER BY regime
    """, (station, model)).fetchall()
    return [dict(r) for r in rows]
