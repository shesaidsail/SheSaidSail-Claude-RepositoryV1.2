"""
Bias engine — computes and stores model accuracy statistics.

Called automatically after each daily settlement via settle_daily.py.
All other modules that need probability estimates import win_probability() from here.
"""

import sqlite3
import statistics
from datetime import datetime, timezone

from scipy.stats import norm


def compute_and_store_stats(station: str, model: str, conn: sqlite3.Connection) -> dict | None:
    """
    Join settled forecasts with actuals, compute bias stats, upsert model_stats.
    Returns the stats dict, or None if fewer than 2 paired records exist.
    """
    rows = conn.execute("""
        SELECT
            ds.settlement_date,
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

    if len(rows) < 2:
        return None

    errors     = [r["error"] for r in rows]
    recent_7d  = [r["error"] for r in rows[:7]]
    recent_30d = [r["error"] for r in rows[:30]]

    stats = {
        "station_code":     station,
        "model_name":       model,
        "avg_bias":         round(statistics.mean(errors), 4),
        "std_dev":          round(statistics.stdev(errors), 4),
        "sample_size":      len(errors),
        "rolling_7d_bias":  round(statistics.mean(recent_7d),  4) if len(recent_7d)  >= 2 else None,
        "rolling_30d_bias": round(statistics.mean(recent_30d), 4) if len(recent_30d) >= 2 else None,
        "updated_at":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    conn.execute("""
        INSERT INTO model_stats
            (station_code, model_name, avg_bias, std_dev, sample_size,
             rolling_7d_bias, rolling_30d_bias, updated_at)
        VALUES
            (:station_code, :model_name, :avg_bias, :std_dev, :sample_size,
             :rolling_7d_bias, :rolling_30d_bias, :updated_at)
        ON CONFLICT(station_code, model_name) DO UPDATE SET
            avg_bias         = excluded.avg_bias,
            std_dev          = excluded.std_dev,
            sample_size      = excluded.sample_size,
            rolling_7d_bias  = excluded.rolling_7d_bias,
            rolling_30d_bias = excluded.rolling_30d_bias,
            updated_at       = excluded.updated_at
    """, stats)
    conn.commit()
    return stats


def get_stats(station: str, model: str, conn: sqlite3.Connection) -> dict | None:
    row = conn.execute(
        "SELECT * FROM model_stats WHERE station_code = ? AND model_name = ?",
        (station, model),
    ).fetchone()
    return dict(row) if row else None


def win_probability(adjusted_forecast: float, std_dev: float, threshold: float, side: str) -> float:
    """
    P(contract wins) using whole-degree settlement logic (T + 0.5 cutoff).

    Markets settle on integer official highs:
      Yes >T wins when actual >= T+1  →  1 - CDF(T+0.5)
      No  >T wins when actual <= T    →  CDF(T+0.5)
    """
    cutoff = threshold + 0.5
    if side.lower() == "yes":
        return 1.0 - norm.cdf(cutoff, loc=adjusted_forecast, scale=std_dev)
    elif side.lower() == "no":
        return norm.cdf(cutoff, loc=adjusted_forecast, scale=std_dev)
    raise ValueError("side must be 'Yes' or 'No'")
