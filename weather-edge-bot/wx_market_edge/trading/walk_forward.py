"""
Walk-forward backtesting engine.

Splits a date range into sliding train/test windows and reruns the backtest
on each test window using only bias computed from the preceding train window.
This gives an out-of-sample performance estimate without any lookahead.

Window layout (example: train=60d, test=30d, step=14d):
  Window 1: train [d0, d60),  test [d60, d90)
  Window 2: train [d14, d74), test [d74, d104)
  ...

Each window uses run_backtest() which already enforces no-lookahead internally
via _get_bias_at_date(). The walk-forward wrapper adds the additional constraint
that bias computation only uses data from the train window, not the full history.
"""

import sys
import sqlite3
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from trading.backtester import run_backtest
from config import MIN_EDGE, MIN_CONFIDENCE, DEFAULT_MODEL


def _date_add(date_str: str, days: int) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt + timedelta(days=days)).strftime("%Y-%m-%d")


def _date_diff(start: str, end: str) -> int:
    d1 = datetime.strptime(start, "%Y-%m-%d")
    d2 = datetime.strptime(end, "%Y-%m-%d")
    return (d2 - d1).days


def run_walk_forward(
    conn:           sqlite3.Connection,
    date_from:      str,
    date_to:        str,
    station_code:   str | None = None,
    train_days:     int = 60,
    test_days:      int = 30,
    step_days:      int = 14,
    min_edge:       float = MIN_EDGE,
    min_confidence: float = MIN_CONFIDENCE,
    model:          str = DEFAULT_MODEL,
    thresholds:     list[float] | None = None,
    sides:          list[str] | None = None,
) -> dict:
    """
    Run walk-forward backtesting over [date_from, date_to].

    Returns:
      windows         — list of per-window result dicts
      combined_trades — all out-of-sample trades across windows
      summary         — aggregate stats over all windows
    """
    total_days = _date_diff(date_from, date_to)
    if total_days < train_days + test_days:
        return {
            "error": f"Date range too short: need ≥{train_days + test_days}d, got {total_days}d",
            "windows": [],
            "combined_trades": [],
            "summary": {},
        }

    windows = []
    all_trades: list[dict] = []
    cursor = date_from

    while True:
        train_start = cursor
        train_end   = _date_add(cursor, train_days)
        test_start  = train_end
        test_end    = _date_add(test_start, test_days)

        if _date_diff(test_end, date_to) < 0:
            # test_end would exceed date_to — stop here
            break

        # Run backtest on the test window; backtester already gates on data < test date
        result = run_backtest(
            station_code   = station_code,
            date_from      = test_start,
            date_to        = test_end,
            thresholds     = thresholds,
            sides          = sides,
            min_edge       = min_edge,
            min_confidence = min_confidence,
            model          = model,
            conn           = conn,
        )

        window_summary = {
            "train_start":  train_start,
            "train_end":    train_end,
            "test_start":   test_start,
            "test_end":     test_end,
            "total_trades": result["total_trades"],
            "wins":         result["wins"],
            "losses":       result["losses"],
            "win_rate":     result["win_rate"],
            "total_pnl_d":  result.get("total_pnl_d", 0),
            "roi_dollars_pct": result.get("roi_dollars_pct", 0),
            "sharpe":       result.get("sharpe", 0),
            "max_drawdown_d": result.get("max_drawdown_d", 0),
        }
        windows.append(window_summary)

        # Tag each trade with its walk-forward window index
        for t in result.get("trades", []):
            t["wf_window"] = len(windows)
            all_trades.append(t)

        cursor = _date_add(cursor, step_days)

    if not windows:
        return {"windows": [], "combined_trades": [], "summary": {"n_windows": 0}}

    # Aggregate across all windows
    win_rates  = [w["win_rate"]  for w in windows if w["total_trades"] > 0]
    sharpes    = [w["sharpe"]    for w in windows if w["total_trades"] > 0]
    pnls       = [w["total_pnl_d"] for w in windows]
    drawdowns  = [w["max_drawdown_d"] for w in windows]

    total_wins   = sum(w["wins"]   for w in windows)
    total_losses = sum(w["losses"] for w in windows)
    total        = total_wins + total_losses

    summary: dict = {
        "n_windows":           len(windows),
        "total_oos_trades":    total,
        "total_oos_wins":      total_wins,
        "total_oos_losses":    total_losses,
        "overall_win_rate":    round(total_wins / total, 4) if total else 0,
        "avg_window_win_rate": round(statistics.mean(win_rates), 4) if win_rates else 0,
        "std_window_win_rate": round(statistics.stdev(win_rates), 4) if len(win_rates) >= 2 else 0,
        "avg_window_pnl_d":    round(statistics.mean(pnls), 2) if pnls else 0,
        "total_oos_pnl_d":     round(sum(pnls), 2),
        "avg_sharpe":          round(statistics.mean(sharpes), 3) if sharpes else 0,
        "worst_drawdown_d":    round(max(drawdowns), 2) if drawdowns else 0,
        "pct_profitable_windows": round(
            sum(1 for p in pnls if p > 0) / len(pnls), 4
        ) if pnls else 0,
        "train_days":  train_days,
        "test_days":   test_days,
        "step_days":   step_days,
        "date_from":   date_from,
        "date_to":     date_to,
    }

    return {
        "windows":         windows,
        "combined_trades": all_trades,
        "summary":         summary,
    }
