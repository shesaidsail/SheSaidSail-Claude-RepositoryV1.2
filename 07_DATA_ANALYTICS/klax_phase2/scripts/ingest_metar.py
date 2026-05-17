"""
Fetch KLAX METAR observations from aviationweather.gov and store in the database.

CLI:      python scripts/ingest_metar.py [--hours 2] [--station KLAX]
Cron:     0 * * * *  cd /path/to/klax_phase2 && python scripts/ingest_metar.py
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from datetime import datetime, timezone

from database.db import get_connection, init_db
from config import STATION

METAR_URL = "https://aviationweather.gov/api/data/metar"


def celsius_to_f(c: float) -> float:
    return round(c * 9.0 / 5.0 + 32.0, 1)


def fetch_metar(station: str, hours: int = 2) -> list[dict]:
    resp = requests.get(
        METAR_URL,
        params={"ids": station, "format": "json", "hours": hours},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError(f"Unexpected API response type: {type(data)}")
    return data


def parse_observation(raw: dict, station: str) -> dict | None:
    if raw.get("temp") is None:
        return None

    # Prefer Unix obsTime; fall back to receiptTime string
    obs_ts = raw.get("obsTime")
    if obs_ts:
        ts = datetime.fromtimestamp(int(obs_ts), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        receipt = raw.get("receiptTime", "")
        ts = receipt.replace(" ", "T")
        if not ts.endswith("Z"):
            ts += "Z"
        if not ts:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Wind direction may be integer degrees or the string "VRB"
    wdir = raw.get("wdir")
    wind_dir = str(wdir) if wdir is not None else None

    # Cloud cover: use lowest reported layer, or CLR
    clouds = raw.get("clouds") or []
    cloud_cover = clouds[0].get("cover", "CLR") if clouds else "CLR"

    return {
        "timestamp_utc":  ts,
        "station_code":   raw.get("icaoId", station),
        "observed_temp":  celsius_to_f(float(raw["temp"])),
        "wind_direction": wind_dir,
        "wind_speed":     float(raw["wspd"]) if raw.get("wspd") is not None else None,
        "cloud_cover":    cloud_cover,
    }


def store_observation(obs: dict, conn) -> bool:
    """Returns True if inserted (new), False if timestamp already exists."""
    try:
        conn.execute("""
            INSERT INTO actual_observations
                (timestamp_utc, station_code, observed_temp, wind_direction, wind_speed, cloud_cover)
            VALUES
                (:timestamp_utc, :station_code, :observed_temp, :wind_direction, :wind_speed, :cloud_cover)
        """, obs)
        conn.commit()
        return True
    except Exception:
        return False


def run(station: str = STATION, hours: int = 2) -> int:
    """Fetch and store METAR observations. Returns count of new rows inserted."""
    init_db()
    raw_list = fetch_metar(station, hours)
    inserted = 0
    with get_connection() as conn:
        for raw in raw_list:
            obs = parse_observation(raw, station)
            if obs and store_observation(obs, conn):
                inserted += 1
                print(
                    f"  Stored {obs['timestamp_utc']}  "
                    f"{obs['observed_temp']}°F  "
                    f"wind {obs['wind_direction']}° @ {obs['wind_speed']} kts  "
                    f"{obs['cloud_cover']}"
                )
    return inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest KLAX METAR observations")
    parser.add_argument("--station", default=STATION)
    parser.add_argument("--hours",   type=int, default=2, help="Fetch last N hours of METARs")
    args = parser.parse_args()

    try:
        n = run(args.station, args.hours)
        print(f"Done: {n} new observation(s) stored for {args.station}.")
    except requests.RequestException as e:
        print(f"METAR fetch failed: {e}", file=sys.stderr)
        sys.exit(1)
