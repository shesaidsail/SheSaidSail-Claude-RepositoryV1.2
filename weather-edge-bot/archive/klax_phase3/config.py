from pathlib import Path

ROOT     = Path(__file__).parent
DATA_DIR = ROOT / "data"
DB_PATH  = DATA_DIR / "klax.db"

STATION            = "KLAX"
DEFAULT_MODEL      = "HRRR/Ventusky"
BET_EDGE_THRESHOLD = 5.0
MIN_SAMPLE_SIZE    = 10
MIN_CONFIDENCE     = 0.55

METAR_POLL_INTERVAL      = 60   # seconds between fetches in --loop mode
SETTLEMENT_SNAP_INTERVAL = 300  # seconds between intra-day settlement snapshots

# PDT = UTC-7 (May–Oct). Change to -8 for PST (Nov–Mar).
KLAX_UTC_OFFSET_HOURS = -7

# Primary: authoritative NWS single-station feed
NWS_METAR_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/{station}.TXT"
# Fallback: AWC JSON API (gives last N hours, useful for backfills)
AWC_METAR_URL = "https://aviationweather.gov/api/data/metar"
