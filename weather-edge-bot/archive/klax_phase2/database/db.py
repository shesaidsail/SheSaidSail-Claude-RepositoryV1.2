"""
Central database module.  All other modules import get_connection() and init_db() from here.
"""

import sqlite3
from config import DB_PATH, DATA_DIR

SCHEMA = """
CREATE TABLE IF NOT EXISTS forecast_runs (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc  TEXT    NOT NULL,
    forecast_date  TEXT    NOT NULL,
    station_code   TEXT    NOT NULL DEFAULT 'KLAX',
    model_name     TEXT    NOT NULL DEFAULT 'HRRR/Ventusky',
    forecast_high  REAL    NOT NULL,
    source         TEXT    DEFAULT 'manual'
);

CREATE TABLE IF NOT EXISTS actual_observations (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc  TEXT    NOT NULL UNIQUE,
    station_code   TEXT    NOT NULL DEFAULT 'KLAX',
    observed_temp  REAL,
    wind_direction TEXT,
    wind_speed     REAL,
    cloud_cover    TEXT
);

CREATE TABLE IF NOT EXISTS daily_settlements (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement_date TEXT   NOT NULL,
    station_code   TEXT    NOT NULL DEFAULT 'KLAX',
    official_high  REAL    NOT NULL,
    source         TEXT    DEFAULT 'computed',
    UNIQUE(settlement_date, station_code)
);

CREATE TABLE IF NOT EXISTS market_snapshots (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc  TEXT    NOT NULL,
    contract_name  TEXT,
    threshold      REAL    NOT NULL,
    side           TEXT    NOT NULL,
    market_price   REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS model_stats (
    station_code     TEXT    NOT NULL,
    model_name       TEXT    NOT NULL,
    avg_bias         REAL,
    std_dev          REAL,
    sample_size      INTEGER,
    rolling_7d_bias  REAL,
    rolling_30d_bias REAL,
    updated_at       TEXT,
    PRIMARY KEY (station_code, model_name)
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
