"""
KLAX Weather Regime Classifier

Translates METAR observations into one of 8 regimes. Each regime has a distinct
historical bias pattern at KLAX, so using regime-specific stats improves forecast
accuracy beyond a simple global average.

REGIME REFERENCE (KLAX-specific):
  OFFSHORE_FLOW  Wind N/NE/E (≥5 kts). Dry, warm. HRRR underestimates by 3-8°F.
  MARINE_STRONG  Thick stratus BKN/OVC < 2500 ft, onshore wind. HRRR over by 3-6°F.
  MARINE_WEAK    Partial stratus FEW/SCT, clears mid-morning. Moderate suppression.
  EARLY_BURNOFF  Stratus present ≤ 10 AM local, clears before noon.
  LATE_BURNOFF   Stratus persists past 1 PM. Significant high-temp suppression.
  CLEAR_SKY      CLR or FEW > 3000 ft, large dewpoint spread. Well-modeled.
  HIGH_VARIANCE  Mixed/ambiguous signals. Wide uncertainty band.
  LOW_VARIANCE   Assigned by bias engine when σ < 1.5°F for a regime.
"""

import json
from dataclasses import dataclass, field

# Wind sectors (degrees true)
_ONSHORE_LO,  _ONSHORE_HI   = 190, 280   # SSW–W (marine influence)
_OFFSHORE_LO, _OFFSHORE_HI  = 330, 360   # N sector
_OFFSHORE_LO2, _OFFSHORE_HI2 = 0, 100   # NE/E sector (incl. Santa Ana)

_CLOUD_RANK = {
    "CLR": 0, "SKC": 0, "CAVOK": 0,
    "FEW": 1, "SCT": 2, "BKN": 3, "OVC": 4, "VV": 4,
}

ALL_REGIMES = [
    "OFFSHORE_FLOW", "MARINE_STRONG", "MARINE_WEAK",
    "EARLY_BURNOFF", "LATE_BURNOFF", "CLEAR_SKY",
    "HIGH_VARIANCE", "LOW_VARIANCE",
]


@dataclass
class RegimeResult:
    regime:     str
    confidence: float
    notes:      list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _rank(cover: str) -> int:
    return _CLOUD_RANK.get(cover.upper()[:3], 0)


def _is_onshore(d: float) -> bool:
    return _ONSHORE_LO <= d <= _ONSHORE_HI


def _is_offshore(d: float) -> bool:
    return d >= _OFFSHORE_LO or d <= _OFFSHORE_HI2


def parse_cloud_layers(cloud_layers_json: str | None) -> tuple[str, float | None]:
    """
    Return (worst_cover_code, lowest_base_ft) from stored JSON cloud layer array.
    Example input: '[{"cover":"BKN","base":1200},{"cover":"OVC","base":2500}]'
    """
    if not cloud_layers_json:
        return "CLR", None
    try:
        layers = json.loads(cloud_layers_json)
        if not layers:
            return "CLR", None
        worst  = max(layers, key=lambda l: _rank(l.get("cover", "CLR")))
        bases  = [l["base"] for l in layers if l.get("base") is not None]
        lowest = min(bases) if bases else None
        return worst.get("cover", "CLR"), lowest
    except (json.JSONDecodeError, TypeError, ValueError):
        return "CLR", None


# ---------------------------------------------------------------------------
# Public classifier
# ---------------------------------------------------------------------------

