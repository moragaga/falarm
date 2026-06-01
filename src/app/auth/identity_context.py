"""
Utility functions to manage and retrieve user identity and session details.

This module provides a series of helper functions to interact with the user session and
identity stored in Flask's `g` and `session` objects. These utilities enable retrieval
of user-specific information such as profile, email, or registration status, and also
facilitate checks against specific roles or profiles.
"""

from __future__ import annotations

from flask import (
    g,
    session,
)

SESSION_IDENTITY_KEY = 'identity'


def get_current_identity() -> dict | None:
    return getattr(g, SESSION_IDENTITY_KEY, None) or session.get(
        SESSION_IDENTITY_KEY,
    )


def get_current_profile(default: str | None = None) -> str | None:
    identity = get_current_identity()

    if not identity:
        return default

    return identity.get('profile', default)
