"""
This module provides functionality for handling user session events.
It includes a dataclass to represent user session events, and utility
functions for data cleaning and validation.

Classes
-------
UserSessionEvent
    A class representing a user session event, which encapsulates details
    including the client session ID, event type, pathname, visibility state,
    and viewport information.

Functions
---------
_clean_string
    Cleans and truncates a string value to ensure it meets the required format
    and length constraints.
_clean_viewport
    Processes and validates viewport information, ensuring width and height
    values are integers and non-negative.
_safe_int
    Safely converts a value to a non-negative integer, returning zero for
    invalid inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class UserSessionEvent:
    client_session_id: str
    event_type: str
    pathname: str
    visibility_state: str
    viewport: dict[str, int]

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any],
    ) -> UserSessionEvent | None:
        client_session_id = _clean_string(
            value=payload.get('client_session_id'),
            max_length=120,
        )

        event_type = _clean_string(
            value=payload.get('event_type'),
            max_length=40,
        )

        pathname = (
            _clean_string(
                value=payload.get('pathname'),
                max_length=500,
            )
            or '/'
        )

        visibility_state = (
            _clean_string(
                value=payload.get('visibility_state'),
                max_length=40,
            )
            or 'visible'
        )

        viewport = _clean_viewport(
            value=payload.get('viewport'),
        )

        if not client_session_id:
            return None

        if event_type not in {
            'register',
            'heartbeat',
            'hidden',
            'visible',
        }:
            return None

        if visibility_state not in {
            'visible',
            'hidden',
        }:
            visibility_state = 'visible'

        return cls(
            client_session_id=client_session_id,
            event_type=event_type,
            pathname=pathname,
            visibility_state=visibility_state,
            viewport=viewport,
        )


def _clean_string(
    *,
    value: Any,
    max_length: int,
) -> str | None:
    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    return value[:max_length]


def _clean_viewport(
    *,
    value: Any,
) -> dict[str, int]:
    if not isinstance(value, dict):
        return {
            'width': 0,
            'height': 0,
        }

    return {
        'width': _safe_int(value.get('width')),
        'height': _safe_int(value.get('height')),
    }


def _safe_int(value: Any) -> int:
    try:
        number = int(value)
    except TypeError, ValueError:
        return 0

    return max(0, number)
