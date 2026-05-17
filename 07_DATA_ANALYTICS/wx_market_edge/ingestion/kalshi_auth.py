"""
Kalshi authenticated API client.

Loads credentials from .env (via python-dotenv).
Supports both the demo sandbox and production environments.

IMPORTANT: Never hardcode credentials. Always use .env.
           Never commit .env to git.
"""

import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass   # python-dotenv not installed; fall back to OS env only

import requests

# ---------------------------------------------------------------------------
# Environment resolution
# ---------------------------------------------------------------------------

def _env() -> str:
    return os.environ.get("KALSHI_ENV", "demo").lower()


def _base_url() -> str:
    if _env() == "prod":
        return "https://trading.kalshi.com/trade-api/v2"
    return "https://demo-api.kalshi.co/trade-api/v2"


def _api_key() -> str:
    return os.environ.get("KALSHI_API_KEY", "")


def _api_secret() -> str:
    return os.environ.get("KALSHI_API_SECRET", "")


def is_configured() -> bool:
    """Return True if an API key is set in the environment."""
    return bool(_api_key())


# ---------------------------------------------------------------------------
# Session / headers
# ---------------------------------------------------------------------------

_session_token: str | None = None
_session_expires: datetime | None = None


def _get_headers(authenticated: bool = True) -> dict:
    """Return request headers.  Falls back to unauthenticated if no key set."""
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if authenticated and is_configured():
        # Kalshi v2 uses API-Key header directly (no OAuth for read-only)
        h["Authorization"] = f"Bearer {_api_key()}"
    return h


# ---------------------------------------------------------------------------
# Public read-only wrappers
# ---------------------------------------------------------------------------

def get_markets(
    status: str = "open",
    limit:  int = 200,
    series_ticker: str | None = None,
) -> list[dict]:
    """List markets from the configured environment."""
    params: dict = {"status": status, "limit": limit}
    if series_ticker:
        params["series_ticker"] = series_ticker

    try:
        r = requests.get(
            f"{_base_url()}/markets",
            headers=_get_headers(),
            params=params,
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("markets", data if isinstance(data, list) else [])
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            print("[kalshi_auth] 401 Unauthorized — check KALSHI_API_KEY in .env")
        else:
            print(f"[kalshi_auth] HTTP error: {e}")
        return []
    except Exception as e:
        print(f"[kalshi_auth] get_markets error: {e}")
        return []


def get_market(ticker: str) -> dict | None:
    """Fetch a single market by ticker."""
    try:
        r = requests.get(
            f"{_base_url()}/markets/{ticker}",
            headers=_get_headers(),
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("market", data)
    except Exception as e:
        print(f"[kalshi_auth] get_market {ticker}: {e}")
        return None


def get_orderbook(ticker: str) -> dict | None:
    """Fetch orderbook for a market."""
    try:
        r = requests.get(
            f"{_base_url()}/markets/{ticker}/orderbook",
            headers=_get_headers(),
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[kalshi_auth] orderbook {ticker}: {e}")
        return None


def get_trades(ticker: str, limit: int = 50) -> list[dict]:
    """Recent trade history for a market."""
    try:
        r = requests.get(
            f"{_base_url()}/markets/{ticker}/trades",
            headers=_get_headers(),
            params={"limit": limit},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("trades", [])
    except Exception as e:
        print(f"[kalshi_auth] trades {ticker}: {e}")
        return []


# ---------------------------------------------------------------------------
# Connection test
# ---------------------------------------------------------------------------

def test_connection() -> dict:
    """
    Test the Kalshi API connection.
    Returns {"ok": bool, "env": str, "message": str, "market_count": int}.
    """
    if not is_configured():
        return {
            "ok":      False,
            "env":     _env(),
            "message": "No API key found. Add KALSHI_API_KEY to your .env file.",
            "market_count": 0,
        }

    markets = get_markets(limit=5)
    if markets:
        return {
            "ok":           True,
            "env":          _env(),
            "message":      f"Connected to Kalshi {_env()} — {len(markets)} markets sample OK",
            "market_count": len(markets),
        }
    return {
        "ok":      False,
        "env":     _env(),
        "message": "Connected but received 0 markets. Check key permissions or try KALSHI_ENV=prod.",
        "market_count": 0,
    }


# ---------------------------------------------------------------------------
# Weather market search using auth client
# ---------------------------------------------------------------------------

WEATHER_KEYWORDS = [
    "high temp", "temperature", "daily high", "degrees", "fahrenheit",
    "weather", "high will", "heat",
]


def search_weather_markets_auth(limit: int = 200) -> list[dict]:
    """Search for weather/temperature markets using authenticated client."""
    markets = get_markets(limit=limit, status="open")
    return [
        m for m in markets
        if any(kw in (m.get("title", "") + m.get("subtitle", "")).lower()
               for kw in WEATHER_KEYWORDS)
    ]


# ---------------------------------------------------------------------------
# Refresh with auth — called by scheduler
# ---------------------------------------------------------------------------

def refresh_with_auth(conn: sqlite3.Connection, verbose: bool = True) -> int:
    """Fetch authenticated weather markets and store snapshots."""
    from ingestion.kalshi import parse_market, store_snapshot

    if not is_configured():
        if verbose:
            print("[kalshi_auth] No API key — falling back to public endpoint")
        from ingestion.kalshi import refresh_all
        return refresh_all(conn, verbose)

    markets = search_weather_markets_auth()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    count = 0

    for m in markets:
        snap = parse_market(m)
        if snap.get("station_code") and snap.get("threshold_f"):
            store_snapshot(snap, conn)
            count += 1

    conn.execute("""
        INSERT INTO data_health (feed, last_success, last_attempt, consecutive_failures)
        VALUES ('kalshi',?,?,0)
        ON CONFLICT(feed) DO UPDATE SET
            last_success=excluded.last_success,
            last_attempt=excluded.last_attempt,
            consecutive_failures=0, last_error=NULL
    """, (now, now))
    conn.commit()

    if verbose:
        key_hint = _api_key()[:8] + "..." if _api_key() else "(none)"
        print(f"[kalshi_auth] {_env()} | key={key_hint} | {count} weather markets stored")
    return count
