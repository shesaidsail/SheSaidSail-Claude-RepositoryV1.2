"""
Open-Meteo forecast ingestion for all active stations.

Fetches 7-day daily + hourly forecasts and current conditions.
Stores into forecast_runs and hourly_forecasts tables.
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from config import (
    OPEN_METEO_BASE, DAILY_VARS, HOURLY_VARS, CURRENT_VARS, STATIONS
)


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_forecast(icao: str) -> dict | None:
    """Fetch full forecast payload from Open-Meteo for one station."""
    s = STATIONS.get(icao)
    if not s:
        return None

    params = {
        "latitude":           s["lat"],
        "longitude":          s["lon"],
        "daily":              ",".join(DAILY_VARS),
        "hourly":             ",".join(HOURLY_VARS),
        "current":            ",".join(CURRENT_VARS),
        "temperature_unit":   "fahrenheit",
        "wind_speed_unit":    "mph",
        "precipitation_unit": "inch",
        "timezone":           s["tz"],
        "forecast_days":      7,
    }

    try:
        r = requests.get(OPEN_METEO_BASE, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[open_meteo] {icao} fetch error: {e}")
        return None


def _safe(d: dict, key, default=None):
    return d.get(key, default)


def store_forecast(icao: str, payload: dict, conn: sqlite3.Connection) -> int:
    """Parse Open-Meteo payload and upsert forecast_runs + hourly_forecasts.
    Returns number of daily rows stored."""
    daily = payload.get("daily", {})
    dates = daily.get("time", [])
    if not dates:
        return 0

    fetched = _ts()
    count = 0

    for i, date in enumerate(dates):
        def g(k): return daily.get(k, [None]*len(dates))[i]

        try:
            cur = conn.execute("""
                INSERT INTO forecast_runs (
                    fetched_at, forecast_date, station_code, model_name,
                    temp_max, temp_min, temp_mean,
                    wind_direction_dominant, wind_speed_max, wind_speed_mean, wind_gusts_max,
                    cloud_cover_mean, cloud_cover_max, cloud_cover_min,
                    dew_point_mean, dew_point_max, dew_point_min,
                    humidity_mean, humidity_max, humidity_min,
                    pressure_msl_mean, pressure_msl_max, pressure_msl_min,
                    surface_pressure_mean, surface_pressure_max, surface_pressure_min,
                    precip_prob_mean, precip_prob_max,
                    precip_sum, rain_sum, snowfall_sum,
                    weather_code, sunshine_duration, sunrise, sunset
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(forecast_date, station_code, model_name) DO UPDATE SET
                    fetched_at=excluded.fetched_at,
                    temp_max=excluded.temp_max, temp_min=excluded.temp_min,
                    temp_mean=excluded.temp_mean,
                    wind_direction_dominant=excluded.wind_direction_dominant,
                    wind_speed_max=excluded.wind_speed_max,
                    wind_speed_mean=excluded.wind_speed_mean,
                    wind_gusts_max=excluded.wind_gusts_max,
                    cloud_cover_mean=excluded.cloud_cover_mean,
                    cloud_cover_max=excluded.cloud_cover_max,
                    cloud_cover_min=excluded.cloud_cover_min,
                    dew_point_mean=excluded.dew_point_mean,
                    dew_point_max=excluded.dew_point_max,
                    dew_point_min=excluded.dew_point_min,
                    humidity_mean=excluded.humidity_mean,
                    humidity_max=excluded.humidity_max,
                    humidity_min=excluded.humidity_min,
                    pressure_msl_mean=excluded.pressure_msl_mean,
                    pressure_msl_max=excluded.pressure_msl_max,
                    pressure_msl_min=excluded.pressure_msl_min,
                    surface_pressure_mean=excluded.surface_pressure_mean,
                    surface_pressure_max=excluded.surface_pressure_max,
                    surface_pressure_min=excluded.surface_pressure_min,
                    precip_prob_mean=excluded.precip_prob_mean,
                    precip_prob_max=excluded.precip_prob_max,
                    precip_sum=excluded.precip_sum,
                    rain_sum=excluded.rain_sum,
                    snowfall_sum=excluded.snowfall_sum,
                    weather_code=excluded.weather_code,
                    sunshine_duration=excluded.sunshine_duration,
                    sunrise=excluded.sunrise,
                    sunset=excluded.sunset
            """, (
                fetched, date, icao, "OpenMeteo",
                g("temperature_2m_max"), g("temperature_2m_min"), g("temperature_2m_mean"),
                g("wind_direction_10m_dominant"), g("wind_speed_10m_max"),
                g("wind_speed_10m_mean"), g("wind_gusts_10m_max"),
                g("cloud_cover_mean"), g("cloud_cover_max"), g("cloud_cover_min"),
                g("dew_point_2m_mean"), g("dew_point_2m_max"), g("dew_point_2m_min"),
                g("relative_humidity_2m_mean"), g("relative_humidity_2m_max"),
                g("relative_humidity_2m_min"),
                g("pressure_msl_mean"), g("pressure_msl_max"), g("pressure_msl_min"),
                g("surface_pressure_mean"), g("surface_pressure_max"),
                g("surface_pressure_min"),
                g("precipitation_probability_mean"), g("precipitation_probability_max"),
                g("precipitation_sum"), g("rain_sum"), g("snowfall_sum"),
                g("weather_code"), g("sunshine_duration"), g("sunrise"), g("sunset"),
            ))
            run_id = cur.lastrowid
            count += 1
        except Exception as e:
            print(f"[open_meteo] store daily {icao}/{date}: {e}")
            run_id = None

        # Store hourly rows for this date
        hourly = payload.get("hourly", {})
        htimes = hourly.get("time", [])
        utc_off = STATIONS[icao]["utc_offset"]

        for j, ht in enumerate(htimes):
            if not ht.startswith(date):
                continue
            def gh(k): return hourly.get(k, [None]*len(htimes))[j]
            try:
                # ht is like "2026-05-17T14:00" local time
                local_hour = int(ht[11:13])
                utc_str = ht.replace("T", "T") + ":00Z"
                conn.execute("""
                    INSERT INTO hourly_forecasts (
                        forecast_run_id, station_code, valid_time_utc,
                        forecast_date, hour_local,
                        temperature_2m, dew_point_2m, wind_direction, wind_speed,
                        wind_gusts, cloud_cover, precip_probability, weather_code
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(station_code, valid_time_utc) DO UPDATE SET
                        temperature_2m=excluded.temperature_2m,
                        dew_point_2m=excluded.dew_point_2m,
                        wind_direction=excluded.wind_direction,
                        wind_speed=excluded.wind_speed,
                        wind_gusts=excluded.wind_gusts,
                        cloud_cover=excluded.cloud_cover,
                        precip_probability=excluded.precip_probability,
                        weather_code=excluded.weather_code
                """, (
                    run_id, icao, utc_str, date, local_hour,
                    gh("temperature_2m"), gh("dew_point_2m"),
                    gh("wind_direction_10m"), gh("wind_speed_10m"),
                    gh("wind_gusts_10m"), gh("cloud_cover"),
                    gh("precipitation_probability"), gh("weather_code"),
                ))
            except Exception:
                pass

    conn.commit()
    return count


def refresh_all(conn: sqlite3.Connection, verbose: bool = True) -> dict:
    """Fetch + store forecasts for all active stations. Returns {icao: rows}."""
    rows = conn.execute("SELECT icao FROM stations WHERE active=1").fetchall()
    results = {}
    for row in rows:
        icao = row["icao"]
        payload = fetch_forecast(icao)
        if payload:
            n = store_forecast(icao, payload, conn)
            results[icao] = n
            # Update data_health
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            conn.execute("""
                INSERT INTO data_health (feed, station_code, last_success, last_attempt, consecutive_failures)
                VALUES ('forecast',?,?,?,0)
                ON CONFLICT(feed) DO UPDATE SET
                    last_success=excluded.last_success,
                    last_attempt=excluded.last_attempt,
                    consecutive_failures=0, last_error=NULL
            """, (icao, now, now))
            conn.commit()
            if verbose:
                print(f"[open_meteo] {icao}: {n} forecast days stored")
        else:
            results[icao] = 0
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            conn.execute("""
                INSERT INTO data_health (feed, station_code, last_attempt, consecutive_failures)
                VALUES ('forecast',?,?,1)
                ON CONFLICT(feed) DO UPDATE SET
                    last_attempt=excluded.last_attempt,
                    consecutive_failures=consecutive_failures+1
            """, (icao, now))
            conn.commit()
    return results


def get_latest_forecast(icao: str, date: str, conn: sqlite3.Connection) -> dict | None:
    row = conn.execute("""
        SELECT * FROM forecast_runs
        WHERE station_code=? AND forecast_date=?
        ORDER BY fetched_at DESC LIMIT 1
    """, (icao, date)).fetchone()
    return dict(row) if row else None


def get_hourly_for_date(icao: str, date: str, conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT * FROM hourly_forecasts
        WHERE station_code=? AND forecast_date=?
        ORDER BY hour_local
    """, (icao, date)).fetchall()
    return [dict(r) for r in rows]
