"""Tests for the confidence scoring engine."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.confidence_engine import compute_confidence
from config import MIN_CONFIDENCE, BET_EDGE_THRESHOLD


def test_no_data_gives_low_confidence():
    score, _ = compute_confidence(0, None, "ALL", 0.0)
    assert score < MIN_CONFIDENCE


def test_large_sample_low_variance_gives_high_confidence():
    score, _ = compute_confidence(50, 0.8, "CLEAR_SKY", 10.0, regime_conf=0.85)
    assert score >= 0.70


def test_low_sample_penalizes():
    score_low,  _ = compute_confidence(3,  1.0, "CLEAR_SKY", 10.0, regime_conf=0.80)
    score_high, _ = compute_confidence(30, 1.0, "CLEAR_SKY", 10.0, regime_conf=0.80)
    assert score_high > score_low


def test_high_variance_penalizes():
    score_low_var,  _ = compute_confidence(20, 1.0, "CLEAR_SKY",    5.0, regime_conf=0.75)
    score_high_var, _ = compute_confidence(20, 4.5, "HIGH_VARIANCE", 5.0, regime_conf=0.40)
    assert score_low_var > score_high_var


def test_larger_edge_increases_score():
    score_small, _ = compute_confidence(15, 1.5, "CLEAR_SKY", 2.0,  regime_conf=0.70)
    score_large, _ = compute_confidence(15, 1.5, "CLEAR_SKY", 20.0, regime_conf=0.70)
    assert score_large > score_small


def test_score_bounded_0_to_1():
    for n, std, regime, edge, rc in [
        (0, None, "HIGH_VARIANCE", 0.0, 0.1),
        (100, 0.1, "CLEAR_SKY", 50.0, 0.99),
        (5, 5.0, "HIGH_VARIANCE", -10.0, 0.3),
    ]:
        score, _ = compute_confidence(n, std, regime, edge, rc)
        assert 0.0 <= score <= 1.0, f"Score out of bounds: {score}"


def test_reasons_list_nonempty():
    _, reasons = compute_confidence(10, 1.5, "OFFSHORE_FLOW", 8.0, 0.80)
    assert len(reasons) >= 3


def test_offshore_flow_note_in_reasons():
    _, reasons = compute_confidence(10, 2.0, "OFFSHORE_FLOW", 6.0, 0.85)
    assert any("OFFSHORE" in r for r in reasons)


if __name__ == "__main__":
    test_no_data_gives_low_confidence()
    test_large_sample_low_variance_gives_high_confidence()
    test_low_sample_penalizes()
    test_high_variance_penalizes()
    test_larger_edge_increases_score()
    test_score_bounded_0_to_1()
    test_reasons_list_nonempty()
    test_offshore_flow_note_in_reasons()
    print("All confidence engine tests passed.")
