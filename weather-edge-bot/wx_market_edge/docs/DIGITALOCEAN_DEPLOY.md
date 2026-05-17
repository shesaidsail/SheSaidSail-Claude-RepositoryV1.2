# DigitalOcean Deployment Guide

Deploy the Weather Market Edge Bot as a 24/7 service on a DigitalOcean Droplet
using Docker Compose + GitHub Actions continuous deployment.

---

## Prerequisites

- DigitalOcean account
- GitHub repository with this code
- Kalshi API key (read-only market data)
- Make.com webhook URL (optional, for SMS/Slack alerts)

---

## 1. Create a Droplet

1. Go to DigitalOcean → Create → Droplets
2. **Image:** Ubuntu 24.04 LTS
3. **Size:** Basic, $12/month (2 vCPU, 2GB RAM) — sufficient for SQLite + 5 workers
4. **Authentication:** Add your SSH public key
5. **Hostname:** `weather-edge-bot` (or anything you like)
6. Click **Create Droplet** and note the IP address

---

## 2. Install Docker on the Droplet

SSH into your droplet, then:

```bash
ssh root@YOUR_DROPLET_IP

# Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# Add your user to the docker group (if not root)
usermod -aG docker $USER
```

---

## 3. Clone the Repository

```bash
cd /opt
git clone https://github.com/YOUR_ORG/SheSaidSail-Claude-RepositoryV1.2.git weather-edge-bot
cd weather-edge-bot/weather-edge-bot/wx_market_edge
```

---

## 4. Configure Environment Variables

```bash
# Copy the production template
cp production.env.example .env

# Edit with your real values
nano .env
```

Required values:
- `KALSHI_API_KEY` — from your Kalshi account
- `KALSHI_API_SECRET` — from your Kalshi account
- `MAKE_ALERT_WEBHOOK_URL` — from Make.com scenario (optional)

**Never commit `.env` to git.**

---

## 5. Start the Services

```bash
cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge
docker compose build
docker compose up -d
```

Check everything is running:

```bash
docker compose ps
docker compose logs -f
```

The dashboard will be available at: `http://YOUR_DROPLET_IP:8501`

---

## 6. Configure GitHub Actions for Auto-Deploy

### 6a. Add GitHub Secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret Name           | Value                                      |
|-----------------------|--------------------------------------------|
| `DO_HOST`             | Your droplet IP address                    |
| `DO_USERNAME`         | `root` (or your sudo user)                 |
| `DO_SSH_PRIVATE_KEY`  | Your SSH private key (full content)        |
| `KALSHI_API_KEY`      | Your Kalshi API key                        |
| `KALSHI_API_SECRET`   | Your Kalshi API secret                     |
| `MAKE_ALERT_WEBHOOK_URL` | Your Make.com webhook URL              |

### 6b. Push to main to trigger deploy

Every push to `main` that touches `weather-edge-bot/**` will:
1. SSH into your droplet
2. Pull the latest code
3. Write `.env` from GitHub Secrets (not from git)
4. Rebuild Docker images
5. Restart all services
6. Verify the dashboard health endpoint

---

## 7. Verify the Deployment

```bash
# Check all services are healthy
docker compose ps

# Tail logs for a specific service
docker compose logs -f scanner
docker compose logs -f dashboard

# Check the dashboard health endpoint
curl http://localhost:8501/_stcore/health

# Check the database is being written to
ls -lh data/wx_edge.db
```

---

## 8. Services Overview

| Container          | Role                                                  |
|--------------------|-------------------------------------------------------|
| `wx_dashboard`     | Streamlit dashboard on port 8501                      |
| `wx_scanner`       | Fetches forecasts/METARs/Kalshi data, runs edge calc  |
| `wx_settlement`    | Settles closed paper trades each hour                 |
| `wx_clv`           | Records CLV market-price snapshots every 15 min       |
| `wx_daily_report`  | Sends daily summary alert via Make.com                |

All containers share the same SQLite database via Docker volumes.

---

## 9. Backup Instructions

The database is stored in Docker volume `wx_data`. To back it up:

```bash
# Run the built-in backup script
docker compose exec scanner python scripts/backup_database.py

# Or copy the volume data directly
docker run --rm \
  -v weather-edge-bot_wx_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/wx_edge_$(date +%Y%m%d).tar.gz -C /data .
```

Schedule daily backups with cron:

```bash
crontab -e
# Add:
0 3 * * * cd /opt/weather-edge-bot/weather-edge-bot/wx_market_edge && docker compose exec -T scanner python scripts/backup_database.py >> /opt/backup.log 2>&1
```

---

## 10. Rollback Instructions

If a bad deploy breaks the system:

```bash
# On the droplet:
cd /opt/weather-edge-bot
git log --oneline -10   # find the last good commit

# Roll back to that commit
git checkout GOOD_COMMIT_HASH -- weather-edge-bot/wx_market_edge/

# Rebuild and restart
cd weather-edge-bot/wx_market_edge
docker compose build
docker compose down && docker compose up -d
```

Or use GitHub to revert the commit and push to `main` — the deploy workflow
will automatically redeploy the reverted version.

---

## 11. Firewall (optional but recommended)

```bash
# Allow only SSH and the dashboard port
ufw allow ssh
ufw allow 8501/tcp
ufw enable
```

If you want to restrict dashboard access to your IP only:

```bash
ufw allow from YOUR_IP to any port 8501
ufw deny 8501
```

---

## 12. Monitoring

```bash
# Real-time resource usage
docker stats

# Service restart counts (indicates crashes)
docker compose ps

# Last N lines of logs for all services
docker compose logs --tail=50

# Check data freshness
docker compose exec scanner python -c "
from database.db import init_db
from datetime import datetime, timezone
conn = init_db()
row = conn.execute('SELECT MAX(captured_at) FROM market_snapshots').fetchone()
print('Latest market snapshot:', row[0])
"
```
