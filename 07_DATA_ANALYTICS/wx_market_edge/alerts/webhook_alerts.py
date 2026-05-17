"""
Make.com webhook alert service.

Sends structured JSON payloads to a Make.com Custom Webhook trigger.
Make handles all downstream delivery (Quo, SMS, Slack, email, etc.).

Design principles:
- Never crash the trading engine on alert failure
- Log every attempt and response
- Enforce cooldown to prevent duplicate alerts
- .env is the only source of secrets — never hardcode
"""

import os
import sys
import json
import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

import requests

log = logging.getLogger("webhook_alerts")

# ---------------------------------------------------------------------------
# Environment config
# ---------------------------------------------------------------------------

CONFIDENCE_LEVELS = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "VERY_HIGH": 4}


def _webhook_url() -> str:
    return os.environ.get("MAKE_ALERT_WEBHOOK_URL", "")


def _alerts_enabled() -> bool:
    return os.environ.get("ALERTS_ENABLED", "true").lower() == "true"


def _min_edge() -> float:
    try:
        return float(os.environ.get("MIN_ALERT_EDGE_CENTS", "10"))
    except ValueError:
        return 10.0


def _min_confidence_rank() -> int:
    level = os.environ.get("MIN_ALERT_CONFIDENCE", "MEDIUM").upper()
    return CONFIDENCE_LEVELS.get(level, 2)


def _cooldown_minutes() -> int:
    try:
        return int(os.environ.get("ALERT_COOLDOWN_MINUTES", "30"))
    except ValueError:
        return 30


def _dashboard_url() -> str:
    return os.environ.get("DASHBOARD_URL", "http://localhost:8501")


def is_configured() -> bool:
    return bool(_webhook_url())


# ---------------------------------------------------------------------------
# Confidence label helpers
# ---------------------------------------------------------------------------

def confidence_label(score: float) -> str:
    """Convert 0-1 float to human label."""
    if score >= 0.80:
        return "VERY_HIGH"
    if score >= 0.65:
        return "HIGH"
    if score >= 0.50:
        return "MEDIUM"
    return "LOW"


def _confidence_rank(score: float) -> int:
    return CONFIDENCE_LEVELS.get(confidence_label(score), 1)


# ---------------------------------------------------------------------------
# Cooldown check
# ---------------------------------------------------------------------------

