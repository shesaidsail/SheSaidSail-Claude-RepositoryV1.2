"""
Send a test alert to your Make.com webhook.

Usage:
  python scripts/test_make_alert.py             # sends real POST if URL is set
  python scripts/test_make_alert.py --dry-run   # prints payload, does not POST

Tip: if MAKE_ALERT_WEBHOOK_URL is not set in .env this will print an error
and tell you what to do.
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

from database.db         import init_db
from alerts.webhook_alerts import (
    send_alert, is_configured, format_sms, _webhook_url,
    _alerts_enabled, _min_edge, confidence_label,
)


# Synthetic A+ signal for testing — no real market data needed
FAKE_SIGNAL = {
    "station_code":      "KLAX",
    "forecast_date":     "2026-05-17",
    "threshold_f":       69.0,
    "side":              "Yes",
    "market_ticker":     "TEST-KLAX-HIGH69",
    "market_price":      31.0,
    "fair_value":        56.0,
    "edge":              25.0,
    "confidence":        0.78,
    "grade":             "A+",
    "regime":            "MARINE_WEAK",
    "adjusted_forecast": 70.4,
    "forecast_high":     68.2,
    "blended_bias":      2.2,
    "model_prob":        0.56,
    "regime_notes":      ["Onshore flow at 8 kts with 40% cloud cover — classic marine layer."],
    "bias_note":         "Mostly regime (72%): bias=+2.20°F, σ=1.43°F (n=14)",
    "quality_flags":     [],
    "regime_n":          14,
    "metar_age_min":     12.0,
    "spread":            2.0,
    "signal":            "BET",
}


def main():
    parser = argparse.ArgumentParser(description="Test Make.com webhook alert")
    parser.add_argument("--dry-run", action="store_true",
                        help="Build payload and print it, but do not POST")
    args = parser.parse_args()

    print("=" * 60)
    print("Weather Market Edge Tracker — Make.com Alert Test")
    print("=" * 60)

    # Config status
    print(f"\nAlerts enabled:   {_alerts_enabled()}")
    print(f"Webhook URL set:  {'YES  ' + _webhook_url()[:40] + '...' if is_configured() else 'NO — set MAKE_ALERT_WEBHOOK_URL in .env'}")
    print(f"Min edge:         {_min_edge():.0f}¢")
    print()

    if not is_configured() and not args.dry_run:
        print("ERROR: MAKE_ALERT_WEBHOOK_URL is not set.")
        print("\nTo fix:")
        print("  1. Open  07_DATA_ANALYTICS/wx_market_edge/.env")
        print("  2. Paste your Make.com Custom Webhook URL after MAKE_ALERT_WEBHOOK_URL=")
        print("  3. Re-run this script")
        print("\nTo test without a URL:")
        print("  python scripts/test_make_alert.py --dry-run")
        sys.exit(1)

    conn = init_db()

    result = send_alert(FAKE_SIGNAL, conn, force=True, dry_run=args.dry_run)

    print("-" * 60)
    if args.dry_run:
        from alerts.webhook_alerts import build_payload
        payload = build_payload(FAKE_SIGNAL, conn)
        print("\nPayload that would be sent to Make.com:")
        print(json.dumps(payload, indent=2))
        print()
        print("SMS text:")
        print("-" * 40)
        print(payload.get("sms_text", ""))
        print("-" * 40)
    elif result["sent"]:
        print(f"✅  Alert sent successfully  (HTTP {result.get('response_code')})")
        print(f"    Alert ID in DB: {result.get('alert_id')}")
        print()
        print("SMS text delivered to Make:")
        from alerts.webhook_alerts import build_payload, format_sms
        payload = build_payload(FAKE_SIGNAL, conn)
        print("-" * 40)
        print(payload.get("sms_text", ""))
        print("-" * 40)
        print()
        print("Check your Make.com scenario — it should have received a webhook trigger.")
    else:
        print(f"❌  Alert not sent: {result['reason']}")
        if "suppressed" not in result.get("reason", "").lower():
            print("Check logs above for details.")


if __name__ == "__main__":
    main()
