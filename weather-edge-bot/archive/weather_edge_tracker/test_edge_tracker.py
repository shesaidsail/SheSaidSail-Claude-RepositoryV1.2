"""
Tests for whole-degree settlement probability math.

Markets settle on whole-degree official highs, so the CDF cutoff is T + 0.5:
  Yes >T wins when actual >= T+1  →  P(actual > T+0.5) = 1 - CDF(T+0.5)
  No  >T wins when actual <= T    →  P(actual <= T+0.5) = CDF(T+0.5)
"""

from edge_tracker import win_probability


def test_symmetric_at_cutoff():
    """When adjusted forecast == T+0.5, Yes and No are each exactly 50%."""
    yes_prob = win_probability(adjusted_forecast=68.5, std_dev=1.0, threshold=68, side="yes")
    no_prob  = win_probability(adjusted_forecast=68.5, std_dev=1.0, threshold=68, side="no")
    assert abs(yes_prob - 0.50) < 1e-9, f"Yes >68 expected 50%, got {yes_prob:.6f}"
    assert abs(no_prob  - 0.50) < 1e-9, f"No  >68 expected 50%, got {no_prob:.6f}"


def test_cold_forecast_favors_no():
    """When adjusted forecast is below T+0.5, No >T should be more likely than Yes >T."""
    yes_prob = win_probability(adjusted_forecast=67.5, std_dev=1.0, threshold=68, side="yes")
    no_prob  = win_probability(adjusted_forecast=67.5, std_dev=1.0, threshold=68, side="no")
    assert no_prob > yes_prob, (
        f"Expected No ({no_prob:.4f}) > Yes ({yes_prob:.4f}) when forecast < threshold"
    )


def test_warm_forecast_favors_yes():
    """When adjusted forecast is above T+0.5, Yes >T should be more likely than No >T."""
    yes_prob = win_probability(adjusted_forecast=69.5, std_dev=1.0, threshold=68, side="yes")
    no_prob  = win_probability(adjusted_forecast=69.5, std_dev=1.0, threshold=68, side="no")
    assert yes_prob > no_prob, (
        f"Expected Yes ({yes_prob:.4f}) > No ({no_prob:.4f}) when forecast > threshold"
    )


def test_yes_and_no_sum_to_one():
    """Yes and No probabilities must always sum to 1.0 (exhaustive, mutually exclusive)."""
    for forecast in [66.0, 68.5, 71.0]:
        yes_prob = win_probability(adjusted_forecast=forecast, std_dev=1.5, threshold=68, side="yes")
        no_prob  = win_probability(adjusted_forecast=forecast, std_dev=1.5, threshold=68, side="no")
        assert abs(yes_prob + no_prob - 1.0) < 1e-9, (
            f"Yes + No = {yes_prob + no_prob:.10f} (expected 1.0) at forecast={forecast}"
        )


if __name__ == "__main__":
    test_symmetric_at_cutoff()
    test_cold_forecast_favors_no()
    test_warm_forecast_favors_yes()
    test_yes_and_no_sum_to_one()
    print("All tests passed.")
