# Deploying Weather Market Edge Tracker — 24/7 Guide

This guide covers running the full system continuously so it:
- pulls Open-Meteo forecasts every hour
- pulls NOAA/METAR observations every 5 minutes
- pulls Kalshi market data every 2 minutes
- enters paper trades automatically when rules are met
- tracks bankroll and fires Make/Quo alerts
- keeps the Streamlit dashboard live

**Everything is paper trading. No real money. No trade execution.**

---

## Architecture

```
┌─────────────────────────────────────┐
│  docker compose                     │
│                                     │
│  dashboard   (Streamlit :8501)      │
│  scanner     (scheduler.py loop)    │
│  settlement  (settle_worker.py)     │
│                                     │
│  shared volume: data/wx_edge.db     │
└─────────────────────────────────────┘
```

Three services share one SQLite database on a named Docker volume so data survives container restarts and updates.

---

## Quick Start (local)

### 1. Prerequisites

- Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- `docker compose` v2

### 2. Clone / navigate to the project

```bash
cd 07_DATA_ANALYTICS/wx_market_edge
```

### 3. Create your `.env` file

```bash
cp .env.example .env
nano .env   # fill in your values
```

Minimum required:

```
MAKE_ALERT_WEBHOOK_URL=https://hook.eu1.make.com/YOUR_HOOK_ID
PAPER_TRADING_ENABLED=true
PAPER_ALERTS_ENABLED=true
```

Optional (for Kalshi market data):

```
KALSHI_API_KEY=your_key
KALSHI_API_SECRET=your_secret
KALSHI_ENV=demo
```

### 4. Start everything

```bash
docker compose up -d
```

### 5. Confirm it's running

```bash
docker compose ps
```

```
NAME             STATUS    PORTS
wx_dashboard     running   0.0.0.0:8501->8501/tcp
wx_scanner       running
wx_settlement    running
```

Open the dashboard: **http://localhost:8501**

---

## Common Commands

| Task | Command |
|---|---|
| Start all services | `docker compose up -d` |
| Stop all services | `docker compose down` |
| Restart all services | `docker compose restart` |
| Restart one service | `docker compose restart scanner` |
| View all logs | `docker compose logs -f` |
| View scanner logs | `docker compose logs -f scanner` |
| View settlement logs | `docker compose logs -f settlement` |
| Check health | `docker compose exec scanner python scripts/health_check.py` |
| Run backup | `docker compose exec scanner python scripts/backup_database.py --keep 30` |
| Open bash in scanner | `docker compose exec scanner bash` |

---

## View Logs

Log files are written to the `wx_logs` Docker volume and mounted at `/app/logs/` inside containers.

```bash
docker compose logs -f scanner       # live scanner output
docker compose logs -f settlement    # settlement + alert output
docker compose logs --tail=100       # last 100 lines from all services
```

To access log files directly:

```bash
docker compose exec scanner cat logs/scheduler.log
docker compose exec scanner cat logs/settlement.log
```

---

## How Alerts Work

1. **Scanner** finds an A+/B signal → sends `WEATHER_SIGNAL` alert to Make webhook
2. **Scanner** auto-enters paper trade → sends `PAPER_TRADE_OPENED` alert
3. **Settlement worker** settles trade → sends `PAPER_TRADE_SETTLED` alert
4. **Settlement worker** at 23:50 UTC → sends `PAPER_DAILY_SUMMARY` alert

Make.com receives all payloads at the same `MAKE_ALERT_WEBHOOK_URL` and routes by `alert_type` field.

---

## Pause / Resume Paper Trading

```bash
# Pause — edit .env
PAPER_TRADING_ENABLED=false

# Apply without full restart
docker compose restart scanner settlement
```

Or pause alerts only:

```bash
PAPER_ALERTS_ENABLED=false
docker compose restart scanner settlement
```

---

## Reset Paper Bankroll

From the dashboard: **Page 10 → Admin → Reset Paper Bankroll to $1,000**

Or from command line:

