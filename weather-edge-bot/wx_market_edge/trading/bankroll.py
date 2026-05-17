"""
Bankroll tracker for paper trading.

Tracks current balance, peak, drawdown, open exposure, and daily P&L.
All values are in dollars (paper money).
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    STARTING_BANKROLL,
    DRAWDOWN_REDUCE_THRESHOLD,
    DRAWDOWN_HALF_THRESHOLD,
    DRAWDOWN_PAUSE_THRESHOLD,
    MAX_DAILY_LOSS_PCT,
)


def get_current_bankroll(conn: sqlite3.Connection) -> float:
    """
    Current bankroll = starting capital + sum of all settled pnl_dollars.
    Open (unsettled) trades tie up stake but haven't realised P&L yet.
    """
    row = conn.execute("""
        SELECT COALESCE(SUM(pnl_dollars), 0) AS realised
        FROM paper_trades
        WHERE status='CLOSED' AND pnl_dollars IS NOT NULL
    """).fetchone()
    return round(STARTING_BANKROLL + (row["realised"] or 0), 4)


def get_peak_bankroll(conn: sqlite3.Connection) -> float:
    """Historical peak bankroll — computed from the trade P&L sequence."""
    # Reconstruct running bankroll from each closed trade in chronological order
    trades = conn.execute("""
        SELECT pnl_dollars FROM paper_trades
        WHERE status='CLOSED' AND pnl_dollars IS NOT NULL
        ORDER BY closed_at ASC
    """).fetchall()

    running = STARTING_BANKROLL
    peak    = STARTING_BANKROLL
    for t in trades:
        running += t["pnl_dollars"]
        if running > peak:
            peak = running

    # Also honour any snapshot peak that may be higher (e.g. after manual adjustments)
    snap = conn.execute("""
        SELECT COALESCE(MAX(peak_bankroll), 0) AS snap_peak FROM bankroll_history
    """).fetchone()
    snap_peak = snap["snap_peak"] or 0

    return round(max(peak, snap_peak), 4)


def get_drawdown(conn: sqlite3.Connection) -> float:
    """Current drawdown as a fraction (0.0 – 1.0). 0 = at peak."""
    current = get_current_bankroll(conn)
    peak    = get_peak_bankroll(conn)
    if peak <= 0:
        return 0.0
    dd = (peak - current) / peak
    return max(0.0, round(dd, 6))


def get_open_exposure(conn: sqlite3.Connection) -> float:
    """
    Total dollars committed to open (unsettled) trades.
    Each open trade's stake_dollars is money at risk until settlement.
    """
    row = conn.execute("""
        SELECT COALESCE(SUM(stake_dollars), 0) AS exposure
        FROM paper_trades
        WHERE status='OPEN' AND stake_dollars IS NOT NULL
    """).fetchone()
    return round(row["exposure"] or 0, 4)


def get_station_exposure(station_code: str, conn: sqlite3.Connection) -> float:
    """Open exposure (dollars) for a single station."""
    row = conn.execute("""
        SELECT COALESCE(SUM(stake_dollars), 0) AS exposure
        FROM paper_trades
        WHERE status='OPEN' AND station_code=? AND stake_dollars IS NOT NULL
    """, (station_code,)).fetchone()
    return round(row["exposure"] or 0, 4)


def get_regime_exposure(regime: str, conn: sqlite3.Connection) -> float:
    """Open exposure (dollars) for a single regime."""
    row = conn.execute("""
        SELECT COALESCE(SUM(stake_dollars), 0) AS exposure
        FROM paper_trades
        WHERE status='OPEN' AND regime=? AND stake_dollars IS NOT NULL
    """, (regime,)).fetchone()
    return round(row["exposure"] or 0, 4)


def get_daily_pnl(conn: sqlite3.Connection, date: str | None = None) -> float:
    """Realised P&L (dollars) for a calendar date (defaults to today UTC)."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = conn.execute("""
        SELECT COALESCE(SUM(pnl_dollars), 0) AS daily
        FROM paper_trades
        WHERE status='CLOSED'
          AND pnl_dollars IS NOT NULL
          AND DATE(closed_at) = ?
    """, (date,)).fetchone()
    return round(row["daily"] or 0, 4)


def is_daily_loss_limit_hit(conn: sqlite3.Connection, date: str | None = None) -> bool:
    """True if today's realised losses exceed MAX_DAILY_LOSS_PCT of bankroll."""
    daily_pnl = get_daily_pnl(conn, date)
    if daily_pnl >= 0:
        return False
    bankroll = get_current_bankroll(conn)
    if bankroll <= 0:
        return True
    return abs(daily_pnl) / bankroll >= MAX_DAILY_LOSS_PCT


