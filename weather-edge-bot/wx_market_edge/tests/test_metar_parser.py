"""Tests for the METAR raw-string parser."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.metar import parse_raw_metar


SAMPLE_KLAX = (
    "KLAX 172353Z 21013KT 10SM SCT150 BKN250 22/14 A3001 "
    "RMK AO2 SLP160 T02170139 10244 20189 58022"
)

SAMPLE_GUSTY = "KJFK 171955Z 29018G28KT 10SM FEW060 BKN200 24/11 A2997 RMK AO2 T02440111"

SAMPLE_VRB = "KMIA 171800Z VRB03KT 9SM FEW040 SCT200 32/24 A3003"

SAMPLE_LOW_VIS = "KSFO 170455Z 28012KT 2 1/2SM BR OVC003 13/12 A3012 RMK AO2"


def test_basic_parse():
    obs = parse_raw_metar(SAMPLE_KLAX)
    assert obs is not None
    assert obs["wind_direction"] == 210
    assert obs["wind_speed"]     == 13
    assert obs["gust_speed"]     is None
    assert obs["visibility_sm"]  == 10.0


def test_precise_temp_remark():
    obs = parse_raw_metar(SAMPLE_KLAX)
    assert obs is not None
    # T02170139 → temp=21.7°C=71.06°F, dew=13.9°C=57.02°F
    assert obs["observed_temp"] is not None
    assert abs(obs["observed_temp"] - 71.06) < 0.2


def test_gust_parsed():
    obs = parse_raw_metar(SAMPLE_GUSTY)
    assert obs is not None
    assert obs["wind_speed"]  == 18
    assert obs["gust_speed"]  == 28


def test_vrb_wind():
    obs = parse_raw_metar(SAMPLE_VRB)
    assert obs is not None
    assert obs["wind_direction"] is None   # VRB → None
    assert obs["wind_speed"]     == 3


def test_fractional_visibility():
    obs = parse_raw_metar(SAMPLE_LOW_VIS)
    assert obs is not None
    assert abs(obs["visibility_sm"] - 2.5) < 0.01


def test_cloud_layers_json():
    import json
    obs = parse_raw_metar(SAMPLE_KLAX)
    assert obs is not None
    layers = json.loads(obs["cloud_layers"])
    assert len(layers) >= 1
    assert any(l["cover"] == "SCT" for l in layers)


def test_pressure_parsed():
    obs = parse_raw_metar(SAMPLE_KLAX)
    assert obs is not None
    assert abs(obs["pressure_inHg"] - 30.01) < 0.01


def test_timestamp_present():
    obs = parse_raw_metar(SAMPLE_KLAX)
    assert obs is not None
    assert "timestamp_utc" in obs
    assert obs["timestamp_utc"].endswith("Z")


def test_6h_max_temp():
    obs = parse_raw_metar(SAMPLE_KLAX)
    assert obs is not None
    # 10244 → 6h max = 24.4°C = 75.9°F
    assert obs["max_temp_6h"] is not None


def test_invalid_metar_returns_none():
    assert parse_raw_metar("not a metar at all") is None
    assert parse_raw_metar("") is None


if __name__ == "__main__":
    test_basic_parse()
    test_precise_temp_remark()
    test_gust_parsed()
    test_vrb_wind()
    test_fractional_visibility()
    test_cloud_layers_json()
    test_pressure_parsed()
    test_timestamp_present()
    test_6h_max_temp()
    test_invalid_metar_returns_none()
    print("All METAR parser tests passed.")
