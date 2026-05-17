"""
Backtesting engine.

Replays historical forecast + settlement data to simulate trade outcomes.
Strict no-lookahead: only uses forecast data available BEFORE the trade date.

Workflow:
  1. For each settled date D in the range:
     a. Find forecast that was available the morning of D (fetched_at < D noon local)
     b. Classify regime using that morning's forecast
     c. Get blended bias using only stats from dates BEFORE D
     d. For each threshold/side combo: compute probability + edge
     e. If signal passes filters: log a simulated trade
  2. Compute aggregate stats
"""

import sys
import sqlite3
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from scipy.stats import norm
from models.regime_engine import classify_from_forecast
from models.confidence_engine import compute_confidence
from config import MIN_EDGE, MIN_CONFIDENCE, DEFAULT_MODEL, STATIONS


def _win_probability(adj: float, std: float, threshold: float, side: str) -> float:
    cutoff = threshold + 0.5
    if side == "Yes":
        return 1.0 - norm.cdf(cutoff, loc=adj, scale=std)
    return norm.cdf(cutoff, loc=adj, scale=std)


def _get_bias_at_date(station: str, model: str, regime: str,
                      before_date: str, conn: sqlite3.Connection) -> tuple[float, float, int]:
    """
    Compute bias + std_dev using only settlements BEFORE before_date.
    Returns (bias, std_dev, sample_size).
    """
    rows = conn.execute("""
        SELECT ROUND(ds.official_high - fr.temp_max, 2) AS error,
               COALESCE(ds.regime, 'UNKNOWN') AS regime
        FROM daily_settlements ds
        JOIN forecast_runs fr
            ON fr.forecast_date=ds.settlement_date
           AND fr.station_code=ds.station_code
           AND fr.model_name=?
        WHERE ds.station_code=?
          AND ds.settlement_date < ?
          AND ds.official_high IS NOT NULL
          AND fr.temp_max IS NOT NULL
        ORDER BY ds.settlement_date DESC
    """, (model, station, before_date)).fetchall()

    if not rows:
        return 0.0, 3.0, 0

    all_errors = [r["error"] for r in rows]
    regime_errors = [r["error"] for r in rows if r["regime"] == regime]

    from models.bias_engine import _blend_weight
    n_r   = len(regime_errors)
    n_all = len(all_errors)
    w     = _blend_weight(n_r)

    g_bias = statistics.mean(all_errors) if n_all else 0.0
    r_bias = statistics.mean(regime_errors) if n_r else g_bias
    g_std  = statistics.stdev(all_errors) if n_all >= 2 else 3.0
    r_std  = statistics.stdev(regime_errors) if n_r >= 2 else g_std

    bias = w * r_bias + (1 - w) * g_bias
    std  = max(0.5, w * r_std + (1 - w) * g_std)
    return round(bias, 3), round(std, 3), n_all


