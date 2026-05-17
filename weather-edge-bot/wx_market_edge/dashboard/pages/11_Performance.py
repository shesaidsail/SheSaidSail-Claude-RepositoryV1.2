"""
Page 11 — Performance Analytics

Full analytics layer for the paper trading system:
  - Bankroll growth, drawdown, daily P&L
  - Expected value vs realised value
  - Edge quality and calibration
  - Breakdown by station / regime / threshold / grade
  - Model improvement trend over time
  - Closing Line Value (CLV) proxy
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

from database.db import init_db
from config import STARTING_BANKROLL

st.set_page_config(page_title="Performance Analytics", page_icon="📊", layout="wide")
st.title("📊 Performance Analytics")
st.caption("⚠️ PAPER TRADING ONLY — all figures are simulated, no real money.")

conn = init_db()

# ── Load trades ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_trades(_conn_id):
    rows = conn.execute("""
        SELECT id, opened_at, closed_at, station_code, regime, threshold_f,
               side, entry_price, fair_value, edge, confidence, model_prob,
               status, result, pnl_cents, pnl_dollars, stake_dollars,
               kelly_fraction, grade, settlement_price, adjusted_forecast,
               forecast_date
        FROM paper_trades
        WHERE status IN ('CLOSED','OPEN')
        ORDER BY COALESCE(closed_at, opened_at)
    """).fetchall()
    return [dict(r) for r in rows]

@st.cache_data(ttl=60)
def load_history(_conn_id):
    rows = conn.execute("""
        SELECT snapshot_date, bankroll, peak_bankroll, drawdown_pct, daily_pnl, trades_today
        FROM bankroll_history
        ORDER BY snapshot_date
    """).fetchall()
    return [dict(r) for r in rows]

all_trades  = load_trades(id(conn))
history     = load_history(id(conn))
closed      = [t for t in all_trades if t["status"] == "CLOSED"]
open_trades = [t for t in all_trades if t["status"] == "OPEN"]

# ── Date range filter ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    all_dates = sorted({t["closed_at"][:10] for t in closed if t.get("closed_at")})
    min_date  = datetime.strptime(all_dates[0], "%Y-%m-%d").date() if all_dates else (datetime.now(timezone.utc) - timedelta(days=90)).date()
    max_date  = datetime.strptime(all_dates[-1], "%Y-%m-%d").date() if all_dates else datetime.now(timezone.utc).date()

    date_from = st.date_input("From",  value=min_date)
    date_to   = st.date_input("To",    value=max_date)

    grade_filter = st.multiselect("Grade", ["A+", "B", "Watchlist", "Avoid"],
                                  default=["A+", "B", "Watchlist", "Avoid"])
    station_filter = st.multiselect("Station",
                                    sorted({t["station_code"] for t in closed if t.get("station_code")}),
                                    default=[])

df_from = date_from.strftime("%Y-%m-%d")
df_to   = date_to.strftime("%Y-%m-%d")

def in_range(t):
    d = (t.get("closed_at") or "")[:10]
    return df_from <= d <= df_to

filtered = [t for t in closed if in_range(t)]
if grade_filter:
    filtered = [t for t in filtered if (t.get("grade") or "—") in grade_filter]
if station_filter:
    filtered = [t for t in filtered if t.get("station_code") in station_filter]

n_trades = len(filtered)

# ── Top-level metrics ─────────────────────────────────────────────────────────
if not filtered:
    st.info("No closed trades in the selected period. Adjust the date range or run the scanner to generate trades.")
    st.stop()

wins   = sum(1 for t in filtered if t["result"] == "WIN")
losses = n_trades - wins
pnl_d  = [t["pnl_dollars"] or 0 for t in filtered]
pnl_c  = [t["pnl_cents"]   or 0 for t in filtered]
edges  = [abs(t["edge"] or 0)   for t in filtered]
conf   = [t["confidence"] or 0  for t in filtered]
stakes = [t["stake_dollars"] or 0 for t in filtered]

total_pnl_d  = sum(pnl_d)
total_pnl_c  = sum(pnl_c)
win_rate     = wins / n_trades if n_trades else 0
avg_edge     = np.mean(edges) if edges else 0
avg_conf     = np.mean(conf) if conf else 0
total_stake  = sum(stakes)
roi_pct      = total_pnl_d / STARTING_BANKROLL * 100

# Max drawdown from pnl stream
running = 0.0; peak_r = 0.0; max_dd_d = 0.0
for p in pnl_d:
    running += p
    peak_r   = max(peak_r, running)
    max_dd_d = max(max_dd_d, peak_r - running)

# Expected value per trade (Kelly: edge × confidence)
ev_per_trade = np.mean([abs(t["edge"] or 0) * (t["confidence"] or 0) for t in filtered]) if filtered else 0
realized_per = np.mean(pnl_c) if pnl_c else 0  # cents per trade

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
c1.metric("Trades",         n_trades)
c2.metric("Win Rate",       f"{win_rate:.1%}", delta=f"{wins}W / {losses}L")
c3.metric("Total P&L",      f"${total_pnl_d:+.2f}")
c4.metric("ROI",            f"{roi_pct:+.2f}%")
c5.metric("Avg Edge",       f"{avg_edge:.1f}¢")
c6.metric("Max Drawdown",   f"${max_dd_d:.2f}", delta_color="inverse")
c7.metric("EV / trade",     f"{ev_per_trade:.1f}¢", delta=f"Realized {realized_per:+.1f}¢")

st.divider()

# ── 1. Growth charts ──────────────────────────────────────────────────────────
st.subheader("1 — Bankroll & P&L Over Time")

# Build cumulative P&L from filtered trades
trades_df = pd.DataFrame(filtered)
trades_df["closed_date"] = trades_df["closed_at"].str[:10]
trades_df["pnl_dollars"]  = trades_df["pnl_dollars"].fillna(0)
trades_df["pnl_cents"]    = trades_df["pnl_cents"].fillna(0)
trades_df["cumulative_pnl_d"] = trades_df["pnl_dollars"].cumsum()
trades_df["bankroll_d"]       = STARTING_BANKROLL + trades_df["cumulative_pnl_d"]

tab1, tab2, tab3, tab4 = st.tabs(["Bankroll Curve", "Cumulative P&L", "Daily P&L", "Drawdown"])

with tab1:
    if history:
        h_df = pd.DataFrame(history)
        h_df = h_df[(h_df["snapshot_date"] >= df_from) & (h_df["snapshot_date"] <= df_to)]
        if not h_df.empty:
            h_df["snapshot_date"] = pd.to_datetime(h_df["snapshot_date"])
            h_df = h_df.set_index("snapshot_date")
            st.line_chart(h_df[["bankroll", "peak_bankroll"]].rename(columns={"bankroll": "Current $", "peak_bankroll": "Peak $"}))
        else:
            # Fall back to trade-by-trade curve
            tc = trades_df[["closed_at", "bankroll_d"]].copy()
            tc["closed_at"] = pd.to_datetime(tc["closed_at"])
            st.line_chart(tc.set_index("closed_at")["bankroll_d"])
    else:
        tc = trades_df[["closed_at", "bankroll_d"]].copy()
        tc["closed_at"] = pd.to_datetime(tc["closed_at"])
        st.line_chart(tc.set_index("closed_at")["bankroll_d"])
    st.caption(f"Start: ${STARTING_BANKROLL:,.0f}  →  Current: ${STARTING_BANKROLL + total_pnl_d:,.2f}  (+${total_pnl_d:+.2f})")

with tab2:
    tc = trades_df[["closed_at", "cumulative_pnl_d"]].copy()
    tc["closed_at"] = pd.to_datetime(tc["closed_at"])
    st.line_chart(tc.set_index("closed_at")["cumulative_pnl_d"].rename("Cumulative P&L $"))
    # Add zero line annotation
    if total_pnl_d >= 0:
        st.success(f"Net profit: **${total_pnl_d:+.2f}** across {n_trades} trades")
    else:
        st.error(f"Net loss: **${total_pnl_d:+.2f}** across {n_trades} trades")

with tab3:
    daily = trades_df.groupby("closed_date")["pnl_dollars"].sum().reset_index()
    daily.columns = ["Date", "Daily P&L $"]
    daily["Date"] = pd.to_datetime(daily["Date"])
    daily = daily.set_index("Date")
    st.bar_chart(daily["Daily P&L $"])

with tab4:
    if history:
        h_df = pd.DataFrame(history)
        h_df = h_df[(h_df["snapshot_date"] >= df_from) & (h_df["snapshot_date"] <= df_to)]
        if not h_df.empty:
            h_df["snapshot_date"] = pd.to_datetime(h_df["snapshot_date"])
            h_df["Drawdown %"] = (h_df["drawdown_pct"] * 100).round(2)
            st.line_chart(h_df.set_index("snapshot_date")["Drawdown %"])
        else:
            st.info("Drawdown data will populate once bankroll_history snapshots are recorded.")
    else:
        # Compute from trades
        dd_running = 0.0; dd_peak = 0.0
        dd_series  = []
        for _, row in trades_df.iterrows():
            dd_running += row["pnl_dollars"]
            dd_peak     = max(dd_peak, dd_running)
            dd_pct      = (dd_peak - dd_running) / (STARTING_BANKROLL + dd_peak) * 100 if dd_peak > 0 else 0
            dd_series.append({"date": row["closed_at"], "Drawdown %": round(dd_pct, 2)})
        dd_df = pd.DataFrame(dd_series)
        dd_df["date"] = pd.to_datetime(dd_df["date"])
        st.line_chart(dd_df.set_index("date")["Drawdown %"])

st.divider()

# ── 2. Edge quality: Expected vs Realised ────────────────────────────────────
st.subheader("2 — Expected Value vs Realised Value")
st.caption("EV = edge × confidence per trade. If realised ≥ EV, the model has real edge.")

ev_rows = []
for t in filtered:
    ev = abs(t["edge"] or 0) * (t["confidence"] or 0)
    rv = t["pnl_cents"] or 0
    ev_rows.append({"EV (¢)": round(ev, 2), "Realised (¢)": rv,
                    "Grade": t.get("grade") or "?",
                    "Station": t.get("station_code") or "?"})

ev_df = pd.DataFrame(ev_rows)

col_a, col_b = st.columns(2)
with col_a:
    avg_ev = ev_df["EV (¢)"].mean()
    avg_rv = ev_df["Realised (¢)"].mean()
    edge_ratio = avg_rv / avg_ev if avg_ev > 0 else 0

    ev_summary = pd.DataFrame({
        "Metric": ["Avg Expected Value", "Avg Realised Value", "Capture Ratio"],
        "Value":  [f"{avg_ev:.1f}¢", f"{avg_rv:.1f}¢", f"{edge_ratio:.2f}×"]
    })
    st.dataframe(ev_summary, hide_index=True, use_container_width=True)
    if edge_ratio >= 0.8:
        st.success(f"✅ Model capturing {edge_ratio:.0%} of expected edge — real edge confirmed.")
    elif edge_ratio >= 0.4:
        st.warning(f"⚠️ Capturing {edge_ratio:.0%} of EV — variance or execution drag.")
    else:
        st.error(f"❌ Capturing only {edge_ratio:.0%} of EV — model edge may be illusory.")

with col_b:
    # EV vs Realised by grade
    grade_ev = ev_df.groupby("Grade")[["EV (¢)", "Realised (¢)"]].mean().round(2)
    st.dataframe(grade_ev, use_container_width=True)

# Scatter: EV vs Realised per trade (sample up to 500)
sample = ev_df.sample(min(len(ev_df), 500), random_state=42) if len(ev_df) > 0 else ev_df
st.scatter_chart(sample, x="EV (¢)", y="Realised (¢)", color="Grade", size=30)

st.divider()

# ── 3. Calibration chart ─────────────────────────────────────────────────────
st.subheader("3 — Confidence Calibration")
st.caption("A well-calibrated model has predicted win % ≈ actual win %. Flat or inverted → the model is guessing.")

calib = conn.execute("""
    SELECT ROUND(model_prob * 10) / 10 AS bucket,
           COUNT(*) AS n,
           ROUND(AVG(CASE WHEN result='WIN' THEN 1.0 ELSE 0.0 END), 3) AS actual_wr
    FROM paper_trades
    WHERE status='CLOSED'
      AND model_prob IS NOT NULL
      AND DATE(closed_at) BETWEEN ? AND ?
    GROUP BY bucket
    HAVING n >= 3
    ORDER BY bucket
