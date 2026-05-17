"""
Market microstructure engine.

Measures how fast markets adapt to signals, how quickly edge decays,
and which stations/regimes have lasting vs ephemeral edge.

Key concepts:
  Edge half-life    — time (minutes) for observed edge to decay to half its entry value
  Price velocity    — rate of market-price change (¢ per minute)
  CLV               — closing-line value: entry price vs final pre-settlement price
  Market lag        — minutes from signal generation to market reaction
  Liquidity score   — edge surviving after realistic spread costs
"""

import sys
import math
import sqlite3
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))


# ── CLV Calculation ────────────────────────────────────────────────────────────

def compute_clv(paper_trade_id: int, conn: sqlite3.Connection) -> dict | None:
    """
    Closing-line value for a single closed trade.

    CLV = fair_value_at_entry − final_market_price_before_settlement
    Positive CLV = we entered before the market moved in our favour.
    """
    trade = conn.execute("""
        SELECT entry_price, fair_value, gross_edge, net_edge, opened_at,
               station_code, threshold_f, side, result
        FROM paper_trades WHERE id=? AND status='CLOSED'
    """, (paper_trade_id,)).fetchone()

    if not trade:
        return None

    # Find the latest CLV snapshot (closest to settlement)
    latest_snap = conn.execute("""
        SELECT market_price, minutes_after_open, captured_at
        FROM market_price_snapshots
        WHERE paper_trade_id=?
        ORDER BY minutes_after_open DESC
        LIMIT 1
    """, (paper_trade_id,)).fetchone()

    if not latest_snap:
        return None

    closing_price = latest_snap["market_price"]
    entry_price   = trade["entry_price"]
    fair_value    = trade["fair_value"] or entry_price

    clv = round(fair_value - closing_price, 2)

    return {
        "paper_trade_id":  paper_trade_id,
        "entry_price":     entry_price,
        "closing_price":   closing_price,
        "clv":             clv,
        "clv_positive":    clv > 0,
        "fair_value":      fair_value,
        "minutes_tracked": latest_snap["minutes_after_open"],
    }


def compute_clv_summary(conn: sqlite3.Connection,
                        station: str | None = None) -> dict:
    """
    Aggregate CLV stats: avg, pct positive, by station, by regime.
    """
    q = """
        SELECT pt.id, pt.entry_price, pt.fair_value, pt.station_code,
               pt.regime, pt.grade, pt.result,
               mps.market_price AS closing_price
        FROM paper_trades pt
        JOIN (
            SELECT paper_trade_id, market_price
            FROM market_price_snapshots
            WHERE (paper_trade_id, minutes_after_open) IN (
                SELECT paper_trade_id, MAX(minutes_after_open)
                FROM market_price_snapshots
                GROUP BY paper_trade_id
            )
        ) mps ON mps.paper_trade_id = pt.id
        WHERE pt.status='CLOSED'
    """
    params = []
    if station:
        q += " AND pt.station_code=?"
        params.append(station)

    rows = conn.execute(q, params).fetchall()
    if not rows:
        return {"n": 0, "avg_clv": 0, "pct_positive": 0}

    clvs = [
        (r["fair_value"] or r["entry_price"]) - r["closing_price"]
        for r in rows if r["closing_price"] is not None
    ]
    if not clvs:
        return {"n": 0}

    return {
        "n":            len(clvs),
        "avg_clv":      round(statistics.mean(clvs), 3),
        "median_clv":   round(statistics.median(clvs), 3),
        "pct_positive": round(sum(1 for c in clvs if c > 0) / len(clvs), 4),
        "std_clv":      round(statistics.stdev(clvs), 3) if len(clvs) >= 2 else 0,
    }


# ── Edge Decay / Half-Life ─────────────────────────────────────────────────────

