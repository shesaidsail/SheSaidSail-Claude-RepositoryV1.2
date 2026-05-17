# Deploy Today: Step-by-Step Guide

**Who this is for:** Non-technical operators. No coding experience required.
**What you'll have at the end:** A live, 24/7 weather trading bot on a cloud server with a dashboard in your browser and SMS alerts on your phone.
**Time required:** 45–90 minutes.

> **Safety first:**
> This bot places **zero real trades**. It is paper-trading only.
> Kalshi API is used for market-data reading only — no orders are sent.
> No Robinhood integration. No real money moves automatically.

---

## Overview of what you're building

```
DigitalOcean server (always on)
  ├── Dashboard          → browser tab you open to see signals
  ├── Scanner            → fetches weather + market data every 2 min
  ├── Settlement worker  → closes paper trades each evening
  ├── CLV worker         → tracks how markets react to signals
  └── Daily report       → sends you a summary each morning

GitHub repository → auto-deploys to server when you push changes

Make.com → receives alerts from bot → sends you Quo SMS
```

---

## Part 1: DigitalOcean — Your Cloud Server

### Step 1.1 — Create a DigitalOcean account

👉 Go to: **https://cloud.digitalocean.com/registrations/new**

- Enter your email and create a password
- Verify your email address
- Add a payment method (credit card or PayPal)
- You get $200 free credits for 60 days as a new user

### Step 1.2 — Create a Droplet (your server)

👉 Go to: **https://cloud.digitalocean.com/droplets/new**

Fill in exactly these settings:

| Field | What to choose |
|-------|---------------|
| **Region** | Choose the city closest to you |
| **Image** | Ubuntu 24.04 (LTS) x64 |
| **Size** | **Basic → Regular → $12/month** (2 vCPU, 2 GB RAM, 60 GB disk) |
| **Authentication** | SSH Key (see step 1.3 below) |
| **Hostname** | `weather-edge-bot` |

Click **Create Droplet** and wait ~60 seconds.

When it's ready, you'll see an IP address like `143.244.12.55`. **Copy this — you'll need it.**

### Step 1.3 — Set up SSH key (your secure password to the server)

An SSH key is like a digital key that lets you log into your server securely. You need one.

**On Mac:**

Open the Terminal app (search "Terminal" in Spotlight).

```bash
ssh-keygen -t ed25519 -C "weather-bot"
```

Press Enter three times to accept defaults (no passphrase is fine).

Then run:
```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output — it starts with `ssh-ed25519`.

**On Windows:**

Open PowerShell (search "PowerShell" in Start menu).

```powershell
ssh-keygen -t ed25519 -C "weather-bot"
```

Press Enter three times.

Then run:
```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub
```

Copy the entire output.

**Add key to DigitalOcean:**

👉 Go to: **https://cloud.digitalocean.com/account/security**

- Click **Add SSH Key**
- Paste the key you copied
- Name it `weather-bot`
- Click **Add SSH Key**

> Full guide: **https://docs.digitalocean.com/products/droplets/how-to/add-ssh-keys/**

### Step 1.4 — Connect to your server

In Terminal (Mac) or PowerShell (Windows), replace `YOUR_IP` with your Droplet's IP:

```bash
ssh root@YOUR_IP
```

If it asks "Are you sure you want to continue connecting?" — type `yes` and press Enter.

You should see a prompt like `root@weather-edge-bot:~#` — you're now inside your server.

### Step 1.5 — Install Docker

Copy and paste this entire block into your server terminal:

```bash
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker
```

Wait for it to finish (about 60 seconds). Then verify:

```bash
docker --version
```

You should see something like `Docker version 26.x.x`.

> Full Docker install guide: **https://docs.docker.com/engine/install/ubuntu/**

Docker Compose comes bundled with modern Docker — you don't need to install it separately.

### Step 1.6 — Clone the repository

Still in your server terminal:

