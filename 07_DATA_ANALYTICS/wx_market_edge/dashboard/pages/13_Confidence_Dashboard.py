"""
Confidence Dashboard — visualises the 4-factor confidence scoring engine
and its relationship to actual outcomes.

Answers: Is the confidence score well-calibrated? Which factor drives
score differences the most? Are high-confidence trades actually winning more?
"""

import sys
import sqlite3
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.db import init_db
from models.confidence_engine import (
    compute_confidence, _sample_score, _variance_score,
    _regime_score, _edge_score,
)
from config import STATIONS, DEFAULT_MODEL

st.set_page_config(page_title="Confidence Dashboard", page_icon="🎯", layout="wide")
st.title("🎯 Confidence Dashboard")
st.caption(
    "Calibration, factor breakdown, and predictive power of the 4-factor confidence engine — "
    "PAPER TRADING ONLY"
)

conn = init_db()


# ── data loading ───────────────────────────────────────────────────────────────

def _load_closed_trades(conn) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT pt.id, pt.station_code, pt.regime, pt.grade, pt.side,
               pt.threshold_f, pt.entry_price, pt.fair_value, pt.edge,
               pt.confidence, pt.result, pt.pnl_dollars, pt.stake_dollars,
               pt.kelly_fraction, pt.opened_at, pt.forecast_date
        FROM paper_trades pt
        WHERE pt.status='CLOSED' AND pt.confidence IS NOT NULL
        ORDER BY pt.opened_at DESC
    """).fetchall()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame([dict(r) for r in rows])
    df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce", utc=True)
    df["win"] = (df["result"] == "WIN").astype(float)
    return df


def _load_model_stats(conn) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT station_code, model_name, regime, sample_size,
               avg_bias, std_dev, confidence, updated_at
        FROM model_stats
        WHERE model_name=?
        ORDER BY station_code, regime
    """, (DEFAULT_MODEL,)).fetchall()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame([dict(r) for r in rows])


trades_df = _load_closed_trades(conn)
stats_df  = _load_model_stats(conn)
has_data  = not trades_df.empty


# ── Section 1: Confidence Score Explorer ──────────────────────────────────────

st.header("1. Confidence Score Explorer")
st.markdown(
    "Interactively explore how each factor contributes to the composite score. "
    "Useful for understanding which inputs move the needle most."
)

with st.expander("⚙️ Score Calculator", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    n_ex    = col1.slider("Sample size (n)", 0, 100, 20)
    std_ex  = col2.slider("Std dev (σ °F)",  0.5, 8.0, 2.5, step=0.1)
    edge_ex = col3.slider("Edge (¢)",         0.0, 40.0, 12.0, step=0.5)
    regime_ex = col4.selectbox("Regime", [
        "CLEAR_SKY", "MARINE_WEAK", "MARINE_STRONG", "OFFSHORE_FLOW",
        "DRY_HEAT", "HUMID_HEAT", "HEAT_SPIKE_RISK", "COASTAL_STRATUS",
        "STORM_RISK", "RAIN_RISK", "UNKNOWN",
    ], index=0)

    conf_val, reasons = compute_confidence(
        sample_size=n_ex, std_dev=std_ex,
        regime=regime_ex, edge=edge_ex, regime_conf=0.70,
    )

    ss = _sample_score(n_ex)
    vs = _variance_score(std_ex)
    rs = _regime_score(regime_ex, 0.70)
    es = _edge_score(edge_ex)

    st.metric("Composite Confidence", f"{conf_val:.1%}")

    factor_df = pd.DataFrame({
        "Factor":       ["Sample Size (30%)", "Variance (30%)", "Regime (25%)", "Edge (15%)"],
        "Raw Score":    [ss, vs, rs, es],
        "Weighted":     [0.30*ss, 0.30*vs, 0.25*rs, 0.15*es],
    })

    fig_factors = px.bar(
        factor_df, x="Factor", y=["Raw Score", "Weighted"],
        barmode="group",
        title=f"Factor Breakdown — Composite: {conf_val:.1%}",
        range_y=[0, 1],
        color_discrete_map={"Raw Score": "#90e0ef", "Weighted": "#0077b6"},
    )
    st.plotly_chart(fig_factors, use_container_width=True)

    with st.expander("Scoring reasons"):
        for r in reasons:
            st.text(r)


# ── Section 2: Calibration Curve ──────────────────────────────────────────────

st.divider()
st.header("2. Confidence Calibration")
st.markdown(
    "A **well-calibrated** model has actual win rate ≈ confidence score. "
    "Points on the diagonal = perfect calibration. "
    "Points above = under-confident; below = over-confident."
)

if has_data and len(trades_df) >= 10:
    # Bin confidence into 10-point buckets
    calib_df = trades_df[trades_df["confidence"].notna()].copy()
    calib_df["conf_bucket"] = (calib_df["confidence"] * 10).apply(math.floor) / 10
    calib = (
        calib_df.groupby("conf_bucket")["win"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "win_rate", "count": "n"})
    )

    fig_cal = go.Figure()
    fig_cal.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode="lines", name="Perfect calibration",
        line=dict(dash="dash", color="gray"),
    ))
    fig_cal.add_trace(go.Scatter(
        x=calib["conf_bucket"],
        y=calib["win_rate"],
        mode="markers+lines",
        name="Actual win rate",
        marker=dict(size=calib["n"].apply(lambda n: max(8, min(24, n))),
                    color="#0077b6"),
        text=[f"n={n}" for n in calib["n"]],
        hovertemplate="%{x:.0%} conf → %{y:.1%} actual win rate<br>%{text}",
    ))
    fig_cal.update_layout(
        title="Calibration Curve — Model Confidence vs Actual Win Rate",
        xaxis=dict(title="Model Confidence Bucket", tickformat=".0%", range=[0, 1]),
        yaxis=dict(title="Actual Win Rate", tickformat=".0%", range=[0, 1]),
        showlegend=True,
    )
    st.plotly_chart(fig_cal, use_container_width=True)

    # Calibration ECE (expected calibration error)
    ece = (calib["n"] / calib["n"].sum() * abs(calib["conf_bucket"] - calib["win_rate"])).sum()
    col_a, col_b = st.columns(2)
    col_a.metric("Expected Calibration Error (ECE)", f"{ece:.3f}",
                 help="Lower is better. <0.05 = well calibrated, >0.10 = needs work")
    col_b.metric("Trades in calibration chart", str(int(calib["n"].sum())))
