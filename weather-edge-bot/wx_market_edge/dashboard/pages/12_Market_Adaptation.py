"""
Market Adaptation — tracks how model edge decays once a signal is published,
CLV (closing-line value) by station and regime, and staleness detection.

Answers: Are we getting good entry prices? Are markets adapting faster than
we think? Which regimes hold edge longest?
"""

import sys
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.db import init_db

st.set_page_config(page_title="Market Adaptation", page_icon="📉", layout="wide")
st.title("📉 Market Adaptation")
st.caption("Closing-line value, edge decay, and market efficiency analysis — PAPER TRADING ONLY")

conn = init_db()


# ── helpers ────────────────────────────────────────────────────────────────────

def _load_closed_trades(conn) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT pt.id, pt.station_code, pt.regime, pt.grade, pt.side,
               pt.threshold_f, pt.entry_price, pt.fair_value, pt.edge,
               pt.opened_at, pt.closed_at, pt.result, pt.pnl_dollars,
               pt.stake_dollars, pt.kelly_fraction, pt.forecast_date
        FROM paper_trades pt
        WHERE pt.status='CLOSED' AND pt.entry_price IS NOT NULL
        ORDER BY pt.opened_at DESC
    """).fetchall()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame([dict(r) for r in rows])
    df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce", utc=True)
    df["closed_at"] = pd.to_datetime(df["closed_at"], errors="coerce", utc=True)
    return df


def _load_price_snapshots(conn) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT mps.paper_trade_id, mps.market_ticker, mps.captured_at,
               mps.market_price, mps.minutes_after_open, pt.entry_price,
               pt.fair_value, pt.station_code, pt.regime, pt.grade
        FROM market_price_snapshots mps
        JOIN paper_trades pt ON pt.id = mps.paper_trade_id
        ORDER BY mps.paper_trade_id, mps.minutes_after_open
    """).fetchall()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame([dict(r) for r in rows])
    df["captured_at"] = pd.to_datetime(df["captured_at"], errors="coerce", utc=True)
    return df


trades_df     = _load_closed_trades(conn)
snapshots_df  = _load_price_snapshots(conn)
has_trades    = not trades_df.empty
has_snapshots = not snapshots_df.empty


# ── no data guard ──────────────────────────────────────────────────────────────

if not has_trades:
    st.info("No closed paper trades yet. Once trades settle, CLV and adaptation metrics appear here.")
    st.stop()


# ── Section 1: Closing-Line Value Summary ──────────────────────────────────────

st.header("1. Closing-Line Value (CLV)")
st.markdown(
    "CLV measures whether entry price beat the final pre-settlement market price. "
    "Positive CLV = entered before the market moved in your favour. "
    "**This is the primary measure of edge quality and timing.**"
)

if has_snapshots:
    # Find the latest price snapshot per trade (proxy for closing line)
    close_snap = (
        snapshots_df
        .sort_values("minutes_after_open")
        .groupby("paper_trade_id")
        .last()
        .reset_index()
    )
    merged = trades_df.merge(
        close_snap[["paper_trade_id", "market_price"]].rename(
            columns={"market_price": "closing_price"}
        ),
        left_on="id", right_on="paper_trade_id", how="left"
    )
    merged["clv"] = merged["fair_value"] - merged["closing_price"]
    merged = merged.dropna(subset=["clv"])

    if not merged.empty:
        avg_clv = merged["clv"].mean()
        pct_pos = (merged["clv"] > 0).mean() * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Avg CLV", f"{avg_clv:+.2f}¢",
                  help="Average cents gained vs closing market price")
        c2.metric("% Positive CLV", f"{pct_pos:.1f}%",
                  help="Trades where entry beat the close")
        c3.metric("Trades with CLV data", str(len(merged)))

        fig = px.histogram(
            merged, x="clv", nbins=30,
            title="Distribution of CLV (cents vs closing line)",
            labels={"clv": "CLV (cents)", "count": "Trades"},
            color_discrete_sequence=["#00b4d8"],
        )
        fig.add_vline(x=0, line_dash="dash", line_color="red")
        fig.add_vline(x=avg_clv, line_dash="dot", line_color="green",
                      annotation_text=f"Avg: {avg_clv:+.2f}¢")
        st.plotly_chart(fig, use_container_width=True)

        # CLV by station
        clv_station = (
            merged.groupby("station_code")["clv"]
            .agg(["mean", "count"])
            .reset_index()
            .rename(columns={"mean": "avg_clv", "count": "n"})
            .sort_values("avg_clv", ascending=False)
        )
        fig2 = px.bar(
            clv_station, x="station_code", y="avg_clv",
            text="n",
            title="Average CLV by Station",
            labels={"avg_clv": "Avg CLV (¢)", "station_code": "Station",
                    "n": "# Trades"},
            color="avg_clv",
            color_continuous_scale="RdYlGn",
        )
        fig2.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("CLV data available but merge produced no rows.")