def compute_edge_halflife(
    paper_trade_ids: list[int],
    conn: sqlite3.Connection,
) -> dict:
    """
    Estimate how quickly edge decays after entry.

    Method: for each trade, compute edge at each price snapshot relative
    to entry edge. Fit an exponential decay curve and return the half-life.

    Returns:
      half_life_minutes   — estimated minutes for edge to halve
      decay_rate          — λ in e^(-λt)
      avg_edge_by_bucket  — dict of {time_bucket: avg_edge_fraction}
    """
    if not paper_trade_ids:
        return {"half_life_minutes": None, "decay_rate": None, "n": 0}

    # Gather snapshots for all trades
    placeholders = ",".join("?" * len(paper_trade_ids))
    rows = conn.execute(f"""
        SELECT mps.paper_trade_id, mps.minutes_after_open, mps.market_price,
               pt.entry_price, pt.fair_value, pt.gross_edge
        FROM market_price_snapshots mps
        JOIN paper_trades pt ON pt.id = mps.paper_trade_id
        WHERE mps.paper_trade_id IN ({placeholders})
          AND mps.minutes_after_open > 0
          AND pt.gross_edge IS NOT NULL AND pt.gross_edge != 0
        ORDER BY mps.paper_trade_id, mps.minutes_after_open
    """, paper_trade_ids).fetchall()

    if not rows:
        return {"half_life_minutes": None, "decay_rate": None, "n": 0}

    # Group by time bucket and compute average edge fraction remaining
    buckets: dict[int, list[float]] = {}
    for r in rows:
        if r["fair_value"] is None or r["entry_price"] is None:
            continue
        current_edge = (r["fair_value"] - r["market_price"])
        initial_edge = r["gross_edge"]
        if abs(initial_edge) < 0.5:
            continue
        fraction = current_edge / initial_edge
        t = r["minutes_after_open"]
        buckets.setdefault(t, []).append(fraction)

    if len(buckets) < 2:
        return {"half_life_minutes": None, "decay_rate": None, "n": len(paper_trade_ids)}

    avg_by_bucket = {t: statistics.mean(fracs) for t, fracs in buckets.items()}

    # Estimate decay rate via log regression on positive fractions
    data_points = [
        (t, avg) for t, avg in avg_by_bucket.items()
        if avg > 0.01
    ]
    if len(data_points) < 2:
        return {
            "half_life_minutes": None, "decay_rate": None,
            "avg_edge_by_bucket": avg_by_bucket, "n": len(paper_trade_ids)
        }

    # Simple linear regression on log(fraction) vs time → λ = -slope
    xs = [d[0] for d in data_points]
    ys = [math.log(max(d[1], 0.001)) for d in data_points]
    n = len(xs)
    x_bar, y_bar = sum(xs) / n, sum(ys) / n
    denom = sum((x - x_bar) ** 2 for x in xs)
    if denom == 0:
        return {"half_life_minutes": None, "decay_rate": None, "n": n}

    slope = sum((xs[i] - x_bar) * (ys[i] - y_bar) for i in range(n)) / denom
    decay_rate = -slope  # λ = -slope
    half_life  = math.log(2) / decay_rate if decay_rate > 0 else None

    return {
        "half_life_minutes":  round(half_life, 1) if half_life else None,
        "decay_rate":         round(decay_rate, 6),
        "avg_edge_by_bucket": {str(k): round(v, 4) for k, v in sorted(avg_by_bucket.items())},
        "n":                  len(paper_trade_ids),
        "data_points":        len(data_points),
    }


# ── Price Velocity ─────────────────────────────────────────────────────────────

