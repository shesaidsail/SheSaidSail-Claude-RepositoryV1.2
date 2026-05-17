"""
Compute and store the official KLAX daily high, then retrain the model.

Usage:
    python scripts/settle_daily.py                      # settles yesterday
    python scripts/settle_daily.py --date 2026-05-17    # settles a specific date
    python scripts/settle_daily.py --manual 84.0        # NWS official override (skips METAR max)
    python scripts/settle_daily.py --date 2026-05-17 --manual 84.0

After storing the settlement, model stats (bias, std dev, rolling windows)
are automatically recalculated and saved to model_stats.
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, datetime, timedelta

from database.db import get_connection, init_db
from models.bias_engine import compute_and_store_stats
from config import STATION, DEFAULT_MODEL, KLAX_UTC_OFFSET_HOURS


def compute_daily_high(settlement_date: str, station: str, conn) -> float | None:
    """
    Return the max observed temperature for `settlement_date` in KLAX local time.

    METAR observations are stored as UTC strings.  We shift by KLAX_UTC_OFFSET_HOURS
    to find the correct UTC window that covers midnight-to-midnight local time.
    e.g. PDT (UTC-7): 2026-05-17 local = 2026-05-17T07:00:00Z → 2026-05-18T07:00:00Z
    """
    local_midnight = datetime.strptime(settlement_date, "%Y-%m-%d")
    utc_start = local_midnight + timedelta(hours=-KLAX_UTC_OFFSET_HOURS)
    utc_end   = utc_start + timedelta(days=1)

    row = conn.execute("""
        SELECT MAX(observed_temp) AS max_temp
        FROM actual_observations
        WHERE station_code  = ?
          AND timestamp_utc >= ?
          AND timestamp_utc <  ?
    """, (
        station,
        utc_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        utc_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )).fetchone()

    return row["max_temp"] if row and row["max_temp"] is not None else None


def store_settlement(
    settlement_date: str, station: str, official_high: float, source: str, conn
) -> None:
    conn.execute("""
        INSERT INTO daily_settlements (settlement_date, station_code, official_high, source)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(settlement_date, station_code) DO UPDATE SET
            official_high = excluded.official_high,
            source        = excluded.source
    """, (settlement_date, station, official_high, source))
    conn.commit()


def settle(
    settlement_date: str,
    station: str = STATION,
    manual_high: float | None = None,
) -> dict:
    """
    Core settlement function — importable by the dashboard or called from the CLI.
    Returns a result dict with settlement details and updated model stats.
    """
    init_db()
    with get_connection() as conn:
        if manual_high is not None:
            official_high = manual_high
            source = "manual_nws"
        else:
            official_high = compute_daily_high(settlement_date, station, conn)
            if official_high is None:
                raise ValueError(
                    f"No METAR observations found for {station} on {settlement_date}. "
                    "Run `python scripts/ingest_metar.py` first, or pass --manual <temp>."
                )
            source = "computed_from_metar"

        store_settlement(settlement_date, station, official_high, source, conn)
        stats = compute_and_store_stats(station, DEFAULT_MODEL, conn)

    return {
        "settlement_date": settlement_date,
        "official_high":   official_high,
        "source":          source,
        "stats_updated":   stats is not None,
        "stats":           stats,
    }


if __name__ == "__main__":
    yesterday = str(date.today() - timedelta(days=1))
    parser = argparse.ArgumentParser(description="Settle KLAX daily high and retrain model")
    parser.add_argument("--date",    default=yesterday,
                        help="Settlement date YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--manual",  type=float, default=None,
                        help="Official NWS high °F. Skips METAR max computation.")
    parser.add_argument("--station", default=STATION)
    args = parser.parse_args()

    try:
        r = settle(args.date, args.station, args.manual)
        print(f"Settled {r['settlement_date']}: {r['official_high']}°F ({r['source']})")
        if r["stats_updated"]:
            s = r["stats"]
            print(
                f"Model retrained — bias: {s['avg_bias']:+.2f}°F  "
                f"σ: {s['std_dev']:.2f}°F  n={s['sample_size']}"
            )
        else:
            print("Model not yet retrained — need ≥ 2 paired forecast/settlement records.")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
