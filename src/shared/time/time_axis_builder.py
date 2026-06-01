"""
Utility functions for working with localized time axes and labels.

This module provides functions to build a localized time axis based on
a given starting timestamp, step size, length, and target timezone. It also
includes functionality to generate a list of formatted time labels from
the localized time axis.

Functions
---------
build_local_time_axis : Constructs a localized time axis.
build_local_time_labels : Generates formatted time labels for a given
    localized time axis.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Sequence
from zoneinfo import ZoneInfo

from .timestamps import SANTIAGO_TZ


def build_local_time_axis(
    *,
    start_timestamp_utc: str,
    step_seconds: int,
    length: int,
    target_tz: ZoneInfo = SANTIAGO_TZ,
) -> list[datetime]:
    start_utc = datetime.fromisoformat(start_timestamp_utc)

    if start_utc.tzinfo is None:
        start_utc = start_utc.replace(tzinfo=timezone.utc)

    step = timedelta(seconds=step_seconds)

    return [(start_utc + i * step).astimezone(target_tz) for i in range(length)]


def build_local_time_labels(
    *,
    axis_local: Sequence[datetime],
) -> list[str]:
    base_labels = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in axis_local]

    counts: dict[str, int] = {}
    for label in base_labels:
        counts[label] = counts.get(label, 0) + 1

    result: list[str] = []
    for dt, label in zip(axis_local, base_labels):
        if counts[label] > 1:
            offset = dt.strftime('%z')
            offset = f'UTC{offset[:3]}:{offset[3:]}'
            result.append(f'{label} ({offset})')
        else:
            result.append(label)

    return result
