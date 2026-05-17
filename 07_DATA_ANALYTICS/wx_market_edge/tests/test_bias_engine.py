"""Tests for the blended bias engine."""

import sys, sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db      import SCHEMA
from models.bias_engine import compute_and_store_stats, get_stats, blended_bias, _blend_weight


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.execute("""
        INSERT INTO stations (icao,name,latitude,longitude,timezone,utc_offset)
        VALUES ('KLAX','Los Angeles',33.94,-118.41,'America/Los_Angeles',-7)
    """)
    conn.commit()
    return conn


def seed(conn, pairs):
    for d, fc, actual, regime in pairs:
        conn.execute("""
            INSERT INTO forecast_runs (fetched_at,forecast_date,station_code,model_name,temp_max)
            VALUES (?,?,'KLAX','OpenMeteo',?)
        """, (f"{d}T06:00:00Z", d, fc))
        conn.execute("""
            INSERT INTO daily_settlements (settlement_date,station_code,official_high,regime)
            VALUES (?,?,?,?)
            ON CONFLICT(settlement_date,station_code) DO UPDATE SET
                official_high=excluded.official_high, regime=excluded.regime
        """, (d, "KLAX", actual, regime))
    conn.commit()


def test_blend_weight_extremes():
    assert abs(_blend_weight(0) - 0.10) < 1e-6
    assert abs(_blend_weight(4) - 0.10) < 1e-6
    assert abs(_blend_weight(21) - 0.90) < 1e-6


def test_blend_weight_midpoint():
    w = _blend_weight(12)
    assert 0.10 < w < 0.90


def test_no_data_returns_empty():
    conn = make_db()
    assert compute_and_store_stats("KLAX", "OpenMeteo", conn) == {}


def test_global_stats_computed():
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 72.0, "CLEAR_SKY"),
        ("2026-05-02", 70.0, 71.0, "CLEAR_SKY"),
        ("2026-05-03", 70.0, 73.0, "CLEAR_SKY"),
    ])
    results = compute_and_store_stats("KLAX", "OpenMeteo", conn)
    assert "ALL" in results
    assert abs(results["ALL"]["avg_bias"] - 2.0) < 1e-3


def test_blended_bias_no_data_returns_defaults():
    conn = make_db()
    bias, std, note = blended_bias("KLAX", "OpenMeteo", "CLEAR_SKY", conn)
    assert bias == 0.0
    assert std  == 3.0
    assert "no regime data" in note.lower()


def test_blended_bias_uses_global_when_regime_small():
    conn = make_db()
    # 3 CLEAR_SKY records, 1 OFFSHORE
    seed(conn, [
        ("2026-05-01", 70.0, 72.0, "CLEAR_SKY"),
        ("2026-05-02", 70.0, 73.0, "CLEAR_SKY"),
        ("2026-05-03", 70.0, 74.0, "CLEAR_SKY"),
        ("2026-05-04", 70.0, 76.0, "OFFSHORE_FLOW"),
    ])
    compute_and_store_stats("KLAX", "OpenMeteo", conn)
    bias, std, note = blended_bias("KLAX", "OpenMeteo", "OFFSHORE_FLOW", conn)
    # regime n=1, so weight 0.10; should be close to global bias
    assert note != ""   # has a note
    assert 0 < bias < 10   # somewhere between 0 and 6


def test_get_stats_fallback():
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 72.0, "CLEAR_SKY"),
        ("2026-05-02", 70.0, 71.0, "CLEAR_SKY"),
        ("2026-05-03", 70.0, 73.0, "MARINE_STRONG"),
    ])
    compute_and_store_stats("KLAX", "OpenMeteo", conn)
    stats = get_stats("KLAX", "OpenMeteo", "MARINE_STRONG", conn)
    assert stats is not None
    assert stats["regime_note"] is not None
    assert stats["regime"] == "ALL"


if __name__ == "__main__":
    test_blend_weight_extremes()
    test_blend_weight_midpoint()
    test_no_data_returns_empty()
    test_global_stats_computed()
    test_blended_bias_no_data_returns_defaults()
    test_blended_bias_uses_global_when_regime_small()
    test_get_stats_fallback()
    print("All bias engine tests passed.")
