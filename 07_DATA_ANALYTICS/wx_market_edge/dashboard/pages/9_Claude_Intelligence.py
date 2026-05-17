"""
Page 9 — Claude Intelligence

Daily performance review, model self-critique, regime analysis, and
preparation for Claude API pipeline integration.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

from database.db import init_db
from reports.report_engine import generate_report
from config import STATIONS, DEFAULT_MODEL

st.set_page_config(page_title="Claude Intelligence", page_icon="🧠", layout="wide")
st.title("🧠 Claude Intelligence Layer")
st.caption("Python handles live math. Claude acts as the analyst, reviewer, and model improvement engine.")

conn = init_db()

# ── Report generation ─────────────────────────────────────────────────────────
st.subheader("Daily Report Engine")

col_date, col_btn = st.columns([2, 1])
with col_date:
    report_date = st.date_input(
        "Report date",
        value=(datetime.now(timezone.utc) - timedelta(days=1)).date()
    )
with col_btn:
    st.write("")
    gen_btn = st.button("📄 Generate Report", type="primary")

if gen_btn:
    date_str = report_date.strftime("%Y-%m-%d")
    with st.spinner(f"Generating report for {date_str}..."):
        md_path, json_path = generate_report(date_str, conn)
    st.success(f"Report generated:  `{md_path}`")

    # Show Markdown inline
    try:
        md_text = Path(md_path).read_text(encoding="utf-8")
        with st.expander("View Report (Markdown)", expanded=True):
            st.markdown(md_text)
    except Exception:
        pass

    # Download buttons
    try:
        col_md, col_json = st.columns(2)
        with col_md:
            st.download_button("⬇ Download .md", Path(md_path).read_text(), "daily_model_report.md", "text/markdown")
        with col_json:
            st.download_button("⬇ Download .json", Path(json_path).read_text(), "daily_model_report.json", "application/json")
    except Exception:
        pass

st.divider()

# ── Latest review from DB ─────────────────────────────────────────────────────
st.subheader("Latest Model Review")

latest_review = conn.execute("""
    SELECT * FROM claude_reviews ORDER BY report_date DESC LIMIT 1
""").fetchone()

if latest_review:
    r = dict(latest_review)
    st.info(f"**{r['report_date']}** — {r.get('summary', '')}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Weaknesses detected:**")
        try:
            items = json.loads(r.get("weaknesses") or "[]")
            for item in items:
                st.write(f"• {item}")
            if not items:
                st.write("_None flagged_")
        except Exception:
            st.write(r.get("weaknesses", "—"))

    with col2:
        st.write("**Suggested changes:**")
        try:
            items = json.loads(r.get("suggested_changes") or "[]")
            for item in items:
                st.write(f"• {item}")
            if not items:
                st.write("_None suggested_")
        except Exception:
            st.write(r.get("suggested_changes", "—"))

    suspicious = json.loads(r.get("suspicious_regimes") or "[]") if r.get("suspicious_regimes") else []
    if suspicious:
        st.warning("Suspicious regimes: " + ", ".join(suspicious))
else:
    st.info("No reports generated yet. Click 'Generate Report' above.")

st.divider()

# ── Model self-critique dashboard ─────────────────────────────────────────────
st.subheader("Model Self-Critique — Active Lessons")

lessons = conn.execute("""
    SELECT * FROM model_lessons
    WHERE applied=0
    ORDER BY severity DESC, created_at DESC
    LIMIT 50
""").fetchall()

if lessons:
    severity_icons = {"INFO": "ℹ️", "WARN": "⚠️", "ALERT": "🚨"}
    for l in lessons:
        l = dict(l)
        icon = severity_icons.get(l["severity"], "•")
        with st.expander(f"{icon} **{l['severity']}** — {l['station_code']} / {l['regime']}"):
            st.write(f"**Lesson:** {l['lesson']}")
            if l.get("recommendation"):
                st.success(f"💡 Recommendation: {l['recommendation']}")
            st.caption(f"Logged: {l['created_at'][:16]}")
            if st.button(f"Mark resolved #{l['id']}", key=f"resolve_{l['id']}"):
                conn.execute("UPDATE model_lessons SET applied=1 WHERE id=?", (l["id"],))
                conn.commit()
                st.rerun()
else:
    st.success("No active model lessons — system looks healthy.")

st.divider()

# ── Regime strength summary ────────────────────────────────────────────────────
st.subheader("Regime Performance — Last 30 Days")

regime_perf = conn.execute("""
    SELECT pt.regime, pt.station_code,
           COUNT(*) AS n,
           SUM(CASE WHEN pt.result='WIN' THEN 1 ELSE 0 END) AS wins,
           ROUND(SUM(pt.pnl_cents),1) AS total_pnl,
           ROUND(AVG(pt.edge),1) AS avg_edge_entered
    FROM paper_trades pt
    WHERE pt.status='CLOSED'
      AND DATE(pt.closed_at) >= DATE('now','-30 days')
    GROUP BY pt.regime, pt.station_code
    HAVING n >= 2
    ORDER BY total_pnl DESC