def classify(
    wind_direction:    float | None,
    wind_speed:        float | None,
    cloud_layers_json: str   | None,
    visibility_sm:     float | None,
    dewpoint_spread_f: float | None,   # temp_f - dewpoint_f
    obs_hour_local:    int,             # 0-23 KLAX local
    month:             int,             # 1-12
) -> RegimeResult:
    """
    Classify KLAX weather regime.  Priority order:
      1. Offshore flow (strongest bias signal)
      2. Marine layer strong
      3. Late burnoff (marine persisting past 1 PM)
      4. Early burnoff (marine clearing before noon)
      5. Marine weak (partial, mid-morning)
      6. Clear sky
      7. High variance (fallback)
    """
    notes = []
    cover, base_ft = parse_cloud_layers(cloud_layers_json)
    cloud_rank = _rank(cover)
    wspd  = wind_speed     or 0.0
    wdir  = wind_direction
    vis   = visibility_sm  or 10.0
    dps   = dewpoint_spread_f

    # ---- 1. Offshore / Santa Ana ----
    if wdir is not None and _is_offshore(wdir) and wspd >= 5:
        conf = min(0.65 + (wspd - 5) * 0.015, 0.92)
        notes.append(f"Offshore wind {wdir:.0f}° @ {wspd:.0f} kts — HRRR likely underestimates")
        if dps is not None and dps > 20:
            conf = min(conf + 0.05, 0.95)
            notes.append(f"Very dry air (dewpoint spread {dps:.0f}°F) — Santa Ana conditions")
        return RegimeResult("OFFSHORE_FLOW", round(conf, 2), notes)

    # ---- 2. Marine strong ----
    if cloud_rank >= 3 and (base_ft is None or base_ft < 2500):
        # ---- 3. Late burnoff (still thick past 1 PM) ----
        if obs_hour_local >= 13:
            notes.append(
                f"{cover} at {int(base_ft or 0)} ft persisting past 1 PM — "
                "afternoon high significantly suppressed"
            )
            return RegimeResult("LATE_BURNOFF", 0.78, notes)
        conf = 0.82
        if base_ft is not None and base_ft < 1000:
            conf += 0.08
            notes.append(f"Very low stratus ({int(base_ft)} ft) — strong suppression likely")
        if vis < 3:
            notes.append(f"Reduced visibility {vis:.1f} sm — dense marine layer")
        notes.append(f"Marine layer: {cover} at {int(base_ft or 0)} ft")
        notes.append("HRRR typically overestimates high temp by 3-6°F in this regime")
        return RegimeResult("MARINE_STRONG", round(min(conf, 0.92), 2), notes)

    # ---- 4. Early burnoff (FEW/SCT, morning obs) ----
    if cloud_rank in (1, 2) and (base_ft is None or base_ft < 3000) and obs_hour_local <= 10:
        conf = 0.58
        if month in (6, 7, 8):
            conf = 0.50
            notes.append("Jun–Aug: marine layer may linger past 10 AM (June Gloom)")
        notes.append(f"{cover} at {int(base_ft or 0)} ft at {obs_hour_local:02d}:xx local")
        notes.append("Pattern: stratus clears by late morning → well-modeled afternoon high")
        return RegimeResult("EARLY_BURNOFF", conf, notes)

    # ---- 5. Marine weak ----
    if cloud_rank in (1, 2) and (base_ft is None or base_ft < 3500):
        conf = 0.60
        notes.append(f"Partial marine influence: {cover} at {int(base_ft or 0)} ft")
        notes.append("Moderate cooling expected — mild positive bias in HRRR forecast")
        return RegimeResult("MARINE_WEAK", conf, notes)

    # ---- 6. Clear sky ----
    if cloud_rank <= 1:
        conf = 0.72
        if dps is not None:
            if dps > 25:
                conf += 0.12
                notes.append(f"Very dry air (dewpoint spread {dps:.0f}°F) — HRRR well-calibrated")
            elif dps > 15:
                conf += 0.05
                notes.append(f"Dry air (dewpoint spread {dps:.0f}°F)")
        notes.append(f"Clear sky ({cover}) — best model conditions")
        return RegimeResult("CLEAR_SKY", round(min(conf, 0.90), 2), notes)

    # ---- 7. High variance fallback ----
    notes.append("Mixed signals — no dominant regime pattern")
    if dps is not None and dps < 8:
        notes.append(f"Moist air (dewpoint spread {dps:.0f}°F) — cloud development uncertain")
    if wdir is not None:
        notes.append(f"Wind {wdir:.0f}° @ {wspd:.0f} kts (no strong offshore or onshore signal)")
    return RegimeResult("HIGH_VARIANCE", 0.40, notes)