else:
    st.info(
        f"Need ≥10 closed trades with confidence scores for calibration. "
        f"Currently: {len(trades_df)} closed trades."
    )


# ── Section 3: Confidence vs Outcome by Grade ─────────────────────────────────

st.divider()
st.header("3. Confidence Distribution by Grade and Outcome")

if has_data and len(trades_df) >= 5:
    fig_box = px.box(
        trades_df, x="grade", y="confidence",
        color="result",
        title="Confidence Distribution by Grade and Win/Loss",
        labels={"confidence": "Confidence Score", "grade": "Signal Grade"},
        color_discrete_map={"WIN": "#2dc653", "LOSS": "#e63946"},
        category_orders={"grade": ["A+", "B", "Watchlist", "Avoid"]},
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Avg confidence by grade + win rate
    grade_summary = (
        trades_df.groupby("grade")
        .agg(avg_conf=("confidence", "mean"),
             win_rate=("win", "mean"),
             n=("win", "count"))
        .reset_index()
        .sort_values("avg_conf", ascending=False)
    )
    st.dataframe(
        grade_summary.style.format({
            "avg_conf": "{:.2%}",
            "win_rate": "{:.2%}",
        }),
        use_container_width=True,
    )
else:
    st.info("Need ≥5 closed trades to plot this section.")


# ── Section 4: Factor Sensitivity ─────────────────────────────────────────────

st.divider()
st.header("4. Factor Sensitivity Analysis")
st.markdown(
    "How much does each factor shift the score? "
    "Generated by sweeping each input while holding others at median values."
)

if not stats_df.empty:
    med_n   = int(stats_df["sample_size"].median() or 10)
    med_std = float(stats_df["std_dev"].median() or 2.5)
else:
    med_n, med_std = 10, 2.5

sweep_rows = []

# Sweep sample size
for n_val in range(0, 51, 5):
    c, _ = compute_confidence(n_val, med_std, "CLEAR_SKY", 12.0, 0.70)
    sweep_rows.append({"Factor": "Sample Size", "x": n_val, "score": c})

# Sweep std dev
for std_val in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]:
    c, _ = compute_confidence(med_n, std_val, "CLEAR_SKY", 12.0, 0.70)
    sweep_rows.append({"Factor": "Std Dev (σ)", "x": std_val, "score": c})

# Sweep edge
for edge_val in range(0, 41, 2):
    c, _ = compute_confidence(med_n, med_std, "CLEAR_SKY", float(edge_val), 0.70)
    sweep_rows.append({"Factor": "Edge (¢)", "x": edge_val, "score": c})

