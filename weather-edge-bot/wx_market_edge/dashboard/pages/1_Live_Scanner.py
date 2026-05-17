"""
Page 1 — Live Scanner

Shows the top current edges across all stations.
Auto-refreshes every 5 minutes via st.rerun().
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from database.db            import init_db
from models.edge_calculator import scan_all_markets, calculate_edge
from models.signal_ranker   import grade_all
from ingestion.kalshi       import get_latest_snapshots
from config import STATIONS, MIN_EDGE, MIN_CONFIDENCE

st.set_page_config(page_title="Live Scanner", page_icon="🔍", layout="wide")
st.title("🔍 Live Market Scanner")

conn = init_db()
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Auto-refresh toggle
col_refresh, col_date = st.columns([1, 2])
with col_refresh:
    auto = st.toggle("Auto-refresh (5 min)", value=False)
with col_date:
    scan_date = st.date_input("Scan date", value=datetime.now(timezone.utc).date())
    scan_date_str = scan_date.strftime("%Y-%m-%d")

st.divider()

# Pull snapshots
snapshots = get_latest_snapshots(conn, date=scan_date_str)

if not snapshots:
    st.info("No Kalshi market snapshots found for this date. Run the Kalshi refresh or add markets manually in the Edge Calculator.")
    st.stop()

# Calculate edge for each
results = []
for snap in snapshots:
    if not snap.get("station_code") or not snap.get("threshold_f"):
        continue
    r = calculate_edge(
        station_code  = snap["station_code"],
        forecast_date = snap.get("expiry_date") or scan_date_str,
        threshold_f   = snap["threshold_f"],
        side          = snap.get("side", "Yes"),
        market_price  = snap.get("market_price") or 50,
        best_bid      = snap.get("best_bid"),
        best_ask      = snap.get("best_ask"),
        conn          = conn,
    )
    r["market_ticker"] = snap.get("market_ticker", "")
    r["volume"]        = snap.get("volume")
    results.append(r)

if not results:
    st.warning("Could not compute edges — ensure forecasts are loaded for the scan date.")
    st.stop()

# Grade signals: A+, B, Watchlist, Avoid
results = grade_all(results, conn)

grade_icons = {"A+": "🏆", "B": "🟢", "Watchlist": "👀", "Avoid": "🔇"}

# ── Summary bar ──────────────────────────────────────────────────────────────
a_plus  = [r for r in results if r.get("grade") == "A+"]
b_grade = [r for r in results if r.get("grade") == "B"]
watch   = [r for r in results if r.get("grade") == "Watchlist"]
avoid   = [r for r in results if r.get("grade") == "Avoid"]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Markets", len(results))
c2.metric("🏆 A+ Signals",   len(a_plus))
c3.metric("🟢 B Signals",    len(b_grade))
c4.metric("👀 Watchlist",    len(watch))
c5.metric("🔇 Avoid",        len(avoid))

# Default tab: A+/B only
tab_main, tab_watch, tab_all = st.tabs(["A+ and B Signals", "Watchlist", "All Markets"])

with tab_main:
    active = a_plus + b_grade
    if active:
        for r in active:
            grade    = r.get("grade", "?")
            icon     = grade_icons.get(grade, "")
            station_name = STATIONS.get(r["station_code"], {}).get("name", r["station_code"])
            with st.expander(
                f"{icon} **{grade}** — {r['station_code']} ({station_name}) "
                f"{r['side']} >{r['threshold_f']:.0f}°F  |  "
                f"Edge: **{r['edge']:+.1f}¢**  |  "
                f"Conf: {r['confidence']:.0%}  |  "
                f"Regime: {r['regime']}"
            ):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Adjusted Forecast", f"{r.get('adjusted_forecast', '?'):.1f}°F",
                          delta=f"Bias {r.get('blended_bias', 0):+.2f}°F")
                c2.metric("Model Probability", f"{(r.get('model_prob') or 0)*100:.1f}%")
                c3.metric("Fair Value",         f"{r.get('fair_value', 0):.1f}¢")
                c4.metric("Market Price",       f"{r.get('market_price', '?'):.0f}¢")
                st.info(f"**Regime:** {r['regime']} (n={r.get('regime_n', 0)})  |  "
                        + "  ".join(r.get('regime_notes', [])[:2]))
                st.code(r.get("bias_note", ""))
                for gr in r.get("grade_reasons", []):
                    st.write(f"• {gr}")
                if r.get("quality_flags"):
                    st.warning("Quality flags: " + ", ".join(r["quality_flags"]))
    else:
        st.info("No A+ or B signals right now. Check back after next data refresh.")

with tab_watch:
    if watch:
        for r in watch:
            station_name = STATIONS.get(r["station_code"], {}).get("name", r["station_code"])
            st.write(f"👀 {r['station_code']} ({station_name}) — "
                     f"{r['side']} >{r['threshold_f']:.0f}°F | "
                     f"Edge: {r['edge']:+.1f}¢ | Conf: {r['confidence']:.0%} | "
                     + ", ".join(r.get("quality_flags", [])))
    else:
        st.info("No watchlist items.")

st.divider()

with tab_all:
    st.subheader("All Markets")
    table_rows = []
    for r in results:
        table_rows.append({
            "Grade":    r.get("grade", "—"),
            "Station":  r.get("station_code"),
            "Name":     STATIONS.get(r.get("station_code"), {}).get("name", ""),
            "Side":     r.get("side"),
            "Threshold":f">{r.get('threshold_f', '?'):.0f}°F",
            "Market ¢": r.get("market_price"),
            "Fair ¢":   f"{r.get('fair_value', 0):.1f}" if r.get("fair_value") else "—",
            "Edge ¢":   f"{r.get('edge', 0):+.1f}" if r.get("edge") is not None else "—",
            "Adj Fcst": f"{r.get('adjusted_forecast', 0):.1f}°F" if r.get("adjusted_forecast") else "—",
            "Regime":   r.get("regime", "UNKNOWN"),
            "Conf":     f"{r.get('confidence', 0):.0%}",
            "Flags":    ", ".join(r.get("quality_flags", [])),
        })

    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

if auto:
    import time
    time.sleep(300)
    st.rerun()