def _in_cooldown(
    station: str, threshold_f: float, side: str, conn: sqlite3.Connection
) -> bool:
    """Return True if an alert was sent within the cooldown window."""
    cutoff = (
        datetime.now(timezone.utc) - timedelta(minutes=_cooldown_minutes())
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    row = conn.execute("""
        SELECT id FROM webhook_alerts
        WHERE station_code=? AND threshold_f=? AND side=?
          AND status='SENT'
          AND created_at >= ?
        LIMIT 1
    """, (station, threshold_f, side, cutoff)).fetchone()
    return row is not None


# ---------------------------------------------------------------------------
# SMS text formatter
# ---------------------------------------------------------------------------

def format_sms(payload: dict) -> str:
    """Build a short SMS-friendly message (≤160 chars per segment)."""
    grade      = payload.get("grade", "?")
    station    = payload.get("station", "?")
    side       = payload.get("side", "?").upper()
    threshold  = payload.get("threshold", "?")
    price      = payload.get("market_price_cents", "?")
    fair       = payload.get("fair_value_cents", "?")
    edge       = payload.get("edge_cents", "?")
    conf       = payload.get("confidence", "?")
    regime     = payload.get("regime", "?")

    return (
        f"{grade} WEATHER SIGNAL\n"
        f"{station} {side} >{threshold}\n"
        f"Price: {price}¢ | Fair: {fair}¢\n"
        f"Edge: +{edge}¢ | Conf: {conf}\n"
        f"Regime: {regime}\n"
        f"Action: Manual review"
    )


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------

def build_payload(edge_result: dict, conn: sqlite3.Connection) -> dict:
    """
    Convert an edge_result + live METAR into the Make.com webhook payload.
    """
    from ingestion.metar import get_latest_obs
    from config import STATIONS

    station   = edge_result.get("station_code", "")
    threshold = edge_result.get("threshold_f", 0)
    side      = (edge_result.get("side") or "Yes").upper()
    conf_f    = edge_result.get("confidence") or 0
    conf_lbl  = confidence_label(conf_f)
    grade     = edge_result.get("grade", "?")
    regime    = edge_result.get("regime", "UNKNOWN")

    # Live METAR
    obs = get_latest_obs(station, conn)
    official_temp = obs.get("observed_temp") if obs else None
    wind_summary  = None
    if obs and obs.get("wind_speed") is not None:
        wd = f"{obs['wind_direction']:.0f}°" if obs.get("wind_direction") else "VRB"
        ws = f"{obs['wind_speed']:.0f}"
        wg = f" (gusts {obs['gust_speed']:.0f})" if obs.get("gust_speed") else ""
        wind_summary = f"{wd} @ {ws} kts{wg}"

    station_name = STATIONS.get(station, {}).get("name", station)

    # Reason string drawn from bias note + regime notes
    regime_notes = edge_result.get("regime_notes") or []
    bias_note    = edge_result.get("bias_note") or ""
    reason_parts = []
    if regime_notes:
        reason_parts.append(regime_notes[0])
    if bias_note and len(bias_note) < 120:
        reason_parts.append(bias_note)
    reason = "  ".join(reason_parts) or f"Edge detected in {regime} regime."

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "alert_type":            "WEATHER_SIGNAL",
        "grade":                 grade,
        "station":               station,
        "station_name":          station_name,
        "market_ticker":         edge_result.get("market_ticker", f"{station}-HIGH-{threshold:.0f}"),
        "side":                  side,
        "threshold":             int(threshold),
        "market_price_cents":    edge_result.get("market_price"),
        "fair_value_cents":      edge_result.get("fair_value"),
        "edge_cents":            edge_result.get("edge"),
        "confidence":            conf_lbl,
        "confidence_score":      round(conf_f, 3),
        "regime":                regime,
        "adjusted_forecast_f":   edge_result.get("adjusted_forecast"),
        "openmeteo_forecast_f":  edge_result.get("forecast_high"),
        "official_current_temp_f": official_temp,
        "wind":                  wind_summary,
        "reason":                reason,
        "action":                "MANUAL REVIEW / PAPER TRADE",
        "timestamp_utc":         now,
        "dashboard_url":         _dashboard_url(),
    }

    payload["sms_text"] = format_sms(payload)
    return payload


# ---------------------------------------------------------------------------
# Send
# ---------------------------------------------------------------------------