```bash
cd /opt
git clone https://github.com/shesaidsail/SheSaidSail-Claude-RepositoryV1.2.git weather-edge-bot
cd weather-edge-bot/weather-edge-bot/wx_market_edge
```

You should now be at the prompt:
`root@weather-edge-bot:/opt/weather-edge-bot/weather-edge-bot/wx_market_edge#`

### Step 1.7 — Create your .env file

This file holds your private API keys. It is never committed to git.

```bash
cp .env.example .env
nano .env
```

The nano editor opens. Use arrow keys to navigate. Fill in:

```
KALSHI_API_KEY=          ← paste your Kalshi API key here (Part 3 below)
KALSHI_API_SECRET=       ← paste your Kalshi API secret here
KALSHI_ENV=prod
MAKE_ALERT_WEBHOOK_URL=  ← paste your Make.com webhook URL here (Part 4 below)
ALERTS_ENABLED=true
PAPER_TRADING_ENABLED=true
PAPER_STARTING_BANKROLL=1000
PAPER_ALERTS_ENABLED=true
PAPER_ALERT_OPEN_TRADES=true
PAPER_ALERT_SETTLEMENTS=true
PAPER_ALERT_DAILY_SUMMARY=true
DASHBOARD_URL=http://YOUR_IP:8501
```

Replace `YOUR_IP` with your Droplet's IP address.

Save: press `Ctrl+X`, then `Y`, then `Enter`.

### Step 1.8 — Start the bot

```bash
docker compose build
docker compose up -d
```

The first build takes 3–5 minutes (downloading dependencies). Subsequent starts take 10 seconds.

### Step 1.9 — Open the dashboard

In your web browser, go to:

```
http://YOUR_IP:8501
```

Replace `YOUR_IP` with your Droplet IP. You should see the Weather Market Edge dashboard.

> If the page doesn't load immediately, wait 30 seconds and refresh — the dashboard takes a moment to start.

### Step 1.10 — Check everything is running

In your server terminal:

```bash
docker compose ps
```

You should see 5 services, all showing `running`:

```
NAME                STATUS
wx_dashboard        Up (healthy)
wx_scanner          Up
wx_settlement       Up
wx_clv              Up
wx_daily_report     Up
```

### Step 1.11 — View logs

```bash
# See all logs
docker compose logs -f

# See just the scanner
docker compose logs -f scanner

# See just the dashboard
docker compose logs -f dashboard

# Exit log view: press Ctrl+C
```

---

## Part 2: GitHub — Auto-Deploy Setup

Every time you push code changes to GitHub, the server automatically pulls them and restarts. This means you can update the bot from anywhere without SSH-ing in.

### Step 2.1 — Find the repository

👉 Go to: **https://github.com/shesaidsail/SheSaidSail-Claude-RepositoryV1.2**

### Step 2.2 — Add GitHub Secrets

These are the encrypted credentials that GitHub uses to deploy to your server.

👉 Go to: **https://github.com/shesaidsail/SheSaidSail-Claude-RepositoryV1.2/settings/secrets/actions**

Click **New repository secret** for each of the following:

| Secret Name | Where to get it | Example value |
|-------------|----------------|---------------|
| `DO_HOST` | Your Droplet IP address | `143.244.12.55` |
| `DO_USERNAME` | Always `root` (unless you created another user) | `root` |
| `DO_SSH_PRIVATE_KEY` | Your private SSH key (see below) | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `KALSHI_API_KEY` | From Kalshi (Part 3 below) | `abc123...` |
| `KALSHI_API_SECRET` | From Kalshi (Part 3 below) | `xyz789...` |
| `MAKE_ALERT_WEBHOOK_URL` | From Make.com (Part 4 below) | `https://hook.us1.make.com/abc123` |

**Getting your private SSH key:**

On Mac:
```bash
cat ~/.ssh/id_ed25519
```

