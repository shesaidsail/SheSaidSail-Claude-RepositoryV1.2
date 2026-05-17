"""
KLAX METAR Ingestion

Primary source:  NWS KLAX.TXT   (https://tgftp.nws.noaa.gov/data/observations/metar/stations/KLAX.TXT)
Fallback source: AWC JSON API   (https://aviationweather.gov/api/data/metar)

The NWS feed is authoritative and updated every ~20 minutes.  The fallback is
used automatically when the NWS endpoint is unreachable, and also for --backfill
mode to retrieve the last N hours of observations.

CLI usage:
  python scripts/ingest_metar.py               # single fetch from NWS
  python scripts/ingest_metar.py --loop         # poll every 60 s (Ctrl-C to stop)
  python scripts/ingest_metar.py --backfill 24  # backfill last 24 h via AWC

Cron (every minute, single fetch):
  * * * * *  cd /path/to/klax_phase3 && python scripts/ingest_metar.py
"""

import sys
import re
import json
import time
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from datetime import datetime, timezone, timedelta

from database.db import get_connection, init_db
from config import STATION, NWS_METAR_URL, AWC_METAR_URL, METAR_POLL_INTERVAL


# ---------------------------------------------------------------------------
# Unit helpers
# ---------------------------------------------------------------------------

def c_to_f(c: float) -> float:
    return round(c * 9.0 / 5.0 + 32.0, 1)

def inhg_to_hpa(inhg: float) -> float:
    return round(inhg * 33.8639, 1)


# ---------------------------------------------------------------------------
# Raw METAR parser  (handles standard ASOS/AWOS reports from NWS)
# ---------------------------------------------------------------------------

_M_TEMP = re.compile(r'\b(M?\d{1,2})/(M?\d{1,2})\b')
_WIND   = re.compile(r'\b(VRB|\d{3})(\d{2,3})(?:G(\d{2,3}))?KT\b')
_VIS    = re.compile(r'\b(\d+(?:\s+\d+/\d+)?)\s*SM\b')
_CLOUD  = re.compile(r'\b(CLR|SKC|NSC|CAVOK|FEW|SCT|BKN|OVC|VV)(\d{3})?\b')
_ALT_A  = re.compile(r'\bA(\d{4})\b')       # altimeter in inHg  (A2979 = 29.79)
_ALT_Q  = re.compile(r'\bQ(\d{4})\b')       # altimeter in hPa
_SLP    = re.compile(r'\bSLP(\d{3})\b')     # sea-level pressure (SLP086 = 1008.6)
_TPRECISE = re.compile(r'\bT([01]\d{3})([01]\d{3})\b')  # T02060128
_TIME   = re.compile(r'\b(\d{2})(\d{2})(\d{2})Z\b')    # DDHHMMZ
_MAXMIN6  = re.compile(r'\b([12])(\d{4})\b')            # 1/0XXX max, 2/1XXX min
_MAX24    = re.compile(r'\b4(\d{4})\b')                 # 24h max/min


def _parse_metar_temp(s: str) -> float:
    """Parse M03 → -3 or 21 → 21 (Celsius)."""
    if s.startswith('M'):
        return -float(s[1:])
    return float(s)


