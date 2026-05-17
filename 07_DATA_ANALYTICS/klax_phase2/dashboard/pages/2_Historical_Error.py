import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from database.db import get_connection, init_db
from models.bias_engine import get_stats
from config import STATION, DEFAULT_MODEL

init_db()

st.header("📈 Historical Forecast Error")

# ---------------------------------------------------------------------------
# Load paired forecast / settlement records
# ---------------------------------------------------------------------------

with get_connection() as conn:
    stats = get_stats(STATION, DEFAULT_MODEL, conn)

    paired = pd.read_sql_query("""
        SELECT
            ds.settlement_date,
            fr.forecast_high,
            ds.official_high,
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
    st.info(
        "No paired records yet. Enter a forecast on the Current Forecast page, "
        "then run `python scripts/settle_daily.py` after the day ends."
    )
    st.stop()

paired["settlement_date"] = pd.to_datetime(paired["settlement_date"])

# ---------------------------------------------------------------------------
# Summary metrics
# ---------------------------------------------------------------------------

if stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sample Size", stats["sample_size"])
    c2.metric("All-time Bias", f"{stats['avg_bias']:+.2f}°F",
              help="Positive = HRRR consistently underestimates KLAX high")
    c3.metric("Std Deviation", f"{stats['std_dev']:.2f}°F",
              help="Typical size of individual forecast errors")
    r30 = stats.get("rolling_30d_bias")
    c4.metric("30-Day Bias", f"{r30:+.2f}°F" if r30 is not None else "—")

st.divider()

# ---------------------------------------------------------------------------
# Forecast vs Actual
# ---------------------------------------------------------------------------

st.subheader("Forecast vs Actual High")
fc_vs_act = paired.set_index("settlement_date")[["forecast_high", "official_high"]]
fc_vs_act.columns = ["Forecast (°F)", "Actual (°F)"]
st.line_chart(fc_vs_act)

# ---------------------------------------------------------------------------
# Error over time
# ---------------------------------------------------------------------------

st.subheader("Forecast Error  (actual − forecast)")
err_chart = paired.set_index("settlement_date")[["error"]]
err_chart.columns = ["Error (°F)"]
st.bar_chart(err_chart)

# ---------------------------------------------------------------------------
# Rolling bias
# ---------------------------------------------------------------------------

if len(paired) >= 3:
    st.subheader("Rolling Bias")
    df = paired.sort_values("settlement_date").copy()
    df["7d"]  = df["error"].rolling(7,  min_periods=2).mean()
    df["30d"] = df["error"].rolling(30, min_periods=2).mean()
    roll = df.set_index("settlement_date")[["7d", "30d"]].dropna(how="all")
    roll.columns = ["7-Day Rolling Bias (°F)", "30-Day Rolling Bias (°F)"]
    st.line_chart(roll)

st.divider()

# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------

st.subheader("Settlement Log")
display = paired.copy()
display["settlement_date"] = display["settlement_date"].dt.strftime("%Y-%m-%d")
display = display[["settlement_date", "forecast_high", "official_high", "error", "source"]]
display.columns = ["Date", "Forecast (°F)", "Actual (°F)", "Error (°F)", "Source"]
st.dataframe(display, use_container_width=True, hide_index=True)
