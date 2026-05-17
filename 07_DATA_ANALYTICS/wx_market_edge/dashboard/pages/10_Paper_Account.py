"""
Page 10 — Paper Account

Live paper bankroll, open positions, closed trade journal,
P&L curve, performance by station/regime/threshold, and
bankroll management settings display.

Everything here is PAPER TRADING ONLY. No real money.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

from database.db import init_db
from trading.bankroll import bankroll_status, get_daily_pnl
from trading.paper_trader import get_open_trades, get_closed_trades, performance_summary
from config import (
    STARTING_BANKROLL,
    MAX_SINGLE_TRADE_PCT, MAX_DAILY_LOSS_PCT,
    MAX_STATION_EXPOSURE_PCT, MAX_REGIME_EXPOSURE_PCT,
    KELLY_FRACTION_NORMAL, KELLY_FRACTION_APLUS,
    DRAWDOWN_REDUCE_THRESHOLD, DRAWDOWN_HALF_THRESHOLD, DRAWDOWN_PAUSE_THRESHOLD,
    _paper_trading_enabled,
)

st.set_page_config(page_title="Paper Account", page_icon="💰", layout="wide")
st.title("💰 Paper Account")
st.caption("⚠️ PAPER TRADING ONLY — No real money. No real execution. Simulation only.")

conn = init_db()

# ── Status banner ─────────────────────────────────────────────────────────────
status = bankroll_status(conn)

if status["trading_paused"]:
    if status["daily_halt"]:
        st.error("🛑 Daily loss limit hit — paper trading halted for today.")
    elif status["drawdown_pct"] >= DRAWDOWN_PAUSE_THRESHOLD:
        st.error(f"🛑 Drawdown {status['drawdown_pct']:.1%} ≥ {DRAWDOWN_PAUSE_THRESHOLD:.0%} pause threshold — paper trading paused.")
elif status["drawdown_pct"] >= DRAWDOWN_HALF_THRESHOLD:
    st.warning(f"⚠️ Drawdown {status['drawdown_pct']:.1%} — bet sizes reduced 50%.")
elif status["drawdown_pct"] >= DRAWDOWN_REDUCE_THRESHOLD:
    st.warning(f"⚠️ Drawdown {status['drawdown_pct']:.1%} — bet sizes reduced 25%.")
else:
    trading_label = "✅ Paper trading active (always-on)" if _paper_trading_enabled() else "⏸️ Paper trading paused (PAPER_TRADING_ENABLED=false)"
    st.info(trading_label)

# ── Key metrics row ───────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
bankroll  = status["current_bankroll"]
peak      = status["peak_bankroll"]
dd        = status["drawdown_pct"]
exposure  = status["open_exposure"]
available = status["available"]
roi       = status["roi_pct"]

c1.metric("Bankroll",         f"${bankroll:,.2f}",    delta=f"Start ${STARTING_BANKROLL:,.0f}")
c2.metric("Peak",             f"${peak:,.2f}")
c3.metric("Drawdown",         f"{dd:.1%}",            delta=f"Mult {status['sizing_multiplier']:.2f}x", delta_color="inverse")
c4.metric("Open Exposure",    f"${exposure:,.2f}")
c5.metric("Available",        f"${available:,.2f}")
c6.metric("ROI",              f"{roi:+.2f}%",         delta_color="normal")

st.divider()

# ── Bankroll curve ────────────────────────────────────────────────────────────
st.subheader("Bankroll Curve")

history = conn.execute("""
    SELECT snapshot_date, bankroll, peak_bankroll, drawdown_pct, daily_pnl, trades_today
    FROM bankroll_history
    ORDER BY snapshot_date
