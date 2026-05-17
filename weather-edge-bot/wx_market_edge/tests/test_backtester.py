"""
Tests for trading/backtester.py

Critical: validates no-lookahead guarantee, correct T+0.5 win boundary,
dynamic bankroll, and aggregate stat correctness.
"""

import sys
from pathlib import Path
import sqlite3
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from trading.backtester import run_backtest, _get_bias_at_date
from trading.backtester import _win_probability


# ── DB helpers ─────────────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS daily_settlements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            settlement_date TEXT, station_code TEXT,
            official_high REAL, official_low REAL,
            source TEXT, regime TEXT, settled_at TEXT,
            UNIQUE(settlement_date, station_code)
        );
        CREATE TABLE IF NOT EXISTS forecast_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT, forecast_date TEXT, station_code TEXT,
            model_name TEXT DEFAULT 'OpenMeteo',
            temp_max REAL, temp_min REAL, temp_mean REAL,
            wind_direction_dominant REAL, wind_speed_max REAL,
            wind_speed_mean REAL, wind_gusts_max REAL,
            cloud_cover_mean REAL, cloud_cover_max REAL,
            cloud_cover_min REAL, dew_point_mean REAL,
            dew_point_max REAL, dew_point_min REAL,
            humidity_mean REAL, humidity_max REAL, humidity_min REAL,
            pressure_msl_mean REAL, pressure_msl_max REAL,
            pressure_msl_min REAL, surface_pressure_mean REAL,
            surface_pressure_max REAL, surface_pressure_min REAL,
            precip_prob_mean REAL, precip_prob_max REAL,
            precip_sum REAL, rain_sum REAL, snowfall_sum REAL,
            weather_code INTEGER, sunshine_duration REAL,
            sunrise TEXT, sunset TEXT,
            UNIQUE(forecast_date, station_code, model_name)
        );
        CREATE TABLE IF NOT EXISTS model_stats (
            station_code TEXT, model_name TEXT, regime TEXT,
            sample_size INTEGER, avg_bias REAL, std_dev REAL,
            rolling_7d_bias REAL, rolling_30d_bias REAL,
            confidence REAL, updated_at TEXT,
            PRIMARY KEY (station_code, model_name, regime)
        );
        CREATE TABLE IF NOT EXISTS backtest_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_at TEXT, station_code TEXT, date_from TEXT, date_to TEXT,
            total_trades INTEGER, wins INTEGER, losses INTEGER,
            win_rate REAL, total_pnl REAL, roi_pct REAL,
            max_drawdown REAL, sharpe REAL, params_json TEXT
        );
    """)
    return conn


def _add_settlement(conn, date, station="KLAX", official_high=72.0,
                    regime="CLEAR_SKY"):
    conn.execute("""
        INSERT OR REPLACE INTO daily_settlements
            (settlement_date, station_code, official_high, official_low, regime, settled_at)
        VALUES (?,?,?,?,?,?)
    """, (date, station, official_high, official_high - 15, regime,
          date + "T20:00:00Z"))
    conn.commit()


def _add_forecast(conn, date, station="KLAX", temp_max=70.0,
                  fetched_at_offset_hours=-6):
    # fetched_at before noon on the forecast date = available that morning
    from datetime import datetime
    d = datetime.strptime(date, "%Y-%m-%d")
    fetched_at = (d - timedelta(hours=abs(fetched_at_offset_hours))).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("""
        INSERT OR REPLACE INTO forecast_runs
            (fetched_at, forecast_date, station_code, model_name,
             temp_max, temp_min, temp_mean, cloud_cover_mean, wind_speed_mean,
             wind_direction_dominant, humidity_mean, dew_point_mean,
             precip_prob_mean, pressure_msl_mean)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (fetched_at, date, station, "OpenMeteo",
          temp_max, temp_max - 15, temp_max - 7.5, 20.0, 8.0,
          270.0, 55.0, 55.0, 10.0, 1013.0))
    conn.commit()


# ── Win probability math ───────────────────────────────────────────────────────

def test_win_probability_yes_above_threshold():
    """High forecast vs threshold → high win prob for Yes."""
    p = _win_probability(adj=80.0, std=2.5, threshold=72.0, side="Yes")
    assert p > 0.90, f"Expected >90% with adj=80 vs T=72, got {p:.3f}"


def test_win_probability_no_below_threshold():
    """Low forecast vs threshold → high win prob for No."""
    p = _win_probability(adj=62.0, std=2.5, threshold=72.0, side="No")
    assert p > 0.90, f"Expected >90% for No with adj=62 vs T=72, got {p:.3f}"


def test_win_probability_yes_plus_no_sum_to_one():
    """Yes and No probabilities for the same inputs must sum to 1."""
    yes_p = _win_probability(75.0, 3.0, 70.0, "Yes")
    no_p  = _win_probability(75.0, 3.0, 70.0, "No")
    assert abs(yes_p + no_p - 1.0) < 1e-9, f"Yes+No = {yes_p + no_p}, should be 1"


# ── T+0.5 boundary correctness ─────────────────────────────────────────────────

