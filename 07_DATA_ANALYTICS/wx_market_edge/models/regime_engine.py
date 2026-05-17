"""
Multi-station weather regime classifier.

Works on both METAR observations and Open-Meteo forecast data.
Returns a RegimeResult with primary regime, confidence, and notes.
"""

import json
from dataclasses import dataclass, field


REGIMES = [
    "MARINE_STRONG",
    "MARINE_WEAK",
    "OFFSHORE_FLOW",
    "ONSHORE_FLOW",
    "EARLY_BURNOFF",
    "LATE_BURNOFF",
    "CLEAR_SKY",
    "CLOUDY_CAP",
    "HEAT_SPIKE_RISK",
    "HIGH_VARIANCE",
    "LOW_VARIANCE",
    "RAIN_RISK",
    "STORM_RISK",
    "DRY_HEAT",
    "HUMID_HEAT",
    "UNKNOWN",
]


@dataclass
class RegimeResult:
    regime:     str
    confidence: float          # 0-1
    notes:      list[str] = field(default_factory=list)
    secondary:  str | None = None


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def _low_cloud(cloud_layers_json: str | None) -> bool:
    """True if any cloud layer below 2000 ft."""
    if not cloud_layers_json:
        return False
    try:
        layers = json.loads(cloud_layers_json)
        return any(
            l.get("base", 99999) < 2000 and l.get("cover") in ("BKN", "OVC", "SCT")
            for l in layers
        )
    except Exception:
        return False


def _cloud_cover_frac(cloud_layers_json: str | None) -> float:
    """Estimate fractional cloud cover 0-1 from layers."""
    if not cloud_layers_json:
        return 0.0
    cover_map = {"FEW": 0.2, "SCT": 0.4, "BKN": 0.75, "OVC": 1.0, "VV": 1.0}
    try:
        layers = json.loads(cloud_layers_json)
        if not layers:
            return 0.0
        return max(cover_map.get(l.get("cover", ""), 0.0) for l in layers)
    except Exception:
        return 0.0


def classify(
    wind_direction:    float | None,
    wind_speed:        float | None,   # knots (METAR) or mph (OM) — treated generically
    gust_speed:        float | None,
    cloud_cover_pct:   float | None,   # 0-100 from Open-Meteo, or derived from METAR
    cloud_layers_json: str | None,     # METAR cloud layers JSON
    pressure:          float | None,   # hPa or inHg (used comparatively only)
    dew_point_spread:  float | None,   # temp - dewpoint in °F
    humidity:          float | None,   # 0-100
    visibility_sm:     float | None,
    precip_prob:       float | None,   # 0-100
    temp_f:            float | None,
    obs_hour_local:    int | None,
    month:             int | None,
    forecast_spread:   float | None = None,  # temp_max - temp_min if available
) -> RegimeResult:
    """
    Classify weather regime.  Priority order:
    STORM_RISK > RAIN_RISK > OFFSHORE_FLOW > MARINE_STRONG >
    HEAT_SPIKE_RISK > DRY_HEAT > HUMID_HEAT >
    MARINE_WEAK > CLOUDY_CAP > EARLY_BURNOFF > LATE_BURNOFF >
    CLEAR_SKY > HIGH_VARIANCE > LOW_VARIANCE > UNKNOWN
    """
    notes = []
    wind = wind_speed or 0
    gust = gust_speed or wind

    # Normalise cloud cover
    cloud_pct = cloud_cover_pct
    if cloud_pct is None and cloud_layers_json is not None:
        cloud_pct = _cloud_cover_frac(cloud_layers_json) * 100
    cloud_pct = cloud_pct or 0

    low_cloud = _low_cloud(cloud_layers_json) if cloud_layers_json else (cloud_pct > 50)
    spread    = dew_point_spread or 0
    hum       = humidity or 0
    vis       = visibility_sm if visibility_sm is not None else 99
    pp        = precip_prob or 0
    temp      = temp_f or 70
    hour      = obs_hour_local if obs_hour_local is not None else 12

    # ── STORM_RISK ────────────────────────────────────────────────────────
    if pp >= 60 or (pp >= 40 and gust > 30):
        notes.append("High precipitation probability or strong gusts with precip")
        return RegimeResult("STORM_RISK", 0.85, notes)

    # ── OFFSHORE_FLOW ─────────────────────────────────────────────────────
    if wind_direction is not None:
        offshore = (wind_direction >= 330) or (wind_direction <= 130)
        if offshore and wind >= 8 and cloud_pct < 40:
            notes.append(f"Offshore flow from {wind_direction:.0f}° at {wind:.0f} kts/mph, clear skies")
            return RegimeResult("OFFSHORE_FLOW", 0.80, notes)

    # ── MARINE_STRONG (before RAIN_RISK — marine clouds ≠ rain) ──────────
    onshore = wind_direction is not None and 180 <= wind_direction <= 300
    if onshore and wind >= 15 and low_cloud:
        notes.append(f"Strong marine layer: onshore {wind:.0f} kts/mph, low clouds")
        return RegimeResult("MARINE_STRONG", 0.85, notes)

    # ── RAIN_RISK ─────────────────────────────────────────────────────────
    if pp >= 30 or (cloud_pct >= 80 and spread < 8 and not (onshore and wind >= 10)):
        notes.append(f"Precip prob {pp}% / cloud {cloud_pct}%")
        return RegimeResult("RAIN_RISK", 0.75, notes)

    # ── DRY_HEAT (before HEAT_SPIKE_RISK — dew spread is more specific) ──
    if temp >= 85 and spread >= 30 and hum < 25:
        notes.append(f"Dry heat: {temp:.0f}°F, spread {spread:.0f}°F, RH {hum:.0f}%")
        return RegimeResult("DRY_HEAT", 0.78, notes)

    # ── HEAT_SPIKE_RISK ───────────────────────────────────────────────────
    if temp >= 95 and hum < 30 and cloud_pct < 30:
        notes.append(f"Extreme heat {temp:.0f}°F, low humidity {hum:.0f}%, clear")
        return RegimeResult("HEAT_SPIKE_RISK", 0.80, notes)

    if forecast_spread and forecast_spread >= 25:
        notes.append(f"Large forecast spread {forecast_spread:.0f}°F suggests heat spike possible")
        return RegimeResult("HEAT_SPIKE_RISK", 0.65, notes)

    # ── HUMID_HEAT ────────────────────────────────────────────────────────
    if temp >= 80 and hum >= 65:
        notes.append(f"Humid heat: {temp:.0f}°F, RH {hum:.0f}%")
        return RegimeResult("HUMID_HEAT", 0.75, notes)

    # ── MARINE_WEAK ───────────────────────────────────────────────────────
    if onshore and (wind >= 8 or low_cloud) and cloud_pct >= 30:
        notes.append(f"Weak marine influence: onshore at {wind:.0f}, clouds {cloud_pct:.0f}%")
        return RegimeResult("MARINE_WEAK", 0.70, notes)

    # ── CLOUDY_CAP ────────────────────────────────────────────────────────
    if cloud_pct >= 70:
        notes.append(f"Persistent cloud cover {cloud_pct:.0f}%, suppresses afternoon high")
        return RegimeResult("CLOUDY_CAP", 0.72, notes)

    # ── EARLY_BURNOFF ─────────────────────────────────────────────────────
    if cloud_pct >= 40 and 4 <= hour <= 10:
        notes.append(f"Morning clouds {cloud_pct:.0f}% at hour {hour} — likely burns off")
        return RegimeResult("EARLY_BURNOFF", 0.65, notes)

    # ── LATE_BURNOFF ──────────────────────────────────────────────────────
    if cloud_pct >= 40 and 10 < hour <= 14:
        notes.append(f"Midday clouds {cloud_pct:.0f}% at hour {hour} — late burnoff delays high")
        return RegimeResult("LATE_BURNOFF", 0.60, notes)

    # ── HIGH_VARIANCE / LOW_VARIANCE ─────────────────────────────────────
    if forecast_spread is not None:
        if forecast_spread >= 18:
            notes.append(f"Large daily spread {forecast_spread:.0f}°F — uncertain forecast")
            return RegimeResult("HIGH_VARIANCE", 0.60, notes)
        if forecast_spread <= 8:
            notes.append(f"Tight daily spread {forecast_spread:.0f}°F — stable, predictable")
            return RegimeResult("LOW_VARIANCE", 0.72, notes)

    # ── CLEAR_SKY ─────────────────────────────────────────────────────────
    if cloud_pct < 30 and vis >= 6:
        notes.append(f"Clear sky: cloud {cloud_pct:.0f}%, vis {vis:.0f} SM")
        return RegimeResult("CLEAR_SKY", 0.70, notes)

    # ── ONSHORE_FLOW (default with wind) ─────────────────────────────────
    if onshore and wind >= 5:
        notes.append(f"Onshore flow from {wind_direction:.0f}°, mild")
        return RegimeResult("ONSHORE_FLOW", 0.55, notes)

    notes.append("Insufficient data for classification")
    return RegimeResult("UNKNOWN", 0.30, notes)


