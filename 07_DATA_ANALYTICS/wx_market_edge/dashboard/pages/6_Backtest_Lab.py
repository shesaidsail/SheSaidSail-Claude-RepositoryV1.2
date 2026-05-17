"""
Page 6 — Backtest Lab

Full historical replay with no-lookahead bias.
Supports:
  - Open-Meteo real-time forecasts (if stored during operation)
  - Open-Meteo archive reanalysis (pulled on demand)
  - Historical METAR observations (pulled via AWC backfill)
  - Simulated market prices (forecast-only mode)

Labels each backtest clearly:
  "Full backtest" — real market prices present
  "Forecast-only" — no Kalshi price history, synthetic 50¢ market used
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

from database.db              import init_db
from trading.backtester       import run_backtest
from ingestion.open_meteo_historical import backfill_station
from ingestion.metar          import backfill as backfill_metar
from config import STATIONS, MIN_EDGE, MIN_CONFIDENCE, DEFAULT_MODEL

st.set_page_config(page_title="Backtest Lab", page_icon="🔬", layout="wide")
st.title("🔬 Backtest Lab")

conn = init_db()

# ── Mode selector ─────────────────────────────────────────────────────────────
st.info("""
**Backtest modes:**
- **Full backtest** — uses real stored Kalshi prices (requires having run Kalshi ingestion historically)
- **Forecast-only** — uses Open-Meteo accuracy only, with a synthetic 50¢ market. Measures forecast quality, not trading edge.
""")

mode = st.radio("Backtest mode", ["Forecast-only (synthetic 50¢ market)",
                                   "Full (use stored Kalshi prices)"],
                index=0, horizontal=True)
forecast_only = "Forecast-only" in mode

st.divider()

# ── Historical data prep ──────────────────────────────────────────────────────
with st.expander("📥 Pull Historical Data (one-time setup)"):
    st.write("Pull Open-Meteo archive + METAR backfill for the date range you want to test.")
    col1, col2, col3 = st.columns(3)
    with col1:
        hist_station = st.selectbox("Station", options=list(STATIONS.keys()),
                                    format_func=lambda k: f"{k} — {STATIONS[k]['name']}",
                                    key="hist_pull_station")
    with col2:
        hist_from = st.date_input("From", value=(datetime.now(timezone.utc) - timedelta(days=180)).date(),
                                  key="hist_from")
        hist_to   = st.date_input("To",   value=(datetime.now(timezone.utc) - timedelta(days=1)).date(),
                                  key="hist_to")
    with col3:
        pull_archive = st.checkbox("Pull Open-Meteo archive")
        pull_metar   = st.checkbox("Pull METAR backfill")

    if st.button("⬇ Pull Historical Data"):
        if pull_archive:
            with st.spinner(f"Fetching Open-Meteo archive for {hist_station}..."):
                n = backfill_station(hist_station, str(hist_from), str(hist_to), conn)
            st.success(f"Stored {n} archive forecast days for {hist_station}")
        if pull_metar:
            days = (hist_to - hist_from).days
            hours = min(days * 24, 744)   # AWC API max ~31 days
            with st.spinner(f"Backfilling METAR for {hist_station} ({hours}h)..."):
                n = backfill_metar(hist_station, hours, conn)
            st.success(f"Stored {n} new METAR observations for {hist_station}")

st.divider()

# ── Configure backtest ────────────────────────────────────────────────────────
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

        model_opt = st.selectbox("Model", ["OpenMeteo", "OpenMeteo-Archive"])

    with col2:
        earliest = conn.execute("SELECT MIN(settlement_date) FROM daily_settlements").fetchone()[0]
        default_from = earliest or "2026-01-01"
        date_from = st.date_input("From", value=datetime.strptime(default_from, "%Y-%m-%d").date())
        date_to   = st.date_input("To",   value=(datetime.now(timezone.utc) - timedelta(days=1)).date())

    with col3:
        min_edge_val = st.slider("Min Edge (¢)", 1.0, 20.0, 10.0, 0.5)
        min_conf_val = st.slider("Min Confidence", 0.3, 0.9, float(MIN_CONFIDENCE), 0.05)

    st.caption("Signal quality controls applied: only A+/B grade signals are backtested.")
    run_btn = st.form_submit_button("▶ Run Backtest", type="primary")

if run_btn:
    with st.spinner("Running backtest with no-lookahead bias..."):
        result = run_backtest(
            station_code   = station_val,
            date_from      = date_from.strftime("%Y-%m-%d"),
            date_to        = date_to.strftime("%Y-%m-%d"),
            min_edge       = min_edge_val,
            min_confidence = min_conf_val,
            model          = model_opt,
            conn           = conn,
        )

    if result["total_trades"] == 0:
        st.warning("No qualifying trades found. Try loosening filters, pulling more historical data, or expanding the date range.")
        st.stop()

    # Mode label
    label = "Forecast-only backtest" if forecast_only else "Full backtest"
    if forecast_only:
        st.warning(f"⚠️ **{label}** — Market prices are synthetic (50¢). This measures Open-Meteo forecast accuracy only, NOT actual trading edge. Do not use these P&L numbers to size real trades.")
    else:
        st.success(f"✅ **{label}** — Uses stored Kalshi prices where available.")

    st.divider()

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
        st.subheader("P&L by Station")
        bs = result["by_station"]
        if bs:
            rows = sorted(
                [{"Station": k, "W/L": f"{v['wins']}/{v['losses']}",
                  "P&L ¢": round(v["pnl"], 1),
                  "Win %": f"{v['wins']/(v['wins']+v['losses']):.0%}" if v["wins"]+v["losses"] else "—"
                  } for k, v in bs.items()],
                key=lambda x: x["P&L ¢"], reverse=True
            )
            st.dataframe(pd.DataFrame(rows), hide_index=True)

    with col_b:
        st.subheader("P&L by Regime")
        br = result["by_regime"]
        if br:
            rows = sorted(
                [{"Regime": k, "W/L": f"{v['wins']}/{v['losses']}",
                  "P&L ¢": round(v["pnl"], 1),
                  "Win %": f"{v['wins']/(v['wins']+v['losses']):.0%}" if v["wins"]+v["losses"] else "—"
                  } for k, v in br.items()],
                key=lambda x: x["P&L ¢"], reverse=True
            )
            r_df = pd.DataFrame(rows)
            st.dataframe(r_df, hide_index=True)

            # Recommendations
            st.subheader("Regime Recommendations")
            for r in rows:
                try:
                    wl = [int(x) for x in r["W/L"].split("/")]
                    w_rate = wl[0] / sum(wl) if sum(wl) else 0
                except Exception:
                    continue
                if r["P&L ¢"] > 10 and w_rate >= 0.55:
                    st.success(f"✅ Trade: **{r['Regime']}** — win rate {r['Win %']}, P&L {r['P&L ¢']:+.0f}¢")
                elif r["P&L ¢"] < -5 or w_rate < 0.40:
                    st.error(f"🚫 Avoid: **{r['Regime']}** — win rate {r['Win %']}, P&L {r['P&L ¢']:+.0f}¢")
                else:
                    st.info(f"👀 Watch: **{r['Regime']}** — win rate {r['Win %']}, not enough edge")

    with col_c:
        st.subheader("P&L by Threshold Offset")
        bt = result["by_threshold"]
        if bt:
            rows = sorted(
                [{"Offset": k, "W/L": f"{v['wins']}/{v['losses']}",
                  "P&L ¢": round(v["pnl"], 1)} for k, v in bt.items()],
                key=lambda x: x["Offset"]
            )
            st.dataframe(pd.DataFrame(rows), hide_index=True)

    st.divider()

    # ── Calibration chart ─────────────────────────────────────────────────────
    st.subheader("Model Calibration")
    st.caption("Does the model's predicted probability match actual win rate?")
    trades = result["trades"]
    if trades and len(trades) >= 10:
        # Bucket by model_prob
        buckets: dict[float, dict] = {}
        for t in trades:
            bucket = round(t["model_prob"] * 10) / 10
            buckets.setdefault(bucket, {"wins": 0, "n": 0})
            buckets[bucket]["n"] += 1
            if t["result"] == "WIN":
                buckets[bucket]["wins"] += 1
        calib_rows = []
        for prob, d in sorted(buckets.items()):
            actual = d["wins"] / d["n"] if d["n"] else 0
            calib_rows.append({
                "Predicted": f"{prob*100:.0f}%",
                "n": d["n"],
                "Actual Win %": round(actual * 100, 1),
                "Predicted Win %": round(prob * 100, 1),
                "Gap": round((actual - prob) * 100, 1),
            })
        c_df = pd.DataFrame(calib_rows)
        st.dataframe(c_df, hide_index=True, use_container_width=True)

        # Calibration plot
        chart_df = c_df.set_index("Predicted")[["Actual Win %", "Predicted Win %"]]
        st.line_chart(chart_df)

        avg_gap = sum(abs(r["Gap"]) for r in calib_rows) / len(calib_rows)
        if avg_gap < 5:
            st.success(f"✅ Good calibration — average gap {avg_gap:.1f}% (well-calibrated model)")
        elif avg_gap < 12:
            st.warning(f"⚠️ Moderate calibration — average gap {avg_gap:.1f}% (acceptable)")
        else:
            st.error(f"❌ Poor calibration — average gap {avg_gap:.1f}% (model needs more data)")
    else:
        st.info("Need ≥ 10 backtest trades for calibration chart.")

    # ── Cumulative P&L ────────────────────────────────────────────────────────
    if trades:
        pnls = [t["pnl"] for t in trades]
        cum, running = [], 0
        for p in pnls:
            running += p
            cum.append(running)
        st.subheader("Cumulative P&L (cents)")
        st.line_chart(cum)

    # ── Trade log ─────────────────────────────────────────────────────────────
    with st.expander(f"Full Trade Log ({len(trades)} trades)"):
        t_df = pd.DataFrame(trades)[[
            "date", "station_code", "regime", "threshold", "side",
            "fc_high", "adj_forecast", "model_prob", "fair_value",
            "actual_high", "result", "pnl"
        ]]
        t_df.columns = ["Date", "Station", "Regime", "Threshold", "Side",
                         "FC High", "Adj FC", "Prob", "Fair ¢",
                         "Actual High", "Result", "P&L ¢"]
        st.dataframe(t_df, hide_index=True, use_container_width=True)

# ── Previous runs ─────────────────────────────────────────────────────────────
st.divider()
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
