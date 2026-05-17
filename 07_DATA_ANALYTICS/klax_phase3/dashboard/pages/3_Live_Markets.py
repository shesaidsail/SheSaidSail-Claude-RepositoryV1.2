import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from database.db import get_connection, init_db
from models.bias_engine import get_stats, win_probability
from models.confidence_engine import compute_confidence
from models.regime_engine import classify, parse_cloud_layers
from config import STATION, DEFAULT_MODEL, BET_EDGE_THRESHOLD, MIN_CONFIDENCE, KLAX_UTC_OFFSET_HOURS

init_db()
st.header("💰 Live Market Analyzer")

# ---------------------------------------------------------------------------
# Detect live regime
# ---------------------------------------------------------------------------

with get_connection() as conn:
    latest_obs_row = conn.execute("""
        SELECT * FROM actual_observations
        WHERE station_code = ? ORDER BY timestamp_utc DESC LIMIT 1
    """, (STATION,)).fetchone()
    latest_fc_row = conn.execute("""
        SELECT * FROM forecast_runs
        WHERE station_code = ? AND model_name = ?
        ORDER BY forecast_date DESC, timestamp_utc DESC LIMIT 1
    """, (STATION, DEFAULT_MODEL)).fetchone()

live_regime_name = "ALL"
live_regime_conf = 0.5
live_regime_notes: list[str] = []