On Windows PowerShell:
```powershell
type $env:USERPROFILE\.ssh\id_ed25519
```

Copy the **entire output** including the `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----` lines. Paste it as the value for `DO_SSH_PRIVATE_KEY`.

### Step 2.3 — Trigger a deploy manually

To trigger a deploy without pushing code:

👉 Go to: **https://github.com/shesaidsail/SheSaidSail-Claude-RepositoryV1.2/actions/workflows/deploy.yml**

Click **Run workflow** → **Run workflow** (green button).

Watch the workflow run. Green checkmark = success. Red X = something failed (click it to see the error).

### Step 2.4 — Confirm deploy succeeded

After the workflow shows a green checkmark:

1. Open your browser to `http://YOUR_IP:8501` — dashboard should load
2. SSH into your server and run: `docker compose ps` — all 5 services should show `running`

---

## Part 3: Kalshi — Market Data API

The bot reads weather contract prices from Kalshi. It **does not place orders**.

### Step 3.1 — Create a Kalshi account

👉 Go to: **https://kalshi.com**

Sign up and complete identity verification (required for API access).

### Step 3.2 — Get your API key

👉 Go to: **https://kalshi.com/account/api-credentials** (must be logged in)

- Click **Create API Key**
- Name it `weather-bot`
- Copy the **API Key** and **API Secret** — you'll only see the secret once
- **Permissions needed:** Read-only market data. The bot does NOT need trading permissions.

### Step 3.3 — Test the Kalshi connection

SSH into your server, navigate to the app directory, and run:

```bash
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
docker compose exec scanner python -c "
from ingestion.kalshi_auth import refresh_with_auth
from database.db import init_db
conn = init_db()
result = refresh_with_auth(conn)
print('Kalshi snapshots fetched:', result)
"
```

If you see a number (e.g., `Kalshi snapshots fetched: 42`), Kalshi is working.

If you see an authentication error, double-check your API key and secret in `.env`.

---

## Part 4: Make.com + Quo — SMS Alerts

The bot sends a webhook to Make.com when it finds a signal. Make.com routes that to Quo, which sends you an SMS.

### Step 4.1 — Create a Make.com account

👉 Go to: **https://www.make.com** and sign up (free plan is fine to start)

### Step 4.2 — Create a new scenario

1. Click **+ Create a new scenario**
2. Click the **+** circle in the center of the canvas
3. Search for **Webhooks** and select it
4. Choose **Custom Webhook**
5. Click **Add**
6. Click **Save** to create the webhook
7. **Copy the webhook URL** — it looks like: `https://hook.us1.make.com/abc123xyz`
8. Paste this URL into your `.env` as `MAKE_ALERT_WEBHOOK_URL=`

### Step 4.3 — Add the Quo module

1. Click the **+** after the webhook module on the canvas
2. Search for **Quo** and select it
3. Choose the **Send Message** action
4. Connect your Quo account (enter your Quo API key)
5. In the **To** field: enter your phone number (e.g., `+12125551234`)
6. In the **Message** field: click in the box and then click the webhook data bubble on the left to insert dynamic fields

Map the message like this (click each field from the webhook panel on the left):

```
🌡️ SIGNAL: {{1.station_code}} {{1.side}} >{{1.threshold_f}}°F
Market: {{1.market_price}}¢  |  Fair: {{1.fair_value}}¢  |  Edge: {{1.edge}}¢
Grade: {{1.grade}}  |  Confidence: {{1.confidence}}
Regime: {{1.regime}}
```

### Step 4.4 — Turn the scenario ON

At the bottom left of the Make.com canvas, toggle the scenario from **OFF** to **ON**.

### Step 4.5 — Send a test alert

SSH into your server:

```bash
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
docker compose exec scanner python scripts/test_make_alert.py
```

