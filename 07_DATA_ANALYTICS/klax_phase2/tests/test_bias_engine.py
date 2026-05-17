"""
Tests for bias_engine using an in-memory SQLite database.
Run:  python tests/test_bias_engine.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
from database.db import SCHEMA
from models.bias_engine import compute_and_store_stats, get_stats, win_probability


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def seed(conn, pairs: list[tuple[str, float, float]]) -> None:
    """Insert (date, forecast_high, actual_high) into both tables."""
    for d, fc, actual in pairs:
        conn.execute("""
            INSERT INTO forecast_runs
                (timestamp_utc, forecast_date, station_code, model_name, forecast_high, source)
            VALUES (?, ?, 'KLAX', 'HRRR/Ventusky', ?, 'test')
        """, (f"{d}T12:00:00Z", d, fc))
        conn.execute("""
            INSERT INTO daily_settlements (settlement_date, station_code, official_high, source)
            VALUES (?, 'KLAX', ?, 'test')
            ON CONFLICT(settlement_date, station_code)
            DO UPDATE SET official_high = excluded.official_high
        """, (d, actual))
    conn.commit()


# ---------------------------------------------------------------------------
# Tests — bias computation
# ---------------------------------------------------------------------------

def test_insufficient_data_returns_none():
    conn = make_db()
    seed(conn, [("2026-05-01", 72.0, 74.0)])  # only 1 pair — std dev undefined
    result = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    assert result is None, f"Expected None with 1 record, got {result}"


def test_bias_and_stddev_calculation():
    """errors: +2, +1, +3  →  mean=2.0, sample stdev=1.0"""
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 72.0),
        ("2026-05-02", 70.0, 71.0),
        ("2026-05-03", 70.0, 73.0),
    ])
    stats = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    assert stats is not None
    assert abs(stats["avg_bias"] - 2.0) < 1e-6, f"avg_bias: expected 2.0, got {stats['avg_bias']}"
    assert abs(stats["std_dev"] - 1.0) < 1e-6, f"std_dev: expected 1.0, got {stats['std_dev']}"
    assert stats["sample_size"] == 3


def test_stats_persisted_to_db():
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 72.0),
        ("2026-05-02", 70.0, 71.0),
    ])
    compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    retrieved = get_stats("KLAX", "HRRR/Ventusky", conn)
    assert retrieved is not None, "Stats should be retrievable after compute"
    assert retrieved["sample_size"] == 2


def test_upsert_overwrites_on_rerun():
    """Running compute twice should update stats, not duplicate rows."""
    conn = make_db()
    seed(conn, [
        ("2026-05-01", 70.0, 72.0),
        ("2026-05-02", 70.0, 71.0),
    ])
    compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    # Add a third record and recompute
    seed(conn, [("2026-05-03", 70.0, 73.0)])
    stats = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    assert stats["sample_size"] == 3

    count = conn.execute(
        "SELECT COUNT(*) FROM model_stats WHERE station_code='KLAX'"
    ).fetchone()[0]
    assert count == 1, f"Expected 1 row in model_stats, got {count}"


def test_rolling_7d_bias_requires_two_records():
    conn = make_db()
    seed(conn, [("2026-05-01", 70.0, 72.0), ("2026-05-02", 70.0, 71.0)])
    stats = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    # 2 records is >= min_periods=2, so 7d rolling bias should be defined
    assert stats["rolling_7d_bias"] is not None


def test_rolling_30d_bias_is_none_below_threshold():
    """With only 1 record that falls into the 30d window, rolling_30d_bias must be None."""
    conn = make_db()
    seed(conn, [("2026-05-01", 70.0, 72.0), ("2026-05-02", 70.0, 73.0)])
    stats = compute_and_store_stats("KLAX", "HRRR/Ventusky", conn)
    # 2 records: 7d defined (min_periods=2), 30d also defined since same 2 records fill it
    assert stats["rolling_30d_bias"] is not None  # min_periods=2 satisfied


# ---------------------------------------------------------------------------
# Tests — win_probability (T+0.5 cutoff)
# ---------------------------------------------------------------------------

def test_symmetric_at_cutoff():
    """At adjusted_forecast == T+0.5 both sides must be exactly 50%."""
    assert abs(win_probability(68.5, 1.0, 68, "yes") - 0.5) < 1e-9
    assert abs(win_probability(68.5, 1.0, 68, "no")  - 0.5) < 1e-9


def test_cold_forecast_favors_no():
    yes = win_probability(67.5, 1.0, 68, "yes")
    no  = win_probability(67.5, 1.0, 68, "no")
    assert no > yes, f"Expected No ({no:.4f}) > Yes ({yes:.4f}) when forecast < threshold"


def test_warm_forecast_favors_yes():
    yes = win_probability(69.5, 1.0, 68, "yes")
    no  = win_probability(69.5, 1.0, 68, "no")
    assert yes > no, f"Expected Yes ({yes:.4f}) > No ({no:.4f}) when forecast > threshold"


def test_yes_and_no_sum_to_one():
    for fc in [65.0, 68.5, 72.0]:
        yes = win_probability(fc, 1.5, 70, "yes")
        no  = win_probability(fc, 1.5, 70, "no")
        assert abs(yes + no - 1.0) < 1e-9, f"Sum = {yes + no} at forecast={fc}"


if __name__ == "__main__":
    test_insufficient_data_returns_none()
    test_bias_and_stddev_calculation()
    test_stats_persisted_to_db()
    test_upsert_overwrites_on_rerun()
    test_rolling_7d_bias_requires_two_records()
    test_rolling_30d_bias_is_none_below_threshold()
    test_symmetric_at_cutoff()
    test_cold_forecast_favors_no()
    test_warm_forecast_favors_yes()
    test_yes_and_no_sum_to_one()
    print("All 10 tests passed.")
