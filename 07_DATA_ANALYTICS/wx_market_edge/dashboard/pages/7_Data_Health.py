"""
Page 7 — Data Health

Shows feed freshness, failure counts, and stale-data warnings.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

from database.db   import init_db
from ingestion.kalshi import search_weather_markets, parse_market
from config import STATIONS, FORECAST_INTERVAL, METAR_INTERVAL, KALSHI_INTERVAL

st.set_page_config(page_title="Data Health", page_icon="🔧", layout="wide")
st.title("🔧 Data Health Monitor")

conn = init_db()

now_utc = datetime.now(timezone.utc)


def _age(ts_str: str | None) -> str:
    if not ts_str:
        return "never"
    try:
        ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        delta = now_utc - ts
        mins  = int(delta.total_seconds() / 60)
        if mins < 60:
            return f"{mins}m ago"
        return f"{mins//60}h {mins%60}m ago"
    except Exception:
        return ts_str


def _stale(ts_str: str | None, threshold_s: int) -> bool:
    if not ts_str:
        return True
    try:
        ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return (now_utc - ts).total_seconds() > threshold_s
    except Exception:
        return True


# ── Feed Health ───────────────────────────────────────────────────────────────
st.subheader("Feed Status")

feeds = conn.execute("SELECT * FROM data_health ORDER BY feed, station_code").fetchall()
feed_rows = [dict(r) for r in feeds] if feeds else []

# Per-station METAR freshness
metar_rows = []
for icao in STATIONS:
    latest = conn.execute("""
        SELECT MAX(timestamp_utc) AS ts FROM official_observations WHERE station_code=?
    """, (icao,)).fetchone()
    ts = latest["ts"] if latest else None
    stale = _stale(ts, METAR_INTERVAL * 3)
    metar_rows.append({
        "Station": icao,
        "Name":    STATIONS[icao]["name"],
        "Latest METAR": _age(ts),
        "Raw TS":       ts or "—",
        "Status":       "⚠️ STALE" if stale else "✅ OK",
    })

st.subheader("METAR Feed (per station)")
m_df = pd.DataFrame(metar_rows)
st.dataframe(m_df[["Station", "Name", "Latest METAR", "Status"]], hide_index=True, use_container_width=True)

# Per-station forecast freshness
fc_rows = []
today = now_utc.strftime("%Y-%m-%d")
for icao in STATIONS:
    latest = conn.execute("""
        SELECT MAX(fetched_at) AS ts FROM forecast_runs
        WHERE station_code=? AND forecast_date=?
    """, (icao, today)).fetchone()
    ts = latest["ts"] if latest else None
    stale = _stale(ts, FORECAST_INTERVAL * 3)
    fc_rows.append({
        "Station": icao,
        "Name":    STATIONS[icao]["name"],
        "Latest Forecast": _age(ts),
        "Status":  "⚠️ STALE" if stale else ("⏳ No today FC" if ts is None else "✅ OK"),
    })

st.subheader("Open-Meteo Forecast Feed")
fc_df = pd.DataFrame(fc_rows)
st.dataframe(fc_df[["Station", "Name", "Latest Forecast", "Status"]], hide_index=True, use_container_width=True)

# Kalshi feed
kalshi_snap = conn.execute("SELECT MAX(captured_at) AS ts FROM market_snapshots").fetchone()
k_ts = kalshi_snap["ts"] if kalshi_snap else None
k_stale = _stale(k_ts, KALSHI_INTERVAL * 10)

st.subheader("Kalshi Feed")
k_col1, k_col2 = st.columns(2)
k_col1.metric("Last Kalshi Update", _age(k_ts))
k_col2.metric("Status", "⚠️ STALE" if k_stale else "✅ OK")

snap_count = conn.execute("SELECT COUNT(*) FROM market_snapshots").fetchone()[0]
st.caption(f"Total market snapshots stored: {snap_count}")

st.divider()

# ── DB Statistics ─────────────────────────────────────────────────────────────
st.subheader("Database Statistics")

tables = [
    ("stations", "active weather stations"),
    ("forecast_runs", "daily forecast rows"),
    ("hourly_forecasts", "hourly forecast rows"),
    ("official_observations", "METAR observations"),
    ("daily_settlements", "settled days"),
    ("market_snapshots", "Kalshi market snapshots"),
    ("model_stats", "model bias rows"),
    ("paper_trades", "paper trades"),
    ("backtest_runs", "backtest runs"),
    ("alerts", "system alerts"),
]

db_rows = []
for table, desc in tables:
    try:
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    except Exception:
        n = "error"
    db_rows.append({"Table": table, "Rows": n, "Description": desc})

st.dataframe(pd.DataFrame(db_rows), hide_index=True, use_container_width=True)

st.divider()

# ── Alerts ────────────────────────────────────────────────────────────────────
st.subheader("Recent Alerts")
alerts = conn.execute("""
    SELECT * FROM alerts ORDER BY created_at DESC LIMIT 50
""").fetchall()
if alerts:
    a_df = pd.DataFrame([dict(r) for r in alerts])[
        ["created_at", "station_code", "alert_type", "message", "acknowledged"]
    ]
    a_df.columns = ["Time", "Station", "Type", "Message", "ACK"]
    st.dataframe(a_df, hide_index=True, use_container_width=True)

    if st.button("Acknowledge All Alerts"):
        conn.execute("UPDATE alerts SET acknowledged=1")
        conn.commit()
        st.success("All alerts acknowledged.")
        st.rerun()
else:
    st.info("No alerts.")

st.divider()

# ── Live Kalshi market browser ────────────────────────────────────────────────
st.subheader("Live Kalshi Weather Market Browser")
if st.button("🔄 Refresh from Kalshi API"):
    with st.spinner("Querying Kalshi API..."):
        markets = search_weather_markets(limit=100)
    if markets:
        parsed = [parse_market(m) for m in markets]
        df = pd.DataFrame(parsed)
        available_cols = [c for c in ["ticker", "title", "station_code", "threshold_f",
                                       "best_bid", "best_ask", "last_price", "volume",
                                       "expiry_date"] if c in df.columns]
        st.dataframe(df[available_cols], hide_index=True, use_container_width=True)
        st.caption(f"Fetched {len(markets)} weather markets from Kalshi")
    else:
        st.warning("No weather markets returned from Kalshi. Check your API key in .env")

st.divider()

# ── Quick refresh buttons ─────────────────────────────────────────────────────
st.subheader("Manual Refresh")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌤 Refresh Forecasts"):
        from ingestion.open_meteo import refresh_all as rf_fc
        with st.spinner("Fetching forecasts..."):
            r = rf_fc(conn, verbose=True)
        st.success(f"Refreshed {sum(r.values())} forecast rows across {len(r)} stations")
        st.rerun()

with col2:
    if st.button("📡 Refresh METAR"):
        from ingestion.metar import refresh_all as rf_metar
        with st.spinner("Fetching METAR..."):
            r = rf_metar(conn, verbose=True)
        new = sum(r.values())
        st.success(f"METAR refreshed: {new} new observations")
        st.rerun()

with col3:
    if st.button("💹 Refresh Kalshi"):
        from ingestion.kalshi import refresh_all as rf_k
        with st.spinner("Querying Kalshi..."):
            n = rf_k(conn, verbose=True)
        st.success(f"Stored {n} Kalshi market snapshots")
        st.rerun()
