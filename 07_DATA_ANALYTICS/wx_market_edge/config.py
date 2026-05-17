from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT     = Path(__file__).parent
DATA_DIR = ROOT / "data"
LOG_DIR  = ROOT / "logs"
DB_PATH  = DATA_DIR / "wx_edge.db"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Stations  (ICAO, name, lat, lon, tz, utc_offset_hours)
# ---------------------------------------------------------------------------
STATIONS = {
    "KLAX": {"name": "Los Angeles",    "lat": 33.9425, "lon": -118.4081, "tz": "America/Los_Angeles", "utc_offset": -7},
    "KJFK": {"name": "New York JFK",   "lat": 40.6413, "lon":  -73.7781, "tz": "America/New_York",    "utc_offset": -4},
    "KORD": {"name": "Chicago O'Hare", "lat": 41.9742, "lon":  -87.9073, "tz": "America/Chicago",     "utc_offset": -5},
    "KMIA": {"name": "Miami",          "lat": 25.7959, "lon":  -80.2870, "tz": "America/New_York",    "utc_offset": -4},
    "KPHX": {"name": "Phoenix",        "lat": 33.4373, "lon": -112.0078, "tz": "America/Phoenix",     "utc_offset": -7},
    "KDFW": {"name": "Dallas/Ft Worth","lat": 32.8998, "lon":  -97.0403, "tz": "America/Chicago",     "utc_offset": -5},
    "KDEN": {"name": "Denver",         "lat": 39.8561, "lon": -104.6737, "tz": "America/Denver",      "utc_offset": -6},
    "KSEA": {"name": "Seattle",        "lat": 47.4502, "lon": -122.3088, "tz": "America/Los_Angeles", "utc_offset": -7},
    "KSFO": {"name": "San Francisco",  "lat": 37.6213, "lon": -122.3790, "tz": "America/Los_Angeles", "utc_offset": -7},
    "KBOS": {"name": "Boston",         "lat": 42.3656, "lon":  -71.0096, "tz": "America/New_York",    "utc_offset": -4},
}

# ---------------------------------------------------------------------------
# Open-Meteo API
# ---------------------------------------------------------------------------
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

DAILY_VARS = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "wind_direction_10m_dominant", "wind_speed_10m_max", "wind_speed_10m_mean",
    "wind_gusts_10m_max",
    "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min",
    "dew_point_2m_mean", "dew_point_2m_max", "dew_point_2m_min",
    "relative_humidity_2m_mean", "relative_humidity_2m_max", "relative_humidity_2m_min",
    "pressure_msl_mean", "pressure_msl_max", "pressure_msl_min",
    "surface_pressure_mean", "surface_pressure_max", "surface_pressure_min",
    "precipitation_probability_mean", "precipitation_probability_max",
    "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum",
    "weather_code", "sunshine_duration", "daylight_duration",
    "sunrise", "sunset",
]

HOURLY_VARS = [
    "temperature_2m", "dew_point_2m",
    "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m",
    "cloud_cover", "precipitation_probability", "weather_code",
]

CURRENT_VARS = [
    "temperature_2m", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
    "cloud_cover", "pressure_msl", "surface_pressure",
    "relative_humidity_2m", "apparent_temperature",
]

# ---------------------------------------------------------------------------
# METAR / NOAA
# ---------------------------------------------------------------------------
NWS_METAR_URL    = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/{station}.TXT"
AWC_CACHE_URL    = "https://aviationweather.gov/data/cache/metars.cache.csv.gz"
AWC_API_URL      = "https://aviationweather.gov/api/data/metar"

# ---------------------------------------------------------------------------
# Kalshi
# ---------------------------------------------------------------------------
KALSHI_BASE_URL  = "https://trading.kalshi.com/trade-api/v2"
KALSHI_API_KEY   = ""   # set via env var KALSHI_API_KEY or leave blank for public-only
KALSHI_SERIES    = ["HIGHNY", "HIGHLAX", "HIGHMIA", "HIGHCHI", "HIGHDAL",
                    "HIGHDEN", "HIGHSEA", "HIGHSFO", "HIGHBOS", "HIGHPHX"]

# ---------------------------------------------------------------------------
# Signal filters
# ---------------------------------------------------------------------------
MIN_EDGE          = 5.0    # cents – minimum edge to flag a signal
MIN_CONFIDENCE    = 0.55   # 0-1 – minimum model confidence
MAX_SPREAD        = 8.0    # cents – maximum bid/ask spread
MIN_REGIME_N      = 3      # minimum regime sample size for blended use
DEFAULT_MODEL     = "OpenMeteo"

# ---------------------------------------------------------------------------
# Polling intervals (seconds)
# ---------------------------------------------------------------------------
FORECAST_INTERVAL = 3600   # 1 hour
METAR_INTERVAL    = 300    # 5 minutes
KALSHI_INTERVAL   = 120    # 2 minutes
