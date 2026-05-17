"""
Page 2 — Station Detail

Deep dive on one station: live METAR, current forecast, regime, probability table.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from database.db          import init_db
from ingestion.open_meteo import get_latest_forecast, get_hourly_for_date
from ingestion.metar      import get_latest_obs
from models.edge_calculator import calculate_edge, win_probability
from models.regime_engine import classify_from_metar, classify_from_forecast
from models.bias_engine   import blended_bias, all_regime_stats
from config import STATIONS, DEFAULT_MODEL

st.set_page_config(page_title="Station Detail", page_icon="📡", layout="wide")
st.title("📡 Station Detail")

conn = init_db()
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Station selector
station = st.selectbox(
    "Station",
    options=list(STATIONS.keys()),
    format_func=lambda k: f"{k} — {STATIONS[k]['name']}",
)
s_info = STATIONS[station]
st.caption(f"Lat {s_info['lat']}  Lon {s_info['lon']}  UTC{s_info['utc_offset']:+d}  ({s_info['tz']})")

forecast_date = st.date_input("Forecast date", value=datetime.now(timezone.utc).date())
fc_date_str   = forecast_date.strftime("%Y-%m-%d")

st.divider()

# ── Live METAR ────────────────────────────────────────────────────────────────
st.subheader("Live METAR")
obs = get_latest_obs(station, conn)
if obs:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature",  f"{obs.get('observed_temp', '?'):.1f}°F" if obs.get('observed_temp') else "—")
    c2.metric("Dewpoint",     f"{obs.get('dewpoint', '?'):.1f}°F"      if obs.get('dewpoint')      else "—")
    c3.metric("Wind",
              f"{obs.get('wind_direction', '?'):.0f}°@{obs.get('wind_speed', '?'):.0f}kts"
              if obs.get("wind_speed") else "Calm")
    c4.metric("Visibility",   f"{obs.get('visibility_sm', '?'):.0f} SM" if obs.get("visibility_sm") else "—")

    c5, c6, c7 = st.columns(3)
    c5.metric("Pressure",     f"{obs.get('pressure_inHg', '?'):.2f} inHg" if obs.get("pressure_inHg") else "—")
    c6.metric("Gusts",        f"{obs.get('gust_speed'):.0f} kts" if obs.get("gust_speed") else "None")
    c7.metric("Observation",  obs.get("timestamp_utc", "—")[:16] + "Z")

    import json
    clouds = obs.get("cloud_layers") or "[]"
    try:
        cloud_list = json.loads(clouds)
        if cloud_list:
            st.caption("Cloud layers: " + ", ".join(
                f"{l['cover']} {l['base']:,}ft" for l in cloud_list
            ))
    except Exception:
        pass

    st.code(obs.get("raw_metar", ""), language=None)

    # Current regime
    utc_off = s_info["utc_offset"]
    try:
        ts = datetime.strptime(obs["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
        local_hour = (ts.hour + utc_off) % 24
    except Exception:
        local_hour = 12
    regime_r = classify_from_metar(obs, local_hour)
    st.info(f"**Regime:** {regime_r.regime} (confidence {regime_r.confidence:.0%})  \n"
            + "  \n".join(f"• {n}" for n in regime_r.notes))
else:
    st.warning("No METAR observations found. Run `python scripts/scheduler.py --once`")
    regime_r = None

st.divider()

# ── Open-Meteo Forecast ───────────────────────────────────────────────────────
st.subheader("Open-Meteo Forecast")
fr = get_latest_forecast(station, fc_date_str, conn)
if fr:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Forecast High", f"{fr['temp_max']:.1f}°F" if fr.get("temp_max") else "—")
    c2.metric("Forecast Low",  f"{fr['temp_min']:.1f}°F" if fr.get("temp_min") else "—")
    c3.metric("Wind",          f"{fr.get('wind_direction_dominant', '?'):.0f}°@{fr.get('wind_speed_mean', '?'):.0f}mph"
              if fr.get("wind_speed_mean") else "—")
    c4.metric("Cloud Cover",   f"{fr.get('cloud_cover_mean', '?'):.0f}%" if fr.get("cloud_cover_mean") is not None else "—")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Humidity",      f"{fr.get('humidity_mean', '?'):.0f}%" if fr.get("humidity_mean") is not None else "—")
    c6.metric("Dewpoint Mean", f"{fr.get('dew_point_mean', '?'):.1f}°F" if fr.get("dew_point_mean") else "—")
    c7.metric("Precip Prob",   f"{fr.get('precip_prob_mean', '?'):.0f}%" if fr.get("precip_prob_mean") is not None else "—")
    c8.metric("Precip Sum",    f"{fr.get('precip_sum', 0) or 0:.2f}\"")

    if not regime_r:
        regime_r = classify_from_forecast(fr)
        st.info(f"**Forecast Regime:** {regime_r.regime} (confidence {regime_r.confidence:.0%})")

    # Bias
    bias, std, bias_note = blended_bias(station, DEFAULT_MODEL, regime_r.regime, conn)
    adj = round(fr["temp_max"] + bias, 2) if fr.get("temp_max") else None
    st.success(f"Adjusted forecast: **{adj:.1f}°F**  ({bias_note})" if adj else "")

    st.divider()

    # ── Probability table ─────────────────────────────────────────────────────
    if fr.get("temp_max") and adj:
        st.subheader("Probability Table")
        base = int(fr["temp_max"])
        rows = []
        for offset in range(-4, 5):
            thresh = base + offset
            p_yes = win_probability(adj, std, thresh, "Yes")
            p_no  = win_probability(adj, std, thresh, "No")
            rows.append({
                "Threshold": f">{thresh}°F",
                "Yes P(win)": f"{p_yes*100:.1f}%",
                "No P(win)":  f"{p_no*100:.1f}%",
                "Yes Fair ¢": f"{p_yes*100:.1f}",
                "No Fair ¢":  f"{p_no*100:.1f}",
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    # ── Hourly chart ──────────────────────────────────────────────────────────
    hourly = get_hourly_for_date(station, fc_date_str, conn)
    if hourly:
        st.subheader("Hourly Temperature Forecast")
        h_df = pd.DataFrame(hourly)[["hour_local", "temperature_2m", "cloud_cover", "wind_speed"]].dropna(subset=["temperature_2m"])
        h_df.columns = ["Hour (local)", "Temp °F", "Cloud %", "Wind mph"]
        st.line_chart(h_df.set_index("Hour (local)")[["Temp °F"]])
        st.dataframe(h_df, hide_index=True, use_container_width=True)
else:
    st.warning(f"No forecast for {station}/{fc_date_str}. Run `python scripts/scheduler.py --once`")

st.divider()

# ── Historical bias by regime ────────────────────────────────────────────────
st.subheader("Historical Bias by Regime")
stats = all_regime_stats(station, DEFAULT_MODEL, conn)
if stats:
    df = pd.DataFrame(stats)[["regime", "avg_bias", "std_dev", "sample_size",
                               "rolling_7d_bias", "rolling_30d_bias"]]
    df.columns = ["Regime", "Avg Bias °F", "Std Dev", "n", "7d Bias", "30d Bias"]
    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.info("No model stats yet — need at least 2 settled days with matching forecasts.")