else:
    st.info("No intra-trade price snapshots yet (market_price_snapshots table is empty). "
            "CLV tracking activates once the scanner begins logging price updates at t+15/30/60 min.")


# ── Section 2: Edge Decay ──────────────────────────────────────────────────────

st.divider()
st.header("2. Edge Decay Over Time")
st.markdown(
    "If edge decays quickly, it means the market is efficient and we need to enter fast. "
    "If edge is still present at +60 min, we have more flexibility on timing."
)

if has_snapshots and len(snapshots_df) > 10:
    # Compute edge at each snapshot = fair_value (from trade) - market_price (from snapshot)
    snap_copy = snapshots_df.copy()
    snap_copy["snap_edge"] = snap_copy["fair_value"] - snap_copy["market_price"]

    # Bin time windows
    bins = [0, 5, 15, 30, 60, 120, 999]
    labels = ["0-5 min", "5-15 min", "15-30 min", "30-60 min", "60-120 min", ">120 min"]
    snap_copy["time_bucket"] = pd.cut(
        snap_copy["minutes_after_open"], bins=bins, labels=labels, right=False
    )
    decay = (
        snap_copy.groupby("time_bucket", observed=True)["snap_edge"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "avg_edge", "count": "n"})
    )

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=decay["time_bucket"].astype(str),
        y=decay["avg_edge"],
        text=[f"n={n}" for n in decay["n"]],
        textposition="auto",
        marker_color=["green" if v > 0 else "red" for v in decay["avg_edge"]],
    ))
    fig3.add_hline(y=0, line_dash="dash", line_color="gray")
    fig3.update_layout(
        title="Average Edge at Each Time Window After Entry",
        xaxis_title="Minutes After Trade Opened",
        yaxis_title="Avg Edge (¢)",
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Edge decay by regime
    if "regime" in snap_copy.columns:
        decay_regime = (
            snap_copy.groupby(["regime", "time_bucket"], observed=True)["snap_edge"]
            .mean()
            .reset_index()
            .rename(columns={"snap_edge": "avg_edge"})
        )
        fig4 = px.line(
            decay_regime, x="time_bucket", y="avg_edge",
            color="regime",
            title="Edge Decay by Regime",
            labels={"avg_edge": "Avg Edge (¢)", "time_bucket": "Time Bucket"},
            markers=True,
        )
        fig4.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Insufficient intra-trade snapshots to plot edge decay (need >10 snapshots). "
            "The scanner logs price updates every 15 min after each paper trade opens.")


# ── Section 3: Edge at Entry vs Final Outcome ─────────────────────────────────

st.divider()
st.header("3. Entry Edge vs Outcome")
st.markdown("Do larger edges at entry actually predict more wins?")

