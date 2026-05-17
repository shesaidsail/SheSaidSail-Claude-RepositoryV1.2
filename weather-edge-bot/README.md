# Weather Edge Bot

A multi-station weather prediction market analysis and paper trading system
built on Kalshi temperature contracts.

**This project is 100% standalone. It shares no code with the SheSaidSail
production application.** Alerts are sent through Make.com webhooks via
environment variables — the only connection to the broader stack.

---

## What It Does

- Pulls daily high-temperature forecasts from Open-Meteo (free API)
- Ingests live METAR observations from NOAA NWS
- Reads Kalshi market prices (read-only — no order placement)
- Classifies weather regimes and applies a bias-corrected probability engine
- Grades trade signals A+/B/Watchlist/Avoid with fee-aware net edge
- Auto-opens paper trades (simulated — no real money)
- Tracks a $1,000 simulated bankroll with fractional Kelly sizing
- Sends alerts to Make.com → Quo/SMS for paper trade events
- Runs a 14-page Streamlit dashboard

---

## Project Layout

```
weather-edge-bot/
├── wx_market_edge/          ← main production system
│   ├── config.py            ← all settings (reads from .env)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── run.sh               ← start dashboard + scanner locally
│   ├── setup.sh             ← first-time setup
│   ├── alerts/              ← Make.com webhook alerts
│   ├── dashboard/           ← 14-page Streamlit app
│   ├── database/            ← SQLite schema + migrations
│   ├── docs/                ← DEPLOY_24_7.md — production deployment guide
│   ├── ingestion/           ← Open-Meteo, METAR, Kalshi fetchers
│   ├── models/              ← bias, regime, confidence, edge, fee engines
│   ├── scripts/             ← scheduler, settlement worker, health check
│   ├── tests/               ← 89 pytest tests (all passing)
│   └── trading/             ← bankroll, bet sizer, paper trader, backtester
└── archive/                 ← earlier single-station prototypes (KLAX only)
    ├── klax_phase2/
    ├── klax_phase3/
    └── weather_edge_tracker/
```

---

## Quick Start (Local)

```bash
cd weather-edge-bot/wx_market_edge

# 1. Copy and configure environment
cp .env.example .env
# Edit .env — add your KALSHI_API_KEY and MAKE_WEBHOOK_URL at minimum

# 2. Install dependencies
pip install -r requirements.txt

# 3. First-time setup (creates data/ and logs/ dirs, initialises DB)
python setup.sh       # or: python -c "from database.db import init_db; init_db()"

# 4. Run the dashboard
streamlit run dashboard/app.py --server.port 8501

# 5. Run the market scanner (separate terminal)
python scripts/scheduler.py

# 6. Run the settlement worker (separate terminal)
python scripts/settle_worker.py
```

Dashboard opens at: http://localhost:8501

---

## Run with Docker (recommended for 24/7)

```bash
cd weather-edge-bot/wx_market_edge

# Copy and fill in your .env file
cp .env.example .env

# Start all three services (dashboard + scanner + settlement)
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

See `docs/DEPLOY_24_7.md` for full cloud deployment guide (DigitalOcean, Render).

---

## Run Tests

```bash
cd weather-edge-bot/wx_market_edge
python -m pytest tests/ -v
# Expected: 89 passed
```

---

## Environment Variables

Create `wx_market_edge/.env` (never committed). See `.env.example` for all options.

Critical variables:

| Variable | Required | Description |
|---|---|---|
| `KALSHI_API_KEY` | Optional | Kalshi API key — for authenticated market data. Public markets work without it. |
| `MAKE_WEBHOOK_URL` | Optional | Make.com webhook URL for alerts → Quo/SMS. Alerts are silently skipped if not set. |
| `PAPER_STARTING_BANKROLL` | No | Starting bankroll in dollars (default: 1000) |
| `KALSHI_SETTLEMENT_FEE_PCT` | No | Kalshi fee rate on winning profits (default: 3.0) |
| `MIN_NET_EDGE` | No | Minimum net edge after fees to open a trade (default: 3.0¢) |

**No API keys are shared with the SheSaidSail application.**
Each project maintains its own separate `.env` file.

---

## Alerts via Make.com

The bot sends webhook POSTs to `MAKE_WEBHOOK_URL` only. Make.com routes these
to Quo/SMS. No direct Quo API calls, no hardcoded credentials.

Alert types:
- `PAPER_TRADE_OPENED` — new simulated trade
- `PAPER_TRADE_SETTLED` — trade result + P&L
- `PAPER_DAILY_SUMMARY` — end-of-day bankroll summary

---

## PAPER TRADING ONLY

All trades are simulated. No real money. No real orders are placed on Kalshi.
Kalshi API access is read-only for market data only.
Every alert and dashboard display is labeled: **PAPER TRADE — NOT REAL MONEY**.

---

## Stations Tracked

KLAX, KJFK, KORD, KMIA, KPHX, KDFW, KDEN, KSEA, KSFO, KBOS
