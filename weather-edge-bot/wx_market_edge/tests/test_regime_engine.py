"""Tests for the multi-station regime engine."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.regime_engine import classify


def test_storm_risk_high_precip():
    r = classify(wind_direction=200, wind_speed=20, gust_speed=35,
                 cloud_cover_pct=90, cloud_layers_json=None, pressure=1008,
                 dew_point_spread=5, humidity=85, visibility_sm=3,
                 precip_prob=70, temp_f=75, obs_hour_local=14, month=7)
    assert r.regime == "STORM_RISK"


def test_rain_risk():
    r = classify(wind_direction=200, wind_speed=10, gust_speed=12,
                 cloud_cover_pct=85, cloud_layers_json=None, pressure=1012,
                 dew_point_spread=4, humidity=80, visibility_sm=5,
                 precip_prob=40, temp_f=68, obs_hour_local=10, month=4)
    assert r.regime == "RAIN_RISK"


def test_offshore_flow():
    r = classify(wind_direction=70, wind_speed=15, gust_speed=20,
                 cloud_cover_pct=10, cloud_layers_json=None, pressure=1018,
                 dew_point_spread=35, humidity=20, visibility_sm=15,
                 precip_prob=0, temp_f=80, obs_hour_local=13, month=10)
    assert r.regime == "OFFSHORE_FLOW"


def test_marine_strong():
    r = classify(wind_direction=250, wind_speed=18, gust_speed=22,
                 cloud_cover_pct=80, cloud_layers_json='[{"cover":"BKN","base":1200}]',
                 pressure=1014, dew_point_spread=5, humidity=85, visibility_sm=4,
                 precip_prob=5, temp_f=62, obs_hour_local=9, month=6)
    assert r.regime == "MARINE_STRONG"


def test_dry_heat():
    r = classify(wind_direction=340, wind_speed=5, gust_speed=8,
                 cloud_cover_pct=5, cloud_layers_json=None, pressure=1010,
                 dew_point_spread=45, humidity=10, visibility_sm=20,
                 precip_prob=0, temp_f=105, obs_hour_local=14, month=7)
    assert r.regime == "DRY_HEAT"


def test_humid_heat():
    r = classify(wind_direction=190, wind_speed=8, gust_speed=10,
                 cloud_cover_pct=40, cloud_layers_json=None, pressure=1010,
                 dew_point_spread=8, humidity=78, visibility_sm=8,
                 precip_prob=15, temp_f=92, obs_hour_local=15, month=8)
    assert r.regime == "HUMID_HEAT"


def test_clear_sky():
    r = classify(wind_direction=None, wind_speed=3, gust_speed=None,
                 cloud_cover_pct=10, cloud_layers_json=None, pressure=1020,
                 dew_point_spread=25, humidity=30, visibility_sm=10,
                 precip_prob=0, temp_f=72, obs_hour_local=12, month=5)
    assert r.regime == "CLEAR_SKY"


def test_high_variance_forecast_spread():
    r = classify(wind_direction=180, wind_speed=5, gust_speed=None,
                 cloud_cover_pct=20, cloud_layers_json=None, pressure=1015,
                 dew_point_spread=20, humidity=35, visibility_sm=12,
                 precip_prob=5, temp_f=75, obs_hour_local=12, month=4,
                 forecast_spread=22)
    assert r.regime == "HIGH_VARIANCE"


def test_low_variance_forecast_spread():
    r = classify(wind_direction=180, wind_speed=5, gust_speed=None,
                 cloud_cover_pct=20, cloud_layers_json=None, pressure=1015,
                 dew_point_spread=20, humidity=35, visibility_sm=12,
                 precip_prob=5, temp_f=75, obs_hour_local=12, month=4,
                 forecast_spread=6)
    assert r.regime == "LOW_VARIANCE"


def test_result_has_notes():
    r = classify(wind_direction=200, wind_speed=20, gust_speed=35,
                 cloud_cover_pct=90, cloud_layers_json=None, pressure=1008,
                 dew_point_spread=5, humidity=85, visibility_sm=3,
                 precip_prob=70, temp_f=75, obs_hour_local=14, month=7)
    assert len(r.notes) >= 1


def test_confidence_bounded():
    for kw in [
        dict(wind_direction=None, wind_speed=None, gust_speed=None,
             cloud_cover_pct=None, cloud_layers_json=None, pressure=None,
             dew_point_spread=None, humidity=None, visibility_sm=None,
             precip_prob=None, temp_f=None, obs_hour_local=None, month=None),
        dict(wind_direction=270, wind_speed=25, gust_speed=30,
             cloud_cover_pct=100, cloud_layers_json=None, pressure=995,
             dew_point_spread=2, humidity=99, visibility_sm=0.5,
             precip_prob=95, temp_f=55, obs_hour_local=8, month=12),
    ]:
        r = classify(**kw)
        assert 0 <= r.confidence <= 1, f"Confidence out of bounds: {r}"


if __name__ == "__main__":
    test_storm_risk_high_precip()
    test_rain_risk()
    test_offshore_flow()
    test_marine_strong()
    test_dry_heat()
    test_humid_heat()
    test_clear_sky()
    test_high_variance_forecast_spread()
    test_low_variance_forecast_spread()
    test_result_has_notes()
    test_confidence_bounded()
    print("All regime engine tests passed.")