def get_sizing_multiplier(conn: sqlite3.Connection) -> float:
    """
    Drawdown-based multiplier applied to all bet sizes.
    - Drawdown < 10%  → 1.0  (full sizing)
    - 10%–20%         → 0.75 (25% reduction)
    - 20%–30%         → 0.50 (50% reduction)
    - ≥30%            → 0.0  (pause — no new trades)
    """
    dd = get_drawdown(conn)
    if dd >= DRAWDOWN_PAUSE_THRESHOLD:
        return 0.0
    if dd >= DRAWDOWN_HALF_THRESHOLD:
        return 0.50
    if dd >= DRAWDOWN_REDUCE_THRESHOLD:
        return 0.75
    return 1.0


def log_snapshot(conn: sqlite3.Connection, note: str = "") -> None:
    """Upsert today's bankroll snapshot into bankroll_history."""
    today   = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    current = get_current_bankroll(conn)
    peak    = get_peak_bankroll(conn)
    dd      = get_drawdown(conn)
    exp     = get_open_exposure(conn)
    daily   = get_daily_pnl(conn, today)

    trades_today = conn.execute("""
        SELECT COUNT(*) AS n FROM paper_trades
        WHERE DATE(opened_at) = ?
    """, (today,)).fetchone()["n"]

    conn.execute("""
        INSERT INTO bankroll_history
            (snapshot_date, bankroll, peak_bankroll, drawdown_pct,
             open_exposure, daily_pnl, trades_today, note)
        VALUES (?,?,?,?,?,?,?,?)
        ON CONFLICT(snapshot_date) DO UPDATE SET
            bankroll=excluded.bankroll,
            peak_bankroll=excluded.peak_bankroll,
            drawdown_pct=excluded.drawdown_pct,
            open_exposure=excluded.open_exposure,
            daily_pnl=excluded.daily_pnl,
            trades_today=excluded.trades_today,
            note=excluded.note
    """, (today, current, peak, dd, exp, daily, trades_today, note))
    conn.commit()


def bankroll_status(conn: sqlite3.Connection) -> dict:
    """Full bankroll state summary dict — used by dashboard and bet_sizer."""
    current   = get_current_bankroll(conn)
    peak      = get_peak_bankroll(conn)
    dd        = get_drawdown(conn)
    exp       = get_open_exposure(conn)
    daily_pnl = get_daily_pnl(conn)
    multiplier = get_sizing_multiplier(conn)
    daily_halt = is_daily_loss_limit_hit(conn)

    return {
        "current_bankroll":   current,
        "starting_bankroll":  STARTING_BANKROLL,
        "peak_bankroll":      peak,
        "drawdown_pct":       dd,
        "open_exposure":      exp,
        "available":          max(0.0, current - exp),
        "daily_pnl":          daily_pnl,
        "sizing_multiplier":  multiplier,
        "daily_halt":         daily_halt,
        "trading_paused":     multiplier == 0.0 or daily_halt,
        "roi_pct":            round((current - STARTING_BANKROLL) / STARTING_BANKROLL * 100, 2),
    }