""").fetchall()

if history and len(history) >= 2:
    h_df = pd.DataFrame([dict(r) for r in history])
    h_df["snapshot_date"] = pd.to_datetime(h_df["snapshot_date"])
    h_df = h_df.set_index("snapshot_date")

    tab_curve, tab_drawdown, tab_daily = st.tabs(["Bankroll vs Peak", "Drawdown %", "Daily P&L"])
    with tab_curve:
        st.line_chart(h_df[["bankroll", "peak_bankroll"]])
    with tab_drawdown:
        dd_pct = h_df[["drawdown_pct"]].copy()
        dd_pct.columns = ["Drawdown %"]
        dd_pct["Drawdown %"] = (dd_pct["Drawdown %"] * 100).round(2)
        st.line_chart(dd_pct)
    with tab_daily:
        st.bar_chart(h_df[["daily_pnl"]])
else:
    st.info("Bankroll curve will appear after at least 2 daily snapshots. Snapshots are saved each time a trade opens or settles.")

st.divider()

# ── Open trades ───────────────────────────────────────────────────────────────
st.subheader("Open Paper Positions")

open_trades = get_open_trades(conn)
if open_trades:
    ot_rows = []
    for t in open_trades:
        ot_rows.append({
            "Grade":     t.get("grade") or "—",
            "Station":   t.get("station_code"),
            "Side":      t.get("side"),
            "Strike °F": t.get("threshold_f"),
            "Price ¢":   t.get("entry_price"),
            "Fair ¢":    t.get("fair_value"),
            "Edge ¢":    t.get("edge"),
            "Stake $":   f"${t.get('stake_dollars') or 0:.2f}",
            "Kelly":     f"{(t.get('kelly_fraction') or 0):.3f}",
            "Regime":    t.get("regime") or "—",
            "Opened":    (t.get("opened_at") or "")[:16],
        })
    st.dataframe(pd.DataFrame(ot_rows), hide_index=True, use_container_width=True)
    total_stake = sum(t.get("stake_dollars") or 0 for t in open_trades)
    st.caption(f"Total open exposure: **${total_stake:.2f}**  ({total_stake / bankroll:.1%} of bankroll)")
else:
    st.info("No open paper trades at the moment.")

st.divider()

# ── Closed trades / journal ───────────────────────────────────────────────────
st.subheader("Trade Journal — Recent Closed Trades")

closed_trades = get_closed_trades(conn, limit=100)
if closed_trades:
    ct_rows = []
    for t in closed_trades:
        pnl_d = t.get("pnl_dollars") or 0
        ct_rows.append({
            "Date":      (t.get("closed_at") or "")[:10],
            "Grade":     t.get("grade") or "—",
            "Station":   t.get("station_code"),
            "Side":      t.get("side"),
            "Strike":    t.get("threshold_f"),
            "Result":    t.get("result"),
            "P&L $":     round(pnl_d, 2),
            "P&L ¢":     t.get("pnl_cents"),
            "Stake $":   round(t.get("stake_dollars") or 0, 2),
            "Regime":    t.get("regime") or "—",
        })
    ct_df = pd.DataFrame(ct_rows)
    st.dataframe(
        ct_df.style.map(lambda v: "color: green" if v == "WIN" else ("color: red" if v == "LOSS" else ""),
                        subset=["Result"]),
        hide_index=True, use_container_width=True
    )
else:
    st.info("No closed paper trades yet.")

st.divider()

# ── Performance breakdown ─────────────────────────────────────────────────────
st.subheader("Performance Breakdown")

perf = performance_summary(conn)
if perf.get("total", 0) > 0:
    col_a, col_b = st.columns(2)

    with col_a:
        st.metric("Total Trades",  perf["total"])
        st.metric("Win Rate",      f"{perf['win_rate']:.1%}")
        st.metric("Total P&L $",   f"${perf['total_pnl_d']:+.2f}")
        st.metric("ROI (dollars)", f"{perf['roi_dollars_pct']:+.2f}%")
        st.metric("Max Drawdown $",f"${perf['max_drawdown']:.2f}")

    with col_b:
        # By station
        if perf.get("by_station"):
            st.write("**By Station**")
            rows = []
            for st_code, d in perf["by_station"].items():
                t = d["wins"] + d["losses"]
                rows.append({
                    "Station": st_code,
                    "W": d["wins"], "L": d["losses"],
                    "Win%": f"{d['wins']/t:.0%}" if t else "—",
                    "P&L $": round(d["pnl_dollars"], 2),
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    # By regime
    if perf.get("by_regime"):
        st.write("**By Regime**")
        rows = []
        for regime, d in sorted(perf["by_regime"].items(), key=lambda x: -x[1]["pnl_dollars"]):
            t = d["wins"] + d["losses"]
            rows.append({
                "Regime": regime,
                "W": d["wins"], "L": d["losses"],
                "Win%": f"{d['wins']/t:.0%}" if t else "—",
                "P&L $": round(d["pnl_dollars"], 2),
            })
        reg_df = pd.DataFrame(rows)
        st.dataframe(reg_df, hide_index=True, use_container_width=True)
        st.bar_chart(reg_df.set_index("Regime")["P&L $"])

    # By threshold
    if perf.get("by_threshold"):
        st.write("**By Strike Threshold**")
        rows = []
        for thr, d in sorted(perf["by_threshold"].items(), key=lambda x: -x[1]["pnl_dollars"]):
            t = d["wins"] + d["losses"]
            rows.append({
                "Threshold °F": thr,
                "W": d["wins"], "L": d["losses"],
                "Win%": f"{d['wins']/t:.0%}" if t else "—",
                "P&L $": round(d["pnl_dollars"], 2),
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
else:
    st.info("No closed trades yet — performance data will appear after first settlements.")

st.divider()

# ── What the model learned ────────────────────────────────────────────────────
st.subheader("What the Model Learned")

lessons = conn.execute("""
    SELECT * FROM model_lessons
    ORDER BY severity DESC, created_at DESC
    LIMIT 20
