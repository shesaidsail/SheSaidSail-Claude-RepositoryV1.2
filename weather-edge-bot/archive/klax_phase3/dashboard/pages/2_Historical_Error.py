import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from database.db import get_connection, init_db
from models.bias_engine import all_regime_stats
from config import STATION, DEFAULT_MODEL

init_db()
st.header("📈 Historical Forecast Error")

with get_connection() as conn:
    regime_stats = all_regime_stats(STATION, DEFAULT_MODEL, conn)

    paired = pd.read_sql_query("""
        SELECT
            ds.settlement_date,
            COALESCE(ds.regime, 'UNKNOWN') AS regime,
            fr.forecast_high,
            ds.official_high,
            ds.official_low,
            ROUND(ds.official_high - fr.forecast_high, 2) AS error,
            ds.source
        FROM daily_settlements ds
        JOIN forecast_runs fr
            ON  fr.forecast_date = ds.settlement_date
            AND fr.station_code  = ds.station_code
            AND fr.model_name    = ?
        WHERE ds.station_code = ?
        ORDER BY ds.settlement_date ASC
    """, conn, params=(DEFAULT_MODEL, STATION))

if paired.empty:
    st.info("No settled records yet. Enter a forecast and run `python scripts/settle_daily.py`.")
    st.stop()

paired["settlement_date"] = pd.to_datetime(paired["settlement_date"])

# ---- Global summary ----
global_stats = next((s for s in regime_stats if s["regime"] == "ALL"), None)
if global_stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sample Size", global_stats["sample_size"])
    c2.metric("All-time Bias", f"{global_stats['avg_bias']:+.2f}°F")
    c3.metric("Std Deviation", f"{global_stats['std_dev']:.2f}°F")
    r30 = global_stats.get("rolling_30d_bias")
    c4.metric("30-Day Bias", f"{r30:+.2f}°F" if r30 else "—")

st.divider()

# ---- Forecast vs Actual ----
st.subheader("Forecast vs Actual High")
fc_vs = paired.set_index("settlement_date")[["forecast_high", "official_high"]]
fc_vs.columns = ["Forecast (°F)", "Actual (°F)"]
st.line_chart(fc_vs)

# ---- Error over time, coloured by regime ----
st.subheader("Forecast Error by Regime  (actual − forecast)")
col_map = {
    "OFFSHORE_FLOW": "#e74c3c", "MARINE_STRONG": "#3498db",
    "MARINE_WEAK": "#85c1e9",   "EARLY_BURNOFF": "#f39c12",
    "LATE_BURNOFF": "#8e44ad",  "CLEAR_SKY": "#27ae60",
    "HIGH_VARIANCE": "#95a5a6", "UNKNOWN": "#bdc3c7",
}
err_chart = paired.set_index("settlement_date")[["error"]]
err_chart.columns = ["Error (°F)"]
st.bar_chart(err_chart)

# ---- Rolling bias ----
if len(paired) >= 3:
    st.subheader("Rolling Bias")
    df = paired.sort_values("settlement_date").copy()
    df["7d"]  = df["error"].rolling(7,  min_periods=2).mean()
    df["30d"] = df["error"].rolling(30, min_periods=2).mean()
    roll = df.set_index("settlement_date")[["7d", "30d"]].dropna(how="all")
    roll.columns = ["7-Day Rolling Bias (°F)", "30-Day Rolling Bias (°F)"]
    st.line_chart(roll)

# ---- Per-regime stats table ----
if regime_stats:
    st.divider()
    st.subheader("Per-Regime Model Stats")
    rs_df = pd.DataFrame([
        {
            "Regime": s["regime"],
            "n": s["sample_size"],
            "Bias (°F)": f"{s['avg_bias']:+.2f}",
            "Std Dev (°F)": f"{s['std_dev']:.2f}",
            "7d Bias": f"{s['rolling_7d_bias']:+.2f}" if s.get("rolling_7d_bias") else "—",
            "Confidence": f"{s['confidence']:.0%}" if s.get("confidence") else "—",
            "Updated": s.get("updated_at", "")[:10],
        }
        for s in regime_stats
    ])
    st.dataframe(rs_df, use_container_width=True, hide_index=True)

# ---- Full settlement log ----
st.divider()
st.subheader("Settlement Log")
display = paired.copy()
display["settlement_date"] = display["settlement_date"].dt.strftime("%Y-%m-%d")
display = display[["settlement_date", "regime", "forecast_high", "official_high", "error", "source"]]
display.columns = ["Date", "Regime", "Forecast (°F)", "Actual (°F)", "Error (°F)", "Source"]
st.dataframe(display, use_container_width=True, hide_index=True)
