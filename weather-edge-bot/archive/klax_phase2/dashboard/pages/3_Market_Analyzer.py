import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from database.db import get_connection, init_db
from models.bias_engine import get_stats, win_probability
from config import STATION, DEFAULT_MODEL, BET_EDGE_THRESHOLD

init_db()

st.header("💰 Market Analyzer")

# ---------------------------------------------------------------------------
# Load model stats and latest forecast
# ---------------------------------------------------------------------------

with get_connection() as conn:
    stats = get_stats(STATION, DEFAULT_MODEL, conn)
    latest_fc = conn.execute("""
        SELECT forecast_high, forecast_date FROM forecast_runs
        WHERE station_code = ? AND model_name = ?
        ORDER BY forecast_date DESC, timestamp_utc DESC
        LIMIT 1
    """, (STATION, DEFAULT_MODEL)).fetchone()

if not stats:
    st.warning(
        "No model stats available yet.  \n"
        "Enter forecasts on the **Current Forecast** page, then settle ≥ 2 days via "
        "`python scripts/settle_daily.py`."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Model stats banner
# ---------------------------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Bias", f"{stats['avg_bias']:+.2f}°F")
c2.metric("Std Deviation", f"{stats['std_dev']:.2f}°F")
c3.metric("Sample Size (n)", stats["sample_size"])
r7 = stats.get("rolling_7d_bias")
c4.metric("7-Day Bias", f"{r7:+.2f}°F" if r7 is not None else "—")

st.divider()

st.info(
    "**Settlement note:** Markets settle on whole-degree official highs. "
    "We use T + 0.5 as the probability cutoff — "
    "Yes >68 requires an official high of 69°F or higher, "
    "while No >68 requires 68°F or lower."
)

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

default_fc = float(latest_fc["forecast_high"]) if latest_fc else 72.0
fc_note    = (
    f"Latest on file: {latest_fc['forecast_date']} → {latest_fc['forecast_high']}°F"
    if latest_fc else "No forecast on file yet"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    today_fc = st.number_input(
        f"Ventusky Forecast (°F)  [{fc_note}]",
        40.0, 115.0, default_fc, 0.5,
    )
with col2:
    threshold = st.number_input("Threshold T (e.g. 75 for '>75')", 40.0, 115.0, 75.0, 1.0)
with col3:
    side = st.selectbox(
        "Contract Side", ["Yes", "No"],
        help="Yes >T wins if official high ≥ T+1.  No >T wins if official high ≤ T.",
    )
with col4:
    market_price = st.number_input("Market Price (¢)", 1.0, 99.0, 50.0, 1.0)

if st.button("Calculate Edge", type="primary"):
    adjusted = today_fc + stats["avg_bias"]
    prob     = win_probability(adjusted, stats["std_dev"], threshold, side)
    fair     = prob * 100.0
    edge     = fair - market_price

    if edge >= BET_EDGE_THRESHOLD:
        rec, color = "BET ✅", "green"
    elif edge >= 0:
        rec, color = "THIN EDGE — PASS", "orange"
    else:
        rec, color = "FADE / LAY ❌", "red"

    st.divider()

    rc1, rc2, rc3 = st.columns(3)
    rc1.metric(
        "Adjusted Forecast", f"{adjusted:.1f}°F",
        delta=f"{stats['avg_bias']:+.2f}°F bias correction",
    )
    rc2.metric(
        "Fair Price", f"{fair:.1f}¢",
        delta=f"{edge:+.1f}¢ edge",
        delta_color="normal" if edge >= 0 else "inverse",
    )
    rc3.metric("P(Win)", f"{prob:.1%}")

    box_css = {
        "green":  "background:#d4edda;border-left:6px solid #28a745;",
        "orange": "background:#fff3cd;border-left:6px solid #ffc107;",
        "red":    "background:#f8d7da;border-left:6px solid #dc3545;",
    }[color]

    st.markdown(
        f"""<div style="{box_css} padding:16px 20px; border-radius:6px; margin-top:12px;">
            <strong style="font-size:1.3em;">{rec}</strong><br>
            <span style="color:#555;">
                Contract: <strong>{side} &gt;{int(threshold)}</strong> &nbsp;|&nbsp;
                Market: <strong>{market_price:.1f}¢</strong> &nbsp;|&nbsp;
                Fair: <strong>{fair:.1f}¢</strong> &nbsp;|&nbsp;
                Edge: <strong>{edge:+.1f}¢</strong>
            </span><br>
            <small style="color:#888;">
                Adjusted {adjusted:.1f}°F ± {stats['std_dev']:.2f}°F (1σ),
                CDF cutoff {threshold + 0.5}°F, n={stats['sample_size']}
            </small>
        </div>""",
        unsafe_allow_html=True,
    )

    with st.expander("Calculation breakdown"):
        breakdown = {
            "Step": [
                "Ventusky forecast",
                "Average bias (all-time)",
                "Adjusted forecast",
                "Std deviation",
                "Threshold (T)",
                "CDF cutoff (T + 0.5)",
                "Side",
                "P(win) = normal CDF",
                "Fair price",
                "Market price",
                "Edge",
            ],
            "Value": [
                f"{today_fc}°F",
                f"{stats['avg_bias']:+.2f}°F  (n={stats['sample_size']})",
                f"{adjusted:.2f}°F",
                f"{stats['std_dev']:.2f}°F",
                f"{threshold}°F",
                f"{threshold + 0.5}°F",
                side,
                f"{prob:.4f}  ({prob:.1%})",
                f"{fair:.1f}¢",
                f"{market_price:.1f}¢",
                f"{edge:+.1f}¢",
            ],
        }
        st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)

    # Persist market snapshot
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO market_snapshots (timestamp_utc, contract_name, threshold, side, market_price)
            VALUES (?, ?, ?, ?, ?)
        """, (ts, f"{side} >{int(threshold)}", threshold, side, market_price))
        conn.commit()
    st.caption("Market snapshot saved.")
