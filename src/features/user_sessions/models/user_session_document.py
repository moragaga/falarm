"""
A module for managing user session documents in a structured and immutable format. It includes
functionality for creating, updating, serializing, and deserializing session documents.

This module helps maintain structured data about user sessions, including metadata like session
visibility state, page views, and timings.

Attributes
----------
USER_SESSION_DOCUMENT_TYPE : str
    A constant representing the type identifier for user session documents.

Classes
-------
UserSessionDocument
    Represents a user session document containing structured details about the user's session.

Functions
---------
_to_utc_iso(value: datetime) -> str
    Converts a `datetime` object to an ISO 8601 formatted UTC string.

_parse_utc_datetime(*, value: Any) -> datetime | None
    Parses a string into a `datetime` object with UTC timezone, returning None for invalid inputs.

_calculate_active_delta_seconds(*, start: datetime, end: datetime, max_active_delta_seconds: int) -> int
    Calculates the active session duration in seconds, restricted by a maximum value.

_clean_viewport(value: Any) -> dict[str, int]
    Cleans and ensures a viewport dictionary has valid integer values for width and height.

_safe_int(value: Any) -> int
    Safely converts a value to a non-negative integer, returning 0 for invalid inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import (
    datetime,
    timezone,
)
from typing import Any

from .user_session_event import (
    UserSessionEvent,
)

USER_SESSION_DOCUMENT_TYPE = 'active_user_session'


@dataclass(frozen=True, slots=True)
class UserSessionDocument:
    id: str
    client_session_id: str
    user_key: str
    email: str | None
    display_name: str | None
    profile: str | None

    first_seen_at_utc: str
    last_seen_at_utc: str

    active_seconds: int
    views: int
    visibility_state: str

    initial_pathname: str
    last_pathname: str

    initial_viewport: dict[str, int]
    last_viewport: dict[str, int]

    type: str = USER_SESSION_DOCUMENT_TYPE

    @classmethod
    def create(
        cls,
        *,
        document_id: str,
        user_key: str,
        identity: dict[str, Any],
        event: UserSessionEvent,
        now: datetime,
    ) -> UserSessionDocument:
        now_iso = _to_utc_iso(now)

        visibility_state = 'hidden' if event.event_type == 'hidden' else 'visible'

        return cls(
            id=document_id,
            type=USER_SESSION_DOCUMENT_TYPE,
            client_session_id=event.client_session_id,
            user_key=user_key,
            email=identity.get('email'),
            display_name=identity.get('name'),
            profile=identity.get('profile'),
            first_seen_at_utc=now_iso,
            last_seen_at_utc=now_iso,
            active_seconds=0,
            views=1 if visibility_state == 'visible' else 0,
            visibility_state=visibility_state,
            initial_pathname=event.pathname,
            last_pathname=event.pathname,
            initial_viewport=event.viewport,
            last_viewport=event.viewport,
        )

    @classmethod
    def from_item(
        cls,
        item: dict[str, Any],
    ) -> UserSessionDocument:
        return cls(
            id=str(item.get('id') or ''),
            type=str(item.get('type') or USER_SESSION_DOCUMENT_TYPE),
            client_session_id=str(item.get('client_session_id') or ''),
            user_key=str(item.get('user_key') or ''),
            email=item.get('email'),
            display_name=item.get('display_name'),
            profile=item.get('profile'),
            first_seen_at_utc=str(item.get('first_seen_at_utc') or ''),
            last_seen_at_utc=str(item.get('last_seen_at_utc') or ''),
            active_seconds=int(item.get('active_seconds') or 0),
            views=int(item.get('views') or 0),
            visibility_state=str(item.get('visibility_state') or 'visible'),
            initial_pathname=str(item.get('initial_pathname') or '/'),
            last_pathname=str(item.get('last_pathname') or '/'),
            initial_viewport=_clean_viewport(item.get('initial_viewport')),
            last_viewport=_clean_viewport(item.get('last_viewport')),
        )

    def apply_event(
        self,
        *,
        event: UserSessionEvent,
        now: datetime,
        max_active_delta_seconds: int,
    ) -> UserSessionDocument:
        active_seconds = self.active_seconds
        views = self.views

        previous_last_seen = _parse_utc_datetime(
            value=self.last_seen_at_utc,
        )

        if (
            self.visibility_state == 'visible'
            and event.event_type in {'heartbeat', 'hidden'}
            and previous_last_seen is not None
        ):
            active_seconds += _calculate_active_delta_seconds(
                start=previous_last_seen,
                end=now,
                max_active_delta_seconds=max_active_delta_seconds,
            )

        visibility_state = self.visibility_state

        if event.event_type == 'hidden':
            visibility_state = 'hidden'

        elif event.event_type == 'visible':
            if self.visibility_state != 'visible':
                views += 1

            visibility_state = 'visible'

        elif event.event_type in {'heartbeat', 'register'}:
            if self.visibility_state != 'visible':
                views += 1

            visibility_state = 'visible'

        return UserSessionDocument(
            id=self.id,
            type=self.type,
            client_session_id=self.client_session_id,
            user_key=self.user_key,
            email=self.email,
            display_name=self.display_name,
            profile=self.profile,
            first_seen_at_utc=self.first_seen_at_utc,
            last_seen_at_utc=_to_utc_iso(now),
            active_seconds=active_seconds,
            views=views,
            visibility_state=visibility_state,
            initial_pathname=self.initial_pathname,
            last_pathname=event.pathname,
            initial_viewport=self.initial_viewport,
            last_viewport=event.viewport,
        )

    def to_item(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
            'client_session_id': self.client_session_id,
            'user_key': self.user_key,
            'email': self.email,
            'display_name': self.display_name,
            'profile': self.profile,
            'first_seen_at_utc': self.first_seen_at_utc,
            'last_seen_at_utc': self.last_seen_at_utc,
            'active_seconds': self.active_seconds,
            'views': self.views,
            'visibility_state': self.visibility_state,
            'initial_pathname': self.initial_pathname,
            'last_pathname': self.last_pathname,
            'initial_viewport': self.initial_viewport,
            'last_viewport': self.last_viewport,
        }


def _to_utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def _parse_utc_datetime(
    *,
    value: Any,
) -> datetime | None:
    if not isinstance(value, str):
        return None

    normalized = value.replace('Z', '+00:00')

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def _calculate_active_delta_seconds(
    *,
    start: datetime,
    end: datetime,
    max_active_delta_seconds: int,
) -> int:
    delta_seconds = int((end - start).total_seconds())

    if delta_seconds <= 0:
        return 0

    return min(
        delta_seconds,
        max_active_delta_seconds,
    )


def _clean_viewport(value: Any) -> dict[str, int]:
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
