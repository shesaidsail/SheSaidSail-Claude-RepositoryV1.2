"""
Page 6 — Backtesting

Replay historical signals with strict no-lookahead bias.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta, date as dt_date

from database.db          import init_db
from trading.backtester   import run_backtest
from config import STATIONS, MIN_EDGE, MIN_CONFIDENCE, DEFAULT_MODEL

st.set_page_config(page_title="Backtesting", page_icon="📊", layout="wide")
st.title("📊 Backtesting Engine")
st.caption("All backtests use only data available before each trade date (no-lookahead bias).")

conn = init_db()

# ── Previous runs ─────────────────────────────────────────────────────────────
prev_runs = conn.execute("""
    SELECT * FROM backtest_runs ORDER BY run_at DESC LIMIT 10
""").fetchall()

if prev_runs:
    with st.expander("Previous Backtest Runs"):
        pr_df = pd.DataFrame([dict(r) for r in prev_runs])[[
            "run_at", "station_code", "date_from", "date_to",
            "total_trades", "win_rate", "total_pnl", "roi_pct", "max_drawdown", "sharpe"
        ]]
        st.dataframe(pr_df, hide_index=True, use_container_width=True)

st.divider()

# ── Parameters ───────────────────────────────────────────────────────────────
st.subheader("Configure Backtest")
with st.form("backtest_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        station_opt = st.selectbox(
            "Station (blank = all)",
            options=["All Stations"] + list(STATIONS.keys()),
            format_func=lambda k: k if k == "All Stations" else f"{k} — {STATIONS[k]['name']}",
        )
        station_val = None if station_opt == "All Stations" else station_opt

    with col2:
        earliest = conn.execute("SELECT MIN(settlement_date) FROM daily_settlements").fetchone()[0]
        default_from = earliest or "2026-01-01"
        date_from = st.date_input("From", value=datetime.strptime(default_from, "%Y-%m-%d").date())
        date_to   = st.date_input("To",   value=(datetime.now(timezone.utc) - timedelta(days=1)).date())

    with col3:
        min_edge_val = st.slider("Min Edge (¢)", 1.0, 20.0, float(MIN_EDGE), 0.5)
        min_conf_val = st.slider("Min Confidence", 0.3, 0.9, float(MIN_CONFIDENCE), 0.05)

    run_submitted = st.form_submit_button("▶ Run Backtest", type="primary")

if run_submitted:
    with st.spinner("Running backtest..."):
        result = run_backtest(
            station_code   = station_val,
            date_from      = date_from.strftime("%Y-%m-%d"),
            date_to        = date_to.strftime("%Y-%m-%d"),
            min_edge       = min_edge_val,
            min_confidence = min_conf_val,
            conn           = conn,
        )

    if result["total_trades"] == 0:
        st.warning("No qualifying trades found in this date range. Try loosening filters or adding more data.")
        st.stop()

    # ── Summary metrics ───────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Trades",  result["total_trades"])
    c2.metric("Win Rate",      f"{result['win_rate']:.0%}")
    c3.metric("Total P&L",     f"{result['total_pnl']:+.0f}¢")
    c4.metric("ROI",           f"{result['roi_pct']:+.1f}%")
    c5.metric("Max Drawdown",  f"{result['max_drawdown']:.0f}¢")
    c6.metric("Sharpe",        f"{result['sharpe']:.2f}")

    st.divider()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.subheader("By Station")
        bs = result["by_station"]
        if bs:
            rows = [{"Station": k,
                     "W/L": f"{v['wins']}/{v['losses']}",
                     "P&L ¢": round(v["pnl"], 1)} for k, v in bs.items()]
            st.dataframe(pd.DataFrame(rows), hide_index=True)

    with col_b:
        st.subheader("By Regime")
        br = result["by_regime"]
        if br:
            rows = sorted(
                [{"Regime": k, "W/L": f"{v['wins']}/{v['losses']}",
                  "P&L ¢": round(v["pnl"], 1)} for k, v in br.items()],
                key=lambda x: x["P&L ¢"], reverse=True
            )
            st.dataframe(pd.DataFrame(rows), hide_index=True)

    with col_c:
        st.subheader("By Threshold Offset")
        bt = result["by_threshold"]
        if bt:
            rows = sorted(
                [{"Offset": k, "W/L": f"{v['wins']}/{v['losses']}",
                  "P&L ¢": round(v["pnl"], 1)} for k, v in bt.items()],
                key=lambda x: x["Offset"]
            )
            st.dataframe(pd.DataFrame(rows), hide_index=True)

    st.divider()

    # ── Cumulative P&L ────────────────────────────────────────────────────────
    trades = result["trades"]
    if trades:
        pnls = [t["pnl"] for t in trades]
        cum  = []
        running = 0
        for p in pnls:
            running += p
            cum.append(running)
        st.subheader("Cumulative P&L")
        st.line_chart(cum)

    # ── Trade log ─────────────────────────────────────────────────────────────
    with st.expander(f"Trade Log ({len(trades)} trades)"):
        t_df = pd.DataFrame(trades)[[
            "date", "station_code", "regime", "threshold", "side",
            "fc_high", "adj_forecast", "model_prob", "fair_value",
            "actual_high", "result", "pnl"
        ]]
        t_df.columns = ["Date", "Station", "Regime", "Threshold", "Side",
                         "FC High", "Adj FC", "Prob", "Fair ¢",
                         "Actual High", "Result", "P&L ¢"]
        st.dataframe(t_df, hide_index=True, use_container_width=True)