def parse_raw_metar(raw: str, obs_date: datetime | None = None) -> dict | None:
    """
    Parse a raw METAR string into a normalised observation dict.
    Returns None if the string doesn't look like a valid METAR.
    """
    raw = raw.strip()
    if not raw or not raw.startswith('K'):
        return None

    parts  = raw.split()
    station = parts[0] if parts else STATION

    # ---- Timestamp ----
    tm = _TIME.search(raw)
    if tm and obs_date:
        day, hh, mm = int(tm.group(1)), int(tm.group(2)), int(tm.group(3))
        ts = obs_date.replace(day=day, hour=hh, minute=mm, second=0, microsecond=0,
                              tzinfo=timezone.utc)
    elif tm:
        now = datetime.now(timezone.utc)
        try:
            day = int(tm.group(1))
            ts = now.replace(day=day, hour=int(tm.group(2)), minute=int(tm.group(3)),
                             second=0, microsecond=0)
        except ValueError:
            ts = now
    else:
        ts = datetime.now(timezone.utc)
    ts_str = ts.strftime("%Y-%m-%dT%H:%M:%SZ")

    # ---- Wind ----
    wm = _WIND.search(raw)
    wind_dir  = None if not wm or wm.group(1) == 'VRB' else float(wm.group(1))
    wind_spd  = float(wm.group(2)) if wm else None
    wind_gust = float(wm.group(3)) if wm and wm.group(3) else None

    # ---- Visibility ----
    vm = _VIS.search(raw)
    vis = None
    if vm:
        vis_str = vm.group(1).strip()
        if ' ' in vis_str:
            whole, frac = vis_str.split()
            num, den = frac.split('/')
            vis = float(whole) + float(num) / float(den)
        elif '/' in vis_str:
            num, den = vis_str.split('/')
            vis = float(num) / float(den)
        else:
            vis = float(vis_str)
    if raw.find('10SM') != -1 or '10+SM' in raw:
        vis = 10.0

    # ---- Cloud layers ----
    clouds_raw = [(m.group(1), int(m.group(2)) * 100 if m.group(2) else None)
                  for m in _CLOUD.finditer(raw.split('RMK')[0])
                  if m.group(1) not in ('CAVOK', 'NSC')]
    cloud_layers = json.dumps([{"cover": c, "base": b} for c, b in clouds_raw]) if clouds_raw else json.dumps([])
    if any(c in ('CLR', 'SKC', 'CAVOK', 'NSC') for c, _ in clouds_raw):
        cloud_layers = json.dumps([{"cover": "CLR", "base": None}])

    # ---- Temperature / Dewpoint ----
    # Prefer precise T remark (T02060128 → 20.6°C / 12.8°C)
    tp = _TPRECISE.search(raw)
    if tp:
        sign_t  = -1 if tp.group(1)[0] == '1' else 1
        sign_d  = -1 if tp.group(2)[0] == '1' else 1
        temp_c  = sign_t * float(tp.group(1)[1:]) / 10.0
        dewp_c  = sign_d * float(tp.group(2)[1:]) / 10.0
    else:
        tm2 = _M_TEMP.search(raw.split('RMK')[0])
        if not tm2:
            return None  # can't get temperature
        temp_c = _parse_metar_temp(tm2.group(1))
        dewp_c = _parse_metar_temp(tm2.group(2))

    temp_f = c_to_f(temp_c)
    dewp_f = c_to_f(dewp_c)

    # ---- Pressure ----
    pressure = None
    slp_m = _SLP.search(raw)
    if slp_m:
        v = int(slp_m.group(1))
        pressure = round((1000.0 + v / 10.0) if v < 500 else (900.0 + v / 10.0), 1)
    elif _ALT_Q.search(raw):
        pressure = float(_ALT_Q.search(raw).group(1))
    elif _ALT_A.search(raw):
        pressure = inhg_to_hpa(float(_ALT_A.search(raw).group(1)) / 100.0)

    # ---- 6h/24h max/min from remarks ----
    max6 = min6 = max24 = None
    remark_block = raw.split('RMK')[-1] if 'RMK' in raw else ''
    for mm in _MAXMIN6.finditer(remark_block):
        kind, val_s = mm.group(1), mm.group(2)
        sign = -1 if val_s[0] == '1' else 1
        val_c = sign * float(val_s[1:]) / 10.0
        if kind == '1':
            max6 = c_to_f(val_c)
        else:
            min6 = c_to_f(val_c)
    m24 = _MAX24.search(remark_block)
    if m24:
        v = m24.group(1)
        max24 = c_to_f((-1 if v[0] == '1' else 1) * float(v[1:]) / 10.0)

    return {
        "timestamp_utc":  ts_str,
        "station_code":   station,
        "observed_temp":  temp_f,
        "dewpoint":       dewp_f,
        "wind_direction": wind_dir,
        "wind_speed":     wind_spd,
        "gust_speed":     wind_gust,
        "cloud_layers":   cloud_layers,
        "visibility":     vis,
        "pressure":       pressure,
        "weather_string": None,  # not reliably parseable from raw without full lookup table
        "raw_metar":      raw,
        "max_temp_6h":    max6,
        "min_temp_6h":    min6,
        "max_temp_24h":   max24,
    }


# ---------------------------------------------------------------------------
# Fetch: NWS primary
# ---------------------------------------------------------------------------

def fetch_nws(station: str = STATION) -> list[dict]:
    """Fetch the single latest METAR from the NWS station TXT feed."""
    url = NWS_METAR_URL.format(station=station)
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    lines = [l.strip() for l in resp.text.strip().splitlines() if l.strip()]

    # Format: "2026/05/17 19:53\nKLAX 171953Z ..."
    # Find the raw METAR line (starts with station ID)
    raw_line = next((l for l in lines if l.startswith(station)), None)
    if not raw_line:
        return []

    # Parse approximate date from header line if present
    obs_date = None
    for line in lines:
        m = re.match(r'(\d{4})/(\d{2})/(\d{2})', line)
        if m:
            obs_date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                                tzinfo=timezone.utc)
            break

    obs = parse_raw_metar(raw_line, obs_date)
    return [obs] if obs else []


