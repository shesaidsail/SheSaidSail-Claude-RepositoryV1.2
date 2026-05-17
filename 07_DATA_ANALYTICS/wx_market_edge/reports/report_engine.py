"""
Daily model report engine.

Generates two files per run:
  reports/daily_model_report.md    — human-readable Markdown
  reports/daily_model_report.json  — machine-readable for Claude API pipeline

Also runs automatic model critique (self-critique logic) and logs
model_lessons to the database.

Usage:
  python reports/report_engine.py                     # report for yesterday
  python reports/report_engine.py --date 2026-05-16   # specific date
  python reports/report_engine.py --date 2026-05-16 --all-stations
"""

import sys
import json
import argparse
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db
from config import STATIONS, DEFAULT_MODEL

REPORTS_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# Data aggregation helpers
# ---------------------------------------------------------------------------

def _gather_report_data(date: str, conn) -> dict:
    """Pull all DB data needed for the daily report."""
    d = {"date": date}

    # ── Active stations ────────────────────────────────────────────────────
    d["active_stations"] = [dict(r) for r in conn.execute(
        "SELECT * FROM stations WHERE active=1"
    ).fetchall()]

    # ── Forecasts for this date ────────────────────────────────────────────
    d["forecasts"] = [dict(r) for r in conn.execute("""
        SELECT fr.*, s.name
        FROM forecast_runs fr
        JOIN stations s ON s.icao=fr.station_code
        WHERE fr.forecast_date=? AND fr.model_name=?
        ORDER BY fr.station_code
    """, (date, DEFAULT_MODEL)).fetchall()]

    # ── Settlements ────────────────────────────────────────────────────────
    d["settlements"] = [dict(r) for r in conn.execute("""
        SELECT ds.*, fr.temp_max AS forecast_high,
               ROUND(ds.official_high - fr.temp_max, 2) AS error
        FROM daily_settlements ds
        LEFT JOIN forecast_runs fr
            ON fr.forecast_date=ds.settlement_date
           AND fr.station_code=ds.station_code
           AND fr.model_name=?
        WHERE ds.settlement_date=?
        ORDER BY ds.station_code
    """, (DEFAULT_MODEL, date)).fetchall()]

    # ── Paper trades opened today ─────────────────────────────────────────
    d["trades_opened"] = [dict(r) for r in conn.execute("""
        SELECT pt.*, s.name AS station_name
        FROM paper_trades pt
        LEFT JOIN stations s ON s.icao=pt.station_code
        WHERE DATE(pt.opened_at)=?
        ORDER BY pt.opened_at
    """, (date,)).fetchall()]

    # ── Paper trades closed today ─────────────────────────────────────────
    d["trades_closed"] = [dict(r) for r in conn.execute("""
        SELECT pt.*, s.name AS station_name
        FROM paper_trades pt
        LEFT JOIN stations s ON s.icao=pt.station_code
        WHERE DATE(pt.closed_at)=? AND pt.status='CLOSED'
        ORDER BY pt.closed_at
    """, (date,)).fetchall()]

    # ── Model stats snapshot ───────────────────────────────────────────────
    d["model_stats"] = [dict(r) for r in conn.execute("""
        SELECT * FROM model_stats WHERE model_name=?
        ORDER BY station_code, regime
    """, (DEFAULT_MODEL,)).fetchall()]

    # ── Alerts sent today ─────────────────────────────────────────────────
    d["alerts_sent"] = [dict(r) for r in conn.execute("""
        SELECT * FROM webhook_alerts
        WHERE DATE(created_at)=? AND status='SENT'
    """, (date,)).fetchall()]

    # ── Recent regime performance (last 30 days) ──────────────────────────
    d["regime_perf"] = [dict(r) for r in conn.execute("""
        SELECT pt.regime, pt.station_code,
               COUNT(*) AS n,
               SUM(CASE WHEN pt.result='WIN' THEN 1 ELSE 0 END) AS wins,
               ROUND(SUM(pt.pnl_cents),2) AS total_pnl,
               ROUND(AVG(pt.pnl_cents),2) AS avg_pnl
        FROM paper_trades pt
        WHERE pt.status='CLOSED'
          AND DATE(pt.closed_at) >= DATE('now','-30 days')
        GROUP BY pt.regime, pt.station_code
        ORDER BY total_pnl DESC
    """).fetchall()]

    return d


