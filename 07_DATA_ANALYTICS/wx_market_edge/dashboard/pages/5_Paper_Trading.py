"""
Page 5 — Paper Trading Lab

View open/closed paper trades, settle by date, and review performance.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

from database.db          import init_db
from trading.paper_trader import (
    get_open_trades, get_closed_trades,
    performance_summary, settle_trades
)
from config import STATIONS

st.set_page_config(page_title="Paper Trading Lab", page_icon="📝", layout="wide")
st.title("📝 Paper Trading Lab")

conn = init_db()

# ── Performance summary ───────────────────────────────────────────────────────
st.subheader("Performance Summary")
perf = performance_summary(conn)

if perf.get("total", 0) == 0:
    st.info("No closed paper trades yet. Open a trade from the Edge Calculator page.")
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Trades",  perf["total"])
    c2.metric("Win Rate",      f"{perf['win_rate']:.0%}")
    c3.metric("Total P&L",     f"{perf['total_pnl']:+.0f}¢")
    c4.metric("ROI",           f"{perf['roi_pct']:+.1f}%")
    c5.metric("Max Drawdown",  f"{perf['max_drawdown']:.0f}¢")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("P&L by Station")
        by_s = perf.get("by_station", {})
        if by_s:
            s_rows = [{"Station": k, "Wins": v["wins"], "Losses": v["losses"],
                       "P&L ¢": round(v["pnl"], 2)} for k, v in by_s.items()]
            st.dataframe(pd.DataFrame(s_rows), hide_index=True)

    with col_b:
        st.subheader("P&L by Regime")
        by_r = perf.get("by_regime", {})
        if by_r:
            r_rows = [{"Regime": k, "Wins": v["wins"], "Losses": v["losses"],
                       "P&L ¢": round(v["pnl"], 2)} for k, v in by_r.items()]
            st.dataframe(pd.DataFrame(r_rows), hide_index=True)

st.divider()

# ── Manual settle ─────────────────────────────────────────────────────────────
st.subheader("Settle Open Trades")
with st.form("settle_form"):
    settle_date = st.date_input("Settlement Date",
                                value=(datetime.now(timezone.utc) - timedelta(days=1)).date())
    settle_submitted = st.form_submit_button("Settle Trades for Date")

if settle_submitted:
    from scripts.settle_day import settle_station
    date_str = settle_date.strftime("%Y-%m-%d")
    settled = []
    for station in STATIONS:
        r = settle_station(station, date_str, conn)
        if r.get("status") == "OK":
            settled.append(r)
    if settled:
        st.success(f"Settled {len(settled)} stations for {date_str}")
        for r in settled:
            st.write(f"• {r['station']}: high={r['official_high']}°F, "
                     f"regime={r['regime']}, {r['trades_settled']} trades closed")
    else:
        st.warning("No settlements — check METAR data for that date.")

st.divider()

# ── Open trades ───────────────────────────────────────────────────────────────
st.subheader("Open Paper Trades")
open_trades = get_open_trades(conn)
if open_trades:
    ot_df = pd.DataFrame(open_trades)[[
        "id", "station_code", "forecast_date", "threshold_f", "side",
        "entry_price", "fair_value", "edge", "confidence", "regime", "opened_at"
    ]]
    ot_df.columns = ["#", "Station", "Date", "Threshold", "Side",
                     "Entry ¢", "Fair ¢", "Edge ¢", "Conf", "Regime", "Opened"]
    st.dataframe(ot_df, hide_index=True, use_container_width=True)
else:
    st.info("No open trades.")

st.divider()

# ── Closed trades ─────────────────────────────────────────────────────────────
st.subheader("Closed Paper Trades")
closed_trades = get_closed_trades(conn, limit=100)
if closed_trades:
    ct_df = pd.DataFrame(closed_trades)[[
        "id", "station_code", "forecast_date", "threshold_f", "side",
        "entry_price", "settlement_price", "result", "pnl_cents", "regime", "closed_at"
    ]]
    ct_df.columns = ["#", "Station", "Date", "Threshold", "Side",
                     "Entry ¢", "Settled High", "Result", "P&L ¢", "Regime", "Closed"]

    def _highlight(row):
        if row["Result"] == "WIN":
            return ["background-color: #d4edda"] * len(row)
        elif row["Result"] == "LOSS":
            return ["background-color: #f8d7da"] * len(row)
        return [""] * len(row)

    st.dataframe(ct_df.style.apply(_highlight, axis=1), hide_index=True, use_container_width=True)

    # Cumulative P&L chart
    if len(closed_trades) > 1:
        pnls = [t["pnl_cents"] for t in closed_trades if t.get("pnl_cents") is not None]
        pnls.reverse()
        cum = []
        running = 0
        for p in pnls:
            running += p
            cum.append(running)
        st.subheader("Cumulative P&L (cents)")
        st.line_chart(cum)
else:
    st.info("No closed trades yet.")

st.divider()

# ── Calibration ───────────────────────────────────────────────────────────────
st.subheader("Model Calibration")
st.caption("How often do trades at each model_prob bucket actually win?")

calib = conn.execute("""
    SELECT ROUND(model_prob*10)/10 AS bucket, COUNT(*) AS n,
           SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) AS wins
    FROM paper_trades
    WHERE status='CLOSED' AND model_prob IS NOT NULL
    GROUP BY bucket
    ORDER BY bucket
""").fetchall()

if calib and len(calib) >= 2:
    c_df = pd.DataFrame([dict(r) for r in calib])
    c_df["Predicted Win %"] = (c_df["bucket"] * 100).round(0).astype(str) + "%"
    c_df["Actual Win %"]    = (c_df["wins"] / c_df["n"] * 100).round(1).astype(str) + "%"
    st.dataframe(c_df[["Predicted Win %", "n", "Actual Win %"]], hide_index=True)
else:
    st.info("Need more closed trades for calibration chart.")
