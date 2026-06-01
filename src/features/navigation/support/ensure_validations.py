"""
Utility functions for data normalization and type conversion.

This module provides a set of functions for normalizing profiles, converting
values to integer or boolean, and cleaning optional string inputs.
"""

from __future__ import annotations

from typing import Any


def normalize_profiles(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()

    if isinstance(value, str):
        return tuple(item.strip() for item in value.split(';') if item and item.strip())

    if isinstance(value, (list, tuple, set)):
        return tuple(str(item).strip() for item in value if item is not None and str(item).strip())

    return ()


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except TypeError, ValueError:
        return default


def to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value == 1

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {'true', '1', 'yes', 'y', 'si', 'sí'}:
            return True

        if normalized in {'false', '0', 'no', 'n'}:
            return False

    return default


def clean_optional_string(value: Any) -> str | None:
    if value is None:
        return None

    cleaned = str(value).strip()
    return cleaned or None
