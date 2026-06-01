"""
This module provides utility functions for formatting elapsed time into a human-readable string.

The functions support handling elapsed time in various units such as days, hours, minutes, and seconds.
They ensure proper pluralization based on the provided values and handle optional inputs gracefully.
"""

from __future__ import annotations


def format_elapsed_time(total_seconds: int) -> str:
    if not isinstance(total_seconds, int):
        raise TypeError('total_seconds must be an integer')

    if total_seconds < 0:
        raise ValueError('total_seconds cannot be negative')

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts: list[str] = []

    units = [
        (days, 'Día', 'Días'),
        (hours, 'Hora', 'Horas'),
        (minutes, 'Minuto', 'Minutos'),
        (seconds, 'Segundo', 'Segundos'),
    ]

    for value, singular, plural in units:
        if value:
            parts.append(f'{value} {singular if value == 1 else plural}')

    return ' '.join(parts) if parts else '0 Segundos'


def format_optional_elapsed_time(total_seconds: float | int | None) -> str:
    if total_seconds is None:
        return ''

    return format_elapsed_time(int(total_seconds))
