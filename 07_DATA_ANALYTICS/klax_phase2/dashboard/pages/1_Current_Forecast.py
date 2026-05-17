import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import date, datetime, timezone

from database.db import get_connection, init_db
from models.bias_engine import get_stats
from config import STATION, DEFAULT_MODEL

init_db()

st.header("📡 Current Forecast")

# ---------------------------------------------------------------------------
# Sidebar — enter today's Ventusky forecast
# ---------------------------------------------------------------------------

with st.sidebar:
    st.subheader("Enter Today's Forecast")
    st.caption(
        "Go to ventusky.com → set location KLAX (33.94°N, 118.41°W) → "
        "Temperature Max layer → read the forecast high for your target date."
    )

    fc_date  = st.date_input("Forecast Date", value=date.today())
    fc_high  = st.number_input("Ventusky Forecast High (°F)", 40.0, 115.0, 72.0, 0.5)
    fc_model = st.text_input("Model Name", value=DEFAULT_MODEL)

    if st.button("Save Forecast", type="primary"):
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO forecast_runs
                    (timestamp_utc, forecast_date, station_code, model_name, forecast_high, source)
                VALUES (?, ?, ?, ?, ?, 'manual')
            """, (ts, str(fc_date), STATION, fc_model, fc_high))
            conn.commit()
        st.success(f"Saved: {fc_date}  →  {fc_high}°F")
        st.rerun()

    st.divider()
    st.markdown(
        "**Manual settlement override:**  \n"
        "If you have the official NWS high, run:  \n"
        "`python scripts/settle_daily.py --manual 84.0`  \n"
        "This bypasses the METAR max calculation."
    )

# ---------------------------------------------------------------------------
# Load latest data
# ---------------------------------------------------------------------------

with get_connection() as conn:
    stats = get_stats(STATION, DEFAULT_MODEL, conn)

    latest_fc = conn.execute("""
        SELECT forecast_high, forecast_date, timestamp_utc FROM forecast_runs
        WHERE station_code = ? AND model_name = ?
        ORDER BY forecast_date DESC, timestamp_utc DESC
        LIMIT 1
    """, (STATION, DEFAULT_MODEL)).fetchone()

    latest_obs = conn.execute("""
        SELECT observed_temp, wind_direction, wind_speed, cloud_cover, timestamp_utc
        FROM actual_observations
        WHERE station_code = ?
        ORDER BY timestamp_utc DESC
        LIMIT 1
    """, (STATION,)).fetchone()

# ---------------------------------------------------------------------------
# Model stats banner
# ---------------------------------------------------------------------------

if stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sample Size (n)", stats["sample_size"])
    c2.metric("Avg Bias", f"{stats['avg_bias']:+.2f}°F",
              help="Mean of (actual − forecast). Positive = HRRR runs cold.")
    c3.metric("Std Deviation", f"{stats['std_dev']:.2f}°F",
              help="1-sigma spread of forecast errors.")
    r7 = stats.get("rolling_7d_bias")
    c4.metric("7-Day Rolling Bias", f"{r7:+.2f}°F" if r7 is not None else "—",
              help="Mean error over last 7 settled days.")
else:
    st.info(
        "No model stats yet. Enter forecasts in the sidebar, then run "
        "`settle_daily.py` for at least 2 days to calibrate."
    )

st.divider()

# ---------------------------------------------------------------------------
# Latest forecast card
# ---------------------------------------------------------------------------

if not latest_fc:
    st.info("No forecasts entered yet. Use the sidebar to add today's Ventusky forecast.")
    st.stop()

fc_val   = float(latest_fc["forecast_high"])
bias     = stats["avg_bias"]  if stats else 0.0
std      = stats["std_dev"]   if stats else None
adjusted = fc_val + bias

st.subheader(f"Forecast for {latest_fc['forecast_date']}")

mc1, mc2, mc3 = st.columns(3)
mc1.metric("Ventusky Forecast", f"{fc_val}°F")
mc2.metric(
    "Bias-Adjusted Forecast", f"{adjusted:.1f}°F",
    delta=f"{bias:+.2f}°F correction" if stats else "no bias data yet",
)

if latest_obs:
    mc3.metric(
        "Latest METAR", f"{latest_obs['observed_temp']}°F",
        help=(
            f"{latest_obs['timestamp_utc']}  |  "
            f"Wind {latest_obs['wind_direction']}° @ {latest_obs['wind_speed']} kts  |  "
            f"{latest_obs['cloud_cover']}"
        ),
    )
else:
    mc3.metric("Latest METAR", "—", help="Run `python scripts/ingest_metar.py` to populate.")

# ---------------------------------------------------------------------------
# Confidence intervals
# ---------------------------------------------------------------------------

if std:
    st.subheader("Confidence Intervals")
    ci = pd.DataFrame({
        "Interval":  ["68%  (±1σ)", "90%  (±1.645σ)", "95%  (±1.96σ)"],
        "Low (°F)":  [
            round(adjusted - std,        1),
            round(adjusted - 1.645 * std, 1),
            round(adjusted - 1.96  * std, 1),
        ],
        "High (°F)": [
            round(adjusted + std,        1),
            round(adjusted + 1.645 * std, 1),
            round(adjusted + 1.96  * std, 1),
        ],
    })
    st.dataframe(ci, use_container_width=False, hide_index=True)
elif latest_fc:
    st.caption("Confidence intervals will appear once 2+ days have been settled.")