# ---------------------------------------------------------------------------
# P&L summary from closed trades
# ---------------------------------------------------------------------------

def _pnl_summary(closed: list[dict]) -> dict:
    if not closed:
        return {"total": 0, "wins": 0, "losses": 0, "win_rate": 0, "pnl": 0}
    wins   = sum(1 for t in closed if t.get("result") == "WIN")
    losses = sum(1 for t in closed if t.get("result") == "LOSS")
    pnl    = sum(t.get("pnl_cents") or 0 for t in closed)
    return {
        "total":    len(closed),
        "wins":     wins,
        "losses":   losses,
        "win_rate": round(wins / len(closed), 3) if closed else 0,
        "pnl":      round(pnl, 2),
    }


# ---------------------------------------------------------------------------
# Self-critique / model lessons
# ---------------------------------------------------------------------------

def _generate_lessons(data: dict, conn) -> list[dict]:
    """
    Analyse the data and emit model_lessons for concerning patterns.
    Returns list of lesson dicts; also upserts into DB.
    """
    lessons = []

    # Helper: log a lesson
    def _add(station, regime, lesson, severity, recommendation=""):
        lessons.append({
            "station_code":  station,
            "regime":        regime,
            "lesson":        lesson,
            "severity":      severity,
            "recommendation": recommendation,
        })
        conn.execute("""
            INSERT INTO model_lessons
                (station_code, regime, lesson, severity, recommendation)
            VALUES (?,?,?,?,?)
        """, (station, regime, lesson, severity, recommendation))
    conn.commit()

    # ── 1. Persistent large bias ───────────────────────────────────────────
    for row in data.get("model_stats", []):
        if row["regime"] == "ALL" and row.get("avg_bias") is not None:
            if abs(row["avg_bias"]) > 3.0 and (row.get("sample_size") or 0) >= 10:
                _add(row["station_code"], "ALL",
                     f"Global bias {row['avg_bias']:+.2f}°F persists over {row['sample_size']} samples.",
                     "WARN",
                     "Investigate whether Open-Meteo has a systematic offset at this station.")

    # ── 2. High variance regimes ───────────────────────────────────────────
    for row in data.get("model_stats", []):
        if row.get("std_dev") and row["std_dev"] > 4.5 and (row.get("sample_size") or 0) >= 5:
            _add(row["station_code"], row["regime"],
                 f"High variance σ={row['std_dev']:.2f}°F in {row['regime']} regime.",
                 "WARN",
                 "Increase confidence penalty or avoid this regime until variance reduces.")

    # ── 3. Regime with worsening 7d bias vs 30d bias ──────────────────────
    for row in data.get("model_stats", []):
        r7  = row.get("rolling_7d_bias")
        r30 = row.get("rolling_30d_bias")
        if r7 is not None and r30 is not None and abs(r7 - r30) > 1.5:
            direction = "worsening" if abs(r7) > abs(r30) else "improving"
            _add(row["station_code"], row["regime"],
                 f"7d bias {r7:+.2f}°F vs 30d {r30:+.2f}°F — bias is {direction}.",
                 "INFO" if direction == "improving" else "WARN",
                 f"Monitor for another 5 days before adjusting weights." if direction == "worsening" else "")

    # ── 4. Low sample-size regimes used for real signals ──────────────────
    for row in data.get("model_stats", []):
        if row.get("sample_size") is not None and row["sample_size"] < 5 and row["regime"] != "ALL":
            _add(row["station_code"], row["regime"],
                 f"Regime '{row['regime']}' has only {row['sample_size']} sample(s) — blending heavily with global stats.",
                 "INFO",
                 "Avoid A+ signals for this regime until n≥10.")

    # ── 5. Settlement errors — large misses ───────────────────────────────
    for s in data.get("settlements", []):
        error = s.get("error")
        if error and abs(error) > 4:
            _add(s["station_code"], s.get("regime", "UNKNOWN"),
                 f"Large settlement error {error:+.1f}°F on {s['settlement_date']}.",
                 "ALERT" if abs(error) > 6 else "WARN",
                 "Check whether METAR backfill captured the true daily high; consider official NWS ASOS record.")

    # ── 6. Paper trade losing streaks ─────────────────────────────────────
    for rp in data.get("regime_perf", []):
        n, wins, pnl = rp["n"], rp["wins"], rp["total_pnl"]
        if n >= 5:
            win_rate = wins / n
            if win_rate < 0.35:
                _add(rp["station_code"], rp["regime"],
                     f"Losing streak: {n} trades, win rate {win_rate:.0%}, PnL {pnl:+.0f}¢.",
                     "ALERT",
                     f"Suspend trading in {rp['regime']} at {rp['station_code']} until calibration improves.")

    conn.commit()
    return lessons


