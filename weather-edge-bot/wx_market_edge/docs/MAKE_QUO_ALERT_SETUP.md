# Make.com + Quo Alert Setup

This guide explains how to connect the weather trading system's webhook alerts to SMS/Quo delivery via Make.com.

---

## Overview

```
Python system
  → detects A+/B signal
  → POSTs JSON to Make.com Custom Webhook
      → Make filters/formats
          → Quo sends SMS
          → (optional) Slack/Discord/email
```

Python never touches Quo directly. Make.com owns the delivery layer.

---

## Step 1 — Create the Make.com Scenario

1. Log in to [make.com](https://make.com)
2. Click **Create a new scenario**
3. Add first module: **Webhooks → Custom Webhook**
4. Click **Add** → name it `Weather Signal Alert`
5. Copy the webhook URL shown (looks like `https://hook.eu1.make.com/xxxxxxxx`)
6. Paste it into your `.env` file:

```
MAKE_ALERT_WEBHOOK_URL=https://hook.eu1.make.com/xxxxxxxx
```

---

## Step 2 — Test the Webhook

Run the test script to verify Make receives the payload:

```bash
cd 07_DATA_ANALYTICS/wx_market_edge
python scripts/test_make_alert.py
```

In Make.com, click **Run once** before running the script — Make needs to be listening to learn the data structure.

After the script runs, Make shows the received payload. Click **OK** to save the data structure.

---

## Step 3 — Add a Filter (A+ and B only)

After the webhook module, add a **Filter** module:

- Condition: `grade` **Equal to** `A+`  **OR**  `grade` **Equal to** `B`

This ensures only high-quality signals proceed to SMS.

---

## Step 4 — Format the SMS via Quo

Add a **Quo → Send Message** module (or whatever Quo module you have configured):

**Message body — use the pre-built SMS text:**

```
{{1.sms_text}}
```

This delivers the formatted message:

```
A+ WEATHER SIGNAL
KLAX YES >69
Price: 31¢ | Fair: 56¢
Edge: +25¢ | Conf: HIGH
Regime: MARINE_WEAK
Action: Manual review
```

**Alternative — build a custom message from fields:**

```
{{1.grade}} SIGNAL: {{1.station}} {{1.side}} >{{1.threshold}}°F
Edge: +{{1.edge_cents}}¢  |  Confidence: {{1.confidence}}
Regime: {{1.regime}}
Fair Value: {{1.fair_value_cents}}¢  Market: {{1.market_price_cents}}¢
Adjusted forecast: {{1.adjusted_forecast_f}}°F
{{1.reason}}
Dashboard: {{1.dashboard_url}}
```

---

## Step 5 — Optional: Add Slack or Discord

Add a **Slack → Send a Message** or **Discord → Send a Message** module in parallel:

```
{{1.grade}} | {{1.station}} {{1.side}} >{{1.threshold}} | Edge: +{{1.edge_cents}}¢ | {{1.regime}}
```

---

## Step 6 — Turn On the Scenario

- Set scheduling to **Immediately** (webhook-triggered, not scheduled)
- Click **Save** and **Turn on**

---

## Full Payload Reference

Every alert POSTs this JSON structure:

| Field | Example | Description |
|---|---|---|
| `alert_type` | `WEATHER_SIGNAL` | Always this value |
| `grade` | `A+` | Signal quality: A+ or B |
| `station` | `KLAX` | ICAO station code |
| `station_name` | `Los Angeles` | Human name |
| `market_ticker` | `KLAX-HIGH-69` | Contract identifier |
| `side` | `YES` | YES or NO |
| `threshold` | `69` | Contract strike in °F |
| `market_price_cents` | `31` | Current Kalshi price |
| `fair_value_cents` | `56` | Model fair value |
| `edge_cents` | `25` | fair_value - market_price |
| `confidence` | `HIGH` | LOW / MEDIUM / HIGH / VERY_HIGH |
| `confidence_score` | `0.78` | Raw 0-1 score |
| `regime` | `MARINE_WEAK` | Active weather regime |
| `adjusted_forecast_f` | `70.4` | Bias-corrected forecast |
| `openmeteo_forecast_f` | `68.2` | Raw Open-Meteo forecast |
| `official_current_temp_f` | `67.1` | Latest METAR temp |
| `wind` | `250° @ 8 kts` | Live wind summary |
| `reason` | `"Onshore flow..."` | Model reasoning |
| `action` | `MANUAL REVIEW / PAPER TRADE` | Recommended action |
| `timestamp_utc` | `2026-05-17T14:30:00Z` | Alert time |
| `dashboard_url` | `http://localhost:8501` | Your dashboard |
| `sms_text` | `"A+ WEATHER SIGNAL..."` | Pre-formatted SMS |

---

## Environment Variables

```bash
# .env
MAKE_ALERT_WEBHOOK_URL=https://hook.eu1.make.com/your-hook-id
ALERTS_ENABLED=true
MIN_ALERT_EDGE_CENTS=10
MIN_ALERT_CONFIDENCE=MEDIUM
ALERT_COOLDOWN_MINUTES=30
DASHBOARD_URL=http://localhost:8501
```

| Variable | Default | Description |
|---|---|---|
| `MAKE_ALERT_WEBHOOK_URL` | — | Your Make.com webhook URL |
| `ALERTS_ENABLED` | `true` | Master on/off switch |
| `MIN_ALERT_EDGE_CENTS` | `10` | Minimum edge to alert |
| `MIN_ALERT_CONFIDENCE` | `MEDIUM` | Minimum confidence level |
| `ALERT_COOLDOWN_MINUTES` | `30` | Suppress duplicate alerts |
| `DASHBOARD_URL` | `http://localhost:8501` | Included in payload |

---

## Testing Checklist

```bash
# 1. Check config
python -c "from alerts.webhook_alerts import is_configured; print(is_configured())"

# 2. Dry run (no POST)
python scripts/test_make_alert.py --dry-run

# 3. Send real test (Make.com must be listening)
python scripts/test_make_alert.py

# 4. Check alert was logged
python -c "
import sys; sys.path.insert(0,'.')
from database.db import init_db
conn = init_db()
rows = conn.execute('SELECT id, status, response_code FROM webhook_alerts ORDER BY id DESC LIMIT 5').fetchall()
for r in rows: print(dict(r))
"
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `MAKE_ALERT_WEBHOOK_URL is not set` | Add URL to `.env`, restart dashboard |
| HTTP 400 from Make | Make scenario not active or not in "Run once" mode |
| HTTP 401 | Webhook URL expired — regenerate in Make |
| No SMS received | Check Make execution log; Quo module may have error |
| Duplicate alerts | Increase `ALERT_COOLDOWN_MINUTES` |
| Too many alerts | Raise `MIN_ALERT_EDGE_CENTS` or `MIN_ALERT_CONFIDENCE` |
