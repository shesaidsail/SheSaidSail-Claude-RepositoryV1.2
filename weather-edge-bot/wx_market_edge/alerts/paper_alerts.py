"""
Paper trade webhook alerts — sent via Make.com like signal alerts.

Three alert types:
  PAPER_TRADE_OPENED   — when auto-paper-trade is entered
  PAPER_TRADE_SETTLED  — when a paper trade settles with P&L
  PAPER_DAILY_SUMMARY  — end-of-day performance report

Payloads go to the same MAKE_ALERT_WEBHOOK_URL as signal alerts.
Controlled independently by PAPER_ALERTS_ENABLED, PAPER_ALERT_OPEN_TRADES,
PAPER_ALERT_SETTLEMENTS, PAPER_ALERT_DAILY_SUMMARY env vars.
"""

import os
import sys
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

log = logging.getLogger("paper_alerts")

_CONF_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "VERY_HIGH": 3}


def _webhook_url() -> str:
    return os.getenv("MAKE_ALERT_WEBHOOK_URL", "")


def _enabled() -> bool:
    return os.getenv("PAPER_ALERTS_ENABLED", "true").lower() == "true" and bool(_webhook_url())


def _alert_open() -> bool:
    return os.getenv("PAPER_ALERT_OPEN_TRADES", "true").lower() == "true"


def _alert_settle() -> bool:
    return os.getenv("PAPER_ALERT_SETTLEMENTS", "true").lower() == "true"


def _alert_daily() -> bool:
    return os.getenv("PAPER_ALERT_DAILY_SUMMARY", "true").lower() == "true"


def _cooldown_minutes() -> int:
    return int(os.getenv("PAPER_ALERT_COOLDOWN_MINUTES", "30"))


def _in_cooldown(station_code: str, threshold_f: float, side: str,
                 alert_type: str, conn: sqlite3.Connection) -> bool:
    """Return True if a similar alert was sent within the cooldown window."""
    cd = _cooldown_minutes()
    row = conn.execute("""
        SELECT id FROM webhook_alerts
        WHERE station_code=? AND threshold_f=? AND side=?
          AND alert_type=?
          AND status='SENT'
          AND created_at >= datetime('now', ? || ' minutes')
        LIMIT 1
    """, (station_code, threshold_f, side, alert_type, f"-{cd}")).fetchone()
    return row is not None