# ---------------------------------------------------------------------------
# Report formatters
# ---------------------------------------------------------------------------

def _md_report(data: dict, lessons: list[dict]) -> str:
    date = data["date"]
    pnl  = _pnl_summary(data["trades_closed"])
    lines = [
        f"# Daily Model Report — {date}",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
    ]

    # 1. Active stations
    lines += [
        "## 1. Active Stations",
        "",
        "| ICAO | Name | UTC Offset |",
        "|---|---|---|",
    ]
    for s in data["active_stations"]:
        lines.append(f"| {s['icao']} | {s['name']} | UTC{s['utc_offset']:+d} |")
    lines.append("")

    # 2. Forecast summary
    lines += ["## 2. Forecast Summary", ""]
    if data["forecasts"]:
        lines += [
            "| Station | High °F | Low °F | Wind Dir | Wind Mph | Cloud % | Precip % |",
            "|---|---|---|---|---|---|---|",
        ]
        for f in data["forecasts"]:
            lines.append(
                f"| {f['station_code']} | {f.get('temp_max','—')} | {f.get('temp_min','—')} "
                f"| {f.get('wind_direction_dominant','—')} | {f.get('wind_speed_mean','—')} "
                f"| {f.get('cloud_cover_mean','—')} | {f.get('precip_prob_mean','—')} |"
            )
    else:
        lines.append("_No forecasts stored for this date._")
    lines.append("")

    # 3–5. Trades
    lines += ["## 3. Paper Trades Opened Today", ""]
    if data["trades_opened"]:
        for t in data["trades_opened"]:
            lines.append(f"- {t['station_code']} {t['side']} >{t['threshold_f']:.0f}°F  "
                         f"entry={t['entry_price']:.0f}¢  edge={t['edge']:.1f}¢  "
                         f"regime={t['regime']}  conf={t['confidence']:.0%}")
    else:
        lines.append("_No trades opened._")
    lines.append("")

    lines += ["## 4. Paper Trades Closed Today", ""]
    if data["trades_closed"]:
        for t in data["trades_closed"]:
            lines.append(f"- {t['station_code']} {t['side']} >{t['threshold_f']:.0f}°F  "
                         f"result={t['result']}  pnl={t['pnl_cents']:+.0f}¢  "
                         f"official_high={t['settlement_price']}°F  "
                         f"regime={t['regime']}")
    else:
        lines.append("_No trades closed._")
    lines.append("")

    # 6–8. Performance
    lines += ["## 5. P&L Summary (closed today)", ""]
    lines.append(f"- Trades: {pnl['total']}  wins: {pnl['wins']}  losses: {pnl['losses']}")
    lines.append(f"- Win rate: {pnl['win_rate']:.0%}")
    lines.append(f"- Total P&L: {pnl['pnl']:+.0f}¢")
    lines.append("")

    # 9. Settlements vs forecast
    lines += ["## 6. Settlements vs Forecast", ""]
    if data["settlements"]:
        lines += [
            "| Station | Official High | Forecast High | Error | Regime |",
            "|---|---|---|---|---|",
        ]
        for s in data["settlements"]:
            err = s.get("error")
            err_str = f"{err:+.1f}°F" if err is not None else "—"
            lines.append(f"| {s['station_code']} | {s.get('official_high','—')}°F "
                         f"| {s.get('forecast_high','—')}°F | {err_str} | {s.get('regime','—')} |")
    else:
        lines.append("_No settlements for this date._")
    lines.append("")

    # 10. Regime performance (30d)
    lines += ["## 7. Regime Performance (last 30 days)", ""]
    if data["regime_perf"]:
        lines += [
            "| Station | Regime | n | Win Rate | P&L ¢ |",
            "|---|---|---|---|---|",
        ]
        for r in data["regime_perf"]:
            wr = r["wins"] / r["n"] if r["n"] else 0
            lines.append(f"| {r['station_code']} | {r['regime']} | {r['n']} "
                         f"| {wr:.0%} | {r['total_pnl']:+.0f} |")
    else:
        lines.append("_No closed trades in last 30 days._")
    lines.append("")

    # 11. Model stats
    lines += ["## 8. Current Model Statistics", ""]
    if data["model_stats"]:
        lines += [
            "| Station | Regime | Avg Bias | Std Dev | n | 7d Bias |",
            "|---|---|---|---|---|---|",
        ]
        for m in data["model_stats"]:
            lines.append(f"| {m['station_code']} | {m['regime']} "
                         f"| {m.get('avg_bias','—')} | {m.get('std_dev','—')} "
                         f"| {m.get('sample_size','—')} | {m.get('rolling_7d_bias','—')} |")
    else:
        lines.append("_No model stats yet._")
    lines.append("")

    # 12. Alerts
    lines += ["## 9. Webhook Alerts Sent", ""]
    lines.append(f"Total alerts sent today: {len(data['alerts_sent'])}")
    for a in data["alerts_sent"]:
        lines.append(f"- {a['station_code']} {a['side']} >{a['threshold_f']:.0f} "
                     f"grade={a['grade']} edge={a['edge_cents']:.0f}¢")
    lines.append("")

    # 13. Model lessons / self-critique
    lines += ["## 10. Model Self-Critique", ""]
    if lessons:
        for l in lessons:
            icon = {"INFO": "ℹ️", "WARN": "⚠️", "ALERT": "🚨"}.get(l["severity"], "•")
            lines.append(f"**{icon} {l['severity']}** — {l['station_code']} / {l['regime']}")
            lines.append(f"> {l['lesson']}")
            if l.get("recommendation"):
                lines.append(f"> 💡 {l['recommendation']}")
            lines.append("")
    else:
        lines.append("_No issues flagged today._")
    lines.append("")

    # 14. Claude Review Packet
    lines += [
        "## 11. Claude Review Packet",
        "",
        "_This section is designed to be pasted into a Claude conversation for strategic analysis._",
        "",
        "```",
        f"Date: {date}",
        f"Model: {DEFAULT_MODEL}",
        f"Stations active: {len(data['active_stations'])}",
        f"Forecasts stored: {len(data['forecasts'])}",
        f"Settlements: {len(data['settlements'])}",
        f"Trades opened: {len(data['trades_opened'])}",
        f"Trades closed: {len(data['trades_closed'])}",
        f"Win rate (today): {pnl['win_rate']:.0%}",
        f"P&L (today): {pnl['pnl']:+.0f}¢",
        "",
    ]
    for l in lessons:
        lines.append(f"LESSON [{l['severity']}] {l['station_code']}/{l['regime']}: {l['lesson']}")
    lines += ["```", ""]

    return "\n".join(lines)