if len(trades_df) >= 5:
    plot_df = trades_df[trades_df["edge"].notna() & trades_df["result"].notna()].copy()
    plot_df["win"] = (plot_df["result"] == "WIN").astype(int)

    fig5 = px.scatter(
        plot_df,
        x="edge", y="win",
        color="regime",
        symbol="grade",
        size="stake_dollars" if "stake_dollars" in plot_df.columns else None,
        hover_data=["station_code", "threshold_f", "side", "pnl_dollars"],
        title="Edge at Entry vs Win (1) / Loss (0)",
        labels={"edge": "Edge at Entry (¢)", "win": "Result (1=WIN, 0=LOSS)"},
        opacity=0.7,
    )
    fig5.add_hline(y=0.5, line_dash="dash", line_color="gray")
    fig5.add_vline(x=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig5, use_container_width=True)

    # Win rate by edge bucket
    edge_bins   = [-100, 0, 5, 10, 15, 20, 30, 100]
    edge_labels = ["<0", "0-5", "5-10", "10-15", "15-20", "20-30", ">30"]
    plot_df["edge_bucket"] = pd.cut(
        plot_df["edge"], bins=edge_bins, labels=edge_labels, right=False
    )
    wr_edge = (
        plot_df.groupby("edge_bucket", observed=True)["win"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "win_rate", "count": "n"})
    )
    fig6 = px.bar(
        wr_edge, x="edge_bucket", y="win_rate",
        text=[f"{wr:.0%} (n={n})" for wr, n in zip(wr_edge["win_rate"], wr_edge["n"])],
        title="Win Rate by Edge Bucket",
        labels={"win_rate": "Win Rate", "edge_bucket": "Edge Range (¢)"},
        color="win_rate",
        color_continuous_scale="RdYlGn",
        range_color=[0, 1],
    )
    fig6.add_hline(y=0.5, line_dash="dash", line_color="gray",
                   annotation_text="50% breakeven")
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.info("Need ≥5 closed trades to plot this section.")


# ── Section 4: Stale Edge Detection ───────────────────────────────────────────

st.divider()
st.header("4. Stale Edge Detection")
st.markdown(
    "Signals with high entry edge but poor outcomes may reflect stale data. "
    "This table highlights trades where edge was large but result was LOSS — "
    "possible METAR lag, forecast revision not yet ingested, or market had already moved."
)

if len(trades_df) >= 5:
    stale_candidates = (
        trades_df[
            (trades_df["edge"] >= 10) &
            (trades_df["result"] == "LOSS")
        ]
        [["station_code", "regime", "grade", "side", "threshold_f",
          "edge", "entry_price", "fair_value", "opened_at", "pnl_dollars"]]
        .sort_values("edge", ascending=False)
        .head(20)
    )

    if stale_candidates.empty:
        st.success("No high-edge losses found — model is not producing many 'phantom' signals.")
    else:
        st.warning(f"{len(stale_candidates)} high-edge losses detected. "
                   "These may indicate stale forecasts or rapid market moves post-entry.")
        st.dataframe(stale_candidates, use_container_width=True)
else:
    st.info("Need ≥5 closed trades to run stale edge detection.")


# ── Section 5: Regime Edge Half-Life ─────────────────────────────────────────

st.divider()
st.header("5. Regime Win Rate Over Time")
st.markdown("Rolling 20-trade win rate per regime — do regimes show drift or improvement?")

if len(trades_df) >= 20:
    for regime in trades_df["regime"].dropna().unique():
        subset = (
            trades_df[trades_df["regime"] == regime]
            .sort_values("opened_at")
            .copy()
        )
        if len(subset) < 10:
            continue
        subset["win_num"] = (subset["result"] == "WIN").astype(int)
        subset["rolling_wr"] = subset["win_num"].rolling(10, min_periods=5).mean()
        subset["trade_num"] = range(1, len(subset) + 1)

        fig7 = px.line(
            subset, x="trade_num", y="rolling_wr",
            title=f"{regime} — Rolling 10-Trade Win Rate",
            labels={"rolling_wr": "Win Rate", "trade_num": "Trade #"},
        )
        fig7.add_hline(y=0.5, line_dash="dash", line_color="red",
                       annotation_text="50%")
        st.plotly_chart(fig7, use_container_width=True)
else:
    st.info("Need ≥20 closed trades to plot rolling win rate by regime.")


# ── Footer ─────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "⚠️ PAPER TRADING ONLY — No real money. Market adaptation analysis is "
    "for research and model improvement only. Not financial advice."
)
