import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from collections import Counter

from database.db import get_connection, init_db
from models.bias_engine import all_regime_stats
from config import STATION, DEFAULT_MODEL

init_db()
st.header("🌀 Regime Dashboard")

with get_connection() as conn:
    regime_stats = all_regime_stats(STATION, DEFAULT_MODEL, conn)

    regimes_df = pd.read_sql_query("""
        SELECT settlement_date, regime, confidence, wind_direction, wind_speed,
               cloud_cover, cloud_base_ft, dewpoint_spread, visibility, notes
        FROM weather_regimes
        WHERE station_code = ?
        ORDER BY settlement_date DESC
    """, conn, params=(STATION,))

    paired = pd.read_sql_query("""
        SELECT ds.settlement_date, COALESCE(ds.regime,'UNKNOWN') AS regime,
               fr.forecast_high, ds.official_high,
               ROUND(ds.official_high - fr.forecast_high, 2) AS error
        FROM daily_settlements ds
        JOIN forecast_runs fr
            ON fr.forecast_date = ds.settlement_date
            AND fr.station_code = ds.station_code
            AND fr.model_name   = ?
        WHERE ds.station_code = ?
        ORDER BY ds.settlement_date ASC
    """, conn, params=(DEFAULT_MODEL, STATION))

if paired.empty:
    st.info("No settled data yet.")
    st.stop()

# ---- Regime distribution ----
st.subheader("Regime Distribution")
regime_counts = Counter(paired["regime"].tolist())
count_df = pd.DataFrame(
    [{"Regime": k, "Days": v, "% of Days": f"{100*v/len(paired):.0f}%"}
     for k, v in sorted(regime_counts.items(), key=lambda x: -x[1])]
)
col1, col2 = st.columns([1, 2])
with col1:
    st.dataframe(count_df, use_container_width=True, hide_index=True)
with col2:
    dist_chart = pd.Series(regime_counts).sort_values(ascending=False)
    st.bar_chart(dist_chart)

st.divider()

# ---- Per-regime bias table ----
st.subheader("Per-Regime Bias Statistics")
rs_rows = [s for s in regime_stats if s["regime"] != "ALL"]
if rs_rows:
    rs_df = pd.DataFrame([{
        "Regime":      s["regime"],
        "n":           s["sample_size"],
        "Bias (°F)":   f"{s['avg_bias']:+.2f}",
        "Std Dev":     f"{s['std_dev']:.2f}",
        "7d Bias":     f"{s['rolling_7d_bias']:+.2f}" if s.get("rolling_7d_bias") else "—",
        "Confidence":  f"{s['confidence']:.0%}" if s.get("confidence") else "—",
    } for s in sorted(rs_rows, key=lambda x: x["sample_size"], reverse=True)])
    st.dataframe(rs_df, use_container_width=True, hide_index=True)
    st.caption(
        "Bias = mean(actual − forecast). Positive = HRRR consistently underestimates. "
        "Regime-specific stats used when n ≥ 5; else global 'ALL' is the fallback."
    )
else:
    st.info("Regime-specific stats appear after 2+ settlements per regime.")

st.divider()

# ---- Regime timeline ----
st.subheader("Regime Timeline")
if not regimes_df.empty:
    regimes_df["settlement_date"] = pd.to_datetime(regimes_df["settlement_date"])
    display = regimes_df[["settlement_date","regime","confidence","wind_direction",
                           "wind_speed","cloud_cover","dewpoint_spread","notes"]].copy()
    display["settlement_date"] = display["settlement_date"].dt.strftime("%Y-%m-%d")
    display["confidence"] = display["confidence"].apply(
        lambda x: f"{x:.0%}" if x is not None else "—"
    )
    display.columns = ["Date","Regime","Conf","Wind Dir","Wind Spd","Cloud","DP Spread","Notes"]
    st.dataframe(display, use_container_width=True, hide_index=True)
else:
    st.info("Regime log populates after running settle_daily.py.")

st.divider()

# ---- Error by regime box plots (using simple table) ----
st.subheader("Error Distribution by Regime")
if not paired.empty:
    regime_error = paired.groupby("regime")["error"].agg(
        Mean="mean", Std="std", Min="min", Max="max", Count="count"
    ).round(2).reset_index()
    regime_error.columns = ["Regime", "Mean Error", "Std Dev", "Min Error", "Max Error", "n"]
    st.dataframe(regime_error, use_container_width=True, hide_index=True)
