"""
Page 8 — Alerts

Configure and monitor Make.com webhook alerts.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent / ".env")
except ImportError:
    pass

import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from database.db import init_db
from alerts.webhook_alerts import (
    send_alert, is_configured, format_sms, build_payload,
    _alerts_enabled, _min_edge, _cooldown_minutes,
    confidence_label,
)

st.set_page_config(page_title="Alerts", page_icon="🔔", layout="wide")
st.title("🔔 Make.com Webhook Alerts")

conn = init_db()

# ── Configuration status ──────────────────────────────────────────────────────
st.subheader("Configuration")

webhook_url = os.environ.get("MAKE_ALERT_WEBHOOK_URL", "")
alerts_on   = _alerts_enabled()
min_edge    = _min_edge()
min_conf    = os.environ.get("MIN_ALERT_CONFIDENCE", "MEDIUM")
cooldown    = _cooldown_minutes()
dashboard_url = os.environ.get("DASHBOARD_URL", "http://localhost:8501")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Alerts Enabled",    "YES ✅" if alerts_on   else "NO ⛔")
c2.metric("Webhook Configured","YES ✅" if is_configured() else "NO ⛔")
c3.metric("Min Edge",          f"{min_edge:.0f}¢")
c4.metric("Cooldown",          f"{cooldown} min")

c5, c6 = st.columns(2)
c5.metric("Min Confidence", min_conf)
c6.metric("Dashboard URL",  dashboard_url)

if not is_configured():
    st.warning("""
**Webhook URL not set.**

1. Open `07_DATA_ANALYTICS/wx_market_edge/.env`
2. Add:  `MAKE_ALERT_WEBHOOK_URL=https://hook.eu1.make.com/your-hook-id`
3. Restart the dashboard or re-run `setup.sh`

The URL comes from your Make.com scenario → Custom Webhook trigger.
""")
elif not alerts_on:
    st.warning("Alerts are disabled. Set `ALERTS_ENABLED=true` in `.env` to enable.")
else:
    st.success("Alert system is active. Signals graded A+ or B with sufficient edge will trigger webhooks.")

st.divider()

# ── Test alert ────────────────────────────────────────────────────────────────
st.subheader("Send Test Alert")

col_test, col_preview = st.columns(2)

with col_test:
    st.write("Sends a synthetic A+ signal to your webhook so you can verify Make → Quo delivery end-to-end.")
    dry_run = st.checkbox("Dry run (show payload, do not POST)", value=not is_configured())

    if st.button("🚀 Send Test Alert", type="primary"):
        from scripts.test_make_alert import FAKE_SIGNAL  # noqa: PLC0415
        result = send_alert(FAKE_SIGNAL, conn, force=True, dry_run=dry_run)

        if dry_run:
            payload = build_payload(FAKE_SIGNAL, conn)
            st.success("Dry run complete — payload shown below")
            st.json(payload)
        elif result["sent"]:
            st.success(f"✅ Alert sent (HTTP {result.get('response_code')}) — check Make.com for the trigger")
            st.info(f"Alert logged as ID #{result.get('alert_id')}")
        else:
            st.error(f"Failed: {result['reason']}")

with col_preview:
    st.write("**Sample SMS text:**")
    sample_payload = {
        "grade": "A+", "station": "KLAX", "side": "YES",
        "threshold": 69, "market_price_cents": 31,
        "fair_value_cents": 56, "edge_cents": 25,
        "confidence": "HIGH", "regime": "MARINE_WEAK",
    }
    st.code(format_sms(sample_payload))

st.divider()

# ── Recent alerts ─────────────────────────────────────────────────────────────
st.subheader("Recent Alerts")

recent = conn.execute("""
    SELECT id, created_at, station_code, threshold_f, side, grade,
           edge_cents, confidence, regime, status, response_code, error_message
    FROM webhook_alerts
    ORDER BY created_at DESC
    LIMIT 50
""").fetchall()

if recent:
    r_df = pd.DataFrame([dict(r) for r in recent])
    r_df.columns = ["#", "Time", "Station", "Threshold", "Side", "Grade",
                    "Edge ¢", "Conf", "Regime", "Status", "HTTP", "Error"]

    def _row_color(row):
        if row["Status"] == "SENT":
            return ["background-color: #d4edda"] * len(row)
        if row["Status"] == "FAILED":
            return ["background-color: #f8d7da"] * len(row)
        return [""] * len(row)

    st.dataframe(r_df.style.apply(_row_color, axis=1), hide_index=True, use_container_width=True)

    # Counts
    sent      = sum(1 for r in recent if r["status"] == "SENT")
    failed    = sum(1 for r in recent if r["status"] == "FAILED")
    suppressed = sum(1 for r in recent if r["status"] == "SUPPRESSED")
    st.caption(f"Last 50: {sent} sent  ·  {failed} failed  ·  {suppressed} suppressed by cooldown")
else:
    st.info("No alerts yet. Run `python scripts/test_make_alert.py` to send your first test.")

st.divider()

# ── Failed alerts ─────────────────────────────────────────────────────────────
st.subheader("Failed Alerts")
failed_rows = conn.execute("""
    SELECT id, created_at, station_code, threshold_f, side, error_message, response_code
    FROM webhook_alerts WHERE status='FAILED'
    ORDER BY created_at DESC LIMIT 20
""").fetchall()

if failed_rows:
    f_df = pd.DataFrame([dict(r) for r in failed_rows])
    st.dataframe(f_df, hide_index=True, use_container_width=True)
    st.warning(f"{len(failed_rows)} failed alerts. Check that MAKE_ALERT_WEBHOOK_URL is correct and reachable.")
else:
    st.success("No failed alerts.")

st.divider()

# ── Payload schema reference ──────────────────────────────────────────────────
with st.expander("📋 Webhook Payload Schema Reference"):
    st.code("""{
  "alert_type":              "WEATHER_SIGNAL",
  "grade":                   "A+",
  "station":                 "KLAX",
  "station_name":            "Los Angeles",
  "market_ticker":           "KLAX-HIGH-69",
  "side":                    "YES",
  "threshold":               69,
  "market_price_cents":      31,
  "fair_value_cents":        56,
  "edge_cents":              25,
  "confidence":              "HIGH",
  "confidence_score":        0.78,
  "regime":                  "MARINE_WEAK",
  "adjusted_forecast_f":     70.4,
  "openmeteo_forecast_f":    68.2,
  "official_current_temp_f": 67.1,
  "wind":                    "250° @ 8 kts",
  "reason":                  "Onshore flow + marine layer — model historically too cold.",
  "action":                  "MANUAL REVIEW / PAPER TRADE",
  "timestamp_utc":           "2026-05-17T14:30:00Z",
  "dashboard_url":           "http://localhost:8501",
  "sms_text":                "A+ WEATHER SIGNAL\\nKLAX YES >69\\n..."
}""", language="json")

with st.expander("📖 Make.com + Quo Setup Guide"):
    try:
        guide = (Path(__file__).parent.parent.parent / "docs" / "MAKE_QUO_ALERT_SETUP.md").read_text()
        st.markdown(guide)
    except FileNotFoundError:
        st.info("See docs/MAKE_QUO_ALERT_SETUP.md")
