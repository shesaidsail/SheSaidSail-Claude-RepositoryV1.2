"""
KLAX Weather Market Edge Tracker — Phase 3
Run from the klax_phase3/ directory:
    streamlit run dashboard/app.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from database.db import init_db

init_db()

st.set_page_config(page_title="KLAX Edge Tracker", page_icon="🌡️", layout="wide")
st.title("🌡️ KLAX Weather Market Edge Tracker — Phase 3")
st.markdown("""
| Page | Purpose |
|---|---|
| **1 Current Forecast** | Enter Ventusky forecast with regime metadata and screenshots |
| **2 Historical Error** | Forecast vs actual, error by regime |
| **3 Live Markets** | Full edge calculation with explainability |
| **4 Regime Dashboard** | Regime distribution and per-regime bias |
| **5 Confidence Dashboard** | Confidence score breakdown and calibration |
| **6 Learning Dashboard** | Settlement history and profitability by regime |
""")
st.info(
    "**Daily workflow:**  \n"
    "1. Enter Ventusky forecast → **Current Forecast** page  \n"
    "2. Run `python scripts/ingest_metar.py --loop` in a terminal (hourly METAR auto-poll)  \n"
    "3. After midnight local: `python scripts/settle_daily.py` — settles, classifies regime, retrains"
)
