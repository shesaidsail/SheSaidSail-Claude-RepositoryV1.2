import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd

from database.db import get_connection, init_db
from models.bias_engine import all_regime_stats
from models.confidence_engine import compute_confidence
from config import STATION, DEFAULT_MODEL, MIN_CONFIDENCE

init_db()
st.header("🎯 Confidence Dashboard")

with get_connection() as conn:
    regime_stats = all_regime_stats(STATION, DEFAULT_MODEL, conn)

    snapshots = pd.read_sql_query("""
        SELECT timestamp_utc, contract_name, side, last_price, fair_value, edge, confidence, regime
        FROM market_snapshots
        ORDER BY timestamp_utc DESC
        LIMIT 100
    """, conn)

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

if not regime_stats:
    st.info("No model stats yet. Enter forecasts and settle ≥ 2 days to calibrate.")
    st.stop()

# ---- Confidence by regime ----
st.subheader("Model Confidence by Regime")
conf_rows = []
for s in regime_stats:
    score, reasons = compute_confidence(
        sample_size = s["sample_size"] or 0,
        std_dev     = s["std_dev"],
        regime      = s["regime"],
        edge        = 0.0,
        regime_conf = s.get("confidence") or 0.5,
    )
    conf_rows.append({
        "Regime":     s["regime"],
        "n":          s["sample_size"],
        "Bias (°F)":  f"{s['avg_bias']:+.2f}" if s.get("avg_bias") is not None else "—",
        "Std Dev":    f"{s['std_dev']:.2f}" if s.get("std_dev") is not None else "—",
        "Confidence": f"{score:.0%}",
        "Verdict":    "BET OK" if score >= MIN_CONFIDENCE else "NEEDS MORE DATA",
        "Top reason": reasons[-1] if reasons else "",
    })

conf_df = pd.DataFrame(sorted(conf_rows, key=lambda x: x["Regime"]))
st.dataframe(conf_df, use_container_width=True, hide_index=True)
st.caption(
    f"Bet threshold: confidence ≥ {MIN_CONFIDENCE:.0%}.  "
    "Confidence grows as sample size increases and variance decreases."
)

st.divider()

# ---- Confidence factors for 'ALL' ----
global_s = next((s for s in regime_stats if s["regime"] == "ALL"), None)
if global_s:
    st.subheader("Global Model — Confidence Breakdown")
    score, reasons = compute_confidence(
        sample_size = global_s["sample_size"],
        std_dev     = global_s["std_dev"],
        regime      = "ALL",
        edge        = 0.0,
        regime_conf = global_s.get("confidence") or 0.5,
    )
    st.metric("Overall Confidence", f"{score:.0%}")
    for r in reasons:
        icon = "✅" if any(w in r.lower() for w in ("high", "large", "strong", "low variance")) \
               else ("⚠️" if any(w in r.lower() for w in ("low", "thin", "high variance", "minimal")) \
               else "•")
        st.markdown(f"{icon} {r}")

st.divider()

# ---- Market snapshot history ----
st.subheader("Recent Market Snapshots")
if snapshots.empty:
    st.info("No market snapshots yet. Use the Live Markets page to calculate edge.")
else:
    snaps = snapshots.copy()
    snaps["edge_str"] = snaps["edge"].apply(lambda x: f"{x:+.1f}¢" if x is not None else "—")
    snaps["conf_str"] = snaps["confidence"].apply(lambda x: f"{x:.0%}" if x is not None else "—")
    snaps["fair_str"] = snaps["fair_value"].apply(lambda x: f"{x:.1f}¢" if x is not None else "—")
    display = snaps[["timestamp_utc","contract_name","last_price","fair_str","edge_str","conf_str","regime"]]
    display.columns = ["Time","Contract","Market (¢)","Fair (¢)","Edge","Confidence","Regime"]
    st.dataframe(display, use_container_width=True, hide_index=True)

# ---- Calibration note ----
st.divider()
st.subheader("📘 How to Read This Page")
st.markdown("""
**Confidence score components:**

| Weight | Factor | What it measures |
|--------|--------|-----------------|
| 30% | Sample size | Do we have enough historical data? Saturates at n=30 |
| 30% | Variance (σ) | Is the model's spread tight? σ < 1.5°F is excellent |
| 25% | Regime clarity | How clearly was today's regime classified? |
| 15% | Edge magnitude | Is the mispricing large enough to be real? |

**Interpretation:**
- **≥ 70%** — High confidence: full recommended size
- **55–69%** — Medium: half size, or wait for more data
- **< 55%** — Low: do not bet; accumulate more observations
""")
