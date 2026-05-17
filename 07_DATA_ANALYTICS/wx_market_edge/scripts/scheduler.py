"""
Background scheduler — runs all data refreshes on their configured intervals.

Usage:
  python scripts/scheduler.py         # run forever
  python scripts/scheduler.py --once  # run one cycle and exit

Runs in a single thread; each task logs its completion time.
"""

import sys
import time
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db         import init_db
from ingestion.open_meteo  import refresh_all as refresh_forecasts
from ingestion.metar       import refresh_all as refresh_metar
from ingestion.kalshi_auth import refresh_with_auth as refresh_kalshi
from config import FORECAST_INTERVAL, METAR_INTERVAL, KALSHI_INTERVAL, LOG_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "scheduler.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("scheduler")


class Scheduler:
    def __init__(self, conn):
        self.conn = conn
        self.last_run: dict[str, float] = {
            "forecast": 0,
            "metar":    0,
            "kalshi":   0,
        }

    def _due(self, task: str, interval: int) -> bool:
        return time.time() - self.last_run[task] >= interval

    def tick(self):
        if self._due("metar", METAR_INTERVAL):
            try:
                results = refresh_metar(self.conn, verbose=False)
                new_obs = sum(results.values())
                log.info(f"METAR refresh: {new_obs} new observations across {len(results)} stations")
            except Exception as e:
                log.error(f"METAR refresh failed: {e}")
            self.last_run["metar"] = time.time()

        if self._due("forecast", FORECAST_INTERVAL):
            try:
                results = refresh_forecasts(self.conn, verbose=False)
                rows = sum(results.values())
                log.info(f"Forecast refresh: {rows} daily forecast rows stored")
            except Exception as e:
                log.error(f"Forecast refresh failed: {e}")
            self.last_run["forecast"] = time.time()

        if self._due("kalshi", KALSHI_INTERVAL):
            try:
                n = refresh_kalshi(self.conn, verbose=False)
                log.info(f"Kalshi refresh: {n} market snapshots stored")
            except Exception as e:
                log.error(f"Kalshi refresh failed: {e}")
            self.last_run["kalshi"] = time.time()

    def run_once(self):
        """Force-run all tasks regardless of interval."""
        log.info("Running all tasks once...")
        try:
            results = refresh_forecasts(self.conn, verbose=True)
            log.info(f"Forecasts: {sum(results.values())} rows")
        except Exception as e:
            log.error(f"Forecast error: {e}")
        try:
            results = refresh_metar(self.conn, verbose=True)
            log.info(f"METAR: {sum(results.values())} new")
        except Exception as e:
            log.error(f"METAR error: {e}")
        try:
            n = refresh_kalshi(self.conn, verbose=True)
            log.info(f"Kalshi: {n} snapshots")
        except Exception as e:
            log.error(f"Kalshi error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    conn = init_db()
    sched = Scheduler(conn)

    if args.once:
        sched.run_once()
        return

    log.info("Scheduler started. Intervals: forecast=%ds metar=%ds kalshi=%ds",
             FORECAST_INTERVAL, METAR_INTERVAL, KALSHI_INTERVAL)

    # Immediately run everything on startup
    sched.run_once()
    sched.last_run = {k: time.time() for k in sched.last_run}

    try:
        while True:
            sched.tick()
            time.sleep(30)
    except KeyboardInterrupt:
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
