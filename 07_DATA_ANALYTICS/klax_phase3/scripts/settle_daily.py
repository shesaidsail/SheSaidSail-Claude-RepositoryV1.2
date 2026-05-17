"""
Settle KLAX daily high/low and retrain the model.

Usage:
  python scripts/settle_daily.py                       # settles yesterday
  python scripts/settle_daily.py --date 2026-05-17     # specific date
  python scripts/settle_daily.py --manual 84.0         # NWS official high override
  python scripts/settle_daily.py --date 2026-05-17 --manual 84.0 --manual-low 62.0

After storing the settlement the script:
  1. Classifies the day's weather regime from afternoon observations
  2. Logs the regime to weather_regimes table
  3. Retrains model_stats (ALL + per-regime)
"""

import sys
import json
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, datetime, timedelta, timezone

from database.db import get_connection, init_db
from models.regime_engine import classify, parse_cloud_layers
from models.bias_engine import compute_and_store_stats
from config import STATION, DEFAULT_MODEL, KLAX_UTC_OFFSET_HOURS


# ---------------------------------------------------------------------------
# UTC window for a local date
# ---------------------------------------------------------------------------

def _utc_window(local_date: str) -> tuple[str, str]:
    """
    Convert a KLAX local date to the UTC window for METAR queries.
    PDT (UTC-7): 2026-05-17 local = 2026-05-17T07:00:00Z → 2026-05-18T07:00:00Z
    """
    midnight = datetime.strptime(local_date, "%Y-%m-%d")
    utc_start = midnight + timedelta(hours=-KLAX_UTC_OFFSET_HOURS)
    utc_end   = utc_start + timedelta(days=1)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    return utc_start.strftime(fmt), utc_end.strftime(fmt)


# ---------------------------------------------------------------------------
# Regime classification from day's METAR obs
# ---------------------------------------------------------------------------