You should receive an SMS within 30 seconds. If you don't:
- Check that the Make.com scenario is toggled **ON**
- Check that `MAKE_ALERT_WEBHOOK_URL` in `.env` is correct
- Check Make.com scenario history for errors (Runs → click the latest run)

---

## Part 5: Bot Commands — Daily Operations

All commands run on your server. First SSH in:

```bash
ssh root@YOUR_IP
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
```

### Start everything

```bash
docker compose up -d
```

### Stop everything

```bash
docker compose down
```

### Restart everything

```bash
docker compose restart
```

### Restart one service (e.g., if scanner crashed)

```bash
docker compose restart scanner
```

### View live logs

```bash
docker compose logs -f                  # all services
docker compose logs -f scanner          # scanner only
docker compose logs -f dashboard        # dashboard only
docker compose logs -f settlement       # settlement only
```

Press `Ctrl+C` to stop watching logs.

### Check data health

```bash
docker compose exec scanner python scripts/health_check.py
```

Output shows ✅ or ❌ for each data feed.

### Send a test alert

```bash
docker compose exec scanner python scripts/test_make_alert.py
```

### Open the dashboard

In any browser: `http://YOUR_IP:8501`

### Check paper trade performance

In the dashboard, click **📊 Performance** in the left sidebar.

Or from the terminal:

```bash
docker compose exec scanner python -c "
from database.db import init_db
from trading.paper_trader import performance_summary
conn = init_db()
import json; print(json.dumps(performance_summary(conn), indent=2))
"
```

---

## Part 6: Verification Checklist

Run through this after first deployment. Each item should show ✅.

### Check 1 — All 5 Docker services running

```bash
docker compose ps
```

Expected output (all should say `running`):
```
wx_dashboard    running (healthy)
wx_scanner      running
wx_settlement   running
wx_clv          running
wx_daily_report running
```

✅ Pass if all show `running`
❌ Fail if any show `exited` or `restarting`

**Fix:** `docker compose logs SERVICE_NAME` to see why it crashed

---

### Check 2 — Dashboard loads in browser

Open: `http://YOUR_IP:8501`

✅ Pass if you see the Weather Market Edge dashboard
❌ Fail if you see "This site can't be reached"

**Fix:** Check firewall (`ufw status`). If active, run: `ufw allow 8501/tcp`

---

### Check 3 — Open-Meteo forecast feed working

```bash
docker compose exec scanner python scripts/health_check.py
```

Look for the `forecast` line.

✅ Pass if it shows `✅ forecast`
❌ Fail if it shows `❌ forecast  never succeeded`

**Fix:** Open-Meteo is a free API with no key required. If failing, the scheduler may not have run yet — wait 2 minutes and check again.

---

### Check 4 — NOAA/METAR feed working

Same health check output — look for `metar` line.

✅ Pass if it shows `✅ metar`
❌ Fail if stale or never succeeded

**Fix:** METAR also requires no API key. If failing, wait 5 minutes for first refresh.

---

### Check 5 — Kalshi API working

Same health check output — look for `kalshi` line.

✅ Pass if it shows `✅ kalshi`
❌ Fail if it shows authentication error

**Fix:** Check your `KALSHI_API_KEY` and `KALSHI_API_SECRET` in `.env`. Make sure `KALSHI_ENV=prod` (not `demo`) for live market data.

---

### Check 6 — SQLite database writing

```bash
ls -lh data/wx_edge.db
```

✅ Pass if file exists and size is growing (run twice, 30 seconds apart)
❌ Fail if file doesn't exist

**Fix:** `docker compose logs scanner` — look for database errors

---

### Check 7 — Paper trading enabled

```bash
docker compose exec scanner python -c "
from config import _paper_trading_enabled
print('Paper trading:', _paper_trading_enabled())
"
```

✅ Pass if output is `Paper trading: True`
❌ Fail if output is `Paper trading: False`

**Fix:** In `.env`, set `PAPER_TRADING_ENABLED=true` then restart: `docker compose restart`