def compute_price_velocity(
    market_ticker: str,
    conn: sqlite3.Connection,
    window_minutes: int = 60,
) -> dict:
    """
    Rate of price change (¢ per minute) for a market in the last window.

    Positive velocity = market moving toward Yes (price rising).
    Negative velocity = market moving toward No (price falling).
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=window_minutes))
    cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    snaps = conn.execute("""
        SELECT market_price, captured_at
        FROM market_snapshots
        WHERE market_ticker=? AND captured_at >= ?
        ORDER BY captured_at ASC
    """, (market_ticker, cutoff_str)).fetchall()

    if len(snaps) < 2:
        return {"ticker": market_ticker, "velocity": 0.0, "n": len(snaps)}

    prices = [s["market_price"] for s in snaps if s["market_price"] is not None]
    if len(prices) < 2:
        return {"ticker": market_ticker, "velocity": 0.0, "n": 0}

    # Simple first-last over window
    first_ts = datetime.strptime(snaps[0]["captured_at"], "%Y-%m-%dT%H:%M:%SZ")
    last_ts  = datetime.strptime(snaps[-1]["captured_at"], "%Y-%m-%dT%H:%M:%SZ")
    elapsed_min = (last_ts - first_ts).total_seconds() / 60 or 1

    velocity = round((prices[-1] - prices[0]) / elapsed_min, 4)

    # Acceleration = change in velocity over halves
    mid = len(prices) // 2
    v1 = (prices[mid] - prices[0]) / (elapsed_min / 2 or 1)
    v2 = (prices[-1] - prices[mid]) / (elapsed_min / 2 or 1)
    acceleration = round(v2 - v1, 4)

    return {
        "ticker":         market_ticker,
        "velocity":       velocity,       # ¢/minute
        "acceleration":   acceleration,   # ¢/minute² (change in velocity)
        "price_start":    prices[0],
        "price_end":      prices[-1],
        "price_delta":    round(prices[-1] - prices[0], 2),
        "window_minutes": window_minutes,
        "n":              len(prices),
    }


# ── Market Lag Analysis ────────────────────────────────────────────────────────

def compute_market_lag_stats(conn: sqlite3.Connection) -> dict:
    """
    Estimate how quickly the market responds to information by comparing
    CLV snapshots at t+15 vs t+60 min — large CLV decay = fast market.
    """
    # Get CLV at 15 min and 60 min buckets for all trades
    rows = conn.execute("""
        SELECT
            mps15.market_price AS price_15,
            mps60.market_price AS price_60,
            pt.fair_value,
            pt.entry_price,
            pt.gross_edge
        FROM paper_trades pt
        LEFT JOIN market_price_snapshots mps15
            ON mps15.paper_trade_id=pt.id AND mps15.minutes_after_open=15
        LEFT JOIN market_price_snapshots mps60
            ON mps60.paper_trade_id=pt.id AND mps60.minutes_after_open=60
        WHERE pt.status='CLOSED'
          AND mps15.market_price IS NOT NULL
          AND mps60.market_price IS NOT NULL
          AND pt.gross_edge IS NOT NULL
    """).fetchall()

    if not rows:
        return {"n": 0, "avg_lag_minutes": None}

    edge_15 = [(r["fair_value"] - r["price_15"]) / max(abs(r["gross_edge"]), 0.01)
               for r in rows if r["fair_value"] is not None]
    edge_60 = [(r["fair_value"] - r["price_60"]) / max(abs(r["gross_edge"]), 0.01)
               for r in rows if r["fair_value"] is not None]

    if not edge_15 or not edge_60:
        return {"n": 0}

    return {
        "n":                    len(rows),
        "avg_edge_fraction_15": round(statistics.mean(edge_15), 4),
        "avg_edge_fraction_60": round(statistics.mean(edge_60), 4),
        "pct_edge_lost_by_60":  round(1 - statistics.mean(edge_60), 4),
        "note": (
            "Edge fraction remaining at t+15 and t+60. "
            "Values <1 indicate market is adapting toward fair value."
        ),
    }


# ── Liquidity-Adjusted Edge ────────────────────────────────────────────────────

def liquidity_adjusted_edge(
    gross_edge: float,
    spread: float | None,
    volume: float | None,
    fee_rate: float = 0.03,
) -> dict:
    """
    Compute edge after realistic spread and fee costs, with a liquidity
    discount for low-volume markets.

    volume_discount: 0 = no discount (deep market), 1 = trade blocked
    """
    spread = spread or 0.0
    spread_cost = spread / 2   # taker pays half-spread above mid

    # Liquidity discount: thin markets get a penalty on tradeable size
    volume_discount = 0.0
    if volume is not None:
        if volume < 50:
            volume_discount = 0.20   # 20% size discount (thin book)
        elif volume < 200:
            volume_discount = 0.05

    net = round(gross_edge - spread_cost - fee_rate * max(gross_edge, 0), 2)
    tradeable_size_pct = round(1.0 - volume_discount, 2)

    return {
        "gross_edge":         round(gross_edge, 2),
        "spread_cost":        round(spread_cost, 2),
        "fee_cost":           round(fee_rate * max(gross_edge, 0), 2),
        "net_edge":           net,
        "volume_discount":    volume_discount,
        "tradeable_size_pct": tradeable_size_pct,
        "is_liquid_enough":   volume_discount < 0.15,
        "is_tradeable":       net > 0 and tradeable_size_pct > 0.5,
    }
