"""
KLAX Weather Market Edge Tracker — Phase 2 Dashboard
Run from the klax_phase2/ directory:
    streamlit run dashboard/app.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from database.db import init_db

init_db()

st.set_page_config(
    page_title="KLAX Edge Tracker",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ KLAX Weather Market Edge Tracker — Phase 2")
st.markdown("""
Use the sidebar to navigate between pages.

| Page | Purpose |
|---|---|
| **1 Current Forecast** | Enter today's Ventusky forecast; see adjusted prediction and confidence intervals |
| **2 Historical Error** | Chart model bias and variance over time |
| **3 Market Analyzer** | Calculate fair price, edge, and bet recommendation for any contract |
""")

st.info(
    "**Daily workflow (3 steps):**  \n"
    "1. Enter today's Ventusky HRRR forecast on the **Current Forecast** page.  \n"
    "2. Each hour (or via cron): `python scripts/ingest_metar.py`  \n"
    "3. After midnight local: `python scripts/settle_daily.py` — computes official high "
    "and automatically retrains the model."
)
