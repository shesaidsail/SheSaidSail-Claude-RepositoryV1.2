#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "=== Weather Market Edge Tracker — Setup ==="

# 1. Install Python dependencies
pip install -r requirements.txt --quiet

# 2. Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env — paste your Kalshi credentials into it before running Kalshi ingestion."
else
    echo ".env already exists — skipping."
fi

# 3. Init database + seed stations
python3 - <<'PYEOF'
import sys
sys.path.insert(0, '.')
from database.db import init_db, seed_stations
conn = init_db()
seed_stations(conn)
conn.close()
print("Database initialised and stations seeded.")
PYEOF

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  1. Edit .env and add your Kalshi API key (KALSHI_API_KEY=...)"
echo "  2. Run first data fetch:  python scripts/scheduler.py --once"
echo "  3. Launch dashboard:      streamlit run dashboard/app.py --server.port 8501"
echo "  4. Open browser:          http://localhost:8501"
