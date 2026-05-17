"""
Bet sizing engine — fractional Kelly with hard guardrails.

Sizing rules:
  Grade A+  → 0.5 × Kelly, base 4%, hard cap 5%
  Grade B   → 0.25 × Kelly, base 2%, hard cap 5%
  Other     → 0.25 × Kelly, base 1%, hard cap 5%

Then multiply by drawdown multiplier from bankroll.py.

Correlation controls: reject if station or regime exposure would exceed limits.
Daily halt: reject if daily loss limit already hit.
"""

import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    STARTING_BANKROLL,
    MAX_SINGLE_TRADE_PCT,
    MAX_STATION_EXPOSURE_PCT,
    MAX_REGIME_EXPOSURE_PCT,
    KELLY_FRACTION_NORMAL,
    KELLY_FRACTION_APLUS,
    BASE_RISK_NORMAL_PCT,
    BASE_RISK_B_PCT,
    BASE_RISK_APLUS_PCT,
    MIN_NET_EDGE,
)
from trading.bankroll import (
    get_current_bankroll,
    get_sizing_multiplier,
    get_station_exposure,
    get_regime_exposure,
    is_daily_loss_limit_hit,
    bankroll_status,
)


def kelly_fraction_raw(win_prob: float, entry_price_cents: float) -> float:
    """
    Full Kelly fraction for a binary contract.
    b = net odds on a win (win payout / cost = (100 - price) / price)
    f* = (p*b - q) / b   where q = 1 - p
    """
    if entry_price_cents <= 0 or entry_price_cents >= 100:
        return 0.0
    b = (100.0 - entry_price_cents) / entry_price_cents
    p = win_prob
    q = 1.0 - p
    f_star = (p * b - q) / b
    return max(0.0, f_star)


def size_trade(edge_result: dict, conn: sqlite3.Connection) -> dict:
    """
    Compute the dollar stake for a proposed trade.

    Returns a dict with:
      stake_dollars     – dollars to risk
      kelly_fraction    – effective Kelly fraction used
      grade             – signal grade (from edge_result or default)
      rejected          – True if trade should not be taken
      reject_reason     – explanation if rejected
      bankroll_snapshot – current bankroll state dict
    """
    grade = edge_result.get("grade", "Watchlist")
    win_prob      = edge_result.get("model_prob") or edge_result.get("win_prob") or 0.5
    entry_price   = edge_result.get("market_price") or 50.0
    station_code  = edge_result.get("station_code", "")
    regime        = edge_result.get("regime", "UNKNOWN")

    status = bankroll_status(conn)
    bankroll = status["current_bankroll"]

    net_edge = edge_result.get("net_edge")

    # ── Hard halts ────────────────────────────────────────────────────────
    if status["trading_paused"]:
        reason = ("daily loss limit hit" if status["daily_halt"]
                  else f"drawdown {status['drawdown_pct']:.1%} ≥ pause threshold")
        return _rejected(grade, status, reason)

    if bankroll <= 0:
        return _rejected(grade, status, "bankroll depleted")

    # ── Fee gate: net edge must be positive after fees + spread ──────────
    if net_edge is not None and net_edge <= MIN_NET_EDGE:
        fee_info = edge_result.get("fee_breakdown", {})
        eroded   = fee_info.get("edge_erosion_pct", 0)
        return _rejected(grade, status,
                         f"net edge {net_edge:+.1f}¢ ≤ {MIN_NET_EDGE}¢ threshold "
                         f"(fees+spread eroded {eroded:.0f}% of gross edge)")

    # ── Grade-based Kelly fraction and base risk ───────────────────────────
    if grade == "A+":
        kelly_cap  = KELLY_FRACTION_APLUS
        base_pct   = BASE_RISK_APLUS_PCT
    elif grade == "B":
        kelly_cap  = KELLY_FRACTION_NORMAL
        base_pct   = BASE_RISK_B_PCT
    else:
        kelly_cap  = KELLY_FRACTION_NORMAL
        base_pct   = BASE_RISK_NORMAL_PCT

    raw_kelly  = kelly_fraction_raw(win_prob, entry_price)
    frac_kelly = raw_kelly * kelly_cap   # apply fractional-Kelly scale factor

    # Effective Kelly fraction is max(base, kelly), floored at base
    effective_fraction = max(base_pct, frac_kelly)

    # Hard cap
    effective_fraction = min(effective_fraction, MAX_SINGLE_TRADE_PCT)

    # Drawdown multiplier
    dd_mult = status["sizing_multiplier"]
    effective_fraction *= dd_mult

    stake = round(bankroll * effective_fraction, 2)
    stake = max(0.01, stake)  # never round to zero

    # ── Correlation / exposure limits ──────────────────────────────────────
    if station_code:
        station_exp = get_station_exposure(station_code, conn)
        if station_exp + stake > bankroll * MAX_STATION_EXPOSURE_PCT:
            headroom = max(0.0, bankroll * MAX_STATION_EXPOSURE_PCT - station_exp)
            if headroom < 0.50:
                return _rejected(grade, status, f"station {station_code} exposure limit reached (${station_exp:.2f} open)")
            stake = min(stake, headroom)

    if regime and regime != "UNKNOWN":
        regime_exp = get_regime_exposure(regime, conn)
        if regime_exp + stake > bankroll * MAX_REGIME_EXPOSURE_PCT:
            headroom = max(0.0, bankroll * MAX_REGIME_EXPOSURE_PCT - regime_exp)
            if headroom < 0.50:
                return _rejected(grade, status, f"regime {regime} exposure limit reached (${regime_exp:.2f} open)")
            stake = min(stake, headroom)

    stake = round(stake, 2)

    return {
        "stake_dollars":     stake,
        "kelly_fraction":    round(effective_fraction, 6),
        "grade":             grade,
        "rejected":          False,
        "reject_reason":     "",
        "bankroll_snapshot": status,
    }


def _rejected(grade: str, status: dict, reason: str) -> dict:
    return {
        "stake_dollars":     0.0,
        "kelly_fraction":    0.0,
        "grade":             grade,
        "rejected":          True,
        "reject_reason":     reason,
        "bankroll_snapshot": status,
    }


def explain_sizing(edge_result: dict, conn: sqlite3.Connection) -> str:
    """Human-readable sizing explanation for the dashboard."""
    sizing = size_trade(edge_result, conn)
    if sizing["rejected"]:
        return f"Trade blocked: {sizing['reject_reason']}"

    snap = sizing["bankroll_snapshot"]
    lines = [
        f"Bankroll: ${snap['current_bankroll']:.2f}  |  Drawdown: {snap['drawdown_pct']:.1%}  |  Multiplier: {snap['sizing_multiplier']:.2f}x",
        f"Grade: {sizing['grade']}  |  Kelly fraction: {sizing['kelly_fraction']:.3f}  |  Stake: ${sizing['stake_dollars']:.2f}",
    ]
    if snap["drawdown_pct"] >= 0.10:
        lines.append(f"⚠️ Sizing reduced due to {snap['drawdown_pct']:.1%} drawdown")
    return "\n".join(lines)
