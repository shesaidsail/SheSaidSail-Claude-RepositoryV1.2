"""Tests for the paper trading engine."""

import sys, sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db         import SCHEMA
from trading.paper_trader import open_trade, settle_trades, performance_summary


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.execute("""
        INSERT INTO stations (icao,name,latitude,longitude,timezone,utc_offset)
        VALUES ('KLAX','LA',33.94,-118.41,'America/Los_Angeles',-7)
    """)
    conn.commit()
    return conn


BASE_EDGE = {
    "station_code":      "KLAX",
    "market_ticker":     "TEST-001",
    "forecast_date":     "2026-06-01",
    "threshold_f":       72.0,
    "side":              "Yes",
    "market_price":      40.0,
    "fair_value":        60.0,
    "edge":              20.0,
    "confidence":        0.70,
    "regime":            "CLEAR_SKY",
    "adjusted_forecast": 74.0,
    "model_prob":        0.60,
    "signal":            "BET",
    "spread":            2.0,
}


def test_open_trade_creates_row():
    conn = make_db()
    tid = open_trade(BASE_EDGE, conn)
    assert tid is not None and tid > 0


def test_low_edge_not_opened():
    conn = make_db()
    e = {**BASE_EDGE, "edge": 1.0}
    assert open_trade(e, conn) is None


def test_low_confidence_not_opened():
    conn = make_db()
    e = {**BASE_EDGE, "confidence": 0.30}
    assert open_trade(e, conn) is None


def test_pass_signal_not_opened():
    conn = make_db()
    e = {**BASE_EDGE, "signal": "PASS"}
    assert open_trade(e, conn) is None


def test_settle_yes_win():
    conn = make_db()
    open_trade(BASE_EDGE, conn)
    # Seed a settlement above threshold
    conn.execute("""
        INSERT INTO daily_settlements (settlement_date,station_code,official_high)
        VALUES ('2026-06-01','KLAX',75.0)
    """)
    conn.commit()
    settled = settle_trades("2026-06-01", conn)
    assert len(settled) == 1
    assert settled[0]["result"] == "WIN"
    assert settled[0]["pnl_cents"] == 60.0   # 100 - 40


def test_settle_yes_loss():
    conn = make_db()
    open_trade(BASE_EDGE, conn)
    conn.execute("""
        INSERT INTO daily_settlements (settlement_date,station_code,official_high)
        VALUES ('2026-06-01','KLAX',70.0)   -- below threshold
    """)
    conn.commit()
    settled = settle_trades("2026-06-01", conn)
    assert settled[0]["result"] == "LOSS"
    assert settled[0]["pnl_cents"] == -40.0  # 0 - 40


def test_performance_summary_empty():
    conn = make_db()
    perf = performance_summary(conn)
    assert perf.get("total", 0) == 0


def test_performance_summary_after_trades():
    conn = make_db()
    # Win trade
    open_trade({**BASE_EDGE, "forecast_date": "2026-06-01"}, conn)
    conn.execute("INSERT INTO daily_settlements (settlement_date,station_code,official_high) VALUES ('2026-06-01','KLAX',75.0)")
    conn.commit()
    settle_trades("2026-06-01", conn)
    # Loss trade
    open_trade({**BASE_EDGE, "forecast_date": "2026-06-02"}, conn)
    conn.execute("INSERT INTO daily_settlements (settlement_date,station_code,official_high) VALUES ('2026-06-02','KLAX',70.0)")
    conn.commit()
    settle_trades("2026-06-02", conn)

    perf = performance_summary(conn)
    assert perf["total"] == 2
    assert perf["wins"]   == 1
    assert perf["losses"] == 1
    assert abs(perf["win_rate"] - 0.5) < 1e-6


if __name__ == "__main__":
    test_open_trade_creates_row()
    test_low_edge_not_opened()
    test_low_confidence_not_opened()
    test_pass_signal_not_opened()
    test_settle_yes_win()
    test_settle_yes_loss()
    test_performance_summary_empty()
    test_performance_summary_after_trades()
    print("All paper trader tests passed.")