""", (df_from, df_to)).fetchall()

if calib and len(calib) >= 2:
    cal_df = pd.DataFrame([dict(r) for r in calib])
    cal_df["Predicted %"] = (cal_df["bucket"] * 100).round(0)
    cal_df["Actual %"]    = (cal_df["actual_wr"] * 100).round(1)
    cal_df["Gap"]         = (cal_df["Actual %"] - cal_df["Predicted %"]).round(1)
    avg_gap = cal_df["Gap"].abs().mean()

    col_c, col_d = st.columns([2, 1])
    with col_c:
        chart_cal = cal_df.set_index("Predicted %")[["Actual %", "Predicted %"]].rename(
            columns={"Actual %": "Actual Win %", "Predicted %": "Ideal (Predicted)"})
        st.line_chart(chart_cal)
    with col_d:
        if avg_gap < 5:
            st.success(f"✅ Well-calibrated (avg gap {avg_gap:.1f}%)")
        elif avg_gap < 12:
            st.warning(f"⚠️ Moderate calibration (avg gap {avg_gap:.1f}%)")
        else:
            st.error(f"❌ Poor calibration (avg gap {avg_gap:.1f}%)")
        st.dataframe(cal_df[["Predicted %", "n", "Actual %", "Gap"]], hide_index=True)
else:
    st.info("Need ≥6 closed trades across 2+ probability buckets for calibration chart.")

st.divider()

# ── 4. Win rate by grade ──────────────────────────────────────────────────────
st.subheader("4 — Performance by Signal Grade")

grade_rows = []
for grade in ["A+", "B", "Watchlist", "Avoid"]:
    gt = [t for t in filtered if (t.get("grade") or "?") == grade]
    if not gt:
        continue
    gw   = sum(1 for t in gt if t["result"] == "WIN")
    gpnl = sum(t["pnl_dollars"] or 0 for t in gt)
    gedge = np.mean([abs(t["edge"] or 0) for t in gt])
    grade_rows.append({
        "Grade":    grade,
        "Trades":   len(gt),
        "Win Rate": f"{gw/len(gt):.1%}",
        "Avg Edge": f"{gedge:.1f}¢",
        "P&L $":    round(gpnl, 2),
        "ROI":      f"{gpnl / STARTING_BANKROLL * 100:+.2f}%",
    })

if grade_rows:
    g_df = pd.DataFrame(grade_rows)
    st.dataframe(g_df, hide_index=True, use_container_width=True)

    # Win rate bar chart
    wr_df = pd.DataFrame([{"Grade": r["Grade"], "Win %": float(r["Win Rate"].strip("%"))}
                          for r in grade_rows]).set_index("Grade")
    st.bar_chart(wr_df["Win %"])

st.divider()

# ── 5. Breakdown by station ───────────────────────────────────────────────────
st.subheader("5 — P&L by Station")

station_rows = {}
for t in filtered:
    s = t.get("station_code") or "?"
    station_rows.setdefault(s, {"wins": 0, "losses": 0, "pnl": 0, "edges": [], "trades": 0})
    if t["result"] == "WIN":
        station_rows[s]["wins"] += 1
    else:
        station_rows[s]["losses"] += 1
    station_rows[s]["pnl"]    += (t["pnl_dollars"] or 0)
    station_rows[s]["trades"] += 1
    station_rows[s]["edges"].append(abs(t["edge"] or 0))

st_rows = []
for s, d in sorted(station_rows.items(), key=lambda x: -x[1]["pnl"]):
    tot = d["wins"] + d["losses"]
    st_rows.append({
        "Station":  s,
        "Trades":   tot,
        "Win Rate": f"{d['wins']/tot:.1%}" if tot else "—",
        "Avg Edge": f"{np.mean(d['edges']):.1f}¢" if d["edges"] else "—",
        "P&L $":    round(d["pnl"], 2),
        "Action":   "✅ Keep" if d["pnl"] > 0 and d["wins"]/tot >= 0.55 else
                    ("🚫 Review" if d["pnl"] < -10 else "👀 Watch"),
    })

if st_rows:
    st_df = pd.DataFrame(st_rows)
    col_e, col_f = st.columns([1, 2])
    with col_e:
        st.dataframe(st_df, hide_index=True, use_container_width=True)
    with col_f:
        bar_st = st_df.set_index("Station")["P&L $"]
        st.bar_chart(bar_st)

st.divider()

# ── 6. Breakdown by regime ────────────────────────────────────────────────────
st.subheader("6 — P&L by Regime")

regime_rows = {}
for t in filtered:
    r = t.get("regime") or "UNKNOWN"
    regime_rows.setdefault(r, {"wins": 0, "losses": 0, "pnl": 0, "trades": 0, "edges": []})
    if t["result"] == "WIN":
        regime_rows[r]["wins"] += 1
    else:
        regime_rows[r]["losses"] += 1
    regime_rows[r]["pnl"]    += (t["pnl_dollars"] or 0)
    regime_rows[r]["trades"] += 1
    regime_rows[r]["edges"].append(abs(t["edge"] or 0))

reg_rows = []
for r, d in sorted(regime_rows.items(), key=lambda x: -x[1]["pnl"]):
    tot = d["wins"] + d["losses"]
    reg_rows.append({
        "Regime":   r,
        "Trades":   tot,
        "Win Rate": f"{d['wins']/tot:.1%}" if tot else "—",
        "Avg Edge": f"{np.mean(d['edges']):.1f}¢" if d["edges"] else "—",
        "P&L $":    round(d["pnl"], 2),
        "Verdict":  "✅ Trade" if d["pnl"] > 0 and d["wins"] / tot >= 0.55 else
                    ("🚫 Avoid" if d["pnl"] < -5 else "👀 Watch"),
    })

if reg_rows:
    reg_df = pd.DataFrame(reg_rows)
    col_g, col_h = st.columns([2, 1])
    with col_g:
        bar_reg = reg_df.set_index("Regime")["P&L $"]
        st.bar_chart(bar_reg)
    with col_h:
        st.dataframe(reg_df[["Regime", "Trades", "Win Rate", "P&L $", "Verdict"]],
                     hide_index=True, use_container_width=True)

st.divider()

# ── 7. Breakdown by threshold ─────────────────────────────────────────────────
st.subheader("7 — P&L by Strike Threshold (°F)")

thr_rows = {}
for t in filtered:
    tk = int(t["threshold_f"]) if t.get("threshold_f") else 0
    thr_rows.setdefault(tk, {"wins": 0, "losses": 0, "pnl": 0, "trades": 0})
    if t["result"] == "WIN":
        thr_rows[tk]["wins"] += 1
    else:
        thr_rows[tk]["losses"] += 1
    thr_rows[tk]["pnl"]    += (t["pnl_dollars"] or 0)
    thr_rows[tk]["trades"] += 1

thr_list = []
for thr, d in sorted(thr_rows.items()):
    tot = d["wins"] + d["losses"]
    thr_list.append({
        "Threshold °F": thr,
        "Trades":        tot,
        "Win Rate":      f"{d['wins']/tot:.1%}" if tot else "—",
        "P&L $":         round(d["pnl"], 2),
    })

if thr_list:
    thr_df = pd.DataFrame(thr_list)
    col_i, col_j = st.columns([2, 1])
    with col_i:
        st.bar_chart(thr_df.set_index("Threshold °F")["P&L $"])
    with col_j:
        st.dataframe(thr_df, hide_index=True, use_container_width=True)

st.divider()

# ── 8. Trades over time ───────────────────────────────────────────────────────
st.subheader("8 — Paper Trade Activity Over Time")

activity = trades_df.groupby("closed_date").agg(
    total=("result", "count"),
    wins=("result", lambda x: (x == "WIN").sum()),
    pnl=("pnl_dollars", "sum"),
).reset_index()
activity.columns = ["Date", "Trades", "Wins", "P&L $"]
activity["Date"]   = pd.to_datetime(activity["Date"])
activity["Win %"]  = (activity["Wins"] / activity["Trades"] * 100).round(1)
activity = activity.set_index("Date")

col_k, col_l = st.columns(2)
with col_k:
    st.write("**Daily trade count**")
    st.bar_chart(activity["Trades"])
with col_l:
    st.write("**Daily win rate %**")
    st.line_chart(activity["Win %"])

st.divider()

# ── 9. Rolling performance (is the bot improving?) ────────────────────────────
st.subheader("9 — Is the Model Improving?")
st.caption("Rolling 20-trade win rate and average edge. Upward trend = model calibrating well.")

if n_trades >= 10:
    rolling_df = trades_df[["closed_at", "result", "pnl_dollars", "edge"]].copy()
    rolling_df["win"]      = (rolling_df["result"] == "WIN").astype(float)
    rolling_df["abs_edge"] = rolling_df["edge"].abs().fillna(0)

    window = min(20, n_trades // 2)
    rolling_df["rolling_wr"]  = rolling_df["win"].rolling(window, min_periods=5).mean() * 100
    rolling_df["rolling_edge"] = rolling_df["abs_edge"].rolling(window, min_periods=5).mean()
    rolling_df["rolling_pnl_cum"] = rolling_df["pnl_dollars"].cumsum()

    rolling_df["closed_at"] = pd.to_datetime(rolling_df["closed_at"])
    rolling_df = rolling_df.set_index("closed_at")

    col_m, col_n = st.columns(2)
    with col_m:
        st.write(f"**Rolling {window}-trade win rate %**")
        st.line_chart(rolling_df["rolling_wr"].dropna())
    with col_n:
        st.write(f"**Rolling {window}-trade avg edge (¢)**")
        st.line_chart(rolling_df["rolling_edge"].dropna())

    # Trend signal
    wr_series = rolling_df["rolling_wr"].dropna()
    if len(wr_series) >= 4:
        first_half = wr_series.iloc[:len(wr_series)//2].mean()
        second_half = wr_series.iloc[len(wr_series)//2:].mean()
        trend = second_half - first_half
        if trend > 3:
            st.success(f"✅ Win rate trending UP (+{trend:.1f}pp) — model is learning.")
        elif trend < -3:
            st.error(f"❌ Win rate trending DOWN ({trend:.1f}pp) — review regime rules.")
        else:
            st.info(f"Win rate stable (trend: {trend:+.1f}pp). More trades needed for a clear signal.")
else:
    st.info(f"Need at least 10 closed trades for rolling analysis. Currently {n_trades}.")

st.divider()

# ── 10. Closing Line Value (CLV) proxy ────────────────────────────────────────
st.subheader("10 — Closing Line Value (CLV) Proxy")
st.caption(
    "True CLV = your entry price vs the market's final price before settlement. "
    "Since we don't store Kalshi closing prices, we use **settlement edge** as a proxy: "
    "fair_value − entry_price vs what the market settled at. Positive CLV proxy = you bought good value."
)

clv_rows = []
for t in filtered:
    fv    = t.get("fair_value") or 0
    entry = t.get("entry_price") or 0
    sett  = t.get("settlement_price")  # actual temperature
    thresh = t.get("threshold_f") or 0
    side   = t.get("side", "Yes")

    entry_edge = fv - entry  # positive = we bought below fair value

    # Settlement outcome: did the market agree with our edge?
    if sett is not None:
        if side == "Yes":
            market_was_right = 1 if sett >= thresh + 1 else 0
        else:
            market_was_right = 1 if sett <= thresh else 0
        # CLV proxy: entry_edge × whether settlement confirms direction
        clv_proxy = entry_edge * (1 if (entry_edge > 0) == (market_was_right == 1) else -1)
    else:
        clv_proxy = entry_edge

    clv_rows.append({
        "Entry Edge ¢":  round(entry_edge, 1),
        "CLV Proxy ¢":   round(clv_proxy, 1),
        "Result":         t["result"],
        "Grade":          t.get("grade") or "?",
    })

clv_df = pd.DataFrame(clv_rows)
avg_clv = clv_df["CLV Proxy ¢"].mean()

col_o, col_p = st.columns(2)
with col_o:
    if avg_clv > 2:
        st.success(f"✅ Avg CLV proxy: +{avg_clv:.1f}¢ — consistently buying good value.")
    elif avg_clv > 0:
        st.info(f"ℹ️ Avg CLV proxy: +{avg_clv:.1f}¢ — slight positive selection.")
    else:
        st.warning(f"⚠️ Avg CLV proxy: {avg_clv:.1f}¢ — may be chasing stale quotes.")

    clv_summary = clv_df.groupby("Grade")["CLV Proxy ¢"].mean().round(2).reset_index()
    clv_summary.columns = ["Grade", "Avg CLV ¢"]
    st.dataframe(clv_summary, hide_index=True)

with col_p:
    st.scatter_chart(clv_df.sample(min(len(clv_df), 300), random_state=1),
                     x="Entry Edge ¢", y="CLV Proxy ¢", color="Grade", size=30)

st.divider()

# ── 11. Bankroll sizing effectiveness ────────────────────────────────────────
st.subheader("11 — Bankroll Sizing Effectiveness")
st.caption("Is the Kelly sizing working? Bigger stakes should land on winning trades.")

sized = [t for t in filtered if t.get("stake_dollars") and t["stake_dollars"] > 0]
if len(sized) >= 5:
    sized_df = pd.DataFrame(sized)
    sized_df["stake_dollars"] = sized_df["stake_dollars"].fillna(0)
    sized_df["pnl_dollars"]   = sized_df["pnl_dollars"].fillna(0)
    sized_df["win"]           = (sized_df["result"] == "WIN").astype(int)

    avg_stake_win  = sized_df[sized_df["win"] == 1]["stake_dollars"].mean()
    avg_stake_loss = sized_df[sized_df["win"] == 0]["stake_dollars"].mean()

    col_q, col_r = st.columns(2)
    with col_q:
        sizing_summary = pd.DataFrame({
            "Outcome": ["WIN", "LOSS"],
            "Avg Stake $": [round(avg_stake_win, 2), round(avg_stake_loss, 2)],
        })
        st.dataframe(sizing_summary, hide_index=True)
        if avg_stake_win > avg_stake_loss:
            st.success(f"✅ Sizing working: bigger stakes on wins (${avg_stake_win:.2f} vs ${avg_stake_loss:.2f})")
        else:
            st.warning(f"⚠️ Sizing not optimal: larger stakes on losses (${avg_stake_win:.2f} vs ${avg_stake_loss:.2f})")

    with col_r:
        kelly_df = sized_df.groupby("grade").agg(
            trades=("id", "count"),
            avg_stake=("stake_dollars", "mean"),
            avg_kelly=("kelly_fraction", "mean"),
            pnl=("pnl_dollars", "sum"),
        ).round(3).reset_index()
        kelly_df.columns = ["Grade", "Trades", "Avg Stake $", "Avg Kelly", "P&L $"]
        st.dataframe(kelly_df, hide_index=True, use_container_width=True)
else:
    st.info(f"Sizing analysis needs at least 5 trades with stake data. Currently {len(sized)}.")

st.divider()

# ── Summary verdict ───────────────────────────────────────────────────────────
st.subheader("Model Verdict")

verdict_items = []

if win_rate >= 0.55:
    verdict_items.append(("✅", f"Win rate {win_rate:.1%} — above breakeven threshold (55%)"))
elif win_rate >= 0.48:
    verdict_items.append(("⚠️", f"Win rate {win_rate:.1%} — close to breakeven, watch for variance"))
else:
    verdict_items.append(("❌", f"Win rate {win_rate:.1%} — below breakeven, investigate regime rules"))

if total_pnl_d > 0:
    verdict_items.append(("✅", f"Net profit ${total_pnl_d:+.2f} — positive ROI"))
else:
    verdict_items.append(("❌", f"Net loss ${total_pnl_d:+.2f} — bankroll declining"))

if edge_ratio >= 0.7:
    verdict_items.append(("✅", f"Capturing {edge_ratio:.0%} of expected value"))
else:
    verdict_items.append(("⚠️", f"Only capturing {edge_ratio:.0%} of expected value"))

if max_dd_d < STARTING_BANKROLL * 0.10:
    verdict_items.append(("✅", f"Max drawdown ${max_dd_d:.2f} ({max_dd_d/STARTING_BANKROLL:.1%}) — within limits"))
elif max_dd_d < STARTING_BANKROLL * 0.20:
    verdict_items.append(("⚠️", f"Max drawdown ${max_dd_d:.2f} ({max_dd_d/STARTING_BANKROLL:.1%}) — elevated"))
else:
    verdict_items.append(("❌", f"Max drawdown ${max_dd_d:.2f} ({max_dd_d/STARTING_BANKROLL:.1%}) — high, sizing reduced"))

if avg_edge >= 10:
    verdict_items.append(("✅", f"Avg edge {avg_edge:.1f}¢ — strong signal selection"))
elif avg_edge >= 5:
    verdict_items.append(("ℹ️", f"Avg edge {avg_edge:.1f}¢ — acceptable"))
else:
    verdict_items.append(("⚠️", f"Avg edge {avg_edge:.1f}¢ — signals may be too marginal"))

for icon, msg in verdict_items:
    if icon == "✅":
        st.success(f"{icon} {msg}")
    elif icon == "❌":
        st.error(f"{icon} {msg}")
    elif icon == "⚠️":
        st.warning(f"{icon} {msg}")
    else:
        st.info(f"{icon} {msg}")