sweep_df = pd.DataFrame(sweep_rows)

fig_sens = px.line(
    sweep_df, x="x", y="score", color="Factor",
    facet_col="Factor",
    facet_col_wrap=3,
    title="Sensitivity: How Each Factor Drives Confidence Score",
    labels={"score": "Confidence", "x": "Factor Value"},
    range_y=[0, 1],
)
fig_sens.update_yaxes(tickformat=".0%")
st.plotly_chart(fig_sens, use_container_width=True)


# ── Section 5: Current Model Stats ────────────────────────────────────────────

st.divider()
st.header("5. Current Model Stats & Implied Confidence")
st.markdown("Computed scores for each station/regime pair in the database.")

if not stats_df.empty:
    scores = []
    for _, row in stats_df.iterrows():
        n   = int(row["sample_size"] or 0)
        std = float(row["std_dev"] or 3.0)
        c, _ = compute_confidence(n, std, row["regime"], 12.0, 0.70)
        scores.append({
            "Station":     row["station_code"],
            "Regime":      row["regime"],
            "n":           n,
            "Avg Bias":    row["avg_bias"],
            "Std Dev":     std,
            "Conf Score":  c,
            "Bias Status": (
                "Good" if abs(row["avg_bias"] or 0) < 1 else
                "Moderate" if abs(row["avg_bias"] or 0) < 3 else "High"
            ),
        })

    scores_df = pd.DataFrame(scores).sort_values("Conf Score", ascending=False)

    # Colour-coded table
    def _colour_conf(val):
        if val >= 0.70:
            return "background-color: #d4edda"
        if val >= 0.55:
            return "background-color: #fff3cd"
        return "background-color: #f8d7da"

    styled = (
        scores_df.style
        .format({"Conf Score": "{:.2%}", "Avg Bias": "{:+.2f}°F", "Std Dev": "{:.2f}°F"})
        .applymap(_colour_conf, subset=["Conf Score"])
    )
    st.dataframe(styled, use_container_width=True)

    # Heatmap: station × regime
    pivot = scores_df.pivot_table(
        index="Station", columns="Regime", values="Conf Score", aggfunc="first"
    )
    if not pivot.empty:
        fig_heat = px.imshow(
            pivot,
            title="Confidence Score Heatmap: Station × Regime",
            color_continuous_scale="RdYlGn",
            zmin=0, zmax=1,
            text_auto=".0%",
            aspect="auto",
        )
        st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("No model stats in the database yet. Run the bias engine to populate.")


# ── Section 6: High/Low Confidence Trade Comparison ───────────────────────────

st.divider()
st.header("6. High vs Low Confidence Trade Outcomes")

if has_data and len(trades_df) >= 10:
    threshold = trades_df["confidence"].median()
    high_conf = trades_df[trades_df["confidence"] >= threshold]
    low_conf  = trades_df[trades_df["confidence"] <  threshold]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("High Conf Win Rate",
              f"{high_conf['win'].mean():.1%}" if len(high_conf) else "—",
              f"n={len(high_conf)}")
    c2.metric("Low Conf Win Rate",
              f"{low_conf['win'].mean():.1%}"  if len(low_conf)  else "—",
              f"n={len(low_conf)}")
    c3.metric("Threshold Used", f"{threshold:.1%}")
    c4.metric("Difference",
              f"{(high_conf['win'].mean() - low_conf['win'].mean())*100:+.1f}pp"
              if (len(high_conf) and len(low_conf)) else "—")

    # P&L comparison
    if "pnl_dollars" in trades_df.columns:
        pnl_grouped = pd.DataFrame({
            "Group":   ["High Conf", "Low Conf"],
            "Avg P&L": [
                high_conf["pnl_dollars"].mean() if len(high_conf) else 0,
                low_conf["pnl_dollars"].mean()  if len(low_conf)  else 0,
            ],
            "n": [len(high_conf), len(low_conf)],
        })
        fig_pnl = px.bar(
            pnl_grouped, x="Group", y="Avg P&L",
            text=[f"n={n}" for n in pnl_grouped["n"]],
            title="Average Dollar P&L: High vs Low Confidence",
            color="Avg P&L",
            color_continuous_scale="RdYlGn",
        )
        fig_pnl.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_pnl, use_container_width=True)
else:
    st.info("Need ≥10 closed trades to compare high/low confidence outcomes.")


# ── Footer ─────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "⚠️ PAPER TRADING ONLY — Confidence analysis is for model improvement only. "
    "Not financial advice. All trading simulated."
)
