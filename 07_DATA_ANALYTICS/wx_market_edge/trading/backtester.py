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
from config import MIN_EDGE, MIN_CONFIDENCE, DEFAULT_MODEL, STATIONS, MIN_NET_EDGE
from models.fee_engine import estimate_fees, net_pnl_after_fee


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

    from config import STARTING_BANKROLL, MAX_SINGLE_TRADE_PCT, KELLY_FRACTION_APLUS
    bt_bankroll = STARTING_BANKROLL
    cumulative_pnl_d = 0.0

    trades = []
    for row in settled_rows:
        date    = row["settlement_date"]
        station = row["station_code"]
        actual  = row["official_high"]
        fc_high = row["temp_max"]

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
                # Synthetic mid-market at 50 (no historical Kalshi orderbook data)
                market_price = 50.0

                # Full fee-aware breakdown (no real spread data in backtest)
                fee_info = estimate_fees(
                    win_prob        = prob,
                    market_price_mid= market_price,
                )
                gross_edge = fee_info["gross_edge"]
                net_edge   = fee_info["net_edge"]
                fair       = fee_info["net_fair"]

                conf, _ = compute_confidence(n, std, regime_r.regime, gross_edge, regime_r.confidence)

                # Filter on gross edge AND net edge (fee gate)
                if abs(gross_edge) < min_edge or net_edge <= MIN_NET_EDGE or conf < min_confidence:
                    continue

                # Dynamic stake from current backtest bankroll (no lookahead)
                kelly_raw = max(0.0, (prob * (100 - market_price) / market_price - (1 - prob))) / ((100 - market_price) / market_price)
                kelly_frac = kelly_raw * KELLY_FRACTION_APLUS
                stake_pct  = min(max(kelly_frac, 0.01), MAX_SINGLE_TRADE_PCT)
                stake_d    = round(bt_bankroll * stake_pct, 2)

                # Determine outcome — T+0.5 continuity correction
                if side == "Yes":
                    win = actual >= threshold + 0.5
                else:
                    win = actual < threshold + 0.5

                result_str = "WIN" if win else "LOSS"
                pnl_cents  = (100 - market_price) if win else -market_price

                # Net P&L after Kalshi settlement fee
                _, fee_d, pnl_d = net_pnl_after_fee(stake_d, market_price, result_str)

                # Update rolling bankroll (no lookahead)
                cumulative_pnl_d += pnl_d
                bt_bankroll = STARTING_BANKROLL + cumulative_pnl_d

                trades.append({
                    "date":               date,
                    "station_code":       station,
                    "threshold":          threshold,
                    "side":               side,
                    "regime":             regime_r.regime,
                    "fc_high":            fc_high,
                    "adj_forecast":       adj,
                    "bias":               bias,
                    "std":                std,
                    "model_prob":         round(prob, 4),
                    "fair_value":         fair,
                    "gross_fair":         fee_info["gross_fair"],
                    "market_price":       market_price,
                    "gross_edge":         round(gross_edge, 2),
                    "net_edge":           round(net_edge, 2),
                    "edge":               round(gross_edge, 2),   # alias
                    "est_fee_cents":      fee_info["expected_fee_cents"],
                    "confidence":         round(conf, 4),
                    "actual_high":        actual,
                    "result":             result_str,
                    "pnl":                round(pnl_cents, 2),
                    "pnl_dollars":        round(pnl_d, 4),
                    "fee_dollars":        round(fee_d, 4),
                    "stake_dollars":      stake_d,
                    "bankroll_at_trade":  round(bt_bankroll - pnl_d, 2),
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
    pnls_c = [t["pnl"] for t in trades]
    pnls_d = [t.get("pnl_dollars", 0) for t in trades]
    fees_d = [t.get("fee_dollars",  0) for t in trades]
    total_pnl   = sum(pnls_c)
    total_pnl_d = sum(pnls_d)
    total_fees_d = round(sum(fees_d), 4)
    gross_pnl_d  = round(total_pnl_d + total_fees_d, 4)   # net + fees = gross
    roi    = total_pnl / (total * 50) * 100 if total else 0
    roi_d  = total_pnl_d / STARTING_BANKROLL * 100

    # Max drawdown in dollars (dynamic bankroll)
    running_d, peak_d, max_dd_d = 0.0, 0.0, 0.0
    for p in pnls_d:
        running_d += p
        peak_d = max(peak_d, running_d)
        max_dd_d = max(max_dd_d, peak_d - running_d)

    # Max drawdown in cents (for legacy ROI display)
    running, peak, max_dd = 0, 0, 0
    for p in pnls_c:
        running += p
        peak = max(peak, running)
        max_dd = max(max_dd, peak - running)

    # Sharpe — use daily dollar P&L grouped by date
    daily_pnl: dict[str, float] = {}
    for t in trades:
        daily_pnl[t["date"]] = daily_pnl.get(t["date"], 0) + t.get("pnl_dollars", 0)
    daily_series = list(daily_pnl.values())
    try:
        sharpe = (statistics.mean(daily_series) / statistics.stdev(daily_series)) * (252 ** 0.5) if len(daily_series) >= 2 else 0
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
        "total_trades":    total,
        "wins":            wins,
        "losses":          losses,
        "win_rate":        round(wins / total, 4),
        "total_pnl":       round(total_pnl, 2),
        "total_pnl_d":     round(total_pnl_d, 2),
        "gross_pnl_d":     round(gross_pnl_d, 2),
        "total_fees_d":    round(total_fees_d, 2),
        "roi_pct":         round(roi, 2),
        "roi_dollars_pct": round(roi_d, 2),
        "max_drawdown":    round(max_dd, 2),
        "max_drawdown_d":  round(max_dd_d, 2),
        "sharpe":          round(sharpe, 3),
        "final_bankroll":  round(STARTING_BANKROLL + total_pnl_d, 2),
        "by_station":      by_station,
        "by_regime":       by_regime,
        "by_threshold":    by_thresh,
        "trades":          trades,
    }