---

### Check 8 — Make webhook working

```bash
docker compose exec scanner python scripts/test_make_alert.py
```

✅ Pass if you receive an SMS within 60 seconds
❌ Fail if you get a webhook error or no SMS

**Fix checklist:**
1. Is `MAKE_ALERT_WEBHOOK_URL` set in `.env`?
2. Is the Make.com scenario toggled **ON**?
3. Is the Quo module configured with a valid phone number?

---

### Check 9 — Quo SMS received

This is confirmed by the test in Check 8.

✅ Pass if SMS arrives on your phone
❌ Fail if no SMS

**Fix:** In Make.com, click **History** on your scenario to see if the webhook arrived but the SMS send failed.

---

## Part 7: Daily Use

### What URL do I open?

Bookmark this: `http://YOUR_IP:8501`

The dashboard has 14 pages in the left sidebar:
- **🏠 Home** — current signals and bankroll summary
- **📊 Performance** — win rate, P&L, ROI
- **📈 Backtester** — replay historical data
- **🌡️ Regime Analysis** — how different weather patterns perform
- **💰 Fee Analysis** — gross vs net edge after Kalshi fees
- **⚡ Market Adaptation** — how fast markets react to your signals

### What alerts will I receive?

You get an SMS when:
1. **New signal found** — station, side, edge, grade, regime
2. **Paper trade opened** — same signal, includes stake size
3. **Paper trade settled** — WIN or LOSS, P&L in dollars
4. **Daily summary** — total trades, P&L, win rate (sent each morning)

Alerts respect a cooldown (default 30 min) — you won't get spammed.

### How do I know paper trading is working?

In the dashboard → **Performance** page, you'll see:
- Total trades (paper)
- Win rate
- Cumulative P&L
- Open positions

You can also check the terminal:
```bash
docker compose exec scanner python -c "
from database.db import init_db
from trading.paper_trader import get_open_trades, get_closed_trades
conn = init_db()
print('Open trades:', len(get_open_trades(conn)))
print('Closed trades:', len(get_closed_trades(conn)))
"
```

### How do I review performance?

Dashboard → **📊 Performance** page shows:
- By station (which cities are most profitable)
- By regime (which weather patterns edge best)
- By threshold (which temperature levels are most mispriced)

### How do I pause alerts (without stopping the bot)?

In your `.env` file on the server:

```bash
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
nano .env
```

Change `ALERTS_ENABLED=true` to `ALERTS_ENABLED=false`

Save (`Ctrl+X`, `Y`, `Enter`) and restart:

```bash
docker compose restart scanner
```

To re-enable: change it back to `true` and restart.

### How do I pause paper trading?

In `.env`, change `PAPER_TRADING_ENABLED=true` to `PAPER_TRADING_ENABLED=false`, then:

```bash
docker compose restart scanner
```

No new paper trades will be opened. Existing open trades remain until they settle.

### How do I restart if something breaks?

```bash
ssh root@YOUR_IP
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
docker compose down
docker compose up -d
docker compose ps
```

If a single service is misbehaving:

```bash
docker compose restart scanner     # restart just the scanner
docker compose logs -f scanner     # see what went wrong
```

---

## Part 8: Safety Guarantees

### No real trades are placed

- The bot is 100% paper trading
- It analyzes edges and simulates trades using a virtual $1,000 bankroll
- No money moves — not from any account, not automatically

### Kalshi is market-data only

- The bot connects to Kalshi to read market prices
- It does NOT place orders, does NOT send buy/sell instructions
- Even if you gave it trading API permissions, the code does not call any order endpoint

### Robinhood is not connected

- There is no Robinhood integration, no Robinhood SDK, no Robinhood API calls
- Any real trades on Robinhood are 100% manual decisions you make yourself

### Your .env secrets are never committed to git

Verify:

```bash
cat /opt/weather-edge-bot/.gitignore | grep .env
```

