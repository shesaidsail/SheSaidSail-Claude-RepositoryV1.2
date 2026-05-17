"""
KLAX METAR Ingestion

Fetches from aviationweather.gov and stores all extended observation fields.

CLI usage:
  python scripts/ingest_metar.py             # single fetch
  python scripts/ingest_metar.py --loop      # poll every 60 s (Ctrl-C to stop)
  python scripts/ingest_metar.py --hours 24  # backfill last 24 hours

Cron (single fetch each minute):
  * * * * *  cd /path/to/klax_phase3 && python scripts/ingest_metar.py >> logs/metar.log 2>&1
"""

import sys
import json
import time
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from datetime import datetime, timezone

from database.db import get_connection, init_db
from config import STATION, METAR_URL, METAR_POLL_INTERVAL


# ---------------------------------------------------------------------------
# Unit conversion helpers
# ---------------------------------------------------------------------------

def c_to_f(c: float) -> float:
    return round(c * 9.0 / 5.0 + 32.0, 1)


def hpa_to_inhg(hpa: float) -> float:
    return round(hpa * 0.02953, 2)


# ---------------------------------------------------------------------------
# API fetch
# ---------------------------------------------------------------------------

def fetch_metar(station: str, hours: int = 2) -> list[dict]:
    resp = requests.get(
        METAR_URL,
        params={"ids": station, "format": "json", "hours": hours},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError(f"Unexpected API response: {type(data)}")
    return data


# ---------------------------------------------------------------------------
# Parse one METAR JSON object into our DB row
# ---------------------------------------------------------------------------

def parse_observation(raw: dict, station: str) -> dict | None:
    if raw.get("temp") is None:
        return None  # skip obs with no temperature

    # Timestamp
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

    # Wind — direction may be integer or "VRB"
    wdir_raw = raw.get("wdir")
    try:
        wind_dir = float(wdir_raw) if wdir_raw not in (None, "VRB") else None
    except (TypeError, ValueError):
        wind_dir = None

    # Cloud layers → JSON string
    clouds_raw = raw.get("clouds") or []
    cloud_layers = json.dumps([
        {"cover": c.get("cover", "CLR"), "base": c.get("base")}
        for c in clouds_raw
    ]) if clouds_raw else json.dumps([])

    # Pressure: prefer slp (sea level), fall back to altimeter converted
    pressure = None
    if raw.get("slp") is not None:
        pressure = round(float(raw["slp"]), 1)
    elif raw.get("altim") is not None:
        pressure = round(float(raw["altim"]), 1)

    # 6-hour / 24-hour max/min temps from METAR remarks (if provided by API)
    max6  = c_to_f(float(raw["maxT"]))   if raw.get("maxT")   is not None else None
    min6  = c_to_f(float(raw["minT"]))   if raw.get("minT")   is not None else None
    max24 = c_to_f(float(raw["maxT24"])) if raw.get("maxT24") is not None else None

    return {
        "timestamp_utc":  ts,
        "station_code":   raw.get("icaoId", station),
        "observed_temp":  c_to_f(float(raw["temp"])),
        "dewpoint":       c_to_f(float(raw["dewp"])) if raw.get("dewp") is not None else None,
        "wind_direction": wind_dir,
        "wind_speed":     float(raw["wspd"]) if raw.get("wspd") is not None else None,
        "gust_speed":     float(raw["wgst"]) if raw.get("wgst") is not None else None,
        "cloud_layers":   cloud_layers,
        "visibility":     float(raw["visib"]) if raw.get("visib") not in (None, "10+") else 10.0,
        "pressure":       pressure,
        "weather_string": raw.get("wxString"),
        "raw_metar":      raw.get("rawOb"),
        "max_temp_6h":    max6,
        "min_temp_6h":    min6,
        "max_temp_24h":   max24,
    }


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

def store_observation(obs: dict, conn) -> bool:
    """Returns True if new row inserted (UNIQUE on timestamp_utc)."""
    try:
        conn.execute("""
            INSERT INTO actual_observations (
                timestamp_utc, station_code, observed_temp, dewpoint,
                wind_direction, wind_speed, gust_speed, cloud_layers,
                visibility, pressure, weather_string, raw_metar,
                max_temp_6h, min_temp_6h, max_temp_24h
            ) VALUES (
                :timestamp_utc, :station_code, :observed_temp, :dewpoint,
                :wind_direction, :wind_speed, :gust_speed, :cloud_layers,
                :visibility, :pressure, :weather_string, :raw_metar,
                :max_temp_6h, :min_temp_6h, :max_temp_24h
            )
        """, obs)
        conn.commit()
        return True
    except Exception:
        return False  # duplicate timestamp


# ---------------------------------------------------------------------------
# Single-run fetch
# ---------------------------------------------------------------------------

def run(station: str = STATION, hours: int = 2) -> int:
    """Fetch and store. Returns count of new observations inserted."""
    init_db()
    raw_list = fetch_metar(station, hours)
    inserted = 0
    with get_connection() as conn:
        for raw in raw_list:
            obs = parse_observation(raw, station)
            if obs and store_observation(obs, conn):
                inserted += 1
                gust = f" gust {obs['gust_speed']:.0f}" if obs["gust_speed"] else ""
                print(
                    f"  {obs['timestamp_utc']}  "
                    f"{obs['observed_temp']}°F  "
                    f"wind {obs['wind_direction']}°@{obs['wind_speed']}{gust} kts  "
                    f"{obs['cloud_layers']}"
                )
    return inserted


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest KLAX METAR observations")
    parser.add_argument("--station", default=STATION)
    parser.add_argument("--hours",   type=int, default=2,
                        help="Fetch last N hours of METARs (default 2)")
    parser.add_argument("--loop",    action="store_true",
                        help=f"Poll continuously every {METAR_POLL_INTERVAL} s (Ctrl-C to stop)")
    args = parser.parse_args()

    if args.loop:
        print(f"Starting METAR loop — polling every {METAR_POLL_INTERVAL} s.  Ctrl-C to stop.")
        while True:
            try:
                n = run(args.station, args.hours)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {n} new observation(s) stored.")
            except requests.RequestException as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetch failed: {e}", file=sys.stderr)
            time.sleep(METAR_POLL_INTERVAL)
    else:
        try:
            n = run(args.station, args.hours)
            print(f"Done: {n} new observation(s) for {args.station}.")
        except requests.RequestException as e:
            print(f"METAR fetch failed: {e}", file=sys.stderr)
            sys.exit(1)
