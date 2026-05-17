"""
CLV snapshot + stale-trade void worker.

Runs in a continuous loop:
  Every 15 minutes: record CLV market-price snapshots for open trades
  Every 6 hours:    void trades that have been open beyond TRADE_VOID_AFTER_DAYS

This worker is safe to run alongside scanner and settlement workers —
it only reads market_snapshots and writes to market_price_snapshots / paper_trades.
"""

import sys
import time
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db
from trading.paper_trader import record_clv_snapshot, void_stale_trades

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CLV] %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/clv_worker.log"),
    ],
)
log = logging.getLogger("clv_worker")

CLV_INTERVAL_SEC  = 15 * 60   # snapshot every 15 min
VOID_INTERVAL_SEC = 6 * 60 * 60   # void check every 6 hours

def main():
    log.info("CLV worker starting")
    conn = init_db()
    last_void = 0.0

    while True:
        try:
            written = record_clv_snapshot(conn)
            if written:
                log.info("CLV snapshots recorded: %d", written)
        except Exception as e:
            log.error("CLV snapshot error: %s", e)

        now = time.monotonic()
        if now - last_void >= VOID_INTERVAL_SEC:
            try:
                voided = void_stale_trades(conn)
                if voided:
                    log.warning("Voided %d stale trade(s): %s", len(voided), voided)
            except Exception as e:
                log.error("Void stale trades error: %s", e)
            last_void = now

        time.sleep(CLV_INTERVAL_SEC)


if __name__ == "__main__":
    main()
