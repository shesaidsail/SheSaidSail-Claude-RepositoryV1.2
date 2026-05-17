"""
KLAX Weather Prediction Market Edge Tracker
--------------------------------------------
Compares Ventusky/HRRR forecast highs against KLAX official actuals to estimate
bias-adjusted probability that a contract threshold will be crossed.

Usage (CLI):
    python edge_tracker.py --forecast 74 --threshold 75 --side Yes --price 48
    python edge_tracker.py --forecast 74 --threshold 75 --side No  --price 55

To add today's forecast + actual after settlement:
    python edge_tracker.py --add-record --date 2026-05-17 --forecast 73 --actual 75

Data file: klax_data.csv (same directory as this script)
"""

import argparse
import csv
import math
import os
import statistics
from datetime import date
from pathlib import Path
from scipy.stats import norm

DATA_FILE = Path(__file__).parent / "klax_data.csv"
FIELDNAMES = ["date", "ventusky_forecast_high", "actual_high", "error"]
BET_EDGE_THRESHOLD = 5.0  # cents minimum edge to recommend a bet


# ---------------------------------------------------------------------------
# Data I/O
# ---------------------------------------------------------------------------

def load_records() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, newline="") as f:
        return list(csv.DictReader(f))


def save_record(record_date: str, forecast: float, actual: float) -> None:
    error = actual - forecast
    rows = load_records()

    # Overwrite if date already exists, otherwise append
    updated = False
    for row in rows:
        if row["date"] == record_date:
            row["ventusky_forecast_high"] = forecast
            row["actual_high"] = actual
            row["error"] = round(error, 2)
            updated = True
            break

    if not updated:
        rows.append({
            "date": record_date,
            "ventusky_forecast_high": forecast,
            "actual_high": actual,
            "error": round(error, 2),
        })

    rows.sort(key=lambda r: r["date"])

    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {record_date}  forecast={forecast}  actual={actual}  error={error:+.1f}")


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def compute_bias_stats(records: list[dict]) -> tuple[float, float, int]:
    """Returns (average_bias, standard_deviation, sample_count)."""
    errors = [float(r["error"]) for r in records if r["error"] != ""]
    if len(errors) < 2:
        raise ValueError(f"Need at least 2 settled records to compute stats. Have {len(errors)}.")
    avg_bias = statistics.mean(errors)
    std_dev = statistics.stdev(errors)          # sample std dev (ddof=1)
    return avg_bias, std_dev, len(errors)


# ---------------------------------------------------------------------------
# Core edge calculation
# ---------------------------------------------------------------------------

def calculate_edge(
    ventusky_forecast: float,
    threshold: float,
    side: str,            # "Yes" or "No"
    market_price: float,  # in cents (0–100)
    records: list[dict],
) -> dict:
    avg_bias, std_dev, n = compute_bias_stats(records)
    adjusted_forecast = ventusky_forecast + avg_bias

    # Actual high is modelled as N(adjusted_forecast, std_dev)
    # "Yes >T" wins when actual_high > T  →  P(Z > T)
    # "No  >T" wins when actual_high <= T →  P(Z <= T)
    if side.lower() == "yes":
        probability = 1.0 - norm.cdf(threshold, loc=adjusted_forecast, scale=std_dev)
    elif side.lower() == "no":
        probability = norm.cdf(threshold, loc=adjusted_forecast, scale=std_dev)
    else:
        raise ValueError("side must be 'Yes' or 'No'")

    fair_price = probability * 100.0
    edge = fair_price - market_price
    recommend = "BET" if edge >= BET_EDGE_THRESHOLD else ("PASS" if edge >= 0 else "FADE / LAY")

    return {
        "ventusky_forecast": ventusky_forecast,
        "average_bias": round(avg_bias, 2),
        "std_dev": round(std_dev, 2),
        "sample_n": n,
        "adjusted_forecast": round(adjusted_forecast, 2),
        "threshold": threshold,
        "side": side,
        "probability": round(probability, 4),
        "fair_price": round(fair_price, 1),
        "market_price": market_price,
        "edge": round(edge, 1),
        "recommend": recommend,
    }


def print_result(r: dict) -> None:
    print()
    print("=" * 48)
    print("  KLAX EDGE TRACKER — RESULT")
    print("=" * 48)
    print(f"  Ventusky forecast    : {r['ventusky_forecast']}°F")
    print(f"  Average bias (n={r['sample_n']:>2})  : {r['average_bias']:+.2f}°F")
    print(f"  Adjusted forecast    : {r['adjusted_forecast']}°F")
    print(f"  Std deviation        : {r['std_dev']:.2f}°F")
    print()
    print(f"  Contract             : {r['side']} >{r['threshold']}")
    print(f"  P(win)               : {r['probability']:.1%}")
    print(f"  Fair price           : {r['fair_price']:.1f}¢")
    print(f"  Market price         : {r['market_price']:.1f}¢")
    print(f"  Edge                 : {r['edge']:+.1f}¢")
    print()
    print(f"  Recommendation       : *** {r['recommend']} ***")
    print("=" * 48)
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="KLAX weather market edge tracker")
    subparsers = parser.add_subparsers(dest="command")

    # ---- add-record sub-command ----
    add_p = subparsers.add_parser("add", help="Log a settled day's forecast and actual")
    add_p.add_argument("--date", default=str(date.today()), help="YYYY-MM-DD (default: today)")
    add_p.add_argument("--forecast", type=float, required=True, help="Ventusky forecast high")
    add_p.add_argument("--actual",   type=float, required=True, help="Official KLAX actual high")

    # ---- edge sub-command ----
    edge_p = subparsers.add_parser("edge", help="Calculate edge on a contract")
    edge_p.add_argument("--forecast",  type=float, required=True, help="Today's Ventusky forecast high")
    edge_p.add_argument("--threshold", type=float, required=True, help="Contract threshold (e.g. 68)")
    edge_p.add_argument("--side",      choices=["Yes", "No"], required=True)
    edge_p.add_argument("--price",     type=float, required=True, help="Market price in cents (0-100)")

    # ---- show sub-command ----
    subparsers.add_parser("show", help="Print historical records and current bias")

    args = parser.parse_args()

    if args.command == "add":
        save_record(args.date, args.forecast, args.actual)

    elif args.command == "edge":
        records = load_records()
        result = calculate_edge(args.forecast, args.threshold, args.side, args.price, records)
        print_result(result)

    elif args.command == "show":
        records = load_records()
        print(f"\n{'Date':<12} {'Forecast':>9} {'Actual':>8} {'Error':>7}")
        print("-" * 40)
        for r in records:
            e = float(r["error"])
            print(f"{r['date']:<12} {float(r['ventusky_forecast_high']):>9.1f} "
                  f"{float(r['actual_high']):>8.1f} {e:>+7.1f}")
        if len(records) >= 2:
            bias, std, n = compute_bias_stats(records)
            print("-" * 40)
            print(f"  Bias (mean error): {bias:+.2f}°F  |  Std dev: {std:.2f}°F  |  n={n}")
        print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
