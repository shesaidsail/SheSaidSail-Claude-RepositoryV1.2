"""
Kalshi market data ingestion.

Uses the public Kalshi REST API v2.  Authentication is optional — set
KALSHI_API_KEY in config.py or the environment for private endpoints.

All operations are read-only (no order placement).
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from config import KALSHI_BASE_URL, KALSHI_API_KEY

# City-to-ICAO reverse lookup for matching market titles to stations
CITY_ICAO = {
    "los angeles": "KLAX", "lax": "KLAX",
    "new york":    "KJFK", "jfk": "KJFK", "nyc": "KJFK",
    "chicago":     "KORD", "ord": "KORD",
    "miami":       "KMIA", "mia": "KMIA",
    "phoenix":     "KPHX", "phx": "KPHX",
    "dallas":      "KDFW", "dfw": "KDFW",
    "denver":      "KDEN", "den": "KDEN",
    "seattle":     "KSEA", "sea": "KSEA",
    "san francisco":"KSFO","sfo": "KSFO",
    "boston":      "KBOS", "bos": "KBOS",
}


def _headers() -> dict:
    key = os.environ.get("KALSHI_API_KEY", KALSHI_API_KEY)
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if key:
        h["Authorization"] = f"Bearer {key}"
    return h


def search_weather_markets(limit: int = 200) -> list[dict]:
    """Search Kalshi for active weather/temperature markets."""
    try:
        r = requests.get(
            f"{KALSHI_BASE_URL}/markets",
            headers=_headers(),
            params={
                "status":   "open",
                "limit":    limit,
                "category": "weather",
            },
            timeout=15,
        )
        if r.status_code == 404:
            # Some Kalshi environments use different category strings
            r = requests.get(
                f"{KALSHI_BASE_URL}/markets",
                headers=_headers(),
                params={"status": "open", "limit": limit},
                timeout=15,
            )
        r.raise_for_status()
        data = r.json()
        markets = data.get("markets", data if isinstance(data, list) else [])
        # Filter to temperature/weather titles
        wx_keywords = ["high temp", "temperature", "high will", "daily high",
                       "weather", "degrees", "fahrenheit"]
        return [
            m for m in markets
            if any(kw in (m.get("title", "") + m.get("subtitle", "")).lower()
                   for kw in wx_keywords)
        ]
    except Exception as e:
        print(f"[kalshi] search error: {e}")
        return []


def get_market(ticker: str) -> dict | None:
    """Fetch a single market by ticker."""
    try:
        r = requests.get(
            f"{KALSHI_BASE_URL}/markets/{ticker}",
            headers=_headers(), timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("market", data)
    except Exception as e:
        print(f"[kalshi] market fetch {ticker}: {e}")
        return None


def get_orderbook(ticker: str) -> dict | None:
    """Fetch orderbook depth for a market."""
    try:
        r = requests.get(
            f"{KALSHI_BASE_URL}/markets/{ticker}/orderbook",
            headers=_headers(), timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[kalshi] orderbook {ticker}: {e}")
        return None


def parse_market(market: dict) -> dict:
    """Normalise a Kalshi market dict into our schema."""
    ticker = market.get("ticker", market.get("id", ""))
    title  = market.get("title", "")
    subtitle = market.get("subtitle", "")

    # Infer station from title
    station = None
    for city, icao in CITY_ICAO.items():
        if city in (title + subtitle).lower():
            station = icao
            break

    # Extract threshold from title  (e.g. "above 72°F")
    import re
    thresh = None
    m = re.search(r'(\d{2,3})\s*°?\s*[Ff]', title + " " + subtitle)
    if m:
        thresh = float(m.group(1))

    # Parse expiry date
    close_time = market.get("close_time", market.get("expiration_time", ""))
    expiry_date = close_time[:10] if close_time else None

    # Prices come in different formats (cents vs fractions)
    def _price(v):
        if v is None:
            return None
        v = float(v)
        return v if v <= 100 else v / 100

    yes_bid   = _price(market.get("yes_bid", market.get("last_price")))
    yes_ask   = _price(market.get("yes_ask"))
    last      = _price(market.get("last_price", market.get("yes_bid")))
    volume    = market.get("volume", market.get("volume_24h"))
    open_int  = market.get("open_interest", market.get("liquidity"))

    return {
        "ticker":       ticker,
        "title":        title,
        "station_code": station,
        "threshold_f":  thresh,
        "side":         "Yes",
        "best_bid":     yes_bid,
        "best_ask":     yes_ask,
        "last_price":   last,
        "market_price": last or yes_bid,
        "volume":       float(volume) if volume else None,
        "open_interest": float(open_int) if open_int else None,
        "expiry_date":  expiry_date,
    }


def store_snapshot(snap: dict, conn: sqlite3.Connection) -> int:
    """Insert a market snapshot row. Returns inserted rowid."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.execute("""
        INSERT INTO market_snapshots (
            captured_at, station_code, market_ticker, market_title,
            threshold_f, side, market_price, best_bid, best_ask, last_price,
            volume, open_interest, expiry_date
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        now,
        snap.get("station_code"), snap["ticker"], snap.get("title"),
        snap.get("threshold_f"), snap.get("side", "Yes"),
        snap.get("market_price"), snap.get("best_bid"), snap.get("best_ask"),
        snap.get("last_price"), snap.get("volume"), snap.get("open_interest"),
        snap.get("expiry_date"),
    ))
    conn.commit()
    return cur.lastrowid


def refresh_all(conn: sqlite3.Connection, verbose: bool = True) -> int:
    """Fetch all weather markets from Kalshi and store snapshots."""
    markets = search_weather_markets()
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
        print(f"[kalshi] {count} weather market snapshots stored")
    return count


def get_latest_snapshots(conn: sqlite3.Connection, date: str | None = None) -> list[dict]:
    """Return most recent snapshot per market ticker."""
    q = """
        SELECT ms.*
        FROM market_snapshots ms
        INNER JOIN (
            SELECT market_ticker, MAX(captured_at) AS max_ts
            FROM market_snapshots
            GROUP BY market_ticker
        ) latest ON ms.market_ticker=latest.market_ticker AND ms.captured_at=latest.max_ts
    """
    if date:
        q += f" WHERE ms.expiry_date='{date}'"
    rows = conn.execute(q).fetchall()
    return [dict(r) for r in rows]


def add_manual_market(
    ticker: str, title: str, station_code: str, threshold_f: float,
    side: str, market_price: float, best_bid: float | None,
    best_ask: float | None, expiry_date: str | None,
    conn: sqlite3.Connection,
) -> int:
    snap = {
        "ticker": ticker, "title": title, "station_code": station_code,
        "threshold_f": threshold_f, "side": side, "market_price": market_price,
        "best_bid": best_bid, "best_ask": best_ask, "last_price": market_price,
        "volume": None, "open_interest": None, "expiry_date": expiry_date,
    }
    return store_snapshot(snap, conn)
