"""Tests for the regime-aware bias engine."""

import sys, sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import SCHEMA
from models.bias_engine import compute_and_store_stats, get_stats, win_probability


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def seed(conn, pairs):
    """pairs: (date, forecast, actual, regime)"""
    for d, fc, actual, regime in pairs:
        conn.execute("""
            INSERT INTO forecast_runs
                (timestamp_utc, forecast_date, station_code, model_name, forecast_high, source)
            VALUES (?,?,'KLAX','HRRR/Ventusky',?,'test')
        """, (f"{d}T12:00:00Z", d, fc))
        conn.execute("""
            INSERT INTO daily_settlements (settlement_date, station_code, official_high, source, regime)
            VALUES (?,?,?,?, ?)
            ON CONFLICT(settlement_date, station_code) DO UPDATE SET
                official_high = excluded.official_high, regime = excluded.regime
        """, (d, "KLAX", actual, "test", regime))
    conn.commit()


def test_no_data_returns_empty():
    conn = make_db()
    assert compute_and_store_stats("KLAX", "HRRR/Ventusky", conn) == {}


def test_single_record_returns_empty():
    conn = make_db()
    seed(conn, [("2026-05-01", 70.0, 72.0, "CLEAR_SKY")])
    assert compute_and_store_stats("KLAX", "HRRR/Ventusky", conn) == {}


def test_global_stats_computed():
    conn = make_db()
    # errors: +2, +1, +3 → mean=2.0, std=1.0
    seed(conn, [
        ("2026-05-01", 70.0, 72.0, "CLEAR_SKY"),
        ("2026-05-02", 70.0, 71.0, "CLEAR_SKY"),
        ("2026-05-03", 70.0, 73.0, "CLEAR_SKY"),
    ])
    results = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    assert "ALL" in results
    assert abs(results["ALL"]["avg_bias"] - 2.0) < 1e-4
    assert abs(results["ALL"]["std_dev"]  - 1.0) < 1e-4


def test_regime_stats_computed():
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 74.0, "OFFSHORE_FLOW"),
        ("2026-05-02", 70.0, 75.0, "OFFSHORE_FLOW"),
        ("2026-05-03", 72.0, 73.0, "CLEAR_SKY"),
        ("2026-05-04", 72.0, 73.0, "CLEAR_SKY"),
    ])
    results = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    assert "OFFSHORE_FLOW" in results
    assert results["OFFSHORE_FLOW"]["avg_bias"] == 4.5  # (4+5)/2


def test_get_stats_fallback_to_all():
    """Regime with 1 sample should fall back to ALL stats."""
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 72.0, "CLEAR_SKY"),
        ("2026-05-02", 70.0, 71.0, "CLEAR_SKY"),
        ("2026-05-03", 70.0, 73.0, "MARINE_STRONG"),  # only 1 MARINE_STRONG record
    ])
    compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    stats = get_stats("KLAX", "HRRR/Ventusky", "MARINE_STRONG", conn)
    assert stats is not None
    assert stats["regime_note"] is not None  # should have a fallback note
    assert stats["regime"] == "ALL"


def test_get_stats_uses_regime_when_n_ge_5():
    conn = make_db()
    offshore_pairs = [(f"2026-05-{i:02d}", 70.0, 75.0, "OFFSHORE_FLOW") for i in range(1, 7)]
    seed(conn, offshore_pairs)
    compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    stats = get_stats("KLAX", "HRRR/Ventusky", "OFFSHORE_FLOW", conn)
    assert stats is not None
    assert stats["regime"] == "OFFSHORE_FLOW"
    assert stats["regime_note"] is None


def test_win_probability_t05_correction():
    # At adjusted=68.5, T=68: both Yes and No should be 50%
    assert abs(win_probability(68.5, 1.0, 68, "yes") - 0.5) < 1e-9
    assert abs(win_probability(68.5, 1.0, 68, "no")  - 0.5) < 1e-9


def test_win_probability_sums_to_one():
    for fc in [65.0, 70.0, 75.0]:
        assert abs(win_probability(fc, 1.5, 72, "yes") + win_probability(fc, 1.5, 72, "no") - 1.0) < 1e-9


if __name__ == "__main__":
    test_no_data_returns_empty()
    test_single_record_returns_empty()
    test_global_stats_computed()
    test_regime_stats_computed()
    test_get_stats_fallback_to_all()
    test_get_stats_uses_regime_when_n_ge_5()
    test_win_probability_t05_correction()
    test_win_probability_sums_to_one()
    print("All bias engine tests passed.")
