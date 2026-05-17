"""
METAR ingestion for all active stations.

Primary:  NWS KLAX.TXT  (one station per request, freshest data)
Fallback: AVW cache.csv.gz (all stations in one bulk download)
"""

import sys
import re
import json
import gzip
import sqlite3
import io
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from config import NWS_METAR_URL, AWC_CACHE_URL, AWC_API_URL


# ---------------------------------------------------------------------------
# Raw METAR parser
# ---------------------------------------------------------------------------

def _f(c: float | None) -> float | None:
    """Convert Celsius to Fahrenheit."""
    return round(c * 9 / 5 + 32, 1) if c is not None else None


def parse_raw_metar(raw: str) -> dict | None:
    raw = raw.strip()
    if not raw or not re.search(r'K[A-Z]{3}\s', raw):
        return None

    obs = {
        "observed_temp": None, "dewpoint": None,
        "wind_direction": None, "wind_speed": None, "gust_speed": None,
        "visibility_sm": None, "cloud_layers": None,
        "pressure_inHg": None, "weather_string": None,
        "max_temp_6h": None, "min_temp_6h": None, "max_temp_24h": None,
        "raw_metar": raw,
    }

    # Timestamp from METAR header or body
    m = re.search(r'(\d{2})(\d{2})(\d{2})Z', raw)
    if m:
        day_of_month = int(m.group(1))
        hour         = int(m.group(2))
        minute       = int(m.group(3))
        now = datetime.now(timezone.utc)
        ts = now.replace(day=day_of_month, hour=hour, minute=minute, second=0, microsecond=0)
        if ts > now + timedelta(hours=1):
            # Rolled back to previous month
            first_of_month = now.replace(day=1)
            ts = (first_of_month - timedelta(days=1)).replace(
                day=day_of_month, hour=hour, minute=minute, second=0, microsecond=0)
        obs["timestamp_utc"] = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        return None

    # Wind
    m = re.search(r'(VRB|\d{3})(\d{2,3})(?:G(\d{2,3}))?KT', raw)
    if m:
        obs["wind_direction"] = None if m.group(1) == "VRB" else float(m.group(1))
        obs["wind_speed"]     = float(m.group(2))
        obs["gust_speed"]     = float(m.group(3)) if m.group(3) else None

    # Visibility
    m = re.search(r'(?:^|\s)(\d+(?:\s\d+/\d+)?|M?1/\d+)\s*SM', raw)
    if m:
        vis_str = m.group(1).strip()
        try:
            if " " in vis_str:
                parts = vis_str.split()
                whole = float(parts[0])
                num, den = parts[1].split("/")
                obs["visibility_sm"] = whole + float(num) / float(den)
            elif "/" in vis_str:
                v = vis_str.lstrip("M")
                num, den = v.split("/")
                obs["visibility_sm"] = float(num) / float(den)
            else:
                obs["visibility_sm"] = float(vis_str)
        except ValueError:
            pass

    # Cloud layers
    layers = []
    for m in re.finditer(r'(FEW|SCT|BKN|OVC|VV)(\d{3})', raw):
        layers.append({"cover": m.group(1), "base": int(m.group(2)) * 100})
    obs["cloud_layers"] = json.dumps(layers) if layers else json.dumps([])

    # Temperature / dewpoint  (standard TT/DD format)
    m = re.search(r'\b(M?\d{2})/(M?\d{2})\b', raw)
    if m:
        def decode_temp(s):
            return -(int(s[1:])) if s.startswith("M") else int(s)
        obs["observed_temp"] = _f(decode_temp(m.group(1)))
        obs["dewpoint"]      = _f(decode_temp(m.group(2)))

    # Precise T remark overrides (T02060128 = 20.6°C / 12.8°C)
    m = re.search(r'\bT([01])(\d{3})([01])(\d{3})\b', raw)
    if m:
        sign_t = -1 if m.group(1) == "1" else 1
        sign_d = -1 if m.group(3) == "1" else 1
        obs["observed_temp"] = _f(sign_t * int(m.group(2)) / 10)
        obs["dewpoint"]      = _f(sign_d * int(m.group(4)) / 10)

    # Altimeter (A2992)
    m = re.search(r'\bA(\d{4})\b', raw)
    if m:
        obs["pressure_inHg"] = float(m.group(1)) / 100

    # SLP remark  (SLP123 = 1012.3 hPa, not stored separately but useful)
    # Already captured via A-altimeter above.

    # 6-hour max/min   (1xxxx or 2xxxx groups in remarks)
    m = re.search(r'\b1(\d{4})\b', raw)
    if m:
        v = int(m.group(1))
        obs["max_temp_6h"] = _f((-v/10) if v > 5000 else (v/10))
    m = re.search(r'\b2(\d{4})\b', raw)
    if m:
        v = int(m.group(1))
        obs["min_temp_6h"] = _f((-v/10) if v > 5000 else (v/10))

    # 24-hour max (4xxxx)
    m = re.search(r'\b4(\d{4})(\d{4})\b', raw)
    if m:
        v = int(m.group(1))
        obs["max_temp_24h"] = _f((-v/10) if v > 5000 else (v/10))

    # Weather string (TS, RA, SN, FG, BR, HZ, DZ, etc.)
    wx_codes = re.findall(
        r'\b(?:-|\\+|VC)?(TS|RA|SN|FG|BR|HZ|DZ|GR|GS|SQ|FC|PL|IC|UP|FZRA|FZDZ|FZFG|BLSN|DRSN|RASN|SHRA|SHSN|TSRA|TSGR)\b',
        raw
    )
    obs["weather_string"] = " ".join(wx_codes) if wx_codes else None

    return obs


