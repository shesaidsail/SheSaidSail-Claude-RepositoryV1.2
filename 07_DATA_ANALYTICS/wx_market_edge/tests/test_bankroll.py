"""
Tests for trading/bankroll.py and trading/bet_sizer.py

Validates bankroll tracking, drawdown multipliers, daily loss halts,
Kelly sizing, fractional Kelly, exposure limits, and rejection logic.
"""

import sys
from pathlib import Path
import sqlite3
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from trading.bankroll import (
    get_current_bankroll, get_drawdown, get_open_exposure,
    get_sizing_multiplier, is_daily_loss_limit_hit,
    bankroll_status, get_daily_pnl,
)
from trading.bet_sizer import kelly_fraction_raw, size_trade


# ── In-memory DB setup ─────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS paper_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opened_at TEXT, station_code TEXT, market_ticker TEXT,
            forecast_date TEXT, threshold_f REAL, side TEXT,
            entry_price REAL, fair_value REAL, edge REAL,
            confidence REAL, regime TEXT, adjusted_forecast REAL,
            model_prob REAL, status TEXT DEFAULT 'OPEN',
            settlement_price REAL, result TEXT,
            pnl_cents REAL, pnl_dollars REAL, stake_dollars REAL,
            kelly_fraction REAL, grade TEXT, closed_at TEXT, notes TEXT
        );
        CREATE TABLE IF NOT EXISTS bankroll_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TEXT UNIQUE,
            bankroll REAL, peak_bankroll REAL,
            drawdown_pct REAL, open_exposure REAL,
            daily_pnl REAL, trades_today INTEGER, note TEXT,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
        );
    """)
    return conn


def _add_closed_trade(conn, pnl_dollars, stake=20.0, result="WIN",
                      regime="CLEAR_SKY", station="KLAX", closed_at=None):
    now = closed_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("""
        INSERT INTO paper_trades
            (opened_at, station_code, market_ticker, forecast_date,
             threshold_f, side, entry_price, fair_value, edge,
             confidence, regime, status, result, pnl_dollars, pnl_cents,
             stake_dollars, closed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,'CLOSED',?,?,?,?,?)
    """, (now, station, "TEST", "2026-01-01", 70.0, "Yes", 35.0, 55.0,
          20.0, 0.70, regime, result, pnl_dollars,
          pnl_dollars * 2, stake, now))
    conn.commit()


def _add_open_trade(conn, stake_dollars=30.0, station="KLAX", regime="CLEAR_SKY"):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("""
        INSERT INTO paper_trades
            (opened_at, station_code, market_ticker, forecast_date,
             threshold_f, side, entry_price, fair_value, edge,
             confidence, regime, status, stake_dollars)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,'OPEN',?)
    """, (now, station, "TEST-OPEN", "2026-01-02", 72.0, "Yes",
          35.0, 55.0, 20.0, 0.70, regime, stake_dollars))
    conn.commit()


# ── Bankroll tracking ──────────────────────────────────────────────────────────

def test_bankroll_starts_at_starting_balance():
    conn = _conn()
    from config import STARTING_BANKROLL
    assert get_current_bankroll(conn) == STARTING_BANKROLL


def test_bankroll_increases_on_win():
    conn = _conn()
    from config import STARTING_BANKROLL
    _add_closed_trade(conn, pnl_dollars=50.0, result="WIN")
    assert get_current_bankroll(conn) == STARTING_BANKROLL + 50.0


def test_bankroll_decreases_on_loss():
    conn = _conn()
    from config import STARTING_BANKROLL
    _add_closed_trade(conn, pnl_dollars=-20.0, result="LOSS")
    assert get_current_bankroll(conn) == STARTING_BANKROLL - 20.0


def test_open_exposure_sums_open_stakes():
    conn = _conn()
    _add_open_trade(conn, stake_dollars=30.0)
    _add_open_trade(conn, stake_dollars=25.0)
    assert get_open_exposure(conn) == 55.0


def test_open_exposure_excludes_closed():
    conn = _conn()
    _add_closed_trade(conn, pnl_dollars=10.0, stake=20.0)
    _add_open_trade(conn, stake_dollars=40.0)
    assert get_open_exposure(conn) == 40.0


# ── Drawdown ───────────────────────────────────────────────────────────────────

def test_drawdown_zero_at_start():
    conn = _conn()
    assert get_drawdown(conn) == 0.0


def test_drawdown_computed_after_losses():
    conn = _conn()
    from config import STARTING_BANKROLL
    # Win to establish peak, then lose
    _add_closed_trade(conn, pnl_dollars=100.0, result="WIN")
    _add_closed_trade(conn, pnl_dollars=-200.0, result="LOSS")
    # Peak = 1100, current = 900, dd = 200/1100 ≈ 0.182
    dd = get_drawdown(conn)
    assert 0.17 < dd < 0.20, f"Expected ~18% drawdown, got {dd:.3f}"


# ── Sizing multipliers ─────────────────────────────────────────────────────────

def test_sizing_multiplier_full_at_low_drawdown():
    conn = _conn()
    # No losses — no drawdown
    assert get_sizing_multiplier(conn) == 1.0


def test_sizing_multiplier_reduced_at_10pct_drawdown():
    conn = _conn()
    from config import STARTING_BANKROLL
    # Create ~12% drawdown
    _add_closed_trade(conn, pnl_dollars=200.0, result="WIN")   # peak = 1200
    _add_closed_trade(conn, pnl_dollars=-210.0, result="LOSS") # current = 990 → dd=17%
    mult = get_sizing_multiplier(conn)
    assert mult == 0.75, f"Expected 0.75x at ~17% drawdown, got {mult}"


def test_sizing_multiplier_halved_at_20pct_drawdown():
    conn = _conn()
    from config import STARTING_BANKROLL
    # Create >20% drawdown
    _add_closed_trade(conn, pnl_dollars=500.0, result="WIN")   # peak = 1500
    _add_closed_trade(conn, pnl_dollars=-400.0, result="LOSS") # current = 1100 → dd=26%
    mult = get_sizing_multiplier(conn)
    assert mult == 0.50, f"Expected 0.50x at >20% drawdown, got {mult}"


def test_sizing_multiplier_zero_at_30pct_drawdown():
    conn = _conn()
    # Create >30% drawdown: start with win then big loss
    _add_closed_trade(conn, pnl_dollars=1000.0, result="WIN")   # peak = 2000
    _add_closed_trade(conn, pnl_dollars=-800.0, result="LOSS")  # current = 1200 → dd=40%
    mult = get_sizing_multiplier(conn)
    assert mult == 0.0, f"Expected 0.0x (pause) at >30% drawdown, got {mult}"


# ── Daily loss halt ────────────────────────────────────────────────────────────

def test_daily_loss_limit_not_hit_initially():
    conn = _conn()
    assert not is_daily_loss_limit_hit(conn)


def test_daily_loss_limit_triggered():
    conn = _conn()
    from config import STARTING_BANKROLL, MAX_DAILY_LOSS_PCT
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    loss_amount = STARTING_BANKROLL * (MAX_DAILY_LOSS_PCT + 0.01)  # just over limit
    _add_closed_trade(conn, pnl_dollars=-loss_amount, result="LOSS", closed_at=today)
    assert is_daily_loss_limit_hit(conn), "Daily loss limit should be triggered"


# ── Kelly math ─────────────────────────────────────────────────────────────────

def test_kelly_positive_for_favorable_bet():
    """60% win prob at 50¢ entry → positive Kelly."""
    k = kelly_fraction_raw(0.60, 50.0)
    assert k > 0, f"Expected positive Kelly, got {k}"


def test_kelly_zero_for_unfavorable_bet():
    """40% win prob at 50¢ entry → Kelly=0 (don't bet)."""
    k = kelly_fraction_raw(0.40, 50.0)
    assert k == 0.0, f"Expected 0 Kelly for negative edge, got {k}"


def test_kelly_zero_for_50_50_at_50():
    """50% win at 50¢ entry → exactly zero edge, Kelly=0."""
    k = kelly_fraction_raw(0.50, 50.0)
    assert abs(k) < 0.001, f"Expected ~0 Kelly at breakeven, got {k}"


def test_kelly_bounded_0_1():
    """Kelly should never exceed 1.0."""
    k = kelly_fraction_raw(0.999, 1.0)   # Near certainty + cheap contract
    assert 0.0 <= k <= 1.0, f"Kelly out of bounds: {k}"


# ── Bet sizer integration ──────────────────────────────────────────────────────

def _make_edge_result(grade="A+", win_prob=0.65, price=35.0,
                      station="KLAX", regime="CLEAR_SKY"):
    return {
        "grade": grade, "model_prob": win_prob, "market_price": price,
        "station_code": station, "regime": regime,
        "edge": 20.0, "confidence": 0.75, "signal": "BET",
    }


def test_sizer_returns_positive_stake():
    conn = _conn()
    er = _make_edge_result(grade="A+", win_prob=0.65)
    result = size_trade(er, conn)
    assert not result["rejected"], f"Should not reject: {result['reject_reason']}"
    assert result["stake_dollars"] > 0


def test_sizer_respects_hard_cap():
    conn = _conn()
    from config import MAX_SINGLE_TRADE_PCT, STARTING_BANKROLL
    er = _make_edge_result(grade="A+", win_prob=0.95)  # Very high win prob → big Kelly
    result = size_trade(er, conn)
    max_allowed = STARTING_BANKROLL * MAX_SINGLE_TRADE_PCT
    assert result["stake_dollars"] <= max_allowed + 0.01, \
        f"Stake ${result['stake_dollars']:.2f} exceeds cap ${max_allowed:.2f}"


def test_sizer_rejects_when_paused():
    conn = _conn()
    # Force >30% drawdown
    _add_closed_trade(conn, pnl_dollars=1000.0, result="WIN")
    _add_closed_trade(conn, pnl_dollars=-800.0, result="LOSS")

    er = _make_edge_result(grade="A+", win_prob=0.65)
    result = size_trade(er, conn)
    assert result["rejected"], "Should reject when drawdown>30% (trading paused)"


def test_sizer_smaller_for_grade_b():
    conn = _conn()
    er_aplus = _make_edge_result(grade="A+", win_prob=0.65)
    er_b     = _make_edge_result(grade="B",  win_prob=0.65)
    res_aplus = size_trade(er_aplus, conn)
    res_b     = size_trade(er_b,     conn)
    assert res_aplus["stake_dollars"] >= res_b["stake_dollars"], \
        "A+ stake should be >= B stake"