if latest_obs_row:
    obs = dict(latest_obs_row)
    temp_f = obs.get("observed_temp") or 70.0
    dewp_f = obs.get("dewpoint")
    dps    = round(temp_f - dewp_f, 1) if dewp_f is not None else None
    try:
        utc_dt     = datetime.strptime(obs["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
        local_hour = (utc_dt.hour + KLAX_UTC_OFFSET_HOURS) % 24
        month      = utc_dt.month
    except Exception:
        local_hour, month = 12, 5

    lr = classify(
        wind_direction    = obs.get("wind_direction"),
        wind_speed        = obs.get("wind_speed"),
        cloud_layers_json = obs.get("cloud_layers"),
        visibility_sm     = obs.get("visibility"),
        dewpoint_spread_f = dps,
        obs_hour_local    = local_hour,
        month             = month,
    )
    live_regime_name  = lr.regime
    live_regime_conf  = lr.confidence
    live_regime_notes = lr.notes

with get_connection() as conn:
    stats = get_stats(STATION, DEFAULT_MODEL, live_regime_name, conn)

# ---- Header: regime + model stats ----
col_r, col_b, col_s, col_n = st.columns(4)
col_r.metric("Current Regime", live_regime_name)
col_b.metric("Regime Bias", f"{stats['avg_bias']:+.2f}°F" if stats else "—")
col_s.metric("σ", f"{stats['std_dev']:.2f}°F" if stats else "—")
col_n.metric("n", stats["sample_size"] if stats else "—")

if not stats:
    st.warning("No model stats. Enter forecasts and settle ≥ 2 days.")
    st.stop()

if stats.get("regime_note"):
    st.caption(f"ℹ️ {stats['regime_note']}")

st.divider()
st.info(
    "**Settlement note:** Markets settle on whole-degree official highs. "
    "Probability cutoff is T + 0.5 — Yes >68 requires official high ≥ 69°F, "
    "No >68 requires ≤ 68°F."
)

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

default_fc = float(latest_fc_row["forecast_high"]) if latest_fc_row else 72.0
fc_note    = (
    f"on file: {latest_fc_row['forecast_date']} → {latest_fc_row['forecast_high']}°F"
    if latest_fc_row else "none on file"
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    today_fc = st.number_input(f"Ventusky Forecast (°F) [{fc_note}]",
                               40.0, 115.0, default_fc, 0.5)
with c2:
    threshold = st.number_input("Threshold T", 40.0, 115.0, 75.0, 1.0)
with c3:
    side = st.selectbox("Side", ["Yes", "No"],
                        help="Yes >T wins if official high ≥ T+1.  No >T wins if ≤ T.")
with c4:
    market_price = st.number_input("Market Price (¢)", 1.0, 99.0, 50.0, 1.0)

# Optional: market metadata
with st.expander("Market metadata (optional)"):
    mc1, mc2, mc3 = st.columns(3)
    mkt_ticker    = mc1.text_input("Ticker", placeholder="KXWEATHER-HIGHABOVE68-2026MAY17")
    best_bid      = mc2.number_input("Best Bid (¢)",  0.0, 99.0, 0.0, 1.0)
    best_ask      = mc3.number_input("Best Ask (¢)", 0.0, 99.0, 0.0, 1.0)
    mc4, mc5      = st.columns(2)
    volume        = mc4.number_input("Volume", 0, 1000000, 0, 100)
    open_interest = mc5.number_input("Open Interest", 0, 1000000, 0, 100)

if st.button("Calculate Edge", type="primary"):
    adjusted = today_fc + stats["avg_bias"]
    prob     = win_probability(adjusted, stats["std_dev"], threshold, side)
    fair     = prob * 100.0
    edge     = fair - market_price

    conf_score, conf_reasons = compute_confidence(
        sample_size  = stats["sample_size"],
        std_dev      = stats["std_dev"],
        regime       = live_regime_name,
        edge         = edge,
        regime_conf  = live_regime_conf,
    )

    # Recommendation logic
    if edge >= BET_EDGE_THRESHOLD and conf_score >= MIN_CONFIDENCE:
        rec, color = "BET ✅", "green"
    elif edge >= BET_EDGE_THRESHOLD and conf_score < MIN_CONFIDENCE:
        rec, color = "THIN CONFIDENCE — PASS", "orange"
    elif edge >= 0:
        rec, color = "THIN EDGE — PASS", "orange"
    else:
        rec, color = "FADE / LAY ❌", "red"

    # ---- Metrics ----
    st.divider()
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Adjusted Forecast", f"{adjusted:.1f}°F",
              delta=f"{stats['avg_bias']:+.2f}°F ({live_regime_name})")
    r2.metric("Fair Price", f"{fair:.1f}¢",
              delta=f"{edge:+.1f}¢ edge",
              delta_color="normal" if edge >= 0 else "inverse")
    r3.metric("P(Win)", f"{prob:.1%}")
    r4.metric("Confidence", f"{conf_score:.0%}")

    # ---- Recommendation box ----
    css = {
        "green":  "background:#d4edda;border-left:6px solid #28a745;",
        "orange": "background:#fff3cd;border-left:6px solid #ffc107;",
        "red":    "background:#f8d7da;border-left:6px solid #dc3545;",
    }[color]
    st.markdown(
        f"""<div style="{css} padding:16px 20px; border-radius:6px; margin-top:12px;">
            <strong style="font-size:1.3em;">{rec}</strong><br>
            <span style="color:#555;">
                {side} &gt;{int(threshold)} &nbsp;|&nbsp;
                Market {market_price:.1f}¢ &nbsp;|&nbsp;
                Fair {fair:.1f}¢ &nbsp;|&nbsp;
                Edge {edge:+.1f}¢ &nbsp;|&nbsp;
                Confidence {conf_score:.0%}
            </span><br>
            <small style="color:#888;">
                Regime: {live_regime_name} · adj {adjusted:.1f}°F ±{stats['std_dev']:.2f}°F · cutoff {threshold+0.5}°F · n={stats['sample_size']}
            </small>
        </div>""",
        unsafe_allow_html=True,
    )

    # ---- Explainability panel ----
    st.subheader("🔍 Explainability")

    exp1, exp2 = st.columns(2)

    with exp1:
        st.markdown("**Why the forecast was adjusted**")
        st.markdown(
            f"- Ventusky/HRRR forecast: **{today_fc}°F**\n"
            f"- Regime **{live_regime_name}** historical bias: **{stats['avg_bias']:+.2f}°F** "
            f"(n={stats['sample_size']})\n"
            f"- Adjusted forecast: **{adjusted:.1f}°F**\n"
            f"- 1σ spread: ±{stats['std_dev']:.2f}°F → 68% CI "
            f"[{adjusted - stats['std_dev']:.1f}, {adjusted + stats['std_dev']:.1f}]°F"
        )
        if stats.get("regime_note"):
            st.caption(f"⚠️ {stats['regime_note']}")

        st.markdown("**Why this regime matters**")
        for note in live_regime_notes:
            st.markdown(f"- {note}")

    with exp2:
        st.markdown("**Confidence breakdown**")
        for reason in conf_reasons:
            icon = "✅" if "high" in reason.lower() else ("⚠️" if "low" in reason.lower() else "•")
            st.markdown(f"{icon} {reason}")

        st.markdown("**What could invalidate this trade**")
        invalidators = []
        if live_regime_name == "OFFSHORE_FLOW":
            invalidators = [
                "Wind shifts onshore before afternoon — kills the heat",
                "Unexpected fog/stratus pushes in overnight",
                "Forecast verification shows HRRR corrected upward in 12Z run",
            ]
        elif live_regime_name in ("MARINE_STRONG", "LATE_BURNOFF"):
            invalidators = [
                "Marine layer burns off earlier than expected",
                "Offshore surge breaks through in the afternoon",
                "HRRR 12Z run shifts forecast higher — recalibrate bias",
            ]
        elif live_regime_name == "CLEAR_SKY":
            invalidators = [
                "Unexpected cloud development from desert thunderstorms",
                "Wind shift to onshore brings cooling",
                "Forecast updated significantly in later model run",
            ]
        else:
            invalidators = [
                "Regime classification changes with updated METAR",
                "Model run update shifts forecast materially",
                "Unexpected weather system intrudes",
            ]
        for inv in invalidators:
            st.markdown(f"- ⚠️ {inv}")

    # ---- Calculation breakdown ----
    with st.expander("Full calculation breakdown"):
        breakdown = {
            "Step": [
                "Ventusky forecast", "Regime", "Regime avg bias", "Adjusted forecast",
                "Std deviation", "Threshold T", "CDF cutoff (T+0.5)",
                "Side", "P(win)", "Fair price", "Market price", "Edge", "Confidence",
            ],
            "Value": [
                f"{today_fc}°F", live_regime_name,
                f"{stats['avg_bias']:+.2f}°F (n={stats['sample_size']})",
                f"{adjusted:.2f}°F", f"{stats['std_dev']:.2f}°F",
                f"{threshold}°F", f"{threshold+0.5}°F", side,
                f"{prob:.4f} ({prob:.1%})", f"{fair:.1f}¢",
                f"{market_price:.1f}¢", f"{edge:+.1f}¢", f"{conf_score:.3f} ({conf_score:.0%})",
            ],
        }
        st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)

    # ---- Persist snapshot ----
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    eff_bid = best_bid if best_bid > 0 else None
    eff_ask = best_ask if best_ask > 0 else None
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO market_snapshots
                (timestamp_utc, market_ticker, contract_name, threshold, side,
                 best_bid, best_ask, last_price, volume, open_interest,
                 fair_value, edge, confidence, regime)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            ts, mkt_ticker or None, f"{side} >{int(threshold)}", threshold, side,
            eff_bid, eff_ask, market_price,
            int(volume) if volume else None,
            int(open_interest) if open_interest else None,
            fair, edge, conf_score, live_regime_name,
        ))
        conn.commit()
    st.caption("Market snapshot saved.")