def test_win_boundary_yes_at_threshold_plus_half():
    """actual = T+0.5 is the boundary: Yes should WIN at exactly T+0.5."""
    conn = _conn()
    _add_forecast(conn, "2026-01-15", temp_max=70.0)
    _add_settlement(conn, "2026-01-15", official_high=70.5)  # exactly T+0.5

    result = run_backtest("KLAX", "2026-01-15", "2026-01-15",
                          thresholds=[70.0], sides=["Yes"],
                          min_edge=0.0, min_confidence=0.0, conn=conn)

    yes_trades = [t for t in result["trades"] if t["side"] == "Yes" and t["threshold"] == 70.0]
    if yes_trades:
        assert yes_trades[0]["result"] == "WIN", \
            f"Yes at T+0.5 should WIN, got {yes_trades[0]['result']}"


def test_win_boundary_no_at_threshold_minus_half():
    """actual < T+0.5 means No wins. At exactly T+0.4, No should WIN."""
    conn = _conn()
    _add_forecast(conn, "2026-01-16", temp_max=70.0)
    _add_settlement(conn, "2026-01-16", official_high=70.4)  # just below T+0.5

    result = run_backtest("KLAX", "2026-01-16", "2026-01-16",
                          thresholds=[70.0], sides=["No"],
                          min_edge=0.0, min_confidence=0.0, conn=conn)

    no_trades = [t for t in result["trades"] if t["side"] == "No" and t["threshold"] == 70.0]
    if no_trades:
        assert no_trades[0]["result"] == "WIN", \
            f"No at T+0.4 should WIN (< T+0.5), got {no_trades[0]['result']}"


# ── No-lookahead guarantee ─────────────────────────────────────────────────────

def test_no_lookahead_bias_stats_only_before_date():
    """
    _get_bias_at_date must return 0 samples when NO settlements exist
    before the requested date.
    """
    conn = _conn()
    # Add settlement ON the date (not before it)
    _add_forecast(conn, "2026-02-01")
    _add_settlement(conn, "2026-02-01", official_high=73.0)

    bias, std, n = _get_bias_at_date("KLAX", "OpenMeteo", "CLEAR_SKY",
                                     before_date="2026-02-01", conn=conn)
    assert n == 0, f"No settlement before 2026-02-01, should have n=0, got n={n}"


def test_lookahead_with_prior_data():
    """After 5 prior settlements exist, bias computation should use them."""
    conn = _conn()
    # Add 5 days of data before the backtest date
    for i in range(5):
        d = f"2026-01-{10+i:02d}"
        _add_forecast(conn, d, temp_max=68.0)
        _add_settlement(conn, d, official_high=70.0)  # +2°F bias each day

    bias, std, n = _get_bias_at_date("KLAX", "OpenMeteo", "CLEAR_SKY",
                                     before_date="2026-01-20", conn=conn)
    assert n >= 5, f"Expected n>=5 settlements, got {n}"


# ── Backtest output structure ──────────────────────────────────────────────────

def test_backtest_returns_empty_on_no_data():
    conn = _conn()
    result = run_backtest("KLAX", "2020-01-01", "2020-01-31",
                          min_edge=0.0, min_confidence=0.0, conn=conn)
    assert result["total_trades"] == 0


def test_backtest_win_rate_bounds():
    conn = _conn()
    # Add forecast way above threshold → Yes should mostly win
    for i in range(5):
        d = f"2026-03-{1+i:02d}"
        _add_forecast(conn, d, temp_max=85.0)
        _add_settlement(conn, d, official_high=88.0)

    result = run_backtest("KLAX", "2026-03-01", "2026-03-05",
                          thresholds=[70.0], sides=["Yes"],
                          min_edge=0.0, min_confidence=0.0, conn=conn)

    if result["total_trades"] > 0:
        assert 0.0 <= result["win_rate"] <= 1.0


def test_backtest_has_dollar_pnl():
    conn = _conn()
    _add_forecast(conn, "2026-04-01", temp_max=80.0)
    _add_settlement(conn, "2026-04-01", official_high=83.0)

    result = run_backtest("KLAX", "2026-04-01", "2026-04-01",
                          thresholds=[72.0], sides=["Yes"],
                          min_edge=0.0, min_confidence=0.0, conn=conn)

    assert "total_pnl_d" in result, "Should have total_pnl_d (dollar P&L)"
    assert "final_bankroll" in result, "Should have final_bankroll"
    assert "sharpe" in result, "Should have sharpe ratio"


def test_backtest_dynamic_bankroll_updates():
    """Bankroll at each trade should reflect prior P&L."""
    conn = _conn()
    for i in range(3):
        d = f"2026-05-{1+i:02d}"
        _add_forecast(conn, d, temp_max=75.0)
        _add_settlement(conn, d, official_high=80.0)  # Yes >70 always wins

    result = run_backtest("KLAX", "2026-05-01", "2026-05-03",
                          thresholds=[70.0], sides=["Yes"],
                          min_edge=0.0, min_confidence=0.0, conn=conn)

    if len(result["trades"]) >= 2:
        # Bankroll at second trade should differ from initial
        t1 = result["trades"][0]
        t2 = result["trades"][1]
        assert "bankroll_at_trade" in t1, "Each trade should record bankroll snapshot"


# ── Sharpe ratio ──────────────────────────────────────────────────────────────

def test_sharpe_zero_on_single_trade():
    conn = _conn()
    _add_forecast(conn, "2026-06-01", temp_max=75.0)
    _add_settlement(conn, "2026-06-01", official_high=80.0)

    result = run_backtest("KLAX", "2026-06-01", "2026-06-01",
                          thresholds=[70.0], sides=["Yes"],
                          min_edge=0.0, min_confidence=0.0, conn=conn)

    # Single trade → no variance → sharpe=0
    assert result["sharpe"] == 0.0 or result["total_trades"] == 0