def _classify_day(local_date: str, station: str, conn) -> tuple[str, float, dict]:
    """
    Pick representative afternoon observations (10 AM–3 PM local) and classify regime.
    Falls back to any obs if afternoon data is absent.
    Returns (regime, confidence, regime_inputs_dict).
    """
    utc_start, utc_end = _utc_window(local_date)

    # Afternoon window in UTC
    midnight = datetime.strptime(local_date, "%Y-%m-%d")
    aft_start = (midnight + timedelta(hours=10 - KLAX_UTC_OFFSET_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    aft_end   = (midnight + timedelta(hours=15 - KLAX_UTC_OFFSET_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")

    rows = conn.execute("""
        SELECT observed_temp, dewpoint, wind_direction, wind_speed, cloud_layers, visibility, timestamp_utc
        FROM actual_observations
        WHERE station_code = ?
          AND timestamp_utc >= ?
          AND timestamp_utc <  ?
        ORDER BY observed_temp DESC
        LIMIT 5
    """, (station, aft_start, aft_end)).fetchall()

    if not rows:
        # Fall back to all obs for the day
        rows = conn.execute("""
            SELECT observed_temp, dewpoint, wind_direction, wind_speed, cloud_layers, visibility, timestamp_utc
            FROM actual_observations
            WHERE station_code = ?
              AND timestamp_utc >= ?
              AND timestamp_utc <  ?
            ORDER BY timestamp_utc
            LIMIT 10
        """, (station, utc_start, utc_end)).fetchall()

    if not rows:
        return "UNKNOWN", 0.0, {}

    # Use the hottest afternoon observation as representative
    rep = dict(rows[0])
    temp_f = rep.get("observed_temp") or 70.0
    dewp_f = rep.get("dewpoint")
    dps    = round(temp_f - dewp_f, 1) if dewp_f is not None else None

    cover, base_ft = parse_cloud_layers(rep.get("cloud_layers"))

    # Parse local hour from UTC timestamp
    try:
        utc_dt     = datetime.strptime(rep["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
        local_hour = (utc_dt.hour + KLAX_UTC_OFFSET_HOURS) % 24
    except Exception:
        local_hour = 12

    month = int(local_date[5:7])

    result = classify(
        wind_direction    = rep.get("wind_direction"),
        wind_speed        = rep.get("wind_speed"),
        cloud_layers_json = rep.get("cloud_layers"),
        visibility_sm     = rep.get("visibility"),
        dewpoint_spread_f = dps,
        obs_hour_local    = local_hour,
        month             = month,
    )

    inputs = {
        "wind_direction": rep.get("wind_direction"),
        "wind_speed":     rep.get("wind_speed"),
        "cloud_cover":    cover,
        "cloud_base_ft":  base_ft,
        "dewpoint_spread":dps,
        "visibility":     rep.get("visibility"),
        "notes":          " | ".join(result.notes),
    }
    return result.regime, result.confidence, inputs


# ---------------------------------------------------------------------------
# Daily high / low from METAR obs
# ---------------------------------------------------------------------------

def compute_daily_high_low(local_date: str, station: str, conn) -> tuple[float | None, float | None]:
    utc_start, utc_end = _utc_window(local_date)
    row = conn.execute("""
        SELECT MAX(observed_temp) AS mx, MIN(observed_temp) AS mn
        FROM actual_observations
        WHERE station_code  = ?
          AND timestamp_utc >= ?
          AND timestamp_utc <  ?
    """, (station, utc_start, utc_end)).fetchone()
    return (row["mx"] if row else None, row["mn"] if row else None)


# ---------------------------------------------------------------------------
# Store settlement
# ---------------------------------------------------------------------------

def store_settlement(
    local_date: str, station: str, high: float,
    low: float | None, source: str, regime: str | None, conn
) -> None:
    conn.execute("""
        INSERT INTO daily_settlements (settlement_date, station_code, official_high, official_low, source, regime)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(settlement_date, station_code) DO UPDATE SET
            official_high = excluded.official_high,
            official_low  = excluded.official_low,
            source        = excluded.source,
            regime        = excluded.regime
    """, (local_date, station, high, low, source, regime))
    conn.commit()


def log_regime(local_date: str, station: str, regime: str, conf: float, inputs: dict, conn) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("""
        INSERT INTO weather_regimes
            (timestamp_utc, settlement_date, station_code, regime, confidence,
             wind_direction, wind_speed, cloud_cover, cloud_base_ft,
             dewpoint_spread, visibility, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        ts, local_date, station, regime, conf,
        inputs.get("wind_direction"), inputs.get("wind_speed"),
        inputs.get("cloud_cover"),    inputs.get("cloud_base_ft"),
        inputs.get("dewpoint_spread"), inputs.get("visibility"),
        inputs.get("notes"),
    ))
    conn.commit()


# ---------------------------------------------------------------------------
# Main settlement function
# ---------------------------------------------------------------------------

def settle(
    local_date:   str,
    station:      str   = STATION,
    manual_high:  float | None = None,
    manual_low:   float | None = None,
) -> dict:
    init_db()
    with get_connection() as conn:
        if manual_high is not None:
            official_high = manual_high
            official_low  = manual_low
            source = "manual_nws"
        else:
            high, low = compute_daily_high_low(local_date, station, conn)
            if high is None:
                raise ValueError(
                    f"No METAR observations for {station} on {local_date}. "
                    "Run `python scripts/ingest_metar.py` first, or pass --manual <temp>."
                )
            official_high = high
            official_low  = low
            source = "computed_from_metar"

        regime, regime_conf, regime_inputs = _classify_day(local_date, station, conn)
        store_settlement(local_date, station, official_high, official_low, source, regime, conn)
        log_regime(local_date, station, regime, regime_conf, regime_inputs, conn)
        all_stats = compute_and_store_stats(station, DEFAULT_MODEL, conn)

    return {
        "settlement_date": local_date,
        "official_high":   official_high,
        "official_low":    official_low,
        "source":          source,
        "regime":          regime,
        "regime_conf":     regime_conf,
        "regime_notes":    regime_inputs.get("notes", ""),
        "stats":           all_stats,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    yesterday = str(date.today() - timedelta(days=1))
    parser = argparse.ArgumentParser(description="Settle KLAX daily high and retrain model")
    parser.add_argument("--date",       default=yesterday, help="YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--manual",     type=float, default=None, help="Official NWS high °F")
    parser.add_argument("--manual-low", type=float, default=None, dest="manual_low",
                        help="Official NWS low °F")
    parser.add_argument("--station",    default=STATION)
    args = parser.parse_args()

    try:
        r = settle(args.date, args.station, args.manual, args.manual_low)
        low_str = f" / low {r['official_low']:.0f}°F" if r["official_low"] else ""
        print(f"Settled {r['settlement_date']}: high {r['official_high']:.0f}°F{low_str} ({r['source']})")
        print(f"Regime: {r['regime']} (conf {r['regime_conf']:.0%}) — {r['regime_notes']}")
        if r["stats"].get("ALL"):
            s = r["stats"]["ALL"]
            print(
                f"Global model — bias: {s['avg_bias']:+.2f}°F  "
                f"σ: {s['std_dev']:.2f}°F  n={s['sample_size']}"
            )
        n_regimes = len([k for k in r["stats"] if k != "ALL"])
        if n_regimes:
            print(f"Regime-specific stats updated for {n_regimes} regime(s).")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