Output should include `.env` — confirming it's excluded from git history.

Confirm the live .env file is NOT in git:

```bash
cd /opt/weather-edge-bot
git status weather-edge-bot/wx_market_edge/.env
```

Output should say `nothing to commit` or the file should not appear — not `modified`.

---

## Troubleshooting

### "This site can't be reached" when opening the dashboard

```bash
# Check the dashboard container is running
docker compose ps

# Check the dashboard logs
docker compose logs dashboard

# Check firewall
ufw status
ufw allow 8501/tcp
```

### Dashboard loads but shows no data

The scanner hasn't run a full cycle yet. Wait 3–5 minutes and refresh. Check logs:

```bash
docker compose logs -f scanner
```

### Kalshi authentication error

```bash
docker compose exec scanner python -c "
import os; from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('.')/'.env')
print('Key set:', bool(os.getenv('KALSHI_API_KEY')))
print('Secret set:', bool(os.getenv('KALSHI_API_SECRET')))
print('Env:', os.getenv('KALSHI_ENV'))
"
```

If Key or Secret shows `False`, your `.env` is missing those values. Re-edit with `nano .env`.

### Make.com webhook not receiving data

```bash
docker compose exec scanner python scripts/test_make_alert.py --dry-run
```

`--dry-run` prints the payload without sending. Verify the payload looks correct, then try without `--dry-run`.

### A service keeps restarting (crash loop)

```bash
docker compose logs --tail=50 SERVICE_NAME
```

Common causes:
- Missing `.env` file → recreate it from `.env.example`
- Database corruption → restore from backup (see below)
- Port already in use → `lsof -i :8501` to find what's using it

### Out of disk space

```bash
df -h          # check disk usage
docker system prune -f   # clean up unused Docker layers (frees ~1-2 GB)
```

---

## Rollback Instructions

If an update breaks things:

```bash
cd /opt/weather-edge-bot

# See recent commits
git log --oneline -10

# Roll back to a specific commit (replace HASH with the one you want)
git checkout HASH -- weather-edge-bot/wx_market_edge/

# Restart
cd weather-edge-bot/wx_market_edge
docker compose build
docker compose down && docker compose up -d
```

---

## Backup and Restore

### Create a backup

```bash
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
docker compose exec scanner python scripts/backup_database.py
ls backups/
```

### Restore from backup

```bash
# Stop the bot
docker compose down

# Replace the database
cp backups/wx_edge_YYYYMMDD.db data/wx_edge.db

# Restart
docker compose up -d
```

---

## Repo File Audit

All required files confirmed present:

| File | Purpose | Status |
|------|---------|--------|
| `docker-compose.yml` | Defines all 5 services | ✅ exists |
| `.github/workflows/deploy.yml` | GitHub Actions auto-deploy | ✅ exists |
| `.env.example` | Template for your credentials | ✅ exists |
| `.gitignore` includes `.env` | Prevents secret commits | ✅ confirmed |
| `scripts/test_make_alert.py` | Send a test SMS | ✅ exists |
| `scripts/health_check.py` | Verify all feeds | ✅ exists |
| `docs/DIGITALOCEAN_DEPLOY.md` | Infrastructure detail docs | ✅ exists |

---

## Your First 3 Actions Right Now

### Action 1 — First thing to click

👉 **https://cloud.digitalocean.com/registrations/new**

Create your DigitalOcean account. Takes 3 minutes.

### Action 2 — First command to run (on your laptop)

After creating your DigitalOcean account and getting a Droplet IP:

```bash
ssh root@YOUR_IP
```

This connects you to your server. Everything else runs from there.

### Action 3 — First command to run on the server

```bash
curl -fsSL https://get.docker.com | sh && systemctl enable docker && systemctl start docker
```

This installs Docker — the foundation for everything else.

---

*Once Docker is installed, return to Step 1.6 above and continue from there.*
