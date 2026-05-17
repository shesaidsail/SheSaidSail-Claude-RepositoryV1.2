"""
Paper trading engine.

Auto-generates paper trades for any edge signal that passes all filters.
Settles trades after daily_settlements data is available.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MIN_EDGE, MIN_CONFIDENCE, MAX_SPREAD


def open_trade(edge_result: dict, conn: sqlite3.Connection) -> int | None:
    """
    Open a paper trade from an edge_result dict.
    Returns paper_trade.id, or None if filters not met.
    """
    edge       = edge_result.get("edge") or 0
    confidence = edge_result.get("confidence") or 0
    spread     = edge_result.get("spread")
    signal     = edge_result.get("signal", "PASS")

    if signal not in ("BET", "FADE"):
        return None
    if abs(edge) < MIN_EDGE:
        return None
    if confidence < MIN_CONFIDENCE:
        return None
    if spread is not None and spread > MAX_SPREAD:
        return None

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.execute("""
        INSERT INTO paper_trades (
            opened_at, station_code, market_ticker, forecast_date,
            threshold_f, side, entry_price, fair_value, edge,
            confidence, regime, adjusted_forecast, model_prob, status, notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'OPEN',?)
    """, (
        now,
        edge_result.get("station_code"),
        edge_result.get("market_ticker", "MANUAL"),
        edge_result.get("forecast_date"),
        edge_result.get("threshold_f"),
        edge_result.get("side"),
        edge_result.get("market_price"),
        edge_result.get("fair_value"),
        edge,
        confidence,
        edge_result.get("regime"),
        edge_result.get("adjusted_forecast"),
        edge_result.get("model_prob"),
        f"Signal: {signal}",
    ))
    conn.commit()
    trade_id = cur.lastrowid
    return trade_id


def settle_trades(date: str, conn: sqlite3.Connection) -> list[dict]:
    """
    Settle all open paper trades for a given forecast_date.
    Uses daily_settlements to determine win/loss.
    Returns list of settled trade dicts.
    """
    open_trades = conn.execute("""
        SELECT * FROM paper_trades
        WHERE forecast_date=? AND status='OPEN'
    """, (date,)).fetchall()

    settled = []
    for t in open_trades:
        settlement = conn.execute("""
            SELECT official_high FROM daily_settlements
            WHERE settlement_date=? AND station_code=?
        """, (date, t["station_code"])).fetchone()

        if not settlement or settlement["official_high"] is None:
            continue

        official_high = settlement["official_high"]
        threshold     = t["threshold_f"]
        side          = t["side"]

        # Determine outcome
        if side == "Yes":
            win = official_high >= threshold + 1    # Yes >T: wins if actual >= T+1
        else:
            win = official_high <= threshold        # No >T: wins if actual <= T

        # Kalshi-style P&L: entry=cost, payout=100 if win, 0 if loss
        entry_cost = t["entry_price"]
        payout     = 100 if win else 0
        pnl        = payout - entry_cost

        result_str = "WIN" if win else "LOSS"
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        conn.execute("""
            UPDATE paper_trades
            SET status='CLOSED', settlement_price=?, result=?, pnl_cents=?, closed_at=?
            WHERE id=?
        """, (official_high, result_str, pnl, now, t["id"]))
        conn.commit()

        settled.append({
            "id":             t["id"],
            "station_code":   t["station_code"],
            "threshold_f":    threshold,
            "side":           side,
            "entry_price":    entry_cost,
            "official_high":  official_high,
            "result":         result_str,
            "pnl_cents":      pnl,
        })

    # Trigger learning loop for each settled trade
    for s in settled:
        _update_learning(s, conn)

    return settled


def _update_learning(settled_trade: dict, conn: sqlite3.Connection):
    """
    After a trade settles, record what we predicted vs what happened
    so the bias engine can adapt over time.

    The learning happens automatically via compute_and_store_stats() in
    settle_day.py — this function logs additional calibration metadata
    and flags regimes that are losing repeatedly.
    """
    # Count recent wins/losses in this regime for this station
    station = settled_trade.get("station_code")
    if not station:
        return

    # Look up the closed trade's regime
    trade_row = conn.execute(
        "SELECT regime FROM paper_trades WHERE id=?", (settled_trade["id"],)
    ).fetchone()
    if not trade_row or not trade_row["regime"]:
        return

    regime = trade_row["regime"]

    # Recent performance in this regime (last 10 trades)
    recent = conn.execute("""
        SELECT result FROM paper_trades
        WHERE station_code=? AND regime=? AND status='CLOSED'
        ORDER BY closed_at DESC LIMIT 10
    """, (station, regime)).fetchall()

    if len(recent) < 5:
        return  # not enough data to flag

    wins   = sum(1 for r in recent if r["result"] == "WIN")
    losses = sum(1 for r in recent if r["result"] == "LOSS")
    total  = wins + losses
    win_rate = wins / total if total else 0

    # Flag poorly-performing regimes
    if win_rate < 0.35 and total >= 5:
        conn.execute("""
            INSERT INTO alerts (station_code, alert_type, message)
            VALUES (?,?,?)
        """, (station, "REGIME_LOSING",
              f"{station}/{regime}: win rate {win_rate:.0%} over last {total} trades — consider reducing confidence weight"))
        conn.commit()

    elif win_rate >= 0.65 and total >= 5:
        conn.execute("""
            INSERT INTO alerts (station_code, alert_type, message)
            VALUES (?,?,?)
        """, (station, "REGIME_PROFITABLE",
              f"{station}/{regime}: win rate {win_rate:.0%} over last {total} trades — regime calibrating well"))
        conn.commit()


def get_open_trades(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT pt.*, s.name AS station_name
        FROM paper_trades pt
        LEFT JOIN stations s ON s.icao = pt.station_code
        WHERE pt.status='OPEN'
        ORDER BY pt.opened_at DESC
    """).fetchall()
    return [dict(r) for r in rows]


