"""
Tests for models/signal_ranker.py

Validates A+/B/Watchlist/Avoid grade assignment, hard stops,
spread filters, and METAR freshness requirements.
"""

import sys
from pathlib import Path
import sqlite3

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.signal_ranker import grade_signal, grade_all
from database.db import init_db


# ── Helpers ────────────────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS model_stats (
            station_code TEXT, model_name TEXT, regime TEXT,
            sample_size INTEGER, avg_bias REAL, std_dev REAL,
            rolling_7d_bias REAL, rolling_30d_bias REAL,
            confidence REAL, updated_at TEXT,
            PRIMARY KEY (station_code, model_name, regime)
        );
        CREATE TABLE IF NOT EXISTS official_observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_code TEXT, timestamp_utc TEXT, observed_temp REAL,
            dewpoint REAL, wind_direction REAL, wind_speed REAL,
            gust_speed REAL, visibility_sm REAL, cloud_layers TEXT,
            pressure_inHg REAL, weather_string TEXT,
            max_temp_6h REAL, min_temp_6h REAL, max_temp_24h REAL,
            raw_metar TEXT, UNIQUE(station_code, timestamp_utc)
        );
    """)
    return conn


def _make_edge_result(edge=12.0, confidence=0.75, spread=3.0,
                      station="KLAX", regime="CLEAR_SKY",
                      adj_forecast=72.0, threshold=70.0):
    return {
        "station_code":      station,
        "edge":              edge,
        "confidence":        confidence,
        "spread":            spread,
        "signal":            "BET" if edge > 0 else "FADE",
        "regime":            regime,
        "adjusted_forecast": adj_forecast,
        "threshold_f":       threshold,
        "model_prob":        0.72,
        "fair_value":        60.0,
        "market_price":      48.0,
        "forecast_high":     71.0,
        "grade":             None,
    }


def _add_regime_sample(conn, station="KLAX", regime="CLEAR_SKY", n=10):
    conn.execute("""
        INSERT OR REPLACE INTO model_stats
            (station_code, model_name, regime, sample_size, avg_bias, std_dev, confidence)
        VALUES (?,?,?,?,?,?,?)
    """, (station, "OpenMeteo", regime, n, 0.5, 2.5, 0.65))
    conn.commit()


def _add_fresh_metar(conn, station="KLAX", minutes_ago=5):
    from datetime import datetime, timezone, timedelta
    ts = (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("""
        INSERT OR REPLACE INTO official_observations
            (station_code, timestamp_utc, observed_temp, cloud_layers)
        VALUES (?,?,?,?)
    """, (station, ts, 68.0, "[]"))
    conn.commit()


# ── Grade A+ tests ─────────────────────────────────────────────────────────────

def test_aplus_all_conditions_met():
    conn = _conn()
    _add_regime_sample(conn, n=10)
    _add_fresh_metar(conn, minutes_ago=10)

    er = _make_edge_result(edge=12.0, confidence=0.75, spread=3.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] == "A+", f"Expected A+, got {result['grade']}"


def test_aplus_requires_edge_10():
    """9.9¢ edge should NOT qualify for A+."""
    conn = _conn()
    _add_regime_sample(conn, n=10)
    _add_fresh_metar(conn, minutes_ago=10)

    er = _make_edge_result(edge=9.9, confidence=0.75, spread=3.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] != "A+", f"Should not be A+ with edge=9.9"


def test_aplus_requires_confidence_70():
    """0.69 confidence should not qualify for A+."""
    conn = _conn()
    _add_regime_sample(conn, n=10)
    _add_fresh_metar(conn, minutes_ago=10)

    er = _make_edge_result(edge=12.0, confidence=0.69, spread=3.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] != "A+", f"Should not be A+ with conf=0.69"


def test_aplus_requires_tight_spread():
    """Spread > 5¢ should prevent A+."""
    conn = _conn()
    _add_regime_sample(conn, n=10)
    _add_fresh_metar(conn, minutes_ago=10)

    er = _make_edge_result(edge=12.0, confidence=0.75, spread=5.5)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] != "A+", f"Should not be A+ with spread=5.5"


def test_aplus_requires_regime_sample_n5():
    """Regime sample < 5 should prevent A+."""
    conn = _conn()
    _add_regime_sample(conn, n=4)      # below A+ threshold
    _add_fresh_metar(conn, minutes_ago=10)

    er = _make_edge_result(edge=12.0, confidence=0.75, spread=3.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] != "A+", f"Should not be A+ with regime_n=4"


# ── Grade B tests ──────────────────────────────────────────────────────────────

def test_b_grade_conditions():
    """7¢ edge, 0.60 confidence, 6¢ spread, 4 regime samples → B."""
    conn = _conn()
    _add_regime_sample(conn, n=4)
    _add_fresh_metar(conn, minutes_ago=60)

    er = _make_edge_result(edge=7.0, confidence=0.60, spread=6.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] == "B", f"Expected B, got {result['grade']}"


def test_b_requires_edge_5():
    conn = _conn()
    _add_regime_sample(conn, n=5)
    _add_fresh_metar(conn, minutes_ago=30)

    er = _make_edge_result(edge=4.9, confidence=0.60, spread=5.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] not in ("A+", "B"), f"Edge 4.9 should not grade A+ or B"


# ── Watchlist tests ────────────────────────────────────────────────────────────

def test_watchlist_low_edge():
    """3¢ edge with good confidence → Watchlist."""
    conn = _conn()
    _add_regime_sample(conn, n=3)
    _add_fresh_metar(conn, minutes_ago=120)

    er = _make_edge_result(edge=3.0, confidence=0.50, spread=10.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] == "Watchlist", f"Expected Watchlist, got {result['grade']}"


# ── Avoid / hard stops ─────────────────────────────────────────────────────────

def test_avoid_no_metar_with_tiny_edge():
    """No METAR + edge below WATCHLIST min → Avoid (hard stop triggers)."""
    conn = _conn()
    _add_regime_sample(conn, n=5)
    # No METAR inserted → NO_METAR quality flag

    er = _make_edge_result(edge=1.5, confidence=0.55, spread=5.0)  # below 2.0 WATCHLIST min
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] == "Avoid", f"Expected Avoid with no METAR + tiny edge, got {result['grade']}"
    assert "NO_METAR" in result["quality_flags"]


def test_watchlist_no_metar_medium_edge():
    """No METAR but edge > 2¢ → only Watchlist (not Avoid)."""
    conn = _conn()
    _add_regime_sample(conn, n=5)
    # No METAR

    er = _make_edge_result(edge=4.0, confidence=0.50, spread=5.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] == "Watchlist", f"Expected Watchlist with no METAR + medium edge, got {result['grade']}"


def test_stale_metar_prevents_aplus():
    """METAR older than 30 min prevents A+ grade."""
    conn = _conn()
    _add_regime_sample(conn, n=10)
    _add_fresh_metar(conn, minutes_ago=45)  # 45 min > A+ max 30 min

    er = _make_edge_result(edge=12.0, confidence=0.75, spread=3.0)
    result = grade_signal(er, conn, "OpenMeteo")

    assert result["grade"] != "A+", f"45-min-old METAR should not qualify for A+"


# ── grade_all ordering ─────────────────────────────────────────────────────────

def test_grade_all_sorted_correctly():
    """grade_all should return A+ first, then B, then Watchlist, then Avoid."""
    conn = _conn()
    _add_regime_sample(conn, n=10)
    _add_fresh_metar(conn, minutes_ago=5)

    results = [
        _make_edge_result(edge=3.0,  confidence=0.45, spread=12.0),   # Watchlist
        _make_edge_result(edge=12.0, confidence=0.75, spread=3.0),    # A+
        _make_edge_result(edge=7.0,  confidence=0.60, spread=6.0),    # B
        _make_edge_result(edge=1.0,  confidence=0.35, spread=20.0),   # Avoid
    ]

    graded = grade_all(results, conn, "OpenMeteo")
    grade_order = [g["grade"] for g in graded]

    assert grade_order[0] == "A+",       f"A+ should be first: {grade_order}"
    assert "B" in grade_order,           f"B missing: {grade_order}"
    assert grade_order.index("A+") < grade_order.index("B"), "A+ must precede B"


def test_grade_result_has_required_fields():
    conn = _conn()
    _add_regime_sample(conn, n=5)
    _add_fresh_metar(conn, minutes_ago=10)

    er = _make_edge_result(edge=12.0, confidence=0.75, spread=3.0)
    result = grade_signal(er, conn, "OpenMeteo")

    for field in ("grade", "grade_reasons", "quality_flags", "regime_n", "metar_age_min"):
        assert field in result, f"Missing field: {field}"