# ---------------------------------------------------------------------------
# NWS primary fetch
# ---------------------------------------------------------------------------

def fetch_nws(station: str) -> dict | None:
    """Fetch latest METAR from NWS for a single station."""
    url = NWS_METAR_URL.format(station=station)
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        lines = r.text.strip().splitlines()
        # NWS .TXT: line 0 = timestamp, line 1 = raw METAR
        for line in lines:
            line = line.strip()
            if line.startswith(station) or (len(line) > 10 and station in line):
                obs = parse_raw_metar(line)
                if obs:
                    return obs
        return None
    except Exception as e:
        print(f"[metar] NWS fetch error {station}: {e}")
        return None


# ---------------------------------------------------------------------------
# AWC fallback: bulk cache
# ---------------------------------------------------------------------------
_awc_cache: dict[str, str] = {}
_awc_cache_ts: datetime | None = None


def _load_awc_cache() -> None:
    global _awc_cache, _awc_cache_ts
    try:
        r = requests.get(AWC_CACHE_URL, timeout=30)
        r.raise_for_status()
        content = gzip.decompress(r.content).decode("utf-8", errors="replace")
        cache = {}
        for line in content.splitlines():
            parts = line.split(",")
            if parts and parts[0].strip().startswith("K"):
                station = parts[0].strip()
                raw_metar = parts[1].strip() if len(parts) > 1 else line.strip()
                cache[station] = raw_metar
        _awc_cache = cache
        _awc_cache_ts = datetime.now(timezone.utc)
        print(f"[metar] AWC cache loaded: {len(cache)} stations")
    except Exception as e:
        print(f"[metar] AWC cache load error: {e}")


def fetch_awc_cache(station: str) -> dict | None:
    """Use AWC bulk cache as fallback."""
    global _awc_cache, _awc_cache_ts
    age = (datetime.now(timezone.utc) - _awc_cache_ts).total_seconds() if _awc_cache_ts else 9999
    if not _awc_cache or age > 600:
        _load_awc_cache()
    raw = _awc_cache.get(station)
    if raw:
        return parse_raw_metar(raw)
    return None


