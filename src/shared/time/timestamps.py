"""A collection of functions for working with UTC and Santiago timezones.

This module provides utility functions for handling datetime operations,
including conversions between UTC and Santiago (America/Santiago) timezones,
parsing ISO 8601 formatted datetime strings, and formatting timezone-aware
datetimes for display.

"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

UTC = timezone.utc
SANTIAGO_TZ = ZoneInfo('America/Santiago')


def utc_to_local(value: datetime | None = None) -> datetime:
    return ensure_utc(value).astimezone(SANTIAGO_TZ)


def now_utc() -> datetime:
    return datetime.now(UTC)


def now_utc_iso() -> str:
    return now_utc().isoformat()


def parse_utc_datetime(value: Any) -> datetime | None:
    if value is None:
        return None

    if not isinstance(value, str):
        value = str(value)

    value = value.strip()
    if not value:
        return None

    normalized = value.replace('Z', '+00:00')

    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    return dt.astimezone(UTC)


def to_santiago(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError('Datetime must be timezone-aware.')
    return dt.astimezone(SANTIAGO_TZ)


def to_santiago_display(
    dt: datetime | None,
    fmt: str = '%Y-%m-%d %H:%M:%S',
) -> str | None:
    if dt is None:
        return None

    return to_santiago(dt).strftime(fmt)


def ensure_utc(value: datetime | None = None) -> datetime:
    if value is None:
        return now_utc()

    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)
