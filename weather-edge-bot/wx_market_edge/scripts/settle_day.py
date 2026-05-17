"""
Daily settlement script.

For each active station:
  1. Compute official high from METAR observations (or accept manual override)
  2. Classify the day's regime from afternoon observations
  3. Upsert daily_settlements
  4. Retrain model stats
  5. Settle open paper trades
  6. Log alert

Usage:
  python scripts/settle_day.py                     # settle yesterday for all stations
  python scripts/settle_day.py --date 2026-05-17   # specific date
  python scripts/settle_day.py --station KLAX --high 74 --low 63
"""

import sys
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta, date as dt_date

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db      import init_db
from ingestion.metar  import get_obs_for_date
from models.regime_engine   import classify_from_metar
from models.bias_engine     import compute_and_store_stats
from trading.paper_trader   import settle_trades
from config import STATIONS, DEFAULT_MODEL


def _compute_high_from_metar(obs_list: list[dict]) -> float | None:
    """Return max observed_temp across all obs on the date."""
    temps = [o["observed_temp"] for o in obs_list if o.get("observed_temp") is not None]
    return round(max(temps), 1) if temps else None


def _compute_low_from_metar(obs_list: list[dict]) -> float | None:
    temps = [o["observed_temp"] for o in obs_list if o.get("observed_temp") is not None]
    return round(min(temps), 1) if temps else None


def _classify_day_regime(obs_list: list[dict], utc_offset: int) -> str:
    """Use afternoon (10 AM–3 PM local) obs to classify the day's regime."""
    afternoon = []
    for o in obs_list:
        try:
            ts = datetime.strptime(o["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
            local_h = (ts.hour + utc_offset) % 24
            if 10 <= local_h <= 15:
                afternoon.append((o, local_h))
        except Exception:
            pass

    if not afternoon:
        afternoon = [(o, 12) for o in obs_list]

    if not afternoon:
        return "UNKNOWN"

    # Pick obs closest to 1 PM local
    best = min(afternoon, key=lambda x: abs(x[1] - 13))
    r = classify_from_metar(best[0], best[1])
    return r.regime


def settle_station(
    station: str,
    date: str,
    conn: sqlite3.Connection,
    manual_high: float | None = None,
    manual_low:  float | None = None,
) -> dict:
    utc_off  = STATIONS[station]["utc_offset"]
    obs_list = get_obs_for_date(station, date, utc_off, conn)

    official_high = manual_high or _compute_high_from_metar(obs_list)
    official_low  = manual_low  or _compute_low_from_metar(obs_list)
    regime        = _classify_day_regime(obs_list, utc_off)

    if official_high is None:
        return {"station": station, "date": date, "status": "NO_DATA"}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("""
        INSERT INTO daily_settlements (settlement_date, station_code, official_high, official_low, regime)
        VALUES (?,?,?,?,?)
        ON CONFLICT(settlement_date, station_code) DO UPDATE SET
            official_high=excluded.official_high,
            official_low=excluded.official_low,
            regime=excluded.regime,
            settled_at=?
    """, (date, station, official_high, official_low, regime, now))
    conn.commit()

    # Retrain
    stats = compute_and_store_stats(station, DEFAULT_MODEL, conn)

    # Settle paper trades
    settled_trades = settle_trades(date, conn)

    # Alert
    conn.execute("""
        INSERT INTO alerts (station_code, alert_type, message)
        VALUES (?,?,?)
    """, (station, "SETTLEMENT",
          f"{station} settled {date}: high={official_high}°F, low={official_low}°F, regime={regime}"))
    conn.commit()

    return {
        "station":       station,
        "date":          date,
        "official_high": official_high,
        "official_low":  official_low,
        "regime":        regime,
        "obs_count":     len(obs_list),
        "model_stats":   stats,
        "trades_settled": len(settled_trades),
        "status":        "OK",
    }


def main():
    parser = argparse.ArgumentParser(description="Settle daily weather data")
    parser.add_argument("--date",    default=None, help="Date YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--station", default=None, help="Single ICAO station code")
    parser.add_argument("--high",    type=float, default=None, help="Manual official high °F")
    parser.add_argument("--low",     type=float, default=None, help="Manual official low °F")
    args = parser.parse_args()

    settle_date = args.date or (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")

    conn = init_db()
    stations = [args.station] if args.station else list(STATIONS.keys())

    for station in stations:
        if station not in STATIONS:
            print(f"Unknown station: {station}")
            continue
        r = settle_station(station, settle_date, conn, args.high, args.low)
        if r["status"] == "OK":
            print(f"✓ {station} {settle_date}: high={r['official_high']}°F "
                  f"low={r['official_low']}°F regime={r['regime']} "
                  f"({r['obs_count']} obs, {r['trades_settled']} trades settled)")
        else:
            print(f"✗ {station} {settle_date}: no data")


if __name__ == "__main__":
    main()
