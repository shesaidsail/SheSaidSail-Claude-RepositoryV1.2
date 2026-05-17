"""
Daily SQLite backup script.

Creates a snapshot copy of the live database at:
  backups/weather_trading_YYYY_MM_DD.sqlite

SQLite's backup API is used so the copy is safe even with WAL mode and
concurrent readers/writers.

Usage:
  python scripts/backup_database.py              # backup today
  python scripts/backup_database.py --keep 30    # keep only last N backups

Run via cron (daily at 02:00 UTC):
  0 2 * * * cd /app && python scripts/backup_database.py --keep 30
"""

import sys
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH, ROOT

log = logging.getLogger("backup")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BACKUP_DIR = ROOT / "backups"


def backup(keep: int = 0) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y_%m_%d")
    dest  = BACKUP_DIR / f"weather_trading_{today}.sqlite"

    src = sqlite3.connect(str(DB_PATH))
    dst = sqlite3.connect(str(dest))
    src.backup(dst)
    dst.close()
    src.close()

    size_kb = dest.stat().st_size // 1024
    log.info("Backup complete: %s (%d KB)", dest.name, size_kb)

    if keep > 0:
        _prune(keep)

    return dest


def _prune(keep: int):
    files = sorted(BACKUP_DIR.glob("weather_trading_*.sqlite"))
    while len(files) > keep:
        oldest = files.pop(0)
        oldest.unlink()
        log.info("Pruned old backup: %s", oldest.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup SQLite database")
    parser.add_argument("--keep", type=int, default=0,
                        help="Delete backups older than N most recent (0 = keep all)")
    args = parser.parse_args()
    backup(keep=args.keep)
