"""Tests for the edge calculator (win_probability + T+0.5 correction)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.edge_calculator import win_probability


def test_symmetry_at_half_degree():
    """At adj=68.5, T=68: exactly 50% for both sides."""
    assert abs(win_probability(68.5, 1.0, 68, "yes") - 0.5) < 1e-9
    assert abs(win_probability(68.5, 1.0, 68, "no")  - 0.5) < 1e-9


def test_yes_no_sum_to_one():
    for fc in [60.0, 70.0, 80.0, 90.0]:
        p_yes = win_probability(fc, 1.5, 72, "yes")
        p_no  = win_probability(fc, 1.5, 72, "no")
        assert abs(p_yes + p_no - 1.0) < 1e-9, f"Sum ≠ 1 at fc={fc}"


def test_cold_forecast_favors_no():
    """If adjusted forecast is well below threshold, No should dominate."""
    p_no = win_probability(60.0, 2.0, 72, "no")
    assert p_no > 0.90


def test_warm_forecast_favors_yes():
    """If adjusted forecast is well above threshold, Yes should dominate."""
    p_yes = win_probability(85.0, 2.0, 72, "yes")
    assert p_yes > 0.90


def test_probabilities_bounded():
    for fc in [50, 70, 90]:
        for t in [60, 70, 80]:
            for side in ["yes", "no"]:
                p = win_probability(float(fc), 2.0, float(t), side)
                assert 0 <= p <= 1, f"p={p} out of bounds"


def test_invalid_side_raises():
    try:
        win_probability(72.0, 2.0, 70, "maybe")
        assert False, "Should have raised"
    except ValueError:
        pass


def test_larger_std_widens_distribution():
    """Larger std dev → probability closer to 0.5 for extreme threshold."""
    p_tight = win_probability(85.0, 0.5, 72, "yes")
    p_wide  = win_probability(85.0, 5.0, 72, "yes")
    assert p_tight > p_wide   # tight std → higher confidence in win


if __name__ == "__main__":
    test_symmetry_at_half_degree()
    test_yes_no_sum_to_one()
    test_cold_forecast_favors_no()
    test_warm_forecast_favors_yes()
    test_probabilities_bounded()
    test_invalid_side_raises()
    test_larger_std_widens_distribution()
    print("All edge calculator tests passed.")
