"""
Identity management module.

This module provides the `Identity` data class and utility functions to manage identities
including creation, transformation, and normalization of identity-related attributes.

Attributes
----------
id : str
    Unique identifier for the identity. Can be a user ID, email, or other identifier.
name : str
    Display name of the identity. Typically the user's full name or a fallback value.
email : str
    Email address associated with the identity.
profile : str
    The profile type assigned to the identity, normalized using the `Profile` model.
is_active : bool, default=True
    Represents the active status of the identity.
needs_registration : bool, default=False
    Indicates whether the identity requires registration for further usage.

Methods
-------
from_sharepoint_row(row)
    Class method to construct an `Identity` instance from a SharePoint row dictionary.
build_fallback(email, display_name)
    Class method to create a fallback `Identity` instance with essential values.
build_guest(email, display_name)
    Class method to create a guest identity with restricted attributes.
build_auto_registered(email, display_name)
    Class method to generate an automatically registered identity with a UUID as the ID.
with_display_name(display_name)
    Generates a new `Identity` instance with an updated display name.
to_dict()
    Converts the `Identity` instance to a dictionary representation, excluding internal flags.
to_sharepoint_row()
    Converts the `Identity` instance to a dictionary suitable for SharePoint representation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from src.features.configuration.models import Profile


@dataclass(frozen=True)
class Identity:
    id: str
    name: str
    email: str
    profile: str
    is_active: bool = True
    needs_registration: bool = False

    @classmethod
    def from_sharepoint_row(
        cls,
        row: dict[str, Any],
    ) -> Identity:
        email = _normalize_email(row.get('email'))

        return cls(
            id=str(row.get('user_id') or row.get('id') or email).strip(),
            name=str(row.get('name') or '').strip(),
            email=email,
            profile=Profile.normalize_assignable(row.get('profile')),
            is_active=_to_bool(row.get('is_active'), default=True),
            needs_registration=False,
        )

    @classmethod
    def build_fallback(
        cls,
        *,
        email: str,
        display_name: str,
    ) -> Identity:
        normalized_email = _normalize_email(email)
        final_name = str(display_name or normalized_email or 'Usuario').strip()

        return cls(
            id=normalized_email,
            name=final_name,
            email=normalized_email,
            profile=Profile.default_assignable(),
            is_active=True,
            needs_registration=True,
        )

    @classmethod
    def build_guest(
        cls,
        *,
        email: str,
        display_name: str,
    ) -> Identity:
        normalized_email = _normalize_email(email)
        final_name = str(display_name or normalized_email or 'Usuario').strip()

        return cls(
            id=normalized_email,
            name=final_name,
            email=normalized_email,
            profile=Profile.GUEST.value,
            is_active=False,
            needs_registration=False,
        )

    @classmethod
    def build_auto_registered(
        cls,
        *,
        email: str,
        display_name: str,
    ) -> Identity:
        normalized_email = _normalize_email(email)
        final_name = str(display_name or normalized_email or 'Usuario').strip()

        return cls(
            id=str(uuid4()),
            name=final_name,
            email=normalized_email,
            profile=Profile.default_assignable(),
            is_active=True,
            needs_registration=False,
        )

    def with_display_name(
        self,
        *,
        display_name: str | None,
    ) -> Identity:
        final_name = str(display_name or self.name or self.email).strip()

        return Identity(
            id=self.id,
            name=final_name,
            email=self.email,
            profile=self.profile,
            is_active=self.is_active,
            needs_registration=self.needs_registration,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile': self.profile,
            'needs_registration': self.needs_registration,
        }

    def to_sharepoint_row(self) -> dict[str, Any]:
        return {
            'user_id': self.id,
            'name': self.name,
            'email': self.email,
            'profile': self.profile,
            'is_active': self.is_active,
        }


def _normalize_email(value: Any) -> str:
    return str(value or '').strip().lower()


def _to_bool(
    value: Any,
    default: bool = False,
) -> bool:
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
