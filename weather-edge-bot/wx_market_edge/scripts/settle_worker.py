"""
Settlement worker — runs continuously, settling paper trades once per hour.

Settles trades for yesterday and today (in case today's METAR data just arrived).
Fires Make/Quo settlement alerts via paper_alerts.
Logs daily summary once per UTC day.

Usage:
  python scripts/settle_worker.py          # run forever (production)
  python scripts/settle_worker.py --once   # settle once and exit
"""

import sys
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db          import init_db
from ingestion.metar      import refresh_all as refresh_metar
from trading.paper_trader import settle_trades
from models.bias_engine   import compute_and_store_stats
from config               import STATIONS, DEFAULT_MODEL, LOG_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "settlement.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("settle_worker")

SETTLE_INTERVAL = 3600  # 1 hour


def run_settlement(conn) -> int:
    """Settle all open paper trades for yesterday and today."""
    today     = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")

    total = 0
    for date in [yesterday, today]:
        settled = settle_trades(date, conn)
        if settled:
            log.info("Settled %d trades for %s", len(settled), date)
            total += len(settled)

            # Update bias engine after settlements
            for station in STATIONS:
                try:
                    compute_and_store_stats(station, DEFAULT_MODEL, conn)
                except Exception as e:
                    log.warning("Bias update failed for %s: %s", station, e)

    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one cycle and exit")
    args = parser.parse_args()

    conn = init_db()

    if args.once:
        n = run_settlement(conn)
        log.info("Settled %d trades (once mode)", n)
        return

    log.info("Settlement worker started. Interval: %ds", SETTLE_INTERVAL)
    last_summary_date = ""

    while True:
        try:
            # Refresh latest METAR first so settlements have fresh data
            refresh_metar(conn, verbose=False)
            n = run_settlement(conn)
            if n:
                log.info("Settlement cycle: %d trades settled", n)

            # Daily summary alert near midnight UTC
            now  = datetime.now(timezone.utc)
            today = now.strftime("%Y-%m-%d")
            if now.hour == 23 and now.minute >= 50 and today != last_summary_date:
                try:
                    from alerts.paper_alerts import alert_daily_summary
                    result = alert_daily_summary(conn, date=today)
                    if result.get("sent"):
                        last_summary_date = today
                        log.info("Daily summary alert sent for %s", today)
                except Exception as e:
                    log.error("Daily summary alert failed: %s", e)

        except Exception as e:
            log.error("Settlement cycle error: %s", e)

        time.sleep(SETTLE_INTERVAL)


if __name__ == "__main__":
    main()
