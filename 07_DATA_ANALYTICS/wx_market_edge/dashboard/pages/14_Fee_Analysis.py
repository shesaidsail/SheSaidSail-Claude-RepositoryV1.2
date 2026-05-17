"""
Fee Analysis — tracks gross vs net EV, Kalshi fees paid, spread costs,
and whether certain station/regime combinations remain profitable after costs.

Key questions answered:
  • How much are fees eroding actual edge?
  • Are we over-paying spread on aggressive taker entries?
  • Which stations/regimes are untradeable net of fees?
  • Would maker orders improve our net P&L?
"""

import sys
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.db import init_db
from models.fee_engine import estimate_fees, net_fair_value
from config import KALSHI_SETTLEMENT_FEE_PCT, MIN_NET_EDGE, DEFAULT_ORDER_TYPE, STARTING_BANKROLL

st.set_page_config(page_title="Fee Analysis", page_icon="💸", layout="wide")
st.title("💸 Fee & Cost Analysis")
st.caption(
    "Gross EV vs net EV, Kalshi settlement fees, spread costs, and "
    "maker/taker impact — PAPER TRADING ONLY"
)

conn = init_db()


# ── helpers ────────────────────────────────────────────────────────────────────

def _load_trades(conn) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT id, station_code, regime, grade, side, threshold_f,
               entry_price, fair_value, edge, gross_edge, net_edge,
               est_fee_cents, spread_cost_cents, order_type,
               status, result, pnl_dollars, gross_pnl_dollars, fee_dollars,
               stake_dollars, opened_at, closed_at, forecast_date
        FROM paper_trades
        ORDER BY opened_at DESC
    """).fetchall()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame([dict(r) for r in rows])
    df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce", utc=True)
    df["closed_at"] = pd.to_datetime(df["closed_at"], errors="coerce", utc=True)
    # Fill missing fee columns (trades opened before fee tracking was added)
    if "fee_dollars" not in df.columns:
        df["fee_dollars"] = 0.0
    if "gross_pnl_dollars" not in df.columns:
        df["gross_pnl_dollars"] = df.get("pnl_dollars", 0)
    df["fee_dollars"]       = df["fee_dollars"].fillna(0)
    df["gross_pnl_dollars"] = df["gross_pnl_dollars"].fillna(df["pnl_dollars"].fillna(0))
    return df


all_df    = _load_trades(conn)
closed_df = all_df[all_df["status"] == "CLOSED"].copy() if not all_df.empty else pd.DataFrame()
has_data  = not closed_df.empty


# ── Section 0: Current fee settings ───────────────────────────────────────────

with st.expander("⚙️ Fee Model Settings", expanded=False):
    c1, c2, c3 = st.columns(3)
    c1.metric("Kalshi Settlement Fee", f"{KALSHI_SETTLEMENT_FEE_PCT:.1f}%",
              help="Applied to net profit on winning contracts only")
    c2.metric("Min Net Edge Required", f"{MIN_NET_EDGE:.1f}¢",
              help="Trades blocked if net edge falls below this after fees + spread")
    c3.metric("Default Order Type", DEFAULT_ORDER_TYPE,
              help="TAKER = pay ask (guaranteed fill); MAKER = limit at mid (70% fill est.)")

    st.caption(
        "Change these via environment variables: `KALSHI_SETTLEMENT_FEE_PCT`, "
        "`MIN_NET_EDGE`, `DEFAULT_ORDER_TYPE`"
    )


# ── Section 1: Gross vs Net EV Summary ────────────────────────────────────────

st.header("1. Gross EV vs Net EV")

if has_data:
    total_gross  = closed_df["gross_pnl_dollars"].sum()
    total_fees   = closed_df["fee_dollars"].sum()
    total_net    = closed_df["pnl_dollars"].sum()
    roi_gross    = total_gross / STARTING_BANKROLL * 100
    roi_net      = total_net   / STARTING_BANKROLL * 100
    fee_drag     = total_fees  / max(abs(total_gross), 0.01) * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Gross P&L",    f"${total_gross:+.2f}",  f"ROI: {roi_gross:+.1f}%")
    c2.metric("Fees Paid",    f"${total_fees:.2f}",    f"{fee_drag:.1f}% of gross P&L")
    c3.metric("Net P&L",      f"${total_net:+.2f}",    f"ROI: {roi_net:+.1f}%")
    c4.metric("Avg Fee/Trade",f"${total_fees/max(len(closed_df),1):.2f}")
    c5.metric("Trades",       str(len(closed_df)))

    # Waterfall: gross → fee → net
    fig_waterfall = go.Figure(go.Waterfall(
        name="P&L breakdown",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Gross P&L", "Kalshi Fees", "Net P&L"],
        textposition="outside",
        text=[f"${total_gross:+.2f}", f"−${total_fees:.2f}", f"${total_net:+.2f}"],
        y=[total_gross, -total_fees, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#2dc653"}},
        decreasing={"marker": {"color": "#e63946"}},
        totals={"marker": {"color": "#0077b6"}},
    ))
    fig_waterfall.update_layout(
        title="P&L Waterfall: Gross → Fees → Net",
        showlegend=False,
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)
else:
    st.info("No closed trades yet — P&L metrics will appear once trades settle.")


# ── Section 2: Cumulative Gross vs Net ────────────────────────────────────────

st.divider()
st.header("2. Cumulative P&L: Gross vs Net")

if has_data and "closed_at" in closed_df.columns:
    ts_df = (
        closed_df
        .dropna(subset=["closed_at"])
        .sort_values("closed_at")
        .copy()
    )
    if not ts_df.empty:
        ts_df["cum_gross"] = ts_df["gross_pnl_dollars"].cumsum()
        ts_df["cum_fees"]  = ts_df["fee_dollars"].cumsum()
        ts_df["cum_net"]   = ts_df["pnl_dollars"].cumsum()

        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(
            x=ts_df["closed_at"], y=ts_df["cum_gross"],
            name="Cumulative Gross P&L", line=dict(color="#90e0ef", dash="dot"),
        ))
        fig_cum.add_trace(go.Scatter(
            x=ts_df["closed_at"], y=ts_df["cum_fees"],
            name="Cumulative Fees Paid", line=dict(color="#e63946"),
            fill="tozeroy", fillcolor="rgba(230,57,70,0.10)",
        ))
        fig_cum.add_trace(go.Scatter(
            x=ts_df["closed_at"], y=ts_df["cum_net"],
            name="Cumulative Net P&L", line=dict(color="#2dc653", width=2),
        ))
        fig_cum.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_cum.update_layout(
            title="Cumulative Gross P&L vs Cumulative Net P&L",
            xaxis_title="Date",
            yaxis_title="Cumulative P&L ($)",
        )
        st.plotly_chart(fig_cum, use_container_width=True)
else:
    st.info("Need closed trades with timestamps to plot this chart.")


# ── Section 3: Fee Erosion by Station and Regime ──────────────────────────────

st.divider()
st.header("3. Fee Erosion by Station & Regime")
st.markdown(
    "Stations or regimes where fees consume a large fraction of gross edge "
    "may be **untradeable net of costs** — especially for small-edge signals."
)

if has_data:
    def _erosion_table(df: pd.DataFrame, group_col: str, label: str):
        if group_col not in df.columns:
            return
        grp = (
            df.groupby(group_col)
            .agg(
                trades      =("id",               "count"),
                wins        =("result",            lambda x: (x == "WIN").sum()),
                gross_pnl   =("gross_pnl_dollars", "sum"),
                fees_paid   =("fee_dollars",       "sum"),
                net_pnl     =("pnl_dollars",       "sum"),
                avg_fee_per_trade=("fee_dollars",  "mean"),
            )
            .reset_index()
        )
        grp["win_rate"]      = (grp["wins"] / grp["trades"] * 100).round(1)
        grp["fee_drag_pct"]  = (grp["fees_paid"] / grp["gross_pnl"].abs().clip(lower=0.01) * 100).round(1)
        grp["net_roi_pct"]   = (grp["net_pnl"]   / STARTING_BANKROLL * 100).round(2)
        grp["tradeable"]     = grp["net_pnl"] > 0

        grp = grp.sort_values("net_pnl", ascending=False)

        def _colour(row):
            if row["tradeable"]:
                return ["background-color: #d4edda"] * len(row)
            return ["background-color: #f8d7da"] * len(row)

        styled = grp.style.apply(_colour, axis=1).format({
            "gross_pnl":          "${:.2f}",
            "fees_paid":          "${:.2f}",
            "net_pnl":            "${:.2f}",
            "avg_fee_per_trade":  "${:.2f}",
            "fee_drag_pct":       "{:.1f}%",
            "net_roi_pct":        "{:.2f}%",
            "win_rate":           "{:.1f}%",
        })

        st.subheader(f"By {label}")
        st.dataframe(styled, use_container_width=True)

    _erosion_table(closed_df, "station_code", "Station")
    _erosion_table(closed_df, "regime",       "Regime")
    _erosion_table(closed_df, "grade",        "Grade")
else:
    st.info("No closed trades yet.")


# ── Section 4: Maker vs Taker Analysis ────────────────────────────────────────

st.divider()
st.header("4. Maker vs Taker Impact")
st.markdown(
    "**Taker** entries cross the spread and pay a higher price. "
    "**Maker** limit orders fill at mid but not always. "
    "This section estimates how much better performance would be if all entries were maker orders."
)

if has_data and "entry_price" in closed_df.columns:
    fee_rate = KALSHI_SETTLEMENT_FEE_PCT / 100

    # Recompute what net edge would have been as maker (no spread cost)
    rows_with_edge = closed_df.dropna(subset=["entry_price", "gross_edge"]).copy()

    if not rows_with_edge.empty:
        # Estimate spread cost for each trade (use stored spread_cost_cents if available)
        if "spread_cost_cents" in rows_with_edge.columns:
            rows_with_edge["spread_c"] = rows_with_edge["spread_cost_cents"].fillna(0)
        else:
            rows_with_edge["spread_c"] = 0.0

        rows_with_edge["net_edge_taker"] = rows_with_edge.get(
            "net_edge", rows_with_edge["gross_edge"] - rows_with_edge["spread_c"]
        )
        rows_with_edge["net_edge_maker"] = rows_with_edge["net_edge_taker"] + rows_with_edge["spread_c"]

        taker_positive = (rows_with_edge["net_edge_taker"] > MIN_NET_EDGE).sum()
        maker_positive = (rows_with_edge["net_edge_maker"] > MIN_NET_EDGE).sum()
        total_r        = len(rows_with_edge)

        c1, c2, c3 = st.columns(3)
        c1.metric("Tradeable as TAKER",
                  f"{taker_positive}/{total_r}",
                  f"{taker_positive/max(total_r,1)*100:.0f}%")
        c2.metric("Tradeable as MAKER",
                  f"{maker_positive}/{total_r}",
                  f"{maker_positive/max(total_r,1)*100:.0f}%")
        c3.metric("Signals rescued by MAKER",
                  str(max(0, maker_positive - taker_positive)),
                  help="Trades that fail taker check but pass maker check")

        # Spread cost distribution
        if rows_with_edge["spread_c"].sum() > 0:
            fig_spread = px.histogram(
                rows_with_edge[rows_with_edge["spread_c"] > 0],
                x="spread_c",
                nbins=20,
                title="Distribution of Spread Cost at Entry (¢/contract)",
                labels={"spread_c": "Spread Cost (¢)", "count": "Trades"},
                color_discrete_sequence=["#f48c06"],
            )
            st.plotly_chart(fig_spread, use_container_width=True)
        else:
            st.info("No spread cost data recorded (all entries assumed at mid-market).")

        # Avg net edge: maker vs taker by station
        maker_taker_station = (
            rows_with_edge
            .groupby("station_code")
            .agg(
                avg_net_edge_taker=("net_edge_taker", "mean"),
                avg_net_edge_maker=("net_edge_maker", "mean"),
                n=("id", "count"),
            )
            .reset_index()
        )
        fig_mt = go.Figure()
        fig_mt.add_trace(go.Bar(
            name="TAKER",
            x=maker_taker_station["station_code"],
            y=maker_taker_station["avg_net_edge_taker"],
            marker_color="#0077b6",
        ))
        fig_mt.add_trace(go.Bar(
            name="MAKER",
            x=maker_taker_station["station_code"],
            y=maker_taker_station["avg_net_edge_maker"],
            marker_color="#2dc653",
        ))
        fig_mt.add_hline(y=MIN_NET_EDGE, line_dash="dash", line_color="red",
                         annotation_text=f"Min net edge ({MIN_NET_EDGE}¢)")
        fig_mt.update_layout(
            title="Avg Net Edge: Taker vs Maker by Station",
            barmode="group",
            yaxis_title="Avg Net Edge (¢)",
        )
        st.plotly_chart(fig_mt, use_container_width=True)
    else:
        st.info("Need gross_edge data in paper_trades to run maker/taker analysis.")
else:
    st.info("No closed trades yet for maker/taker analysis.")


# ── Section 5: Edge Erosion Scatter ───────────────────────────────────────────

st.divider()
st.header("5. Gross Edge vs Net Edge — Fee Erosion Scatter")

if has_data and "gross_edge" in closed_df.columns:
    scatter_df = closed_df.dropna(subset=["gross_edge"]).copy()
    if "net_edge" not in scatter_df.columns or scatter_df["net_edge"].isna().all():
        scatter_df["net_edge"] = scatter_df["gross_edge"] - scatter_df.get("est_fee_cents", pd.Series(0))

    scatter_df["net_edge"] = scatter_df["net_edge"].fillna(scatter_df["gross_edge"])

    fig_scatter = px.scatter(
        scatter_df,
        x="gross_edge", y="net_edge",
        color="station_code",
        symbol="result",
        size="stake_dollars" if "stake_dollars" in scatter_df.columns else None,
        hover_data=["regime", "grade", "fee_dollars"],
        title="Gross Edge vs Net Edge (each dot = one trade)",
        labels={
            "gross_edge": "Gross Edge (¢)",
            "net_edge":   "Net Edge (¢)",
        },
        opacity=0.75,
    )
    # Diagonal line y = x (no erosion)
    rng = [scatter_df["gross_edge"].min() - 1, scatter_df["gross_edge"].max() + 1]
    fig_scatter.add_trace(go.Scatter(
        x=rng, y=rng,
        mode="lines", name="No erosion (gross = net)",
        line=dict(dash="dash", color="gray"),
    ))
    fig_scatter.add_hline(y=MIN_NET_EDGE, line_dash="dot", line_color="red",
                          annotation_text=f"Net edge floor ({MIN_NET_EDGE}¢)")
    fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.caption(
        "Points below the dashed diagonal line have erosion from fees/spread. "
        "Points below the red horizontal line were rejected (or should have been)."
    )
else:
    st.info("Need trades with gross_edge data to display this chart.")


# ── Section 6: Fee Impact on Specific Signals ─────────────────────────────────

st.divider()
st.header("6. Live Fee Calculator")
st.markdown("Compute the full cost breakdown for any hypothetical contract.")

col1, col2, col3, col4 = st.columns(4)
win_p    = col1.slider("Win probability (%)", 1, 99, 60) / 100.0
mid_p    = col2.slider("Mid-market price (¢)", 1, 99, 35)
bid_p    = col3.slider("Best bid (¢)", 1, 98, 33)
ask_p    = col4.slider("Best ask (¢)", 2, 99, 37)

if ask_p <= bid_p:
    st.warning("Ask must be greater than bid.")
else:
    breakdown = estimate_fees(
        win_prob        = win_p,
        market_price_mid= float(mid_p),
        best_bid        = float(bid_p),
        best_ask        = float(ask_p),
    )
    breakdown_maker = estimate_fees(
        win_prob        = win_p,
        market_price_mid= float(mid_p),
        best_bid        = float(bid_p),
        best_ask        = float(ask_p),
        order_type      = "MAKER",
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Gross Fair",     f"{breakdown['gross_fair']:.2f}¢")
    c2.metric("Net Fair",       f"{breakdown['net_fair']:.2f}¢")
    c3.metric("Est. Fee",       f"−{breakdown['expected_fee_cents']:.2f}¢")
    c4.metric("Spread Cost",    f"−{breakdown['spread_cost_cents']:.2f}¢")
    c5.metric("Gross Edge",     f"{breakdown['gross_edge']:+.2f}¢")

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.metric("Net Edge (TAKER)", f"{breakdown['net_edge']:+.2f}¢",
              delta="TRADEABLE" if breakdown["is_tradeable"] else "BLOCKED",
              delta_color="normal" if breakdown["is_tradeable"] else "inverse")
    c7.metric("Net Edge (MAKER)", f"{breakdown_maker['net_edge']:+.2f}¢",
              delta="TRADEABLE" if breakdown_maker["is_tradeable"] else "BLOCKED",
              delta_color="normal" if breakdown_maker["is_tradeable"] else "inverse")
    c8.metric("Maker Advantage",  f"+{breakdown['maker_advantage']:.2f}¢",
              help="Extra net edge if filled as limit order at mid")
    c9.metric("Fee Drag",         f"{breakdown['fee_pct_of_gross']*100:.1f}%",
              help="Fee as % of gross edge")
    c10.metric("Total Erosion",   f"{breakdown['edge_erosion_pct']:.1f}%",
               help="(fee + spread) ÷ gross edge × 100")

    # Sensitivity: what mid price makes this trade worthless net-of-fees?
    nfv = breakdown["net_fair"]
    st.info(
        f"**Break-even analysis:**  "
        f"Net fair value = **{nfv:.2f}¢**. "
        f"At TAKER entry ({ask_p}¢), net edge = **{breakdown['net_edge']:+.2f}¢**. "
        f"Trade is {'✅ tradeable' if breakdown['is_tradeable'] else '❌ blocked by fee gate'}. "
        + (f"Switch to MAKER limit at mid ({mid_p}¢) for +{breakdown['maker_advantage']:.2f}¢ improvement."
           if breakdown["maker_advantage"] > 0 else "")
    )


# ── Footer ─────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "⚠️ PAPER TRADING ONLY — All figures are simulated. "
    "Kalshi fee rate is configurable via KALSHI_SETTLEMENT_FEE_PCT env var. "
    "Not financial advice."
)
