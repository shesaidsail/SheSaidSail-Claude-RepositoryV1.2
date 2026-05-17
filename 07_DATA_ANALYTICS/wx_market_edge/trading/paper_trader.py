"""
Paper trading engine — always-on, auto-entry mode.

Every qualifying signal becomes a paper trade automatically.
Bet sizing uses fractional Kelly via bet_sizer.
Settlements trigger P&L accounting and learning loop.
All activity is PAPER ONLY — no real-money execution.
"""

import sys
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MIN_EDGE, MIN_CONFIDENCE, MAX_SPREAD, _paper_trading_enabled

log = logging.getLogger("paper_trader")


def open_trade(edge_result: dict, conn: sqlite3.Connection) -> int | None:
    """
    Open a paper trade from an edge_result dict.
    Uses bet_sizer for stake sizing. Fires paper open alert if configured.
    Returns paper_trade.id, or None if filters not met.
    """
    if not _paper_trading_enabled():
        return None

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

    # Size the trade
    try:
        from trading.bet_sizer import size_trade
        sizing = size_trade(edge_result, conn)
    except Exception as e:
        log.warning("bet_sizer failed (%s) — using $0 stake", e)
        sizing = {"stake_dollars": 0.0, "kelly_fraction": 0.0, "grade": edge_result.get("grade", ""), "rejected": False}

    if sizing.get("rejected"):
        log.info("Trade rejected by bet_sizer: %s", sizing.get("reject_reason"))
        return None

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.execute("""
        INSERT INTO paper_trades (
            opened_at, station_code, market_ticker, forecast_date,
            threshold_f, side, entry_price, fair_value, edge,
            confidence, regime, adjusted_forecast, model_prob,
            status, grade, stake_dollars, kelly_fraction, notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'OPEN',?,?,?,?)
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
        sizing.get("grade") or edge_result.get("grade"),
        sizing.get("stake_dollars", 0.0),
        sizing.get("kelly_fraction", 0.0),
        f"Signal: {signal} | Auto paper trade",
    ))
    conn.commit()
    trade_id = cur.lastrowid

    # Log bankroll snapshot
    try:
        from trading.bankroll import log_snapshot
        log_snapshot(conn, note=f"Opened trade #{trade_id}")
    except Exception:
        pass

    # Fire open alert
    try:
        from alerts.paper_alerts import alert_trade_opened
        trade_row = dict(conn.execute("SELECT * FROM paper_trades WHERE id=?", (trade_id,)).fetchone())
        alert_trade_opened(trade_row, sizing, conn)
    except Exception as e:
        log.debug("Paper open alert skipped: %s", e)

    return trade_id


def settle_trades(date: str, conn: sqlite3.Connection) -> list[dict]:
    """
    Settle all open paper trades for a given forecast_date.
    Computes pnl_dollars from stake and result.
    Fires settlement alert for each settled trade.
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

        if side == "Yes":
            win = official_high >= threshold + 1
        else:
            win = official_high <= threshold

        entry_cost = t["entry_price"]
        payout     = 100 if win else 0
        pnl_cents  = payout - entry_cost

        # Dollar P&L: stake at risk → win returns stake × (payout/entry_cost), loss loses stake
        stake = t["stake_dollars"] or 0.0
        if stake > 0 and entry_cost and entry_cost > 0:
            pnl_dollars = stake * (pnl_cents / entry_cost)
        else:
            pnl_dollars = 0.0
        pnl_dollars = round(pnl_dollars, 4)

        result_str = "WIN" if win else "LOSS"
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        conn.execute("""
            UPDATE paper_trades
            SET status='CLOSED', settlement_price=?, result=?,
                pnl_cents=?, pnl_dollars=?, closed_at=?
            WHERE id=?
        """, (official_high, result_str, pnl_cents, pnl_dollars, now, t["id"]))
        conn.commit()

        # Build the settled record
        from trading.bankroll import get_current_bankroll
        new_bankroll = get_current_bankroll(conn)

        settled_record = {
            "id":            t["id"],
            "station_code":  t["station_code"],
            "threshold_f":   threshold,
            "side":          side,
            "entry_price":   entry_cost,
            "official_high": official_high,
            "result":        result_str,
            "pnl_cents":     pnl_cents,
            "pnl_dollars":   pnl_dollars,
            "stake_dollars": stake,
            "regime":        t["regime"],
            "grade":         t["grade"],
            "new_bankroll":  new_bankroll,
        }
        settled.append(settled_record)

    # Learning loop + bankroll snapshot + settlement alerts
    for s in settled:
        _update_learning(s, conn)
        try:
            from trading.bankroll import log_snapshot
            log_snapshot(conn, note=f"Settled trade #{s['id']}: {s['result']}")
        except Exception:
            pass
        try:
            from alerts.paper_alerts import alert_trade_settled
            alert_trade_settled(s, conn)
        except Exception as e:
            log.debug("Paper settle alert skipped: %s", e)

    return settled


def _update_learning(settled_trade: dict, conn: sqlite3.Connection):
    """
    After a trade settles, flag regimes with poor win rates.
    Also updates regime bias stats.
    """
    station = settled_trade.get("station_code")
    if not station:
        return

    trade_row = conn.execute(
        "SELECT regime FROM paper_trades WHERE id=?", (settled_trade["id"],)
    ).fetchone()
    if not trade_row or not trade_row["regime"]:
        return

    regime = trade_row["regime"]

    recent = conn.execute("""
        SELECT result FROM paper_trades
        WHERE station_code=? AND regime=? AND status='CLOSED'
        ORDER BY closed_at DESC LIMIT 10
    """, (station, regime)).fetchall()

    if len(recent) < 5:
        return

    wins     = sum(1 for r in recent if r["result"] == "WIN")
    losses   = sum(1 for r in recent if r["result"] == "LOSS")
    total    = wins + losses
    win_rate = wins / total if total else 0

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
    """Compute aggregate paper trading performance metrics in dollars and cents."""
    trades = conn.execute("""
        SELECT pnl_cents, pnl_dollars, stake_dollars, result,
               station_code, regime, threshold_f
        FROM paper_trades WHERE status='CLOSED'
    """).fetchall()

    if not trades:
        return {"total": 0}

    pnls_c  = [t["pnl_cents"]   for t in trades if t["pnl_cents"]   is not None]
    pnls_d  = [t["pnl_dollars"] for t in trades if t["pnl_dollars"] is not None]
    wins    = sum(1 for t in trades if t["result"] == "WIN")
    losses  = sum(1 for t in trades if t["result"] == "LOSS")
    total   = wins + losses

    total_pnl_c = sum(pnls_c)
    total_pnl_d = sum(pnls_d)
    roi_cents   = total_pnl_c / (total * 50) * 100 if total else 0

    from config import STARTING_BANKROLL
    roi_dollars = total_pnl_d / STARTING_BANKROLL * 100 if STARTING_BANKROLL else 0

    # Max drawdown in dollars
    running = 0.0
    peak    = 0.0
    max_dd  = 0.0
    for p in pnls_d:
        running += p
        peak = max(peak, running)
        max_dd = max(max_dd, peak - running)

    by_station: dict[str, dict] = {}
    for t in trades:
        s = t["station_code"] or "?"
        by_station.setdefault(s, {"wins": 0, "losses": 0, "pnl": 0, "pnl_dollars": 0})
        if t["result"] == "WIN":
            by_station[s]["wins"] += 1
        else:
            by_station[s]["losses"] += 1
        by_station[s]["pnl"]         += (t["pnl_cents"] or 0)
        by_station[s]["pnl_dollars"] += (t["pnl_dollars"] or 0)

    by_regime: dict[str, dict] = {}
    for t in trades:
        r = t["regime"] or "UNKNOWN"
        by_regime.setdefault(r, {"wins": 0, "losses": 0, "pnl": 0, "pnl_dollars": 0})
        if t["result"] == "WIN":
            by_regime[r]["wins"] += 1
        else:
            by_regime[r]["losses"] += 1
        by_regime[r]["pnl"]         += (t["pnl_cents"] or 0)
        by_regime[r]["pnl_dollars"] += (t["pnl_dollars"] or 0)

    by_threshold: dict[str, dict] = {}
    for t in trades:
        tk = str(int(t["threshold_f"])) if t["threshold_f"] else "?"
        by_threshold.setdefault(tk, {"wins": 0, "losses": 0, "pnl_dollars": 0})
        if t["result"] == "WIN":
            by_threshold[tk]["wins"] += 1
        else:
            by_threshold[tk]["losses"] += 1
        by_threshold[tk]["pnl_dollars"] += (t["pnl_dollars"] or 0)

    return {
        "total":          total,
        "wins":           wins,
        "losses":         losses,
        "win_rate":       round(wins / total, 4) if total else 0,
        "total_pnl":      round(total_pnl_c, 2),
        "total_pnl_d":    round(total_pnl_d, 2),
        "roi_pct":        round(roi_cents, 2),
        "roi_dollars_pct": round(roi_dollars, 2),
        "max_drawdown":   round(max_dd, 2),
        "by_station":     by_station,
        "by_regime":      by_regime,
        "by_threshold":   by_threshold,
    }