```bash
docker compose exec scanner python -c "
from database.db import init_db
conn = init_db()
conn.execute(\"UPDATE paper_trades SET status='VOID' WHERE status='OPEN'\")
conn.execute(\"DELETE FROM bankroll_history\")
conn.commit()
print('Bankroll reset.')
"
```

---

## Database Backup

Backups are written to `backups/weather_trading_YYYY_MM_DD.sqlite`.

**Manual backup:**

```bash
docker compose exec scanner python scripts/backup_database.py --keep 30
```

**Automated daily backup (add to crontab on host):**

```bash
crontab -e
# Add:
0 2 * * * cd /path/to/wx_market_edge && docker compose exec -T scanner python scripts/backup_database.py --keep 30
```

---

## Deploy to DigitalOcean Droplet

### 1. Create droplet

- **Image:** Ubuntu 24.04
- **Size:** Basic, $6/month (1 vCPU, 1 GB RAM) is sufficient
- **Region:** Choose closest to you

### 2. Install Docker

```bash
ssh root@YOUR_DROPLET_IP

curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker
```

### 3. Upload project

From your local machine:

```bash
scp -r 07_DATA_ANALYTICS/wx_market_edge root@YOUR_DROPLET_IP:/opt/wx_market_edge
```

Or clone from GitHub:

```bash
git clone https://github.com/YOUR_ORG/YOUR_REPO.git /opt/wx_repo
cd /opt/wx_repo/07_DATA_ANALYTICS/wx_market_edge
```

### 4. Create `.env` on the server

```bash
cd /opt/wx_market_edge   # or wherever you uploaded to
nano .env                # paste your credentials
```

### 5. Start services

```bash
docker compose up -d
```

### 6. Open firewall for dashboard (optional)

```bash
ufw allow 8501/tcp
```

Access dashboard at: `http://YOUR_DROPLET_IP:8501`

### 7. Auto-restart on server reboot

Docker's `restart: unless-stopped` handles this automatically once the containers have started once.

---

## Deploy to Render

Render can run Docker containers but has limited free-tier support for persistent storage.

**Recommended approach:**

1. Push your repo to GitHub
2. In Render: New Web Service → connect repo → Dockerfile
3. For the scanner and settlement workers: use Render **Background Workers** (paid plan)
4. Use a **Render Disk** ($1/month) mounted at `/app/data` for SQLite persistence
5. Add environment variables in Render dashboard (do not commit `.env`)

**Limitation:** Render free tier sleeps after 15 minutes of inactivity — not suitable for 24/7 scanning. Use paid plan or DigitalOcean.

---

## Health Check

```bash
docker compose exec scanner python scripts/health_check.py
```

Expected output:

```
==================================================
  Weather Market Edge — Health Check
  2026-05-17T14:30:00Z
==================================================
  ✅ forecast              age: 45.2m
  ✅ metar                 age: 3.1m
  ✅ kalshi                age: 1.8m
  ✅ paper_trading         age: 0.3h
  ✅ bankroll              drawdown: 0.0%
  ℹ️  open_positions       2

  Overall: ✅ HEALTHY
```

---

## Updating the System

```bash
# Pull new code
git pull

# Rebuild image with new code
docker compose build

# Restart with new image (data is preserved in volumes)
docker compose up -d
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Dashboard won't load | `docker compose logs dashboard` — check for import errors |
| No paper trades opening | Check `PAPER_TRADING_ENABLED=true` in `.env` |
| No alerts received | Verify `MAKE_ALERT_WEBHOOK_URL` is set; check Make scenario is ON |
| Kalshi data stale | Check API key in `.env`; scanner logs will show error |
| Database locked | Only one process should write at a time; restart all: `docker compose restart` |
| Container keeps restarting | `docker compose logs <service>` — fix the Python error shown |
| Need to wipe and restart fresh | `docker compose down -v` (**deletes all data**) then `docker compose up -d` |

---

## Security Notes

- Never commit `.env` to git (it's in `.gitignore`)
- The SQLite database contains paper trade history — no credentials
- Kalshi API key is read-only for market data; never used for order execution
- The Make webhook URL only receives data from this system; it doesn't grant access