def _json_report(data: dict, lessons: list[dict]) -> dict:
    pnl = _pnl_summary(data["trades_closed"])
    return {
        "report_date":        data["date"],
        "generated_at":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model":              DEFAULT_MODEL,
        "active_stations":    [s["icao"] for s in data["active_stations"]],
        "forecasts_count":    len(data["forecasts"]),
        "settlements":        [
            {"station": s["station_code"], "official_high": s.get("official_high"),
             "forecast_high": s.get("forecast_high"), "error": s.get("error"),
             "regime": s.get("regime")}
            for s in data["settlements"]
        ],
        "trades_opened":      len(data["trades_opened"]),
        "trades_closed":      len(data["trades_closed"]),
        "pnl_summary":        pnl,
        "alerts_sent":        len(data["alerts_sent"]),
        "regime_perf_30d":    data["regime_perf"],
        "model_stats":        [
            {"station": m["station_code"], "regime": m["regime"],
             "avg_bias": m.get("avg_bias"), "std_dev": m.get("std_dev"),
             "sample_size": m.get("sample_size"), "rolling_7d_bias": m.get("rolling_7d_bias")}
            for m in data["model_stats"]
        ],
        "lessons":            lessons,
        "claude_review_packet": {
            "what_happened": (
                f"{len(data['settlements'])} stations settled. "
                f"{pnl['total']} trades closed ({pnl['wins']} wins, {pnl['losses']} losses). "
                f"P&L {pnl['pnl']:+.0f}¢."
            ),
            "lessons_count":  len(lessons),
            "alerts":         [s["severity"] for s in lessons],
            "suggested_questions": [
                "Which regimes had the largest bias drift this week?",
                "Are there any stations where the model is systematically over or underforecasting?",
                "Should any regime confidence weights be adjusted based on recent calibration?",
            ],
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_report(date: str, conn) -> tuple[str, str]:
    """
    Generate daily report for the given date.
    Returns (markdown_path, json_path).
    """
    data    = _gather_report_data(date, conn)
    lessons = _generate_lessons(data, conn)

    md_text  = _md_report(data, lessons)
    json_obj = _json_report(data, lessons)

    md_path   = REPORTS_DIR / "daily_model_report.md"
    json_path = REPORTS_DIR / "daily_model_report.json"

    md_path.write_text(md_text, encoding="utf-8")
    json_path.write_text(json.dumps(json_obj, indent=2), encoding="utf-8")

    # Store in claude_reviews table (auto mode, no Claude API yet)
    conn.execute("""
        INSERT INTO claude_reviews
            (report_date, summary, strengths, weaknesses,
             suggested_changes, suspicious_regimes, full_report_path, review_source)
        VALUES (?,?,?,?,?,?,?,'auto')
        ON CONFLICT(report_date) DO UPDATE SET
            summary=excluded.summary,
            strengths=excluded.strengths,
            weaknesses=excluded.weaknesses,
            suggested_changes=excluded.suggested_changes,
            suspicious_regimes=excluded.suspicious_regimes,
            full_report_path=excluded.full_report_path
    """, (
        date,
        json_obj["claude_review_packet"]["what_happened"],
        json.dumps([]),   # populated later when Claude API is connected
        json.dumps([l["lesson"] for l in lessons if l["severity"] in ("WARN","ALERT")]),
        json.dumps([l.get("recommendation","") for l in lessons if l.get("recommendation")]),
        json.dumps([l["regime"] for l in lessons if l["severity"] == "ALERT"]),
        str(md_path),
    ))
    conn.commit()

    return str(md_path), str(json_path)


def main():
    parser = argparse.ArgumentParser(description="Generate daily model report")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: yesterday)")
    args = parser.parse_args()

    date = args.date or (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    conn = init_db()

    print(f"Generating report for {date}...")
    md_path, json_path = generate_report(date, conn)
    print(f"  Markdown: {md_path}")
    print(f"  JSON:     {json_path}")


if __name__ == "__main__":
    main()