def _post(payload: dict, alert_type: str, conn: sqlite3.Connection) -> dict:
    """POST payload to Make and log to webhook_alerts table."""
    url = _webhook_url()
    status_val = "PENDING"
    response_code = None
    error_msg = None

    if _HAS_REQUESTS and url:
        try:
            resp = requests.post(url, json=payload, timeout=10)
            response_code = resp.status_code
            status_val = "SENT" if resp.status_code < 300 else "FAILED"
            if resp.status_code >= 300:
                error_msg = resp.text[:200]
        except Exception as e:
            status_val = "FAILED"
            error_msg = str(e)[:200]
    else:
        status_val = "SUPPRESSED"
        error_msg = "no requests lib or no URL"

    conn.execute("""
        INSERT INTO webhook_alerts
            (station_code, market_ticker, threshold_f, side,
             market_price, fair_value, edge_cents, confidence,
             grade, regime, adjusted_forecast_f,
             reason, sms_text, payload_json, status,
             response_code, error_message)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
        payload.get("reason", ""),
        payload.get("sms_text", ""),
        json.dumps(payload),
        status_val,
        response_code,
        error_msg,
    ))
    conn.commit()

    return {"sent": status_val == "SENT", "status": status_val, "error": error_msg}


# ── Open trade alert ──────────────────────────────────────────────────────────

def alert_trade_opened(trade: dict, sizing: dict, conn: sqlite3.Connection) -> dict:
    """
    Send paper-trade-opened alert after auto-entry.

    trade   — dict from paper_trades row (or the edge_result used to open it)
    sizing  — dict from bet_sizer.size_trade()
    """
    if not _enabled() or not _alert_open():
        return {"sent": False, "status": "SUPPRESSED", "error": "alerts disabled"}

    grade = sizing.get("grade", trade.get("grade", "B"))
    if grade not in {"A+", "B"}:
        return {"sent": False, "status": "SUPPRESSED", "error": "grade not in whitelist"}

    station   = trade.get("station_code", "")
    threshold = trade.get("threshold_f", 0)
    side      = trade.get("side", "")
    price     = trade.get("entry_price") or trade.get("market_price", 0)
    fair      = trade.get("fair_value", 0)
    edge      = trade.get("edge", 0)
    conf_raw  = trade.get("confidence", 0)
    regime    = trade.get("regime", "UNKNOWN")
    adj_f     = trade.get("adjusted_forecast")
    ticker    = trade.get("market_ticker", "")
    stake     = sizing.get("stake_dollars", 0)
    bankroll  = sizing.get("bankroll_snapshot", {}).get("current_bankroll", 0)
    exposure  = sizing.get("bankroll_snapshot", {}).get("open_exposure", 0)

    if _in_cooldown(station, threshold, side, "PAPER_TRADE_OPENED", conn):
        return {"sent": False, "status": "SUPPRESSED", "error": "cooldown active"}

    conf_str = _conf_label(conf_raw)

    sms = (
        f"PAPER TRADE OPENED\n"
        f"{station} {side.upper()} >{int(threshold)}\n"
        f"Stake: ${stake:.2f}\n"
        f"Price: {int(price)}¢  |  Fair: {int(fair)}¢\n"
        f"Edge: +{int(edge)}¢  |  Conf: {conf_str}\n"
        f"Regime: {regime}\n"
        f"Bankroll: ${bankroll:.2f} → Open risk ${exposure + stake:.2f}\n"
        f"Action: Manual review only"
    )

    payload = {
        "alert_type":          "PAPER_TRADE_OPENED",
        "grade":               grade,
        "station":             station,
        "market_ticker":       ticker,
        "side":                side.upper(),
        "threshold":           threshold,
        "market_price_cents":  price,
        "fair_value_cents":    fair,
        "edge_cents":          edge,
        "confidence":          conf_str,
        "confidence_score":    conf_raw,
        "regime":              regime,
        "adjusted_forecast_f": adj_f,
        "stake_dollars":       stake,
        "bankroll":            bankroll,
        "open_exposure":       exposure + stake,
        "timestamp_utc":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sms_text":            sms,
        "paper_trade":         True,
        "real_money":          False,
    }

    result = _post(payload, "PAPER_TRADE_OPENED", conn)
    if result["sent"]:
        log.info("Paper-open alert sent: %s %s >%s stake=$%.2f", station, side, threshold, stake)
    return result


# ── Settlement alert ──────────────────────────────────────────────────────────

def alert_trade_settled(settled: dict, conn: sqlite3.Connection) -> dict:
    """
    Send paper-trade-settled alert.

    settled — dict returned by paper_trader.settle_trades() (one trade entry)
    """
    if not _enabled() or not _alert_settle():
        return {"sent": False, "status": "SUPPRESSED", "error": "alerts disabled"}

    grade = settled.get("grade", "B")
    if grade not in {"A+", "B"}:
        return {"sent": False, "status": "SUPPRESSED", "error": "grade not in whitelist"}

    station   = settled.get("station_code", "")
    threshold = settled.get("threshold_f", 0)
    side      = settled.get("side", "")
    result    = settled.get("result", "")
    stake     = settled.get("stake_dollars") or 0
    pnl_d     = settled.get("pnl_dollars") or 0
    bankroll  = settled.get("new_bankroll") or 0
    regime    = settled.get("regime", "UNKNOWN")
    lesson    = settled.get("lesson", "")

    sms = (
        f"PAPER TRADE SETTLED\n"
        f"{station} {side.upper()} >{int(threshold)}\n"
        f"Result: {result}\n"
        f"Stake: ${stake:.2f}  |  P&L: {'+' if pnl_d >= 0 else ''}${pnl_d:.2f}\n"
        f"Bankroll: ${bankroll:.2f}\n"
        f"Regime: {regime}"
    )
    if lesson:
        sms += f"\nLesson: {lesson}"

    payload = {
        "alert_type":     "PAPER_TRADE_SETTLED",
        "grade":          grade,
        "station":        station,
        "side":           side.upper(),
        "threshold":      threshold,
        "result":         result,
        "stake_dollars":  stake,
        "pnl_dollars":    pnl_d,
        "bankroll":       bankroll,
        "regime":         regime,
        "lesson":         lesson,
        "timestamp_utc":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sms_text":       sms,
        "paper_trade":    True,
        "real_money":     False,
    }

    result_dict = _post(payload, "PAPER_TRADE_SETTLED", conn)
    if result_dict["sent"]:
        log.info("Paper-settle alert sent: %s %s >%s %s pnl=$%.2f", station, side, threshold, result, pnl_d)
    return result_dict


# ── Daily summary alert ───────────────────────────────────────────────────────

def alert_daily_summary(conn: sqlite3.Connection, date: str | None = None) -> dict:
    """Send end-of-day paper trading summary alert."""
    if not _enabled() or not _alert_daily():
        return {"sent": False, "status": "SUPPRESSED", "error": "alerts disabled"}

    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    trades = conn.execute("""
        SELECT station_code, regime, result, pnl_dollars, stake_dollars
        FROM paper_trades
        WHERE status='CLOSED' AND DATE(closed_at) = ?
          AND pnl_dollars IS NOT NULL
    """, (date,)).fetchall()

    total   = len(trades)
    wins    = sum(1 for t in trades if t["result"] == "WIN")
    losses  = total - wins
    daily_pnl = sum(t["pnl_dollars"] or 0 for t in trades)

    from trading.bankroll import get_current_bankroll
    bankroll = get_current_bankroll(conn)

    # Best/worst regime
    regime_pnl: dict[str, float] = {}
    for t in trades:
        r = t["regime"] or "UNKNOWN"
        regime_pnl[r] = regime_pnl.get(r, 0) + (t["pnl_dollars"] or 0)
    best_regime  = max(regime_pnl, key=lambda k: regime_pnl[k]) if regime_pnl else "—"
    worst_regime = min(regime_pnl, key=lambda k: regime_pnl[k]) if regime_pnl else "—"

    # Latest lesson
    lesson_row = conn.execute("""
        SELECT lesson FROM model_lessons
        ORDER BY created_at DESC LIMIT 1
    """).fetchone()
    top_lesson = lesson_row["lesson"] if lesson_row else "No new lessons"

    sign = "+" if daily_pnl >= 0 else ""
    sms = (
        f"DAILY WEATHER PAPER REPORT\n"
        f"Trades: {total}  |  Wins: {wins}  |  Losses: {losses}\n"
        f"Daily P&L: {sign}${daily_pnl:.2f}\n"
        f"Bankroll: ${bankroll:.2f}\n"
        f"Best regime: {best_regime}\n"
        f"Worst regime: {worst_regime}\n"
        f"Top lesson: {top_lesson[:80]}"
    )

    payload = {
        "alert_type":   "PAPER_DAILY_SUMMARY",
        "date":         date,
        "total_trades": total,
        "wins":         wins,
        "losses":       losses,
        "daily_pnl":    round(daily_pnl, 2),
        "bankroll":     bankroll,
        "best_regime":  best_regime,
        "worst_regime": worst_regime,
        "top_lesson":   top_lesson,
        "sms_text":     sms,
        "paper_trade":  True,
        "real_money":   False,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    result = _post(payload, "PAPER_DAILY_SUMMARY", conn)
    if result["sent"]:
        log.info("Daily summary alert sent: %d trades, P&L=$%.2f", total, daily_pnl)
    return result


# ── Helpers ───────────────────────────────────────────────────────────────────

def _conf_label(conf: float) -> str:
    if conf >= 0.80:
        return "VERY_HIGH"
    if conf >= 0.65:
        return "HIGH"
    if conf >= 0.50:
        return "MEDIUM"
    return "LOW"
