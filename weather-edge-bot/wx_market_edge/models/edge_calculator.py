"""
Edge calculator — the core math that turns forecasts into trade signals.

Steps:
  1. Get latest forecast for station+date
  2. Classify regime
  3. Get blended bias
  4. adjusted_forecast = forecast_high + blended_bias
  5. win_probability via Normal CDF with T+0.5 continuity correction
  6. fair_price = prob * 100
  7. edge = fair_price - market_price
  8. confidence score
  9. signal = BET | PASS | FADE
"""

import sys
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scipy.stats import norm
from models.regime_engine import classify_from_forecast, classify_from_metar, RegimeResult
from models.bias_engine    import blended_bias
from models.confidence_engine import compute_confidence
from ingestion.open_meteo  import get_latest_forecast
from ingestion.metar       import get_latest_obs
from config                import MIN_EDGE, MIN_CONFIDENCE, MAX_SPREAD, MIN_REGIME_N, DEFAULT_MODEL, STATIONS, MIN_NET_EDGE
from models.fee_engine     import estimate_fees


def win_probability(adjusted_forecast: float, std_dev: float,
                    threshold: float, side: str) -> float:
    """
    P(contract wins) using T+0.5 whole-degree continuity correction.
    Yes >T wins when actual >= T+1  →  1 - CDF(T + 0.5)
    No  >T wins when actual <= T    →  CDF(T + 0.5)
    """
    cutoff = threshold + 0.5
    if side.lower() == "yes":
        return 1.0 - norm.cdf(cutoff, loc=adjusted_forecast, scale=std_dev)
    elif side.lower() == "no":
        return norm.cdf(cutoff, loc=adjusted_forecast, scale=std_dev)
    raise ValueError("side must be 'Yes' or 'No'")


def _signal(gross_edge: float, net_edge: float, confidence: float,
            spread: float | None) -> str:
    """Signal requires BOTH gross edge ≥ MIN_EDGE AND net edge > MIN_NET_EDGE."""
    spread_ok = (spread is None) or (spread <= MAX_SPREAD)
    if (gross_edge >= MIN_EDGE and net_edge > MIN_NET_EDGE
            and confidence >= MIN_CONFIDENCE and spread_ok):
        return "BET"
    if (gross_edge <= -MIN_EDGE and net_edge < -MIN_NET_EDGE
            and confidence >= MIN_CONFIDENCE and spread_ok):
        return "FADE"
    return "PASS"


