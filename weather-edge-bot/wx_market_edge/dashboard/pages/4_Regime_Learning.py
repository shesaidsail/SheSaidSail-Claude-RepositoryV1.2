"""
Page 4 — Regime Learning

Shows model bias, std dev, and sample size by regime across all stations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from database.db       import init_db
from models.bias_engine import all_regime_stats
from config import STATIONS, DEFAULT_MODEL

st.set_page_config(page_title="Regime Learning", page_icon="🧠", layout="wide")
st.title("🧠 Regime Learning Dashboard")

conn = init_db()

# ── Across all stations ───────────────────────────────────────────────────────
st.subheader("Bias by Regime — All Stations")

all_rows = conn.execute("""
    SELECT ms.station_code, s.name, ms.regime, ms.avg_bias, ms.std_dev,
           ms.sample_size, ms.rolling_7d_bias, ms.rolling_30d_bias, ms.updated_at
    FROM model_stats ms
    JOIN stations s ON s.icao=ms.station_code
    WHERE ms.model_name=?
    ORDER BY ms.station_code, ms.regime
""", (DEFAULT_MODEL,)).fetchall()

if not all_rows:
    st.info("No model stats yet. Need settled days with matching forecasts. Run settle_day.py after enough data accumulates.")
    st.stop()

df = pd.DataFrame([dict(r) for r in all_rows])
df.columns = ["ICAO", "Station", "Regime", "Avg Bias °F", "Std Dev", "n",
               "7d Bias", "30d Bias", "Updated"]

# Colour-code bias
def _color_bias(val):
    try:
        v = float(val)
        if v > 1:   return "background-color: #d4edda"
        if v < -1:  return "background-color: #f8d7da"
        return ""
    except Exception:
        return ""

styled = df.style.applymap(_color_bias, subset=["Avg Bias °F", "7d Bias", "30d Bias"])
st.dataframe(styled, hide_index=True, use_container_width=True)

st.caption("Green = model underforecasts (actual > forecast).  Red = model overforecasts.")

st.divider()

# ── Per-station drilldown ─────────────────────────────────────────────────────
st.subheader("Per-Station Drilldown")
station = st.selectbox("Station", options=list(STATIONS.keys()),
                       format_func=lambda k: f"{k} — {STATIONS[k]['name']}")

stats = all_regime_stats(station, DEFAULT_MODEL, conn)
if not stats:
    st.info(f"No stats for {station} yet.")
else:
    s_df = pd.DataFrame(stats)[["regime", "avg_bias", "std_dev", "sample_size",
                                 "rolling_7d_bias", "rolling_30d_bias"]]
    s_df.columns = ["Regime", "Avg Bias", "Std Dev", "n", "7d Bias", "30d Bias"]
    st.dataframe(s_df, hide_index=True, use_container_width=True)

    # Bias bar chart
    chart_df = s_df[s_df["Regime"] != "ALL"].set_index("Regime")
    if not chart_df.empty:
        st.bar_chart(chart_df[["Avg Bias"]])

st.divider()

# ── Settlement history ────────────────────────────────────────────────────────
st.subheader("Settlement History")
sel_station = st.selectbox("Station for history", options=list(STATIONS.keys()),
                            format_func=lambda k: f"{k} — {STATIONS[k]['name']}",
                            key="hist_station")

history = conn.execute("""
    SELECT ds.settlement_date, ds.official_high, ds.official_low, ds.regime,
           fr.temp_max AS forecast_high,
           ROUND(ds.official_high - fr.temp_max, 2) AS error
    FROM daily_settlements ds
    LEFT JOIN forecast_runs fr
        ON fr.forecast_date=ds.settlement_date
       AND fr.station_code=ds.station_code
       AND fr.model_name=?
    WHERE ds.station_code=?
    ORDER BY ds.settlement_date DESC
    LIMIT 60
""", (DEFAULT_MODEL, sel_station)).fetchall()

if history:
    h_df = pd.DataFrame([dict(r) for r in history])
    h_df.columns = ["Date", "Official High", "Official Low", "Regime",
                     "Forecast High", "Error (Act-Fc)"]
    st.dataframe(h_df, hide_index=True, use_container_width=True)

    # Error over time
    if "Error (Act-Fc)" in h_df and h_df["Error (Act-Fc)"].notna().sum() > 1:
        st.subheader("Forecast Error Over Time")
        plot_df = h_df.dropna(subset=["Error (Act-Fc)"]).set_index("Date")
        st.line_chart(plot_df[["Error (Act-Fc)"]])
else:
    st.info(f"No settlement data for {sel_station}.")

st.divider()

# ── Regime frequency ─────────────────────────────────────────────────────────
st.subheader("Regime Frequency (all stations)")
regime_counts = conn.execute("""
    SELECT regime, COUNT(*) AS count
    FROM daily_settlements
    WHERE regime IS NOT NULL
    GROUP BY regime
    ORDER BY count DESC
""").fetchall()
if regime_counts:
    r_df = pd.DataFrame([dict(r) for r in regime_counts])
    st.bar_chart(r_df.set_index("regime")["count"])
