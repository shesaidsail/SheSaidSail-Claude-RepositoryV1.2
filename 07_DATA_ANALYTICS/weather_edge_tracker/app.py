"""
KLAX Weather Market Edge Tracker — Streamlit Dashboard
Run with:  streamlit run app.py
"""

import csv
import statistics
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from scipy.stats import norm

DATA_FILE = Path(__file__).parent / "klax_data.csv"
FIELDNAMES = ["date", "ventusky_forecast_high", "actual_high", "error"]
BET_EDGE_THRESHOLD = 5.0


# ---------------------------------------------------------------------------
# Data helpers (mirrors edge_tracker.py — no import to keep app self-contained)
# ---------------------------------------------------------------------------

def load_df() -> pd.DataFrame:
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=FIELDNAMES)
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def save_record(record_date: str, forecast: float, actual: float) -> None:
    error = round(actual - forecast, 2)
    df = load_df()
    mask = df["date"].astype(str).str.startswith(record_date)
    if mask.any():
        df.loc[mask, "ventusky_forecast_high"] = forecast
        df.loc[mask, "actual_high"] = actual
        df.loc[mask, "error"] = error
    else:
        new_row = pd.DataFrame([{
            "date": pd.Timestamp(record_date),
            "ventusky_forecast_high": forecast,
            "actual_high": actual,
            "error": error,
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    df = df.sort_values("date")
    df.to_csv(DATA_FILE, index=False, date_format="%Y-%m-%d")


def bias_stats(df: pd.DataFrame) -> tuple[float, float, int]:
    errors = df["error"].dropna().tolist()
    if len(errors) < 2:
        raise ValueError(f"Need ≥ 2 settled records. Have {len(errors)}.")
    return statistics.mean(errors), statistics.stdev(errors), len(errors)


def calculate_edge(
    ventusky_forecast: float,
    threshold: float,
    side: str,
    market_price: float,
    df: pd.DataFrame,
) -> dict:
    avg_bias, std_dev, n = bias_stats(df)
    adjusted = ventusky_forecast + avg_bias

    if side == "Yes":
        prob = 1.0 - norm.cdf(threshold, loc=adjusted, scale=std_dev)
    else:
        prob = norm.cdf(threshold, loc=adjusted, scale=std_dev)

    fair = prob * 100.0
    edge = fair - market_price

    if edge >= BET_EDGE_THRESHOLD:
        rec, rec_color = "BET ✅", "green"
    elif edge >= 0:
        rec, rec_color = "THIN EDGE — PASS", "orange"
    else:
        rec, rec_color = "FADE / LAY ❌", "red"

    return dict(
        ventusky_forecast=ventusky_forecast,
        avg_bias=round(avg_bias, 2),
        std_dev=round(std_dev, 2),
        n=n,
        adjusted=round(adjusted, 2),
        threshold=threshold,
        side=side,
        prob=round(prob, 4),
        fair=round(fair, 1),
        market_price=market_price,
        edge=round(edge, 1),
        rec=rec,
        rec_color=rec_color,
    )


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="KLAX Edge Tracker",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ KLAX Weather Market Edge Tracker")
st.caption("Compares Ventusky/HRRR forecasts vs. KLAX official settlement highs to find mispriced contracts.")

df = load_df()

# ---------------------------------------------------------------------------
# Sidebar — add / update a record
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("📝 Log Settled Day")
    st.markdown(
        "Enter **yesterday's** Ventusky forecast and KLAX official high "
        "after the market settles. Do this once per day."
    )

    log_date = st.date_input("Date", value=date.today(), key="log_date")
    log_forecast = st.number_input("Ventusky Forecast High (°F)", min_value=40.0, max_value=115.0,
                                   value=72.0, step=0.5, key="log_forecast")
    log_actual = st.number_input("KLAX Official Actual High (°F)", min_value=40.0, max_value=115.0,
                                 value=73.0, step=0.5, key="log_actual")

    if st.button("Save Record", type="primary"):
        save_record(str(log_date), log_forecast, log_actual)
        st.success(f"Saved {log_date}: forecast {log_forecast}°F → actual {log_actual}°F "
                   f"(error {log_actual - log_forecast:+.1f}°F)")
        st.rerun()

    st.divider()
    st.markdown(
        "**How to find Ventusky forecast:**\n"
        "1. Go to [ventusky.com](https://ventusky.com) and set location to KLAX (33.94°N, 118.41°W).\n"
        "2. Switch to **Temperature Max** layer.\n"
        "3. Read the daily high for your target date.\n"
        "4. Enter it in the Edge Calculator (right panel)."
    )

# ---------------------------------------------------------------------------
# Bias summary
# ---------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

if len(df) >= 2:
    avg_bias, std_dev, n = bias_stats(df)
    col1.metric("Sample Size (n)", n)
    col2.metric("Average Bias", f"{avg_bias:+.2f}°F",
                help="Mean of (actual − forecast). Positive = HRRR runs cold.")
    col3.metric("Std Deviation", f"{std_dev:.2f}°F",
                help="1-sigma spread of forecast errors.")
    col4.metric("Model Uncertainty", f"±{std_dev:.1f}°F",
                help="68% of actuals fall within ±1σ of adjusted forecast.")
else:
    st.warning("Add at least 2 settled records to enable edge calculations.")

st.divider()

# ---------------------------------------------------------------------------
# Edge calculator
# ---------------------------------------------------------------------------

st.header("📊 Edge Calculator")

c1, c2, c3, c4 = st.columns(4)

with c1:
    today_forecast = st.number_input(
        "Today's Ventusky Forecast High (°F)",
        min_value=40.0, max_value=115.0, value=74.0, step=0.5,
    )

with c2:
    threshold = st.number_input(
        "Contract Threshold (e.g. 75 for '>75')",
        min_value=40.0, max_value=115.0, value=75.0, step=1.0,
    )

with c3:
    side = st.selectbox("Contract Side", ["Yes", "No"],
                        help="Yes = wins if actual > threshold. No = wins if actual ≤ threshold.")

with c4:
    market_price = st.number_input(
        "Market Price (cents, 0–100)",
        min_value=1.0, max_value=99.0, value=50.0, step=1.0,
    )

if len(df) >= 2 and st.button("Calculate Edge", type="primary"):
    r = calculate_edge(today_forecast, threshold, side, market_price, df)

    st.divider()
    rc1, rc2, rc3 = st.columns(3)

    with rc1:
        st.metric("Adjusted Forecast", f"{r['adjusted']}°F",
                  delta=f"{r['avg_bias']:+.2f}°F bias correction")
    with rc2:
        st.metric("Fair Price", f"{r['fair']:.1f}¢",
                  delta=f"{r['edge']:+.1f}¢ edge",
                  delta_color="normal" if r["edge"] >= 0 else "inverse")
    with rc3:
        st.metric("P(Win)", f"{r['prob']:.1%}")

    # Recommendation box
    box_style = {
        "green":  "background:#d4edda;border-left:6px solid #28a745;",
        "orange": "background:#fff3cd;border-left:6px solid #ffc107;",
        "red":    "background:#f8d7da;border-left:6px solid #dc3545;",
    }[r["rec_color"]]

    st.markdown(
        f"""
        <div style="{box_style} padding:16px 20px; border-radius:6px; margin-top:12px;">
            <strong style="font-size:1.3em;">{r['rec']}</strong><br>
            <span style="color:#555;">
                Contract: <strong>{r['side']} &gt;{int(r['threshold'])}</strong> &nbsp;|&nbsp;
                Market: <strong>{r['market_price']:.1f}¢</strong> &nbsp;|&nbsp;
                Fair: <strong>{r['fair']:.1f}¢</strong> &nbsp;|&nbsp;
                Edge: <strong>{r['edge']:+.1f}¢</strong>
            </span><br>
            <small style="color:#888;">Adjusted forecast {r['adjusted']}°F ± {r['std_dev']}°F (1σ), n={r['n']}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detail table
    with st.expander("Calculation breakdown"):
        breakdown = {
            "Step": [
                "Ventusky forecast",
                "Average bias",
                "Adjusted forecast",
                "Std deviation",
                "Threshold",
                "Side",
                "P(win) = normal CDF",
                "Fair price",
                "Market price",
                "Edge",
            ],
            "Value": [
                f"{r['ventusky_forecast']}°F",
                f"{r['avg_bias']:+.2f}°F (mean of {r['n']} errors)",
                f"{r['adjusted']}°F",
                f"{r['std_dev']}°F",
                f"{r['threshold']}°F",
                r['side'],
                f"{r['prob']:.4f}  ({r['prob']:.1%})",
                f"{r['fair']:.1f}¢",
                f"{r['market_price']:.1f}¢",
                f"{r['edge']:+.1f}¢",
            ],
        }
        st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)

elif len(df) < 2:
    st.info("Add settled records in the sidebar first, then come back here to calculate edge.")

st.divider()

# ---------------------------------------------------------------------------
# Historical data table + error chart
# ---------------------------------------------------------------------------

st.header("📅 Historical Records")

if df.empty:
    st.info("No records yet. Use the sidebar to log settled days.")
else:
    display_df = df.copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    display_df.columns = ["Date", "Forecast (°F)", "Actual (°F)", "Error (°F)"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if len(df) >= 3:
        st.subheader("Forecast Error Over Time")
        chart_df = df[["date", "error"]].set_index("date")
        chart_df.columns = ["Error (actual − forecast, °F)"]
        st.line_chart(chart_df)

        st.subheader("Error Distribution")
        hist_df = df["error"].rename("Forecast Error (°F)")
        st.bar_chart(hist_df.value_counts().sort_index())