# ---------------------------------------------------------------------------
# Fetch: AWC JSON fallback / backfill
# ---------------------------------------------------------------------------

def _parse_awc_json(raw: dict, station: str) -> dict | None:
    if raw.get("temp") is None:
        return None

    obs_ts = raw.get("obsTime")
    if obs_ts:
        ts = datetime.fromtimestamp(int(obs_ts), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        receipt = raw.get("receiptTime", "")
        ts = receipt.replace(" ", "T")
        if not ts.endswith("Z"):
            ts += "Z"

    wdir_raw = raw.get("wdir")
    try:
        wind_dir = float(wdir_raw) if wdir_raw not in (None, "VRB") else None
    except (TypeError, ValueError):
        wind_dir = None

    clouds_raw = raw.get("clouds") or []
    cloud_layers = json.dumps([
        {"cover": c.get("cover", "CLR"), "base": c.get("base")}
        for c in clouds_raw
    ]) if clouds_raw else json.dumps([])

    pressure = None
    if raw.get("slp") is not None:
        pressure = round(float(raw["slp"]), 1)
    elif raw.get("altim") is not None:
        pressure = round(float(raw["altim"]), 1)

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
        "max_temp_6h":    c_to_f(float(raw["maxT"]))   if raw.get("maxT")   is not None else None,
        "min_temp_6h":    c_to_f(float(raw["minT"]))   if raw.get("minT")   is not None else None,
        "max_temp_24h":   c_to_f(float(raw["maxT24"])) if raw.get("maxT24") is not None else None,
    }


def fetch_awc(station: str = STATION, hours: int = 2) -> list[dict]:
    """AWC JSON API — used as fallback and for --backfill."""
    resp = requests.get(
        AWC_METAR_URL,
        params={"ids": station, "format": "json", "hours": hours},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        return []
    return [o for raw in data for o in [_parse_awc_json(raw, station)] if o]


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

def store_observation(obs: dict, conn) -> bool:
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
        return False


def _print_obs(obs: dict) -> None:
    gust = f" G{obs['gust_speed']:.0f}" if obs.get("gust_speed") else ""
    wdir = f"{obs['wind_direction']:.0f}°" if obs.get("wind_direction") is not None else "VRB"
    print(
        f"  {obs['timestamp_utc']}  "
        f"{obs['observed_temp']}°F  "
        f"wind {wdir}@{obs['wind_speed'] or 0:.0f}{gust}kts  "
        f"clouds {obs['cloud_layers']}"
    )


# ---------------------------------------------------------------------------
# Single run
# ---------------------------------------------------------------------------

def run(station: str = STATION, backfill_hours: int = 0) -> int:
    """
    Fetch and store observations.  Returns count of new rows inserted.
    - Normal mode: NWS primary, AWC fallback.
    - backfill_hours > 0: use AWC only (fetches last N hours).
    """
    init_db()
    inserted = 0

    if backfill_hours > 0:
        obs_list = fetch_awc(station, backfill_hours)
    else:
        try:
            obs_list = fetch_nws(station)
            if not obs_list:
                raise ValueError("NWS returned empty")
        except Exception as nws_err:
            print(f"  NWS failed ({nws_err}), falling back to AWC...")
            obs_list = fetch_awc(station, hours=2)

    with get_connection() as conn:
        for obs in obs_list:
            if store_observation(obs, conn):
                inserted += 1
                _print_obs(obs)

    return inserted


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest KLAX METAR observations")
    parser.add_argument("--station",  default=STATION)
    parser.add_argument("--loop",     action="store_true",
                        help=f"Poll every {METAR_POLL_INTERVAL} s (Ctrl-C to stop)")
    parser.add_argument("--backfill", type=int, default=0, metavar="HOURS",
                        help="Backfill last N hours via AWC JSON API")
    args = parser.parse_args()

    if args.backfill:
        n = run(args.station, backfill_hours=args.backfill)
        print(f"Backfill done: {n} observation(s) stored.")
    elif args.loop:
        print(f"METAR loop started — polling every {METAR_POLL_INTERVAL} s.  Ctrl-C to stop.")
        while True:
            try:
                n = run(args.station)
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] {n} new observation(s)." if n else f"[{ts}] No new data.")
            except requests.RequestException as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetch error: {e}", file=sys.stderr)
            time.sleep(METAR_POLL_INTERVAL)
    else:
        try:
            n = run(args.station)
            print(f"Done: {n} new observation(s) for {args.station}.")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
