"""
Fee-aware edge calculation for Kalshi binary prediction markets.

Kalshi fee model:
  - Settlement fee on net profit from winning contracts only (not on cost)
  - Rate: configurable via KALSHI_SETTLEMENT_FEE_PCT (default 3%)
  - No entry/exit transaction fees on binary contracts themselves
  - Spread cost: takers must cross half the bid/ask spread to fill

Maker vs Taker:
  TAKER — executes at best ask (Yes buy) immediately; pays half-spread extra
           but guarantees fill. Default assumption for paper trading.
  MAKER — places limit order at mid; zero spread cost but probabilistic fill.
           We model MAKER fill probability at 70% for comparison purposes.

Net fair value derivation (break-even price after fee):
  EV = 0  ⟹  prob × (100−p) × (1−fee) = (1−prob) × p
  ⟹  p_fair = prob × 100 × (1−fee) / (1 − prob × fee)

This is more accurate than the approximation  p_fair ≈ prob × (100 − fee_pct)
which the simplified edge_calculator uses for speed.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import KALSHI_SETTLEMENT_FEE_PCT, DEFAULT_ORDER_TYPE, MIN_NET_EDGE

MAKER_FILL_PROBABILITY = 0.70   # assumed fill rate for limit orders at mid


# ── Core math ──────────────────────────────────────────────────────────────────

def net_fair_value(win_prob: float, fee_rate: float | None = None) -> float:
    """
    Exact break-even contract price (cents) after Kalshi settlement fee.

    Derived from setting EV = 0:
      p_fair = prob × 100 × (1 − fee) / (1 − prob × fee)

    For extreme probabilities near 0 or 1, falls back gracefully.
    """
    fee = (KALSHI_SETTLEMENT_FEE_PCT / 100) if fee_rate is None else fee_rate
    if win_prob <= 0:
        return 0.0
    if win_prob >= 1:
        return round(100 * (1 - fee), 4)
    denominator = 1 - win_prob * fee
    if denominator <= 0:
        return 0.0
    return round(win_prob * 100 * (1 - fee) / denominator, 4)


def expected_settlement_fee_cents(
    win_prob: float, entry_price: float, fee_rate: float | None = None
) -> float:
    """
    Expected Kalshi settlement fee in cents per contract.

    Only winning contracts pay the fee, on their profit:
      E[fee] = prob × fee_rate × (100 − entry_price)
    """
    fee = (KALSHI_SETTLEMENT_FEE_PCT / 100) if fee_rate is None else fee_rate
    return round(win_prob * fee * max(0.0, 100.0 - entry_price), 4)


# ── Full breakdown ─────────────────────────────────────────────────────────────

def estimate_fees(
    win_prob: float,
    market_price_mid: float,    # mid-market price in cents (0–100)
    best_bid: float | None = None,
    best_ask: float | None = None,
    order_type: str | None = None,
    fee_rate: float | None = None,
) -> dict:
    """
    Full cost breakdown for one proposed contract position.

    Returns a dict suitable for logging to paper_trades and the dashboard.

    Keys:
      gross_fair          ¢  prob × 100 (no fees, no spread)
      gross_edge          ¢  gross_fair − market_price_mid
      net_fair            ¢  exact break-even price after Kalshi fee
      net_edge            ¢  net_fair − effective_entry_price  (TAKER or MAKER)
      net_edge_taker      ¢  net_fair − (mid + half_spread)
      net_edge_maker      ¢  net_fair − mid  (if filled at mid)
      effective_price     ¢  actual price paid given order_type
      spread              ¢  full bid/ask spread (0 if unavailable)
      spread_cost_cents   ¢  cost of crossing spread (0 for MAKER)
      expected_fee_cents  ¢  expected settlement fee per contract
      fee_rate_pct        %  fee rate used
      order_type             "TAKER" or "MAKER"
      is_tradeable           net_edge > MIN_NET_EDGE
      is_tradeable_maker     net_edge_maker > MIN_NET_EDGE
      fee_pct_of_gross       fee ÷ |gross_edge| — edge erosion fraction
      edge_erosion_pct    %  total erosion (fee + spread) ÷ |gross_edge|
      maker_advantage     ¢  improvement from MAKER vs TAKER
    """
    fee = (KALSHI_SETTLEMENT_FEE_PCT / 100) if fee_rate is None else fee_rate
    otype = order_type or DEFAULT_ORDER_TYPE

    # ── Spread ────────────────────────────────────────────────────────────────
    spread = 0.0
    if best_bid is not None and best_ask is not None and best_ask > best_bid:
        spread = round(best_ask - best_bid, 2)
    half_spread = round(spread / 2, 3)

    # ── Effective entry price ─────────────────────────────────────────────────
    if otype == "TAKER":
        effective_price = round(market_price_mid + half_spread, 3)
        spread_cost     = half_spread
    else:  # MAKER
        effective_price = market_price_mid
        spread_cost     = 0.0

    # ── Gross values ─────────────────────────────────────────────────────────
    gross_fair  = round(win_prob * 100, 4)
    gross_edge  = round(gross_fair - market_price_mid, 4)   # vs mid (pre-spread)

    # ── Fee components ────────────────────────────────────────────────────────
    exp_fee     = expected_settlement_fee_cents(win_prob, effective_price, fee)
    exp_fee_mid = expected_settlement_fee_cents(win_prob, market_price_mid, fee)

    # ── Net values ────────────────────────────────────────────────────────────
    nfv = net_fair_value(win_prob, fee)

    # Net edge for taker (pays ask, incurs spread cost + fee)
    net_edge_taker = round(nfv - effective_price, 4)

    # Net edge for maker (fills at mid, pays fee but no spread cost)
    net_edge_maker = round(nfv - market_price_mid, 4)

    # Primary net edge based on chosen order_type
    net_edge = net_edge_taker if otype == "TAKER" else net_edge_maker

    # ── Erosion metrics ───────────────────────────────────────────────────────
    abs_gross = abs(gross_edge)
    fee_pct_of_gross   = round(exp_fee / abs_gross, 4)   if abs_gross > 0 else 0.0
    spread_pct_of_gross = round(spread_cost / abs_gross, 4) if abs_gross > 0 else 0.0
    edge_erosion_pct   = round(
        (exp_fee + spread_cost) / abs_gross * 100, 2) if abs_gross > 0 else 0.0

    return {
        "gross_fair":           round(gross_fair, 2),
        "gross_edge":           round(gross_edge, 2),
        "net_fair":             round(nfv, 2),
        "net_edge":             round(net_edge, 2),
        "net_edge_taker":       round(net_edge_taker, 2),
        "net_edge_maker":       round(net_edge_maker, 2),
        "effective_price":      round(effective_price, 2),
        "spread":               round(spread, 2),
        "spread_cost_cents":    round(spread_cost, 2),
        "expected_fee_cents":   round(exp_fee, 2),
        "fee_rate_pct":         round(fee * 100, 2),
        "order_type":           otype,
        "is_tradeable":         net_edge > MIN_NET_EDGE,
        "is_tradeable_maker":   net_edge_maker > MIN_NET_EDGE,
        "maker_advantage":      round(net_edge_maker - net_edge_taker, 2),
        "fee_pct_of_gross":     fee_pct_of_gross,
        "spread_pct_of_gross":  spread_pct_of_gross,
        "edge_erosion_pct":     edge_erosion_pct,
        "maker_fill_prob":      MAKER_FILL_PROBABILITY,
    }


# ── Realized settlement fee on a closed trade ──────────────────────────────────

def realized_fee_dollars(
    stake_dollars: float,
    entry_price_cents: float,
    result: str,
    fee_rate: float | None = None,
) -> float:
    """
    Kalshi settlement fee actually paid on a closed trade (dollars).

    For wins:   fee = fee_rate × gross_profit = fee_rate × stake × (100−p)/p
    For losses: fee = 0  (no fee on losing contracts)
    """
    if result != "WIN" or entry_price_cents <= 0:
        return 0.0
    fee = (KALSHI_SETTLEMENT_FEE_PCT / 100) if fee_rate is None else fee_rate
    gross_profit_d = stake_dollars * (100.0 - entry_price_cents) / entry_price_cents
    return round(fee * gross_profit_d, 4)


def net_pnl_after_fee(
    stake_dollars: float,
    entry_price_cents: float,
    result: str,
    fee_rate: float | None = None,
) -> tuple[float, float, float]:
    """
    Compute (gross_pnl_dollars, fee_dollars, net_pnl_dollars) for a settled trade.

    gross_pnl_dollars — profit before Kalshi fee (or loss amount)
    fee_dollars       — fee paid to Kalshi (0 on losses)
    net_pnl_dollars   — final P&L credited to bankroll
    """
    fee = (KALSHI_SETTLEMENT_FEE_PCT / 100) if fee_rate is None else fee_rate
    if entry_price_cents <= 0:
        return 0.0, 0.0, 0.0

    if result == "WIN":
        gross_pnl_d = round(stake_dollars * (100.0 - entry_price_cents) / entry_price_cents, 4)
        fee_d       = round(fee * gross_pnl_d, 4)
        net_pnl_d   = round(gross_pnl_d - fee_d, 4)
    else:
        gross_pnl_d = round(-stake_dollars, 4)
        fee_d       = 0.0
        net_pnl_d   = gross_pnl_d

    return gross_pnl_d, fee_d, net_pnl_d
