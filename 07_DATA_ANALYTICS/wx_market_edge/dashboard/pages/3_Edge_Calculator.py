"""
Page 3 — Manual Edge Calculator

Enter any contract manually and get instant edge + explainability.
Optionally open a paper trade.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from datetime import datetime, timezone

from database.db          import init_db
from models.edge_calculator import calculate_edge
from trading.paper_trader import open_trade
from ingestion.kalshi     import add_manual_market
from config import STATIONS, DEFAULT_MODEL

st.set_page_config(page_title="Edge Calculator", page_icon="🧮", layout="wide")
st.title("🧮 Manual Edge Calculator")

conn = init_db()

with st.form("edge_form"):
    st.subheader("Contract Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        station = st.selectbox(
            "Station",
            options=list(STATIONS.keys()),
            format_func=lambda k: f"{k} — {STATIONS[k]['name']}",
        )
        forecast_date = st.date_input("Settlement Date",
                                      value=datetime.now(timezone.utc).date())

    with col2:
        threshold = st.number_input("Threshold °F (contract strike)", value=72.0, step=1.0)
        side      = st.radio("Side", ["Yes", "No"], horizontal=True)

    with col3:
        market_price = st.number_input("Market Price (¢)", min_value=1.0, max_value=99.0,
                                       value=50.0, step=0.5)
        best_bid     = st.number_input("Best Bid (¢)", min_value=0.0, max_value=99.0,
                                       value=49.0, step=0.5)
        best_ask     = st.number_input("Best Ask (¢)", min_value=0.0, max_value=99.0,
                                       value=51.0, step=0.5)

    ticker_input = st.text_input("Kalshi Ticker (optional)", placeholder="HIGLA-25MAY17-B72")
    submitted = st.form_submit_button("Calculate Edge", type="primary")

if submitted:
    fc_date_str = forecast_date.strftime("%Y-%m-%d")
    r = calculate_edge(
        station_code  = station,
        forecast_date = fc_date_str,
        threshold_f   = threshold,
        side          = side,
        market_price  = market_price,
        best_bid      = best_bid if best_bid > 0 else None,
        best_ask      = best_ask if best_ask > 0 else None,
        conn          = conn,
    )

    if r.get("error"):
        st.error(r["error"])
        st.stop()

    # ── Result display ────────────────────────────────────────────────────────
    signal = r["signal"]
    signal_color = {"BET": "success", "FADE": "error", "PASS": "info"}[signal]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fair Value",   f"{r['fair_value']:.1f}¢")
    col2.metric("Edge",         f"{r['edge']:+.1f}¢",
                delta_color="normal" if r['edge'] >= 0 else "inverse")
    col3.metric("Model Prob",   f"{r['model_prob']*100:.1f}%")
    col4.metric("Confidence",   f"{r['confidence']:.0%}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Adj Forecast", f"{r['adjusted_forecast']:.1f}°F",
                delta=f"Bias {r['blended_bias']:+.2f}°F")
    col6.metric("OM High",      f"{r['forecast_high']:.1f}°F" if r.get('forecast_high') else "—")
    col7.metric("Regime",       r["regime"])
    col8.metric("Spread",       f"{r['spread']:.1f}¢" if r.get('spread') else "—")

    if signal == "BET":
        st.success(f"## SIGNAL: {signal} — Edge of {r['edge']:+.1f}¢ exceeds threshold")
    elif signal == "FADE":
        st.error(f"## SIGNAL: {signal} — Reverse trade, edge of {r['edge']:+.1f}¢")
    else:
        st.info(f"## SIGNAL: PASS — Edge {r['edge']:+.1f}¢ or confidence {r['confidence']:.0%} too low")

    st.divider()

    # Full explanation
    st.subheader("Full Explanation")
    st.code(r["explanation"])

    # Regime notes
    if r.get("regime_notes"):
        st.subheader("Regime Analysis")
        for note in r["regime_notes"]:
            st.write(f"• {note}")

    # Confidence breakdown
    if r.get("confidence_reasons"):
        st.subheader("Confidence Breakdown")
        for line in r["confidence_reasons"]:
            st.write(f"• {line}")

    # Bias note
    st.subheader("Bias Engine")
    st.info(r.get("bias_note", "No bias data available"))

    st.divider()

    # ── Paper trade button ────────────────────────────────────────────────────
    if signal in ("BET", "FADE"):
        st.subheader("Paper Trading")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"📝 Open Paper Trade ({signal})", type="primary"):
                r["market_ticker"] = ticker_input or f"MANUAL-{station}-{fc_date_str}"
                trade_id = open_trade(r, conn)
                if trade_id:
                    st.success(f"Paper trade #{trade_id} opened. View in Paper Trading Lab.")
                    if ticker_input:
                        add_manual_market(
                            ticker       = ticker_input,
                            title        = f"{station} Daily High >{threshold:.0f}°F",
                            station_code = station,
                            threshold_f  = threshold,
                            side         = side,
                            market_price = market_price,
                            best_bid     = best_bid,
                            best_ask     = best_ask,
                            expiry_date  = fc_date_str,
                            conn         = conn,
                        )
                else:
                    st.warning("Trade not opened — check filter thresholds in config.py")