def classify_from_forecast(fr: dict, hour: int | None = None) -> RegimeResult:
    """Classify using a forecast_runs row dict."""
    spread = None
    if fr.get("temp_max") is not None and fr.get("temp_min") is not None:
        spread = fr["temp_max"] - fr["temp_min"]

    dew_spread = None
    if fr.get("temp_mean") is not None and fr.get("dew_point_mean") is not None:
        dew_spread = fr["temp_mean"] - fr["dew_point_mean"]

    return classify(
        wind_direction   = fr.get("wind_direction_dominant"),
        wind_speed       = fr.get("wind_speed_mean"),
        gust_speed       = fr.get("wind_gusts_max"),
        cloud_cover_pct  = fr.get("cloud_cover_mean"),
        cloud_layers_json= None,
        pressure         = fr.get("pressure_msl_mean"),
        dew_point_spread = dew_spread,
        humidity         = fr.get("humidity_mean"),
        visibility_sm    = None,
        precip_prob      = fr.get("precip_prob_mean"),
        temp_f           = fr.get("temp_mean") or fr.get("temp_max"),
        obs_hour_local   = hour or 12,
        month            = None,
        forecast_spread  = spread,
    )


def classify_from_metar(obs: dict, hour_local: int | None = None) -> RegimeResult:
    """Classify using an official_observations row dict."""
    spread = None
    if obs.get("observed_temp") is not None and obs.get("dewpoint") is not None:
        spread = obs["observed_temp"] - obs["dewpoint"]
    return classify(
        wind_direction   = obs.get("wind_direction"),
        wind_speed       = obs.get("wind_speed"),
        gust_speed       = obs.get("gust_speed"),
        cloud_cover_pct  = None,
        cloud_layers_json= obs.get("cloud_layers"),
        pressure         = obs.get("pressure_inHg"),
        dew_point_spread = spread,
        humidity         = None,
        visibility_sm    = obs.get("visibility_sm"),
        precip_prob      = None,
        temp_f           = obs.get("observed_temp"),
        obs_hour_local   = hour_local or 12,
        month            = None,
    )
