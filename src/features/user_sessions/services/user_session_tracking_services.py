"""
Service for tracking user sessions.

This service handles the management and tracking of user sessions based on
provided identity and event details. It uses a repository to persist session
information and apply updates as new events are processed.

Classes
-------
UserSessionTrackingService
    A class managing the lifecycle of user sessions, including registering new
    sessions, updating existing ones, and handling related user events.
"""

from __future__ import annotations

import hashlib
from datetime import (
    datetime,
    timezone,
)
from typing import Any

from ..models.user_session_document import (
    UserSessionDocument,
)
from ..models.user_session_event import (
    UserSessionEvent,
)
from ..settings import (
    UserSessionTrackingSettings,
)


class UserSessionTrackingService:
    def __init__(
        self,
        *,
        repository,
        settings: UserSessionTrackingSettings,
    ) -> None:
        self._repository = repository
        self._settings = settings

    def touch(
        self,
        *,
        identity: dict[str, Any],
        event: UserSessionEvent,
    ) -> dict[str, Any]:
        if not self._settings.enabled:
            return {
                'status': 'disabled',
                'tracked': False,
            }

        user_key = self._build_user_key(
            email=str(identity.get('email') or ''),
        )

        if not user_key:
            return {
                'status': 'invalid_user',
                'tracked': False,
            }

        now = datetime.now(timezone.utc)

        document_id = self._build_document_id(
            user_key=user_key,
            client_session_id=event.client_session_id,
        )

        existing = self._repository.get_by_id(
            document_id=document_id,
        )

        if not existing:
            document = UserSessionDocument.create(
                document_id=document_id,
                user_key=user_key,
                identity=identity,
                event=event,
                now=now,
            )

            self._repository.upsert(
                item=document.to_item(),
            )

            return {
                'status': 'registered',
                'tracked': True,
            }

        document = UserSessionDocument.from_item(
            item=existing,
        ).apply_event(
            event=event,
            now=now,
            max_active_delta_seconds=self._settings.max_active_delta_seconds,
        )

        self._repository.upsert(
            item=document.to_item(),
        )

        return {
            'status': 'updated',
            'tracked': True,
        }

    @staticmethod
    def _build_user_key(
        *,
        email: str,
    ) -> str | None:
        normalized_email = email.strip().lower()

        if not normalized_email:
            return None

        return hashlib.sha256(
            normalized_email.encode('utf-8'),
        ).hexdigest()

    @staticmethod
    def _build_document_id(
        *,
        user_key: str,
        client_session_id: str,
    ) -> str:
        raw_key = f'{user_key}:{client_session_id}'

        digest = hashlib.sha256(
            raw_key.encode('utf-8'),
        ).hexdigest()

        return f'user_session::{digest}'
