import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from database.db import get_connection, init_db
from models.bias_engine import all_regime_stats
from config import STATION, DEFAULT_MODEL

init_db()
st.header("📚 Learning Dashboard")
st.caption("Tracks how the model has improved over time and which regimes drive the most value.")

with get_connection() as conn:
    regime_stats = all_regime_stats(STATION, DEFAULT_MODEL, conn)

    paired = pd.read_sql_query("""
        SELECT ds.settlement_date, COALESCE(ds.regime,'UNKNOWN') AS regime,
               fr.forecast_high, ds.official_high,
               ROUND(ds.official_high - fr.forecast_high, 2) AS error
        FROM daily_settlements ds
        JOIN forecast_runs fr ON fr.forecast_date = ds.settlement_date
            AND fr.station_code = ds.station_code AND fr.model_name = ?
        WHERE ds.station_code = ?
        ORDER BY ds.settlement_date ASC
    """, conn, params=(DEFAULT_MODEL, STATION))

    snapshots = pd.read_sql_query("""
        SELECT timestamp_utc, contract_name, side, last_price, fair_value, edge, confidence, regime
        FROM market_snapshots
        WHERE fair_value IS NOT NULL
        ORDER BY timestamp_utc ASC
    """, conn)

if paired.empty:
    st.info("No settled data yet. Enter forecasts and run settle_daily.py daily.")
    st.stop()

paired["settlement_date"] = pd.to_datetime(paired["settlement_date"])
paired = paired.sort_values("settlement_date")

# ---- Running bias convergence ----
st.subheader("Running Bias Convergence")
st.caption("Shows how the all-regime bias estimate evolves as more data is collected.")
paired["running_bias"] = paired["error"].expanding().mean()
paired["running_std"]  = paired["error"].expanding().std()
paired["upper"] = paired["running_bias"] + paired["running_std"]
paired["lower"] = paired["running_bias"] - paired["running_std"]
chart_df = paired.set_index("settlement_date")[["running_bias"]].rename(
    columns={"running_bias": "Running Bias (°F)"}
)
st.line_chart(chart_df)
st.caption(
    "Bias should converge and stabilize as n grows. "
    "If it's still drifting after 30+ days, check whether regime composition has shifted."
)

st.divider()

# ---- Absolute error over time (model accuracy improving?) ----
st.subheader("Absolute Forecast Error Over Time")
paired["abs_error"] = paired["error"].abs()
paired["rolling_mae"] = paired["abs_error"].rolling(7, min_periods=2).mean()
mae_df = paired.set_index("settlement_date")[["abs_error", "rolling_mae"]].rename(
    columns={"abs_error": "|Error| (°F)", "rolling_mae": "7-Day Avg |Error| (°F)"}
)
st.line_chart(mae_df)

st.divider()

# ---- Regime-level learning progress ----
st.subheader("Regime Learning Progress")
regime_progress = []
for s in regime_stats:
    if s["regime"] == "ALL":
        continue
    days_to_target = max(0, 30 - (s["sample_size"] or 0))
    regime_progress.append({
        "Regime":        s["regime"],
        "Days Settled":  s["sample_size"] or 0,
        "Days to n=30":  days_to_target,
        "Status":        "✅ Calibrated" if (s["sample_size"] or 0) >= 10 else "⏳ Building data",
        "Bias":          f"{s['avg_bias']:+.2f}°F" if s.get("avg_bias") is not None else "—",
        "σ":             f"{s['std_dev']:.2f}°F"   if s.get("std_dev")  is not None else "—",
    })

if regime_progress:
    rp_df = pd.DataFrame(
        sorted(regime_progress, key=lambda x: x["Days Settled"], reverse=True)
    )
    st.dataframe(rp_df, use_container_width=True, hide_index=True)
    least_data = min(regime_progress, key=lambda x: x["Days Settled"])
    st.caption(
        f"Least-sampled regime: **{least_data['Regime']}** "
        f"({least_data['Days Settled']} days). "
        "Focus on entering forecasts during these regimes to build the dataset fastest."
    )

st.divider()

# ---- Market snapshot P&L tracker ----
st.subheader("Market Snapshot Edge History")
if snapshots.empty:
    st.info("No market snapshots logged yet. Use the Live Markets page.")
else:
    snaps = snapshots.copy()
    snaps["timestamp_utc"] = pd.to_datetime(snaps["timestamp_utc"])
    snaps = snaps.sort_values("timestamp_utc")
    edge_by_regime = snaps.groupby("regime")["edge"].agg(
        Count="count", MeanEdge="mean", MaxEdge="max", MinEdge="min"
    ).round(2).reset_index()
    edge_by_regime.columns = ["Regime", "Snapshots", "Mean Edge (¢)", "Max Edge (¢)", "Min Edge (¢)"]
    st.dataframe(edge_by_regime, use_container_width=True, hide_index=True)
    st.caption("Edge is fair_value − market_price. Positive = market underpriced contract.")

st.divider()

# ---- What still needs building ----
st.subheader("⚙️ Pre-Production Checklist")
st.markdown("""
| Item | Status | Notes |
|------|--------|-------|
| METAR auto-ingestion | ✅ Ready | Run `ingest_metar.py --loop` |
| Manual forecast entry | ✅ Ready | Dashboard Page 1 |
| Regime classification | ✅ Ready | 7 regimes, KLAX-specific |
| Bias engine (regime-aware) | ✅ Ready | Falls back to ALL if n < 5 |
| Confidence engine | ✅ Ready | 4-factor weighted score |
| Settlement computation | ✅ Ready | METAR max or NWS override |
| Market edge calculator | ✅ Ready | T+0.5 cutoff, full breakdown |
| Ventusky API ingestion | ⏳ Manual | Phase 4: automate via scraper |
| Kalshi API market prices | ⏳ Manual | Phase 4: pull bid/ask automatically |
| Automated bet logging | ⏳ Planned | Phase 4: log actual bets taken |
| P&L tracking | ⏳ Planned | Phase 4: track actual vs expected edge |
| Multi-station support | ⏳ Planned | Phase 5: KBUR, KSNA, KONT |
| Alert on large edge | ⏳ Planned | Phase 4: push notification or email |
""")