""").fetchall()

if regime_perf:
    rp_rows = []
    for r in regime_perf:
        r = dict(r)
        wr = r["wins"] / r["n"] if r["n"] else 0
        label = "✅ Trade" if r["total_pnl"] > 0 and wr >= 0.55 else \
                ("🚫 Avoid" if r["total_pnl"] < -5 or wr < 0.40 else "👀 Watch")
        rp_rows.append({
            "Action": label,
            "Station": r["station_code"],
            "Regime": r["regime"],
            "n": r["n"],
            "Win Rate": f"{wr:.0%}",
            "P&L ¢": r["total_pnl"],
            "Avg Edge Entered": r["avg_edge_entered"],
        })

    rp_df = pd.DataFrame(rp_rows)
    st.dataframe(rp_df, hide_index=True, use_container_width=True)
    st.bar_chart(rp_df.set_index("Regime")["P&L ¢"])
else:
    st.info("No closed trades in the last 30 days.")

st.divider()

# ── Calibration trend ─────────────────────────────────────────────────────────
st.subheader("Confidence Calibration Trend")
st.caption("Does model_prob match actual win rate? A well-calibrated model has these close together.")

calib = conn.execute("""
    SELECT ROUND(model_prob*10)/10 AS bucket,
           COUNT(*) AS n,
           ROUND(AVG(CASE WHEN result='WIN' THEN 1.0 ELSE 0.0 END),3) AS actual_win_rate
    FROM paper_trades
    WHERE status='CLOSED' AND model_prob IS NOT NULL
    GROUP BY bucket
    HAVING n >= 3
    ORDER BY bucket
""").fetchall()

if calib and len(calib) >= 2:
    c_df = pd.DataFrame([dict(r) for r in calib])
    c_df["predicted"] = (c_df["bucket"] * 100).round(0)
    c_df["actual"]    = (c_df["actual_win_rate"] * 100).round(1)
    c_df["gap"]       = (c_df["actual"] - c_df["predicted"]).round(1)

    avg_gap = c_df["gap"].abs().mean()
    if avg_gap < 5:
        st.success(f"✅ Well-calibrated (avg gap: {avg_gap:.1f}%)")
    elif avg_gap < 12:
        st.warning(f"⚠️ Moderate calibration (avg gap: {avg_gap:.1f}%)")
    else:
        st.error(f"❌ Poor calibration (avg gap: {avg_gap:.1f}%) — needs more data or bias correction")

    chart_df = c_df.set_index("predicted")[["actual", "predicted"]]
    chart_df.columns = ["Actual Win %", "Predicted Win %"]
    st.line_chart(chart_df)
    st.dataframe(c_df[["predicted", "n", "actual", "gap"]], hide_index=True)
else:
    st.info("Need ≥6 closed trades across 2 probability buckets for calibration chart.")

st.divider()

# ── Claude API pipeline prep ──────────────────────────────────────────────────
st.subheader("Claude API Pipeline — Status")
st.info("""
**Current status: Infrastructure ready, API not yet connected.**

The system generates:
- `reports/daily_model_report.md` — human-readable daily summary
- `reports/daily_model_report.json` — structured data for Claude API
- `database: claude_reviews` — stores Claude analysis results
- `database: model_lessons` — stores regime-level learning

**To connect Claude API (future step):**
1. Add `ANTHROPIC_API_KEY=` to `.env`
2. Run `python reports/claude_api_review.py --date YYYY-MM-DD`
3. Claude will analyze the JSON report and populate `claude_reviews` table
4. Recommendations appear in this dashboard automatically

**What Claude will analyze when connected:**
- Daily forecast errors and patterns
- Regime drift and calibration quality
- False edges and overconfident signals
- Proposed rule improvements (for human review, not auto-apply)
""")

# Show the Claude Review Packet from latest JSON report
json_report_path = Path(__file__).parent.parent.parent / "reports" / "daily_model_report.json"
if json_report_path.exists():
    try:
        report_json = json.loads(json_report_path.read_text(encoding="utf-8"))
        packet = report_json.get("claude_review_packet", {})
        with st.expander("📋 Latest Claude Review Packet (copy to paste into Claude)"):
            st.write(f"**What happened:** {packet.get('what_happened','—')}")
            st.write(f"**Lessons flagged:** {packet.get('lessons_count', 0)}")
            st.write("**Suggested questions to ask Claude:**")
            for q in packet.get("suggested_questions", []):
                st.write(f"  • {q}")
            st.divider()
            st.code(json.dumps(report_json, indent=2)[:3000] + "\n...", language="json")
    except Exception as e:
        st.caption(f"Could not load latest report: {e}")
