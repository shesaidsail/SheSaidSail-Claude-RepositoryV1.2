"""
SQLite database schema and connection helper.
12 tables covering all system state.
"""

import sqlite3
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ── Stations ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stations (
    icao        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    latitude    REAL NOT NULL,
    longitude   REAL NOT NULL,
    timezone    TEXT NOT NULL,
    utc_offset  INTEGER NOT NULL DEFAULT -5,
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- ── Daily forecasts from Open-Meteo ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS forecast_runs (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at                  TEXT NOT NULL,
    forecast_date               TEXT NOT NULL,
    station_code                TEXT NOT NULL REFERENCES stations(icao),
    model_name                  TEXT NOT NULL DEFAULT 'OpenMeteo',
    temp_max                    REAL,
    temp_min                    REAL,
    temp_mean                   REAL,
    wind_direction_dominant     REAL,
    wind_speed_max              REAL,
    wind_speed_mean             REAL,
    wind_gusts_max              REAL,
    cloud_cover_mean            REAL,
    cloud_cover_max             REAL,
    cloud_cover_min             REAL,
    dew_point_mean              REAL,
    dew_point_max               REAL,
    dew_point_min               REAL,
    humidity_mean               REAL,
    humidity_max                REAL,
    humidity_min                REAL,
    pressure_msl_mean           REAL,
    pressure_msl_max            REAL,
    pressure_msl_min            REAL,
    surface_pressure_mean       REAL,
    surface_pressure_max        REAL,
    surface_pressure_min        REAL,
    precip_prob_mean            REAL,
    precip_prob_max             REAL,
    precip_sum                  REAL,
    rain_sum                    REAL,
    snowfall_sum                REAL,
    weather_code                INTEGER,
    sunshine_duration           REAL,
    sunrise                     TEXT,
    sunset                      TEXT,
    UNIQUE(forecast_date, station_code, model_name)
);

-- ── Hourly forecast data ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hourly_forecasts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    forecast_run_id     INTEGER REFERENCES forecast_runs(id),
    station_code        TEXT NOT NULL REFERENCES stations(icao),
    valid_time_utc      TEXT NOT NULL,
    forecast_date       TEXT NOT NULL,
    hour_local          INTEGER,
    temperature_2m      REAL,
    dew_point_2m        REAL,
    wind_direction      REAL,
    wind_speed          REAL,
    wind_gusts          REAL,
    cloud_cover         REAL,
    precip_probability  REAL,
    weather_code        INTEGER,
    UNIQUE(station_code, valid_time_utc)
);

-- ── METAR observations ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS official_observations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    station_code    TEXT NOT NULL REFERENCES stations(icao),
    timestamp_utc   TEXT NOT NULL,
    observed_temp   REAL,
    dewpoint        REAL,
    wind_direction  REAL,
    wind_speed      REAL,
    gust_speed      REAL,
    visibility_sm   REAL,
    cloud_layers    TEXT,        -- JSON array
    pressure_inHg   REAL,
    weather_string  TEXT,
    max_temp_6h     REAL,
    min_temp_6h     REAL,
    max_temp_24h    REAL,
    raw_metar       TEXT,
    UNIQUE(station_code, timestamp_utc)
);

-- ── Daily settlements ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS daily_settlements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement_date TEXT NOT NULL,
    station_code    TEXT NOT NULL REFERENCES stations(icao),
    official_high   REAL,
    official_low    REAL,
    source          TEXT DEFAULT 'metar',
    regime          TEXT,
    settled_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    UNIQUE(settlement_date, station_code)
);

-- ── Kalshi market snapshots ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS market_snapshots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at     TEXT NOT NULL,
    station_code    TEXT NOT NULL REFERENCES stations(icao),
    market_ticker   TEXT NOT NULL,
    market_title    TEXT,
    threshold_f     REAL NOT NULL,
    side            TEXT NOT NULL CHECK(side IN ('Yes','No')),
    market_price    REAL,
    best_bid        REAL,
    best_ask        REAL,
    last_price      REAL,
    volume          REAL,
    open_interest   REAL,
    expiry_date     TEXT,
    fair_value      REAL,
    edge            REAL,
    confidence      REAL,
    regime          TEXT,
    signal          TEXT   -- 'BET' | 'PASS' | 'FADE'
);