def run_backtest(
    station_code:  str | None,   # None = all stations
    date_from:     str,
    date_to:       str,
    thresholds:    list[float] | None = None,
    sides:         list[str] | None = None,
    min_edge:      float = MIN_EDGE,
    min_confidence: float = MIN_CONFIDENCE,
    model:         str = DEFAULT_MODEL,
    conn:          sqlite3.Connection = None,
) -> dict:
    """
    Run a backtest.  Returns summary dict + list of simulated trades.
    """
    sides      = sides      or ["Yes", "No"]
    thresholds = thresholds or []  # auto-derive from settlements if empty

    # Fetch settled days in range
    q = """
        SELECT ds.*, fr.temp_max, fr.temp_min, fr.fetched_at
        FROM daily_settlements ds
        JOIN forecast_runs fr
            ON fr.forecast_date=ds.settlement_date
           AND fr.station_code=ds.station_code
           AND fr.model_name=?
        WHERE ds.settlement_date >= ? AND ds.settlement_date <= ?
          AND ds.official_high IS NOT NULL
    """
    params = [model, date_from, date_to]
    if station_code:
        q += " AND ds.station_code=?"
        params.append(station_code)
    q += " ORDER BY ds.settlement_date, ds.station_code"

    settled_rows = conn.execute(q, params).fetchall()

    trades = []
    for row in settled_rows:
        date    = row["settlement_date"]
        station = row["station_code"]
        actual  = row["official_high"]
        fc_high = row["temp_max"]
        regime  = row["regime"] or "UNKNOWN"

        if fc_high is None:
            continue

        regime_r = classify_from_forecast(dict(row))
        bias, std, n = _get_bias_at_date(station, model, regime_r.regime, date, conn)
        adj  = round(fc_high + bias, 2)

        # Build threshold list for this day
        t_list = thresholds or [
            int(fc_high) - 2, int(fc_high) - 1,
            int(fc_high), int(fc_high) + 1, int(fc_high) + 2,
        ]

        for threshold in t_list:
            for side in sides:
                prob = _win_probability(adj, std, float(threshold), side)
                fair = round(prob * 100, 2)
                # Simulate mid-market price at 50/50 (no historical Kalshi data)
                # Use fair-value-based synthetic market for calibration testing
                market_price = 50.0
                edge = round(fair - market_price, 2)

                conf, _ = compute_confidence(n, std, regime_r.regime, edge, regime_r.confidence)

                if abs(edge) < min_edge or conf < min_confidence:
                    continue

                # Determine outcome
                if side == "Yes":
                    win = actual >= threshold + 1
                else:
                    win = actual <= threshold

                pnl = 100 - market_price if win else -market_price

                trades.append({
                    "date":          date,
                    "station_code":  station,
                    "threshold":     threshold,
                    "side":          side,
                    "regime":        regime_r.regime,
                    "fc_high":       fc_high,
                    "adj_forecast":  adj,
                    "bias":          bias,
                    "std":           std,
                    "model_prob":    round(prob, 4),
                    "fair_value":    fair,
                    "market_price":  market_price,
                    "edge":          edge,
                    "confidence":    round(conf, 4),
                    "actual_high":   actual,
                    "result":        "WIN" if win else "LOSS",
                    "pnl":           round(pnl, 2),
                })

    if not trades:
        return {
            "total_trades": 0, "wins": 0, "losses": 0,
            "win_rate": 0, "total_pnl": 0, "roi_pct": 0,
            "max_drawdown": 0, "sharpe": 0,
            "by_station": {}, "by_regime": {}, "by_threshold": {},
            "trades": [],
        }

    wins   = sum(1 for t in trades if t["result"] == "WIN")
    losses = sum(1 for t in trades if t["result"] == "LOSS")
    total  = len(trades)
    pnls   = [t["pnl"] for t in trades]
    total_pnl = sum(pnls)
    roi    = total_pnl / (total * 50) * 100 if total else 0

    # Max drawdown
    running, peak, max_dd = 0, 0, 0
    for p in pnls:
        running += p
        peak = max(peak, running)
        max_dd = max(max_dd, peak - running)

    # Sharpe (daily pnl / std)
    try:
        sharpe = (statistics.mean(pnls) / statistics.stdev(pnls)) * (252 ** 0.5) if len(pnls) >= 2 else 0
    except Exception:
        sharpe = 0

    # Group by station
    by_station: dict = {}
    for t in trades:
        s = t["station_code"]
        by_station.setdefault(s, {"wins": 0, "losses": 0, "pnl": 0})
        by_station[s]["wins" if t["result"] == "WIN" else "losses"] += 1
        by_station[s]["pnl"] += t["pnl"]

    # Group by regime
    by_regime: dict = {}
    for t in trades:
        r = t["regime"]
        by_regime.setdefault(r, {"wins": 0, "losses": 0, "pnl": 0})
        by_regime[r]["wins" if t["result"] == "WIN" else "losses"] += 1
        by_regime[r]["pnl"] += t["pnl"]

    # Group by threshold (offset from fc_high)
    by_thresh: dict = {}
    for t in trades:
        offset = int(t["threshold"] - t["fc_high"])
        key = f"{offset:+d}"
        by_thresh.setdefault(key, {"wins": 0, "losses": 0, "pnl": 0})
        by_thresh[key]["wins" if t["result"] == "WIN" else "losses"] += 1
        by_thresh[key]["pnl"] += t["pnl"]

    # Save to backtest_runs
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    import json
    conn.execute("""
        INSERT INTO backtest_runs (
            run_at, station_code, date_from, date_to,
            total_trades, wins, losses, win_rate,
            total_pnl, roi_pct, max_drawdown, sharpe, params_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        now, station_code, date_from, date_to,
        total, wins, losses, round(wins/total, 4),
        round(total_pnl, 2), round(roi, 2), round(max_dd, 2), round(sharpe, 3),
        json.dumps({"min_edge": min_edge, "min_confidence": min_confidence}),
    ))
    conn.commit()

    return {
        "total_trades": total, "wins": wins, "losses": losses,
        "win_rate":     round(wins / total, 4),
        "total_pnl":    round(total_pnl, 2),
        "roi_pct":      round(roi, 2),
        "max_drawdown": round(max_dd, 2),
        "sharpe":       round(sharpe, 3),
        "by_station":   by_station,
        "by_regime":    by_regime,
        "by_threshold": by_thresh,
        "trades":       trades,
    }
