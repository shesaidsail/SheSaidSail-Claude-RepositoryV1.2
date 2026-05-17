"""
DST-aware timezone utilities.

Replaces the static utc_offset lookups in config.STATIONS with live
ZoneInfo-based offsets that automatically handle Daylight Saving Time.
"""

from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
    _HAS_ZONEINFO = True
except ImportError:
    try:
        from backports.zoneinfo import ZoneInfo   # type: ignore
        _HAS_ZONEINFO = True
    except ImportError:
        _HAS_ZONEINFO = False


def local_hour_from_utc(timestamp_utc: str, tz_name: str,
                         fallback_utc_offset: int = -5) -> int:
    """
    Convert a UTC timestamp string (ISO-8601 Z suffix) to local hour (0–23).

    Uses ZoneInfo for DST-correct conversion when available; falls back to
    the static utc_offset from config.STATIONS otherwise.

    Args:
        timestamp_utc       – e.g. "2025-07-15T18:00:00Z"
        tz_name             – IANA tz name, e.g. "America/Los_Angeles"
        fallback_utc_offset – integer hours used when ZoneInfo is unavailable
    """
    try:
        ts = datetime.strptime(timestamp_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if _HAS_ZONEINFO:
            local_dt = ts.astimezone(ZoneInfo(tz_name))
            return local_dt.hour
        # Fallback: static offset (ignores DST)
        return (ts.hour + fallback_utc_offset) % 24
    except Exception:
        return 12   # safe default — mid-day avoids edge-case regime misclassification


def utc_offset_hours(tz_name: str, at_utc: datetime | None = None) -> float:
    """
    Return the current UTC offset (fractional hours) for a timezone,
    accounting for DST at the given moment (defaults to now).
    """
    if not _HAS_ZONEINFO:
        return 0.0
    try:
        dt = (at_utc or datetime.now(timezone.utc)).astimezone(ZoneInfo(tz_name))
        offset = dt.utcoffset()
        return offset.total_seconds() / 3600 if offset else 0.0
    except Exception:
        return 0.0