def get_closed_trades(conn: sqlite3.Connection, limit: int = 200) -> list[dict]:
    rows = conn.execute("""
        SELECT pt.*, s.name AS station_name
        FROM paper_trades pt
        LEFT JOIN stations s ON s.icao = pt.station_code
        WHERE pt.status='CLOSED'
        ORDER BY pt.closed_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def performance_summary(conn: sqlite3.Connection) -> dict:
    """Compute aggregate paper trading performance metrics."""
    trades = conn.execute("""
        SELECT pnl_cents, result, station_code, regime, threshold_f
        FROM paper_trades WHERE status='CLOSED'
    """).fetchall()

    if not trades:
        return {"total": 0}

    pnls   = [t["pnl_cents"] for t in trades if t["pnl_cents"] is not None]
    wins   = sum(1 for t in trades if t["result"] == "WIN")
    losses = sum(1 for t in trades if t["result"] == "LOSS")
    total  = wins + losses

    total_pnl = sum(pnls)
    roi       = total_pnl / (total * 50) * 100 if total else 0   # normalised to 50¢ avg cost

    # Max drawdown (running cumulative)
    running = 0
    peak    = 0
    max_dd  = 0
    for p in pnls:
        running += p
        peak = max(peak, running)
        max_dd = max(max_dd, peak - running)

    # By station
    by_station: dict[str, dict] = {}
    for t in trades:
        s = t["station_code"] or "?"
        by_station.setdefault(s, {"wins": 0, "losses": 0, "pnl": 0})
        if t["result"] == "WIN":
            by_station[s]["wins"] += 1
        else:
            by_station[s]["losses"] += 1
        by_station[s]["pnl"] += (t["pnl_cents"] or 0)

    # By regime
    by_regime: dict[str, dict] = {}
    for t in trades:
        r = t["regime"] or "UNKNOWN"
        by_regime.setdefault(r, {"wins": 0, "losses": 0, "pnl": 0})
        if t["result"] == "WIN":
            by_regime[r]["wins"] += 1
        else:
            by_regime[r]["losses"] += 1
        by_regime[r]["pnl"] += (t["pnl_cents"] or 0)

    return {
        "total":        total,
        "wins":         wins,
        "losses":       losses,
        "win_rate":     round(wins / total, 4) if total else 0,
        "total_pnl":    round(total_pnl, 2),
        "roi_pct":      round(roi, 2),
        "max_drawdown": round(max_dd, 2),
        "by_station":   by_station,
        "by_regime":    by_regime,
    }
