"""
Central database module.  All modules import get_connection() and init_db() from here.
"""

import sqlite3
from config import DB_PATH, DATA_DIR

SCHEMA = """
CREATE TABLE IF NOT EXISTS forecast_runs (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc        TEXT    NOT NULL,
    forecast_date        TEXT    NOT NULL,
    station_code         TEXT    NOT NULL DEFAULT 'KLAX',
    model_name           TEXT    NOT NULL DEFAULT 'HRRR/Ventusky',
    forecast_high        REAL    NOT NULL,
    hottest_station_tile TEXT,
    wind_direction       REAL,
    wind_speed           REAL,
    marine_layer_notes   TEXT,
    screenshot_path      TEXT,
    source               TEXT    DEFAULT 'manual'
);

CREATE TABLE IF NOT EXISTS actual_observations (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc  TEXT    NOT NULL UNIQUE,
    station_code   TEXT    NOT NULL DEFAULT 'KLAX',
    observed_temp  REAL,
    dewpoint       REAL,
    wind_direction REAL,
    wind_speed     REAL,
    gust_speed     REAL,
    cloud_layers   TEXT,
    visibility     REAL,
    pressure       REAL,
    weather_string TEXT,
    raw_metar      TEXT,
    max_temp_6h    REAL,
    min_temp_6h    REAL,
    max_temp_24h   REAL
);

CREATE TABLE IF NOT EXISTS daily_settlements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement_date TEXT    NOT NULL,
    station_code    TEXT    NOT NULL DEFAULT 'KLAX',
    official_high   REAL    NOT NULL,
    official_low    REAL,
    source          TEXT    DEFAULT 'computed',
    regime          TEXT,
    UNIQUE(settlement_date, station_code)
);

CREATE TABLE IF NOT EXISTS market_snapshots (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc  TEXT    NOT NULL,
    market_ticker  TEXT,
    contract_name  TEXT,
    threshold      REAL    NOT NULL,
    side           TEXT    NOT NULL,
    best_bid       REAL,
    best_ask       REAL,
    last_price     REAL,
    volume         INTEGER,
    open_interest  INTEGER,
    fair_value     REAL,
    edge           REAL,
    confidence     REAL,
    regime         TEXT
);

CREATE TABLE IF NOT EXISTS model_stats (
    station_code     TEXT    NOT NULL,
    model_name       TEXT    NOT NULL,
    regime           TEXT    NOT NULL DEFAULT 'ALL',
    avg_bias         REAL,
    std_dev          REAL,
    sample_size      INTEGER,
    rolling_7d_bias  REAL,
    rolling_30d_bias REAL,
    confidence       REAL,
    updated_at       TEXT,
    PRIMARY KEY (station_code, model_name, regime)
);

CREATE TABLE IF NOT EXISTS weather_regimes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc   TEXT    NOT NULL,
    settlement_date TEXT,
    station_code    TEXT    NOT NULL DEFAULT 'KLAX',
    regime          TEXT    NOT NULL,
    confidence      REAL,
    wind_direction  REAL,
    wind_speed      REAL,
    cloud_cover     TEXT,
    cloud_base_ft   REAL,
    dewpoint_spread REAL,
    visibility      REAL,
    notes           TEXT
);
"""


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)
