from pathlib import Path

ROOT     = Path(__file__).parent
DATA_DIR = ROOT / "data"
DB_PATH  = DATA_DIR / "klax.db"

STATION          = "KLAX"
DEFAULT_MODEL    = "HRRR/Ventusky"
BET_EDGE_THRESHOLD = 5.0

# PDT = UTC-7 (May–Oct).  Change to -8 for PST (Nov–Mar).
KLAX_UTC_OFFSET_HOURS = -7
