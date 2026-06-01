"""
Provides utilities for handling localized plant and operational shifts, calculating
operational dates, cutoffs, and formatting time deltas.

This module includes functions for determining shift start times, calculating operational
cutoff times, and formatting time differences in human-readable formats. It leverages the
Santiago timezone and supports localization of timestamps. The module is specifically
designed for schedule management in environments that follow distinct operational and
plant shift logic.
"""

from __future__ import annotations

from datetime import UTC, datetime, time, timedelta

import pytz

from .timestamps import ensure_utc, utc_to_local

SANTIAGO_TZ = pytz.timezone('America/Santiago')

TURN_A_START = time(19, 0, 0)
TURN_B_START = time(7, 0, 0)
TURN_A_END = time(6, 59, 59)
TURN_B_END = time(18, 59, 59)


def _localize(
    year: int, month: int, day: int, hour: int, minute: int = 0, second: int = 0
) -> datetime:
    naive = datetime(year, month, day, hour, minute, second)
    return SANTIAGO_TZ.localize(naive)


def get_plant_turn_date(reference_utc: datetime | None = None) -> tuple[datetime, str]:
    local_now = utc_to_local(value=reference_utc)

    if TURN_A_START <= local_now.time() <= time(23, 59, 59):
        start_local = _localize(local_now.year, local_now.month, local_now.day, 19)
        return start_local.astimezone(UTC), 'A'

    if time(0, 0, 0) <= local_now.time() <= TURN_B_START:
        previous_day = local_now - timedelta(days=1)
        start_local = _localize(previous_day.year, previous_day.month, previous_day.day, 19)
        return start_local.astimezone(UTC), 'A'

    if TURN_B_START <= local_now.time() <= TURN_B_END:
        start_local = _localize(local_now.year, local_now.month, local_now.day, 7)
        return start_local.astimezone(UTC), 'B'

    raise ValueError('[ERROR] Invalid local plant time range')


def get_operational_turn_date(reference_utc: datetime | None = None) -> datetime:
    local_now = utc_to_local(value=reference_utc)

    if TURN_A_START <= local_now.time() <= time(23, 59, 59):
        start_local = _localize(local_now.year, local_now.month, local_now.day, 19)
        return start_local.astimezone(UTC)

    if time(0, 0, 0) <= local_now.time() <= TURN_B_END:
        previous_day = local_now - timedelta(days=1)
        start_local = _localize(previous_day.year, previous_day.month, previous_day.day, 19)
        return start_local.astimezone(UTC)

    raise ValueError('[ERROR] Invalid local operational time range')


def get_first_operational_date_month(reference_utc: datetime | None = None) -> datetime:
    local_now = utc_to_local(value=reference_utc)
    first_day_local = _localize(local_now.year, local_now.month, 1, 19)
    previous_day_local = first_day_local - timedelta(days=1)
    return previous_day_local.astimezone(UTC)


def get_next_operational_cutoff_utc(
    reference_utc: datetime | None = None,
    cutoff_hour: int = 19,
) -> datetime:
    local_now = utc_to_local(value=reference_utc)

    cutoff_local = local_now.replace(
        hour=cutoff_hour,
        minute=0,
        second=0,
        microsecond=0,
    )

    if local_now >= cutoff_local:
        cutoff_local = cutoff_local + timedelta(days=1)

    return cutoff_local.astimezone(UTC)


def get_remaining_time_to_operational_cutoff(
    reference_utc: datetime | None = None,
    cutoff_hour: int = 19,
) -> timedelta:
    now_utc = ensure_utc(value=reference_utc)
    next_cutoff_utc = get_next_operational_cutoff_utc(
        reference_utc=now_utc,
        cutoff_hour=cutoff_hour,
    )

    return next_cutoff_utc - now_utc


def format_timedelta_hh_mm(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        total_seconds = 0

    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f'{hours:02d}:{minutes:02d}'
