"""Tests for the regime classification engine."""

import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.regime_engine import classify, parse_cloud_layers


def _clouds(cover: str, base: int) -> str:
    return json.dumps([{"cover": cover, "base": base}])


# ---- parse_cloud_layers ----

def test_parse_clear():
    cover, base = parse_cloud_layers(None)
    assert cover == "CLR" and base is None

def test_parse_bkn():
    cover, base = parse_cloud_layers(_clouds("BKN", 1200))
    assert cover == "BKN" and base == 1200

def test_parse_picks_worst():
    layers = json.dumps([{"cover": "FEW", "base": 3000}, {"cover": "BKN", "base": 1500}])
    cover, base = parse_cloud_layers(layers)
    assert cover == "BKN" and base == 1500  # lowest base


# ---- classify ----

def test_offshore_flow():
    r = classify(wind_direction=350, wind_speed=15, cloud_layers_json=None,
                 visibility_sm=10, dewpoint_spread_f=25, obs_hour_local=14, month=10)
    assert r.regime == "OFFSHORE_FLOW"
    assert r.confidence >= 0.70

def test_offshore_weak_is_still_offshore():
    r = classify(wind_direction=10, wind_speed=6, cloud_layers_json=None,
                 visibility_sm=10, dewpoint_spread_f=20, obs_hour_local=10, month=5)
    assert r.regime == "OFFSHORE_FLOW"

def test_marine_strong_morning():
    r = classify(wind_direction=250, wind_speed=12, cloud_layers_json=_clouds("BKN", 800),
                 visibility_sm=5, dewpoint_spread_f=5, obs_hour_local=8, month=6)
    assert r.regime == "MARINE_STRONG"
    assert r.confidence >= 0.75

def test_late_burnoff_past_1pm():
    r = classify(wind_direction=250, wind_speed=10, cloud_layers_json=_clouds("OVC", 700),
                 visibility_sm=4, dewpoint_spread_f=4, obs_hour_local=14, month=7)
    assert r.regime == "LATE_BURNOFF"

def test_early_burnoff_morning():
    r = classify(wind_direction=240, wind_speed=8, cloud_layers_json=_clouds("FEW", 1500),
                 visibility_sm=10, dewpoint_spread_f=10, obs_hour_local=8, month=5)
    assert r.regime == "EARLY_BURNOFF"

def test_clear_sky():
    r = classify(wind_direction=270, wind_speed=5, cloud_layers_json=_clouds("CLR", 99999),
                 visibility_sm=10, dewpoint_spread_f=30, obs_hour_local=14, month=4)
    assert r.regime == "CLEAR_SKY"
    assert r.confidence >= 0.72

def test_clear_sky_very_dry_boosts_confidence():
    r_dry  = classify(None, None, None, 10, 30, 14, 4)
    r_moist = classify(None, None, None, 10, 10, 14, 4)
    assert r_dry.confidence > r_moist.confidence

def test_fallback_high_variance():
    r = classify(wind_direction=180, wind_speed=3, cloud_layers_json=_clouds("SCT", 1800),
                 visibility_sm=8, dewpoint_spread_f=7, obs_hour_local=11, month=9)
    assert r.regime in ("HIGH_VARIANCE", "MARINE_WEAK")

def test_offshore_takes_priority_over_marine():
    # Offshore wind + thick clouds: offshore should win (wind is dominant signal)
    r = classify(wind_direction=360, wind_speed=20, cloud_layers_json=_clouds("BKN", 1000),
                 visibility_sm=10, dewpoint_spread_f=5, obs_hour_local=10, month=10)
    assert r.regime == "OFFSHORE_FLOW"

def test_notes_populated():
    r = classify(wind_direction=350, wind_speed=20, cloud_layers_json=None,
                 visibility_sm=10, dewpoint_spread_f=28, obs_hour_local=12, month=10)
    assert len(r.notes) >= 1


if __name__ == "__main__":
    test_parse_clear()
    test_parse_bkn()
    test_parse_picks_worst()
    test_offshore_flow()
    test_offshore_weak_is_still_offshore()
    test_marine_strong_morning()
    test_late_burnoff_past_1pm()
    test_early_burnoff_morning()
    test_clear_sky()
    test_clear_sky_very_dry_boosts_confidence()
    test_fallback_high_variance()
    test_offshore_takes_priority_over_marine()
    test_notes_populated()
    print("All regime tests passed.")