def _log_to_db(
    payload: dict,
    status: str,
    response_code: int | None,
    error: str | None,
    conn: sqlite3.Connection,
) -> int:
    cur = conn.execute("""
        INSERT INTO webhook_alerts (
            station_code, market_ticker, threshold_f, side,
            market_price, fair_value, edge_cents, confidence, grade,
            regime, adjusted_forecast_f, official_temp_f,
            wind_summary, reason, sms_text, payload_json,
            status, response_code, error_message
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        payload.get("station"),
        payload.get("market_ticker"),
        payload.get("threshold"),
        payload.get("side"),
        payload.get("market_price_cents"),
        payload.get("fair_value_cents"),
        payload.get("edge_cents"),
        payload.get("confidence"),
        payload.get("grade"),
        payload.get("regime"),
        payload.get("adjusted_forecast_f"),
        payload.get("official_current_temp_f"),
        payload.get("wind"),
        payload.get("reason"),
        payload.get("sms_text"),
        json.dumps(payload),
        status,
        response_code,
        error,
    ))
    conn.commit()
    return cur.lastrowid


def send_alert(
    edge_result:  dict,
    conn:         sqlite3.Connection,
    force:        bool = False,   # bypass cooldown/enabled checks
    dry_run:      bool = False,   # build payload but don't POST
) -> dict:
    """
    Main entry point.  Call this after grading a signal.

    Returns:
      {"sent": bool, "suppressed": bool, "reason": str, "alert_id": int|None}
    """
    station   = edge_result.get("station_code", "")
    threshold = edge_result.get("threshold_f", 0)
    side      = edge_result.get("side", "Yes")
    edge      = abs(edge_result.get("edge") or 0)
    conf_f    = edge_result.get("confidence") or 0
    grade     = edge_result.get("grade", "Avoid")

    # ── Filter checks ────────────────────────────────────────────────────────
    if not force:
        if not _alerts_enabled():
            return {"sent": False, "suppressed": True, "reason": "Alerts disabled (ALERTS_ENABLED=false)"}

        if not is_configured():
            return {"sent": False, "suppressed": True, "reason": "No MAKE_ALERT_WEBHOOK_URL configured"}

        if grade not in ("A+", "B"):
            return {"sent": False, "suppressed": True, "reason": f"Grade {grade} below threshold (need A+ or B)"}

        if edge < _min_edge():
            return {"sent": False, "suppressed": True, "reason": f"Edge {edge:.1f}¢ < min {_min_edge():.0f}¢"}

        if _confidence_rank(conf_f) < _min_confidence_rank():
            return {"sent": False, "suppressed": True,
                    "reason": f"Confidence {confidence_label(conf_f)} below min {os.environ.get('MIN_ALERT_CONFIDENCE','MEDIUM')}"}

        if _in_cooldown(station, threshold, side, conn):
            return {"sent": False, "suppressed": True,
                    "reason": f"Cooldown active ({_cooldown_minutes()} min window)"}

    # ── Build payload ────────────────────────────────────────────────────────
    try:
        payload = build_payload(edge_result, conn)
    except Exception as e:
        log.error(f"[webhook_alerts] payload build error: {e}")
        return {"sent": False, "suppressed": False, "reason": str(e)}

    if dry_run:
        log.info(f"[webhook_alerts] DRY RUN — payload built, not sent:\n{json.dumps(payload, indent=2)}")
        return {"sent": False, "suppressed": False, "reason": "dry_run", "payload": payload}

    # ── POST to Make ─────────────────────────────────────────────────────────
    url = _webhook_url()
    try:
        r = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        success = r.status_code in (200, 201, 204)
        status  = "SENT" if success else "FAILED"
        error   = None if success else f"HTTP {r.status_code}: {r.text[:200]}"

        alert_id = _log_to_db(payload, status, r.status_code, error, conn)

        if success:
            log.info(f"[webhook_alerts] Sent alert #{alert_id}: {station} {side} >{threshold:.0f} edge={edge:.1f}¢")
        else:
            log.warning(f"[webhook_alerts] Alert failed #{alert_id}: {error}")

        return {"sent": success, "suppressed": False, "reason": status,
                "alert_id": alert_id, "response_code": r.status_code}

    except Exception as e:
        error_str = str(e)
        alert_id  = _log_to_db(payload, "FAILED", None, error_str[:400], conn)
        log.error(f"[webhook_alerts] POST error: {error_str}")
        return {"sent": False, "suppressed": False, "reason": error_str, "alert_id": alert_id}


# ---------------------------------------------------------------------------
# Scan-and-alert helper — called from scanner / scheduler
# ---------------------------------------------------------------------------

def check_and_alert_all(
    graded_results: list[dict], conn: sqlite3.Connection
) -> list[dict]:
    """
    Iterate graded edge results, send alerts for qualifying signals.
    Returns list of alert outcome dicts.
    """
    outcomes = []
    for r in graded_results:
        if r.get("grade") not in ("A+", "B"):
            continue
        outcome = send_alert(r, conn)
        outcome["station"]   = r.get("station_code")
        outcome["threshold"] = r.get("threshold_f")
        outcome["grade"]     = r.get("grade")
        outcomes.append(outcome)
    return outcomes
