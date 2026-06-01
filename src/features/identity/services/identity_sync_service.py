"""
Provides functionality for synchronizing and managing identities from a SharePoint
repository based on specific application settings.

The module includes a class for handling identity resolution, registration of
missing identities, invalidating or refreshing the cached identities, and
retrieving identities from SharePoint while maintaining an in-memory cache.
"""

from __future__ import annotations

from datetime import (
    datetime,
    timedelta,
    timezone,
)
from threading import Lock
from typing import Any

from ..models.identity import Identity
from ..repositories.sharepoint_identity_repository import (
    SharePointIdentityRepository,
)
from ..settings import IdentitySettings


class IdentitySyncService:
    def __init__(
        self,
        sharepoint_repository: SharePointIdentityRepository,
        settings: IdentitySettings,
    ) -> None:
        self._sharepoint_repository = sharepoint_repository
        self._settings = settings

        self._lock = Lock()
        self._cached_users_by_email: dict[str, Identity] = {}
        self._cache_at: datetime | None = None

    def resolve_identity(
        self,
        email: str,
        display_name: str,
        force_refresh: bool = False,
    ) -> dict:
        normalized_email = _normalize_email(email)

        if not normalized_email:
            return Identity.build_fallback(
                email='',
                display_name=display_name,
            ).to_dict()

        users_by_email = self._get_users_by_email(
            force_refresh=force_refresh,
        )

        identity = users_by_email.get(normalized_email)

        if identity is None:
            return Identity.build_fallback(
                email=normalized_email,
                display_name=display_name,
            ).to_dict()

        if not identity.is_active:
            return Identity.build_guest(
                email=normalized_email,
                display_name=display_name or identity.name,
            ).to_dict()

        return identity.with_display_name(
            display_name=display_name,
        ).to_dict()

    def register_missing_identity(
        self,
        *,
        identity: dict[str, Any],
    ) -> bool:
        if not self._settings.should_write:
            return False

        if not identity.get('needs_registration'):
            return False

        email = _normalize_email(identity.get('email'))
        display_name = str(identity.get('name') or email or 'Usuario').strip()

        if not email:
            return False

        with self._lock:
            users_by_email = self._load_users_by_email()

            if email in users_by_email:
                self._cached_users_by_email = users_by_email
                self._cache_at = datetime.now(tz=timezone.utc)
                return False

            new_identity = Identity.build_auto_registered(
                email=email,
                display_name=display_name,
            )

            users_by_email[email] = new_identity

            rows = [
                user.to_sharepoint_row()
                for user in sorted(
                    users_by_email.values(),
                    key=lambda item: item.email,
                )
            ]

            ok = self._sharepoint_repository.save_rows(rows=rows)

            if not ok:
                return False

            self._cached_users_by_email = users_by_email
            self._cache_at = datetime.now(tz=timezone.utc)

            return True

    def invalidate(self) -> None:
        with self._lock:
            self._cached_users_by_email = {}
            self._cache_at = None

    def force_refresh(self) -> None:
        self._get_users_by_email(
            force_refresh=True,
        )

    def _get_users_by_email(
        self,
        *,
        force_refresh: bool = False,
    ) -> dict[str, Identity]:
        with self._lock:
            if not force_refresh and self._is_cache_valid():
                return dict(self._cached_users_by_email)

            self._cached_users_by_email = self._load_users_by_email()
            self._cache_at = datetime.now(tz=timezone.utc)

            return dict(self._cached_users_by_email)

    def _load_users_by_email(self) -> dict[str, Identity]:
        rows = self._sharepoint_repository.load_rows()

        users_by_email: dict[str, Identity] = {}

        for row in rows or []:
            if not isinstance(row, dict):
                continue

            identity = Identity.from_sharepoint_row(row)

            if not identity.email:
                continue

            users_by_email[identity.email] = identity

        return users_by_email

    def _is_cache_valid(self) -> bool:
        if self._cache_at is None:
            return False

        ttl = timedelta(seconds=self._settings.cache_ttl_seconds)

        return datetime.now(tz=timezone.utc) - self._cache_at <= ttl


def _normalize_email(value: Any) -> str:
    return str(value or '').strip().lower()