""").fetchall()

if lessons:
    severity_icons = {"INFO": "ℹ️", "WARN": "⚠️", "ALERT": "🚨"}
    for les in lessons:
        les = dict(les)
        icon = severity_icons.get(les["severity"], "•")
        applied = "✅ Applied" if les["applied"] else "🔵 Active"
        with st.expander(f"{icon} [{applied}] {les['station_code'] or 'ALL'} / {les['regime']}"):
            st.write(f"**{les['lesson']}**")
            if les.get("recommendation"):
                st.success(f"💡 {les['recommendation']}")
            st.caption(f"Logged: {les['created_at'][:16]}")
else:
    st.success("No model lessons yet — system is still learning.")

st.divider()

# ── Bankroll settings display ─────────────────────────────────────────────────
st.subheader("Bankroll Risk Rules (current config)")

col1, col2 = st.columns(2)
with col1:
    st.write("**Sizing rules**")
    st.write(f"• Starting bankroll: **${STARTING_BANKROLL:,.0f}**")
    st.write(f"• Max per trade: **{MAX_SINGLE_TRADE_PCT:.0%}** of bankroll")
    st.write(f"• Daily loss halt: **{MAX_DAILY_LOSS_PCT:.0%}**")
    st.write(f"• Max station exposure: **{MAX_STATION_EXPOSURE_PCT:.0%}**")
    st.write(f"• Max regime exposure: **{MAX_REGIME_EXPOSURE_PCT:.0%}**")
with col2:
    st.write("**Kelly fractions**")
    st.write(f"• Normal / B grade: **{KELLY_FRACTION_NORMAL:.0%}** fractional Kelly")
    st.write(f"• A+ grade (max):   **{KELLY_FRACTION_APLUS:.0%}** fractional Kelly")
    st.write("**Drawdown protection**")
    st.write(f"• >{DRAWDOWN_REDUCE_THRESHOLD:.0%} → 25% size reduction  (mult 0.75×)")
    st.write(f"• >{DRAWDOWN_HALF_THRESHOLD:.0%} → 50% size reduction  (mult 0.50×)")
    st.write(f"• >{DRAWDOWN_PAUSE_THRESHOLD:.0%} → trading paused      (mult 0.00×)")

st.divider()

# ── Reset bankroll (admin) ────────────────────────────────────────────────────
with st.expander("⚙️ Admin — Reset Paper Bankroll"):
    st.warning("This voids all open trades and marks them as VOID. Closed trade history is kept.")
    if st.button("🔄 Reset Paper Bankroll to $1,000", type="secondary"):
        conn.execute("UPDATE paper_trades SET status='VOID' WHERE status='OPEN'")
        conn.execute("DELETE FROM bankroll_history")
        conn.commit()
        st.success(f"Bankroll reset to ${STARTING_BANKROLL:,.0f}. All open trades voided.")
        st.rerun()

# ── Active alerts ─────────────────────────────────────────────────────────────
st.subheader("Active Paper Trade Alerts (last 20)")

alert_rows = conn.execute("""
    SELECT created_at, station_code, threshold_f, side, grade,
           edge_cents, sms_text, status
    FROM webhook_alerts
    WHERE alert_type IN ('PAPER_TRADE_OPENED','PAPER_TRADE_SETTLED','PAPER_DAILY_SUMMARY')
    ORDER BY created_at DESC
    LIMIT 20
""").fetchall()

if alert_rows:
    for row in alert_rows:
        row = dict(row)
        ts  = (row.get("created_at") or "")[:16]
        sta = row.get("station_code") or "ALL"
        lbl = f"{ts} — {sta} {row.get('side','')} >{row.get('threshold_f','')} [{row.get('status')}]"
        with st.expander(lbl):
            st.code(row.get("sms_text", ""), language=None)
else:
    st.info("No paper trade alerts logged yet.")