def fetch_awc_api(station: str, hours: int = 2) -> list[dict]:
    """AWC JSON API for historical backfill."""
    try:
        r = requests.get(AWC_API_URL, params={
            "ids": station, "format": "json", "hours": hours,
        }, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = []
        for item in data:
            raw = item.get("rawOb") or item.get("metar", "")
            obs = parse_raw_metar(raw)
            if obs:
                # Prefer API timestamp if available
                if item.get("obsTime"):
                    obs["timestamp_utc"] = item["obsTime"].replace(" ", "T") + "Z"
                results.append(obs)
        return results
    except Exception as e:
        print(f"[metar] AWC API error {station}: {e}")
        return []


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

def store_observation(station: str, obs: dict, conn: sqlite3.Connection) -> bool:
    """UPSERT one observation. Returns True if new row inserted."""
    try:
        cur = conn.execute("""
            INSERT INTO official_observations (
                station_code, timestamp_utc, observed_temp, dewpoint,
                wind_direction, wind_speed, gust_speed, visibility_sm,
                cloud_layers, pressure_inHg, weather_string,
                max_temp_6h, min_temp_6h, max_temp_24h, raw_metar
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(station_code, timestamp_utc) DO NOTHING
        """, (
            station, obs["timestamp_utc"],
            obs.get("observed_temp"), obs.get("dewpoint"),
            obs.get("wind_direction"), obs.get("wind_speed"), obs.get("gust_speed"),
            obs.get("visibility_sm"), obs.get("cloud_layers"),
            obs.get("pressure_inHg"), obs.get("weather_string"),
            obs.get("max_temp_6h"), obs.get("min_temp_6h"), obs.get("max_temp_24h"),
            obs.get("raw_metar"),
        ))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"[metar] store error {station}: {e}")
        return False


def refresh_all(conn: sqlite3.Connection, verbose: bool = True) -> dict:
    """Fetch latest METAR for all active stations. Returns {icao: new_count}."""
    rows = conn.execute("SELECT icao FROM stations WHERE active=1").fetchall()
    results = {}
    for row in rows:
        icao = row["icao"]
        obs = fetch_nws(icao)
        if not obs:
            obs = fetch_awc_cache(icao)
        new = False
        if obs:
            new = store_observation(icao, obs, conn)
        results[icao] = 1 if new else 0

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if obs:
            conn.execute("""
                INSERT INTO data_health (feed, station_code, last_success, last_attempt, consecutive_failures)
                VALUES ('metar',?,?,?,0)
                ON CONFLICT(feed) DO UPDATE SET
                    last_success=excluded.last_success,
                    last_attempt=excluded.last_attempt,
                    consecutive_failures=0, last_error=NULL
            """, (icao, now, now))
        else:
            conn.execute("""
                INSERT INTO data_health (feed, station_code, last_attempt, consecutive_failures)
                VALUES ('metar',?,?,1)
                ON CONFLICT(feed) DO UPDATE SET
                    last_attempt=excluded.last_attempt,
                    consecutive_failures=consecutive_failures+1
            """, (icao, now))
        conn.commit()

        if verbose:
            status = "new" if new else ("dup" if obs else "fail")
            print(f"[metar] {icao}: {status}")

    return results


def backfill(station: str, hours: int, conn: sqlite3.Connection) -> int:
    """Backfill last N hours for a station via AWC API."""
    observations = fetch_awc_api(station, hours)
    count = 0
    for obs in observations:
        if store_observation(station, obs, conn):
            count += 1
    print(f"[metar] backfill {station}: {count}/{len(observations)} new observations")
    return count


def get_latest_obs(station: str, conn: sqlite3.Connection) -> dict | None:
    row = conn.execute("""
        SELECT * FROM official_observations
        WHERE station_code=?
        ORDER BY timestamp_utc DESC LIMIT 1
    """, (station,)).fetchone()
    return dict(row) if row else None


def get_obs_for_date(station: str, date: str, utc_offset: int,
                     conn: sqlite3.Connection) -> list[dict]:
    """Return all observations for a local calendar date."""
    from datetime import date as dt_date
    d = datetime.strptime(date, "%Y-%m-%d")
    utc_start = (d - timedelta(hours=utc_offset)).strftime("%Y-%m-%dT%H:%M:%SZ")
    utc_end   = (d - timedelta(hours=utc_offset) + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = conn.execute("""
        SELECT * FROM official_observations
        WHERE station_code=? AND timestamp_utc >= ? AND timestamp_utc < ?
        ORDER BY timestamp_utc
    """, (station, utc_start, utc_end)).fetchall()
    return [dict(r) for r in rows]