-- ── Regime stats (per station + regime) ───────────────────────────────────
CREATE TABLE IF NOT EXISTS regime_stats (
    station_code    TEXT NOT NULL REFERENCES stations(icao),
    regime          TEXT NOT NULL,
    sample_size     INTEGER DEFAULT 0,
    avg_bias        REAL,
    std_dev         REAL,
    win_rate        REAL,
    updated_at      TEXT,
    PRIMARY KEY (station_code, regime)
);

-- ── Model stats (bias engine output) ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS model_stats (
    station_code        TEXT NOT NULL REFERENCES stations(icao),
    model_name          TEXT NOT NULL,
    regime              TEXT NOT NULL,
    avg_bias            REAL,
    std_dev             REAL,
    sample_size         INTEGER,
    rolling_7d_bias     REAL,
    rolling_30d_bias    REAL,
    confidence          REAL,
    updated_at          TEXT,
    PRIMARY KEY (station_code, model_name, regime)
);

-- ── Paper trades ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS paper_trades (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    opened_at       TEXT NOT NULL,
    station_code    TEXT NOT NULL REFERENCES stations(icao),
    market_ticker   TEXT NOT NULL,
    forecast_date   TEXT NOT NULL,
    threshold_f     REAL NOT NULL,
    side            TEXT NOT NULL CHECK(side IN ('Yes','No')),
    entry_price     REAL NOT NULL,
    fair_value      REAL NOT NULL,
    edge            REAL NOT NULL,
    confidence      REAL,
    regime          TEXT,
    adjusted_forecast REAL,
    model_prob      REAL,
    status          TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('OPEN','CLOSED','VOID')),
    settlement_price REAL,
    result          TEXT,    -- 'WIN' | 'LOSS' | 'PUSH'
    pnl_cents       REAL,
    closed_at       TEXT,
    notes           TEXT
);

-- ── Backtest runs ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS backtest_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_at          TEXT NOT NULL,
    station_code    TEXT,    -- NULL = all stations
    date_from       TEXT,
    date_to         TEXT,
    total_trades    INTEGER,
    wins            INTEGER,
    losses          INTEGER,
    win_rate        REAL,
    total_pnl       REAL,
    roi_pct         REAL,
    max_drawdown    REAL,
    sharpe          REAL,
    params_json     TEXT     -- JSON of filter params used
);

-- ── Alerts ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS alerts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    station_code TEXT REFERENCES stations(icao),
    alert_type  TEXT NOT NULL,   -- 'EDGE_SIGNAL' | 'STALE_FEED' | 'SETTLEMENT'
    message     TEXT NOT NULL,
    acknowledged INTEGER DEFAULT 0
);

-- ── Data health ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS data_health (
    feed            TEXT PRIMARY KEY,   -- 'forecast' | 'metar' | 'kalshi'
    station_code    TEXT,
    last_success    TEXT,
    last_attempt    TEXT,
    consecutive_failures INTEGER DEFAULT 0,
    last_error      TEXT
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> sqlite3.Connection:
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def upsert_station(icao: str, conn: sqlite3.Connection):
    from config import STATIONS
    s = STATIONS.get(icao)
    if not s:
        return
    conn.execute("""
        INSERT INTO stations (icao, name, latitude, longitude, timezone, utc_offset, active)
        VALUES (?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(icao) DO UPDATE SET
            name=excluded.name, latitude=excluded.latitude,
            longitude=excluded.longitude, timezone=excluded.timezone,
            utc_offset=excluded.utc_offset, active=1
    """, (icao, s["name"], s["lat"], s["lon"], s["tz"], s["utc_offset"]))
    conn.commit()


def seed_stations(conn: sqlite3.Connection):
    from config import STATIONS
    for icao in STATIONS:
        upsert_station(icao, conn)
