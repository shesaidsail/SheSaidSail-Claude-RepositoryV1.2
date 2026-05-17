"""
Health check script — prints a JSON summary of system status.
Returns exit code 0 if healthy, 1 if any critical feed is stale/down.

Usage:
  python scripts/health_check.py
  python scripts/health_check.py --json     # print JSON only
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db


STALE_THRESHOLDS = {
    "forecast": timedelta(hours=2),
    "metar":    timedelta(minutes=15),
    "kalshi":   timedelta(minutes=10),
}


def check_health(conn) -> dict:
    now  = datetime.now(timezone.utc)
    status = {}

    # ── Data feeds ──────────────────────────────────────────────────────────
    feeds = conn.execute("""
        SELECT feed, last_success, last_attempt, consecutive_failures, last_error
        FROM data_health
    """).fetchall()

    feed_map = {f["feed"]: dict(f) for f in feeds}
    for feed, threshold in STALE_THRESHOLDS.items():
        row = feed_map.get(feed)
        if not row or not row["last_success"]:
            status[feed] = {"ok": False, "age_min": None, "note": "never succeeded"}
            continue
        try:
            last = datetime.fromisoformat(row["last_success"].replace("Z", "+00:00"))
            age  = now - last
            ok   = age <= threshold
            status[feed] = {
                "ok":        ok,
                "age_min":   round(age.total_seconds() / 60, 1),
                "last":      row["last_success"][:16],
                "failures":  row["consecutive_failures"],
                "note":      "" if ok else f"stale ({age.total_seconds()/60:.0f}m > {threshold.total_seconds()/60:.0f}m limit)",
            }
        except Exception as e:
            status[feed] = {"ok": False, "age_min": None, "note": str(e)}

    # ── Paper trading ────────────────────────────────────────────────────────
    last_trade = conn.execute("""
        SELECT opened_at FROM paper_trades
        ORDER BY opened_at DESC LIMIT 1
    """).fetchone()
    if last_trade:
        try:
            lt = datetime.fromisoformat(last_trade["opened_at"].replace("Z", "+00:00"))
            age_h = (now - lt).total_seconds() / 3600
            status["paper_trading"] = {
                "ok":    age_h < 25,
                "last":  last_trade["opened_at"][:16],
                "age_h": round(age_h, 1),
                "note":  "" if age_h < 25 else "no paper trade in >24h",
            }
        except Exception:
            status["paper_trading"] = {"ok": False, "last": None}
    else:
        status["paper_trading"] = {"ok": True, "last": None, "note": "no trades yet (normal on first run)"}

    # ── Alerts ───────────────────────────────────────────────────────────────
    last_alert = conn.execute("""
        SELECT created_at FROM webhook_alerts
        WHERE status='SENT'
        ORDER BY created_at DESC LIMIT 1
    """).fetchone()
    status["alerts"] = {
        "last": last_alert["created_at"][:16] if last_alert else None,
        "ok":   True,
    }

    # ── Open paper positions ─────────────────────────────────────────────────
    open_count = conn.execute("SELECT COUNT(*) AS n FROM paper_trades WHERE status='OPEN'").fetchone()["n"]
    status["open_positions"] = open_count

    # ── Bankroll ─────────────────────────────────────────────────────────────
    from trading.bankroll import bankroll_status
    bk = bankroll_status(conn)
    status["bankroll"] = {
        "current":    bk["current_bankroll"],
        "drawdown":   f"{bk['drawdown_pct']:.1%}",
        "paused":     bk["trading_paused"],
        "ok":         not bk["trading_paused"],
    }

    # ── Overall healthy ───────────────────────────────────────────────────────
    critical = ["forecast", "metar", "kalshi"]
    healthy  = all(status.get(f, {}).get("ok", False) for f in critical)
    status["_healthy"] = healthy
    status["_checked_at"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print JSON output only")
    args = parser.parse_args()

    conn = init_db()
    result = check_health(conn)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"  Weather Market Edge — Health Check")
        print(f"  {result['_checked_at']}")
        print(f"{'='*50}")
        for key, val in result.items():
            if key.startswith("_"):
                continue
            if isinstance(val, dict):
                ok_str = "✅" if val.get("ok") else "❌"
                note = val.get("note", "")
                age  = f"  age: {val.get('age_min','?')}m" if val.get("age_min") is not None else ""
                print(f"  {ok_str} {key:<20}{age}  {note}")
            else:
                print(f"  ℹ️  {key:<20}{val}")
        print(f"\n  Overall: {'✅ HEALTHY' if result['_healthy'] else '❌ DEGRADED'}")
        print()

    sys.exit(0 if result["_healthy"] else 1)


if __name__ == "__main__":
    main()
