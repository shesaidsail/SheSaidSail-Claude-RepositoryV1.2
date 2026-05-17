import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import date, datetime, timezone

from database.db import get_connection, init_db
from models.bias_engine import get_stats
from models.regime_engine import classify, parse_cloud_layers
from config import STATION, DEFAULT_MODEL, DATA_DIR

init_db()
st.header("📡 Current Forecast")

# ---------------------------------------------------------------------------
# Detect live regime from latest METAR
# ---------------------------------------------------------------------------

with get_connection() as conn:
    latest_obs = conn.execute("""
        SELECT * FROM actual_observations
        WHERE station_code = ?
        ORDER BY timestamp_utc DESC LIMIT 1
    """, (STATION,)).fetchone()

if latest_obs:
    obs = dict(latest_obs)
    temp_f = obs.get("observed_temp") or 70.0
    dewp_f = obs.get("dewpoint")
    dps    = round(temp_f - dewp_f, 1) if dewp_f is not None else None
    try:
        utc_dt = datetime.strptime(obs["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
        from config import KLAX_UTC_OFFSET_HOURS
        local_hour = (utc_dt.hour + KLAX_UTC_OFFSET_HOURS) % 24
        month      = utc_dt.month
    except Exception:
        local_hour, month = 12, 5

    live_regime = classify(
        wind_direction    = obs.get("wind_direction"),
        wind_speed        = obs.get("wind_speed"),
        cloud_layers_json = obs.get("cloud_layers"),
        visibility_sm     = obs.get("visibility"),
        dewpoint_spread_f = dps,
        obs_hour_local    = local_hour,
        month             = month,
    )
    st.info(
        f"**Live regime (from {obs['timestamp_utc']}):** "
        f"**{live_regime.regime}** (conf {live_regime.confidence:.0%})  \n"
        + "  \n".join(f"- {n}" for n in live_regime.notes)
    )
else:
    live_regime = None
    st.warning("No METAR data yet. Run `python scripts/ingest_metar.py` to populate.")

# ---------------------------------------------------------------------------
# Sidebar — forecast entry (extended)
# ---------------------------------------------------------------------------

with st.sidebar:
    st.subheader("Enter Today's Forecast")
    st.caption(
        "ventusky.com → KLAX (33.94°N, 118.41°W) → Temperature Max layer"
    )

    fc_date  = st.date_input("Forecast Date", value=date.today())
    fc_high  = st.number_input("Ventusky Forecast High (°F)", 40.0, 115.0, 72.0, 0.5)
    fc_tile  = st.text_input("Hottest Station Tile", placeholder="e.g. San Fernando Valley, Downtown LA")
    fc_wdir  = st.number_input("Peak Wind Direction (°)", 0.0, 360.0, 270.0, 5.0)
    fc_wspd  = st.number_input("Peak Wind Speed (kts)", 0.0, 60.0, 10.0, 1.0)
    fc_notes = st.text_area("Marine Layer / Cloud Notes",
                             placeholder="e.g. Low BKN at 600 ft at 6 AM, expect burnoff by 10 AM")

    screenshot = st.file_uploader("Ventusky Screenshot (optional)", type=["png", "jpg", "jpeg"])
    screenshot_path = None
    if screenshot:
        ss_dir = DATA_DIR / "screenshots"
        ss_dir.mkdir(exist_ok=True)
        save_path = ss_dir / f"{fc_date}_{screenshot.name}"
        save_path.write_bytes(screenshot.read())
        screenshot_path = str(save_path)
        st.success(f"Saved to {save_path.name}")

    if st.button("Save Forecast", type="primary"):
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO forecast_runs
                    (timestamp_utc, forecast_date, station_code, model_name, forecast_high,
                     hottest_station_tile, wind_direction, wind_speed, marine_layer_notes,
                     screenshot_path, source)
                VALUES (?,?,?,?,?,?,?,?,?,?,'manual')
            """, (ts, str(fc_date), STATION, DEFAULT_MODEL, fc_high,
                  fc_tile or None, fc_wdir or None, fc_wspd or None,
                  fc_notes or None, screenshot_path))
            conn.commit()
        st.success(f"Saved: {fc_date} → {fc_high}°F")
        st.rerun()

# ---------------------------------------------------------------------------
# Model stats + adjusted forecast
# ---------------------------------------------------------------------------

current_regime = live_regime.regime if live_regime else "ALL"

with get_connection() as conn:
    stats = get_stats(STATION, DEFAULT_MODEL, current_regime, conn)
    latest_fc = conn.execute("""
        SELECT * FROM forecast_runs
        WHERE station_code = ? AND model_name = ?
        ORDER BY forecast_date DESC, timestamp_utc DESC LIMIT 1
    """, (STATION, DEFAULT_MODEL)).fetchone()

if stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Regime", current_regime)
    c2.metric("Avg Bias", f"{stats['avg_bias']:+.2f}°F",
              help="Mean of (actual − forecast) for this regime")
    c3.metric("Std Deviation", f"{stats['std_dev']:.2f}°F")
    c4.metric("Sample Size (n)", stats["sample_size"])
    if stats.get("regime_note"):
        st.caption(f"ℹ️ {stats['regime_note']}")
else:
    st.info("No model stats yet — enter forecasts and settle ≥ 2 days to calibrate.")

st.divider()

if not latest_fc:
    st.info("No forecasts entered yet. Use the sidebar.")
    st.stop()

fc    = dict(latest_fc)
bias  = stats["avg_bias"] if stats else 0.0
std   = stats["std_dev"]  if stats else None
adj   = fc["forecast_high"] + bias

st.subheader(f"Forecast for {fc['forecast_date']}")
m1, m2, m3 = st.columns(3)
m1.metric("Ventusky Forecast", f"{fc['forecast_high']}°F")
m2.metric("Bias-Adjusted Forecast", f"{adj:.1f}°F",
          delta=f"{bias:+.2f}°F ({current_regime})")
if latest_obs:
    m3.metric("Latest METAR", f"{latest_obs['observed_temp']}°F",
              help=latest_obs["timestamp_utc"])

if fc.get("marine_layer_notes"):
    st.markdown(f"**Forecast notes:** {fc['marine_layer_notes']}")

if std:
    from scipy.stats import norm
    st.subheader("Confidence Intervals")
    ci = pd.DataFrame({
        "Interval": ["68%  (±1σ)", "90%  (±1.645σ)", "95%  (±1.96σ)"],
        "Low (°F)":  [round(adj - k * std, 1) for k in [1, 1.645, 1.96]],
        "High (°F)": [round(adj + k * std, 1) for k in [1, 1.645, 1.96]],
    })
    st.dataframe(ci, use_container_width=False, hide_index=True)

if fc.get("screenshot_path"):
    with st.expander("📸 Forecast Screenshot"):
        try:
            st.image(fc["screenshot_path"])
        except Exception:
            st.caption(f"Saved at: {fc['screenshot_path']}")
