#!/usr/bin/env bash
# Start the full system: scheduler (background) + Streamlit (foreground)
set -e
cd "$(dirname "$0")"

echo "Starting data scheduler in background..."
python3 scripts/scheduler.py &
SCHED_PID=$!
echo "Scheduler PID: $SCHED_PID"

echo "Starting Streamlit dashboard..."
echo "Dashboard URL: http://localhost:8501"
streamlit run dashboard/app.py --server.port 8501 --server.headless true

# Cleanup on exit
kill $SCHED_PID 2>/dev/null || true
