"""
Open-Meteo historical archive fetcher.

The Open-Meteo Historical Weather API provides daily data back to 1940.
Free, no API key required.

Used by the backtesting engine to pull actual forecast-era conditions.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from config import STATIONS

HISTORICAL_BASE = "https://archive-api.open-meteo.com/v1/archive"

DAILY_VARS_HIST = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "wind_direction_10m_dominant", "wind_speed_10m_max", "wind_speed_10m_mean",
    "wind_gusts_10m_max",
    "cloud_cover_mean", "precipitation_sum", "rain_sum", "snowfall_sum",
    "weather_code", "sunshine_duration",
    "dew_point_2m_mean", "relative_humidity_2m_mean", "relative_humidity_2m_max",
    "pressure_msl_mean",
]


def fetch_historical(
    icao: str, date_from: str, date_to: str
) -> dict | None:
    """
    Fetch historical daily weather for a station over a date range.
    Returns the raw Open-Meteo response dict, or None on error.
    """
    s = STATIONS.get(icao)
    if not s:
        return None

    params = {
        "latitude":           s["lat"],
        "longitude":          s["lon"],
        "start_date":         date_from,
        "end_date":           date_to,
        "daily":              ",".join(DAILY_VARS_HIST),
        "temperature_unit":   "fahrenheit",
        "wind_speed_unit":    "mph",
        "precipitation_unit": "inch",
        "timezone":           s["tz"],
    }

    try:
        r = requests.get(HISTORICAL_BASE, params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[om_hist] {icao} {date_from}→{date_to}: {e}")
        return None


def store_historical_forecasts(
    icao: str, payload: dict, conn: sqlite3.Connection
) -> int:
    """
    Store historical archive data as forecast_runs rows with model='OpenMeteo-Archive'.
    These represent what Open-Meteo's reanalysis says for each date — useful as a
    proxy forecast for backtesting when real-time forecasts weren't stored.

    Returns number of rows upserted.
    """
    daily = payload.get("daily", {})
    dates = daily.get("time", [])
    if not dates:
        return 0

    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    count = 0

    for i, date in enumerate(dates):
        def g(k):
            return daily.get(k, [None] * len(dates))[i]

        try:
            conn.execute("""
                INSERT INTO forecast_runs (
                    fetched_at, forecast_date, station_code, model_name,
                    temp_max, temp_min, temp_mean,
                    wind_direction_dominant, wind_speed_max, wind_speed_mean, wind_gusts_max,
                    cloud_cover_mean, dew_point_mean, humidity_mean, pressure_msl_mean,
                    precip_sum, rain_sum, snowfall_sum, weather_code, sunshine_duration
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(forecast_date, station_code, model_name) DO UPDATE SET
                    fetched_at=excluded.fetched_at,
                    temp_max=excluded.temp_max, temp_min=excluded.temp_min,
                    temp_mean=excluded.temp_mean,
                    wind_direction_dominant=excluded.wind_direction_dominant,
                    cloud_cover_mean=excluded.cloud_cover_mean,
                    dew_point_mean=excluded.dew_point_mean,
                    humidity_mean=excluded.humidity_mean,
                    pressure_msl_mean=excluded.pressure_msl_mean
            """, (
                fetched, date, icao, "OpenMeteo-Archive",
                g("temperature_2m_max"), g("temperature_2m_min"), g("temperature_2m_mean"),
                g("wind_direction_10m_dominant"), g("wind_speed_10m_max"),
                g("wind_speed_10m_mean"), g("wind_gusts_10m_max"),
                g("cloud_cover_mean"),
                g("dew_point_2m_mean"), g("relative_humidity_2m_mean"),
                g("pressure_msl_mean"),
                g("precipitation_sum"), g("rain_sum"), g("snowfall_sum"),
                g("weather_code"), g("sunshine_duration"),
            ))
            count += 1
        except Exception as e:
            print(f"[om_hist] store {icao}/{date}: {e}")

    conn.commit()
    return count


def backfill_station(
    icao: str, date_from: str, date_to: str, conn: sqlite3.Connection
) -> int:
    """Full pipeline: fetch + store historical archive for a station."""
    print(f"[om_hist] Fetching archive: {icao} {date_from} → {date_to}")
    payload = fetch_historical(icao, date_from, date_to)
    if not payload:
        return 0
    n = store_historical_forecasts(icao, payload, conn)
    print(f"[om_hist] {icao}: stored {n} archive days")
    return n
