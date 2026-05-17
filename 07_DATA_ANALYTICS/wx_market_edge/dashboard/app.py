"""
Weather Market Edge Tracker — Streamlit entry point.

Run:  streamlit run dashboard/app.py --server.port 8501
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from database.db import init_db

st.set_page_config(
    page_title="Weather Market Edge Tracker",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure DB + tables exist on every cold start
conn = init_db()

# Seed stations if empty
count = conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
if count == 0:
    from database.db import seed_stations
    seed_stations(conn)

st.title("⛅ Weather Market Edge Tracker")
st.markdown("""
### Multi-Station Weather Prediction Market Edge System

Navigate using the sidebar pages to:

| Page | Purpose |
|---|---|
| 1 Live Scanner | Top edges across all stations right now |
| 2 Station Detail | Deep-dive on one station: forecast, METAR, regime |
| 3 Edge Calculator | Manual contract entry + instant edge calculation |
| 4 Regime Learning | Bias breakdown by regime across all stations |
| 5 Paper Trading Lab | Open + closed simulated trades, daily P&L |
| 6 Backtesting | Historical replay with no-lookahead bias |
| 7 Data Health | Feed freshness, failure alerts, last update times |

---
""")

col1, col2, col3 = st.columns(3)

total_obs = conn.execute("SELECT COUNT(*) FROM official_observations").fetchone()[0]
total_fc  = conn.execute("SELECT COUNT(*) FROM forecast_runs").fetchone()[0]
total_pt  = conn.execute("SELECT COUNT(*) FROM paper_trades WHERE status='OPEN'").fetchone()[0]

col1.metric("METAR Observations", total_obs)
col2.metric("Forecast Rows", total_fc)
col3.metric("Open Paper Trades", total_pt)

st.caption("Data updates automatically via `python scripts/scheduler.py --once` or the background loop.")