def calculate_edge(
    station_code:  str,
    forecast_date: str,
    threshold_f:   float,
    side:          str,
    market_price:  float,
    best_bid:      float | None,
    best_ask:      float | None,
    conn:          sqlite3.Connection,
    model:         str = DEFAULT_MODEL,
) -> dict:
    """
    Full edge calculation pipeline.

    Returns a rich result dict that powers dashboard display and paper trading.
    """
    result = {
        "station_code":      station_code,
        "forecast_date":     forecast_date,
        "threshold_f":       threshold_f,
        "side":              side,
        "market_price":      market_price,
        "best_bid":          best_bid,
        "best_ask":          best_ask,
        "spread":            round(best_ask - best_bid, 2) if best_bid and best_ask else None,
        # --- filled below ---
        "forecast_high":     None,
        "forecast_low":      None,
        "regime":            "UNKNOWN",
        "regime_confidence": 0.0,
        "regime_notes":      [],
        "blended_bias":      0.0,
        "std_dev":           3.0,
        "bias_note":         "",
        "adjusted_forecast": None,
        "model_prob":        None,
        "fair_value":        None,     # net fair value (after fee) — primary display field
        "gross_fair":        None,     # prob × 100 (no fee)
        "edge":              None,     # gross_edge − spread_cost for backwards compat
        "gross_edge":        None,     # gross_fair − market_price
        "net_edge":          None,     # net after fee + spread (signal gating field)
        "est_fee_cents":     None,
        "spread_cost_cents": None,
        "order_type":        None,
        "is_tradeable":      False,
        "confidence":        0.0,
        "confidence_reasons":[],
        "signal":            "PASS",
        "explanation":       "",
        "error":             None,
    }

    # 1. Get forecast
    fr = get_latest_forecast(station_code, forecast_date, conn)
    if not fr:
        result["error"] = f"No forecast found for {station_code}/{forecast_date}"
        return result

    result["forecast_high"] = fr.get("temp_max")
    result["forecast_low"]  = fr.get("temp_min")

    if result["forecast_high"] is None:
        result["error"] = "Forecast high temperature missing"
        return result

    # 2. Classify regime (prefer live METAR, fall back to forecast)
    obs = get_latest_obs(station_code, conn)
    if obs and obs.get("observed_temp") is not None:
        utc_off = STATIONS.get(station_code, {}).get("utc_offset", -5)
        try:
            ts = datetime.strptime(obs["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
            local_hour = (ts.hour + utc_off) % 24
        except Exception:
            local_hour = 12
        regime_r: RegimeResult = classify_from_metar(obs, local_hour)
    else:
        regime_r = classify_from_forecast(fr)

    result["regime"]            = regime_r.regime
    result["regime_confidence"] = regime_r.confidence
    result["regime_notes"]      = regime_r.notes

    # 3. Get blended bias + std dev
    bias, std, bias_note = blended_bias(station_code, model, regime_r.regime, conn)
    result["blended_bias"] = bias
    result["std_dev"]      = std
    result["bias_note"]    = bias_note

    # 4. Adjusted forecast
    adj = round(fr["temp_max"] + bias, 2)
    result["adjusted_forecast"] = adj

    # 5–7. Probability + full fee-aware breakdown
    prob = win_probability(adj, std, threshold_f, side)
    fee_info = estimate_fees(
        win_prob        = prob,
        market_price_mid= market_price,
        best_bid        = best_bid,
        best_ask        = best_ask,
    )

    result["model_prob"]        = round(prob, 4)
    result["gross_fair"]        = fee_info["gross_fair"]
    result["fair_value"]        = fee_info["net_fair"]      # net fair (after fee) is the headline
    result["gross_edge"]        = fee_info["gross_edge"]
    result["edge"]              = fee_info["gross_edge"]    # backwards compat alias
    result["net_edge"]          = fee_info["net_edge"]
    result["est_fee_cents"]     = fee_info["expected_fee_cents"]
    result["spread_cost_cents"] = fee_info["spread_cost_cents"]
    result["order_type"]        = fee_info["order_type"]
    result["is_tradeable"]      = fee_info["is_tradeable"]
    # Expose full fee dict for dashboard detail views
    result["fee_breakdown"]     = fee_info

    # 8. Confidence
    conf, reasons = compute_confidence(
        sample_size = fr.get("_sample_size_cached", 0),  # filled by caller if known
        std_dev     = std,
        regime      = regime_r.regime,
        edge        = edge,
        regime_conf = regime_r.confidence,
    )

    # Recalculate with actual sample size from DB
    n_row = conn.execute(
        "SELECT sample_size FROM model_stats WHERE station_code=? AND model_name=? AND regime='ALL'",
        (station_code, model)
    ).fetchone()
    n = n_row["sample_size"] if n_row else 0
    conf, reasons = compute_confidence(n, std, regime_r.regime, edge, regime_r.confidence)

    result["confidence"]         = conf
    result["confidence_reasons"] = reasons

    # 9. Signal — gated on both gross edge AND net edge (after fees + spread)
    result["signal"] = _signal(
        fee_info["gross_edge"], fee_info["net_edge"], conf, result["spread"]
    )

    # 10. Human-readable explanation
    station_name = STATIONS.get(station_code, {}).get("name", station_code)
    result["explanation"] = (
        f"{station_code} ({station_name})  {side} >{threshold_f:.0f}°F\n"
        f"  Market price:      {market_price:.0f}¢\n"
        f"  Model probability: {prob*100:.1f}%\n"
        f"  Gross fair value:  {fee_info['gross_fair']:.1f}¢  (prob × 100)\n"
        f"  Kalshi fee est.:   −{fee_info['expected_fee_cents']:.1f}¢"
        f"  (spread: −{fee_info['spread_cost_cents']:.1f}¢)\n"
        f"  Net fair value:    {fee_info['net_fair']:.1f}¢\n"
        f"  Gross edge:        {fee_info['gross_edge']:+.1f}¢\n"
        f"  Net edge:          {fee_info['net_edge']:+.1f}¢  [{fee_info['order_type']}]\n"
        f"  Open-Meteo high:   {fr['temp_max']:.1f}°F\n"
        f"  Adjusted forecast: {adj:.1f}°F (bias {bias:+.2f}°F)\n"
        f"  Regime:            {regime_r.regime} (conf {regime_r.confidence:.0%})\n"
        f"  Bias note:         {bias_note}\n"
        f"  Model confidence:  {conf:.0%}\n"
        f"  Signal:            {result['signal']}"
        + ("  ✓ TRADEABLE" if fee_info["is_tradeable"] else "  ✗ edge destroyed by fees/spread")
    )

    return result


def scan_all_markets(conn: sqlite3.Connection, date: str | None = None) -> list[dict]:
    """
    Run calculate_edge for every market snapshot that has enough data.
    Returns list of edge results, sorted by edge descending.
    """
    from ingestion.kalshi import get_latest_snapshots
    today = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshots = get_latest_snapshots(conn, date=today)

    results = []
    for snap in snapshots:
        if not snap.get("station_code") or not snap.get("threshold_f"):
            continue
        r = calculate_edge(
            station_code  = snap["station_code"],
            forecast_date = snap.get("expiry_date") or today,
            threshold_f   = snap["threshold_f"],
            side          = snap.get("side", "Yes"),
            market_price  = snap.get("market_price") or 50,
            best_bid      = snap.get("best_bid"),
            best_ask      = snap.get("best_ask"),
            conn          = conn,
        )
        r["snapshot_id"] = snap["id"]
        results.append(r)

    results.sort(key=lambda x: abs(x.get("edge") or 0), reverse=True)
    return results
