"""
Utilities for managing user identity and session identity within a Flask application.

This module provides functionality for resolving and loading user identity based
on request headers or session data. It handles scenarios where identity is fetched
from headers, refreshed, or assigned a default if running locally. The identity
profile may also include an associated profile photo.

Functions
---------
load_request_identity(force_refresh: bool = False) -> dict | None
    Resolves and loads the user identity, either from the session or request headers.

Notes
-----
The module makes use of Flask's `session` and `g` global objects to handle identity data.
Local identity support is configured based on the application's `FLASK_ENV` configuration.

"""

from __future__ import annotations

from flask import (
    current_app,
    g,
    request,
    session,
)

from src.features.configuration.models.profile import Profile

from ..dependencies import get_identity_sync_service
from .principal_parser import (
    get_name_from_principal,
    parse_principal_header,
)
from .request_photo import get_default_photo, get_profile_photo_bytes

SESSION_IDENTITY_KEY = 'identity'


def load_request_identity(force_refresh: bool = False) -> dict | None:
    identity = session.get(SESSION_IDENTITY_KEY)
    request_email = request.headers.get('X-MS-CLIENT-PRINCIPAL-NAME')
    principal_header = request.headers.get('X-MS-CLIENT-PRINCIPAL')
    access_token = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN')

    if not force_refresh and _session_matches_request(
        identity=identity,
        request_email=request_email,
    ):
        g.identity = identity
        return identity

    if request_email and principal_header:
        principal_payload = parse_principal_header(
            principal_header=principal_header,
        )

        display_name = get_name_from_principal(
            principal_payload=principal_payload,
            fallback_email=request_email,
        )

        identity = get_identity_sync_service().resolve_identity(
            email=request_email,
            display_name=display_name,
            force_refresh=force_refresh,
        )

        identity = _assign_photo_profile(
            identity=identity,
            access_token=access_token,
            force_refresh=force_refresh,
        )

        _save_identity(identity=identity)
        return identity

    if _allow_local_identity():
        identity = _build_local_identity()

        identity = _assign_photo_profile(
            identity=identity,
            access_token=access_token,
            force_refresh=force_refresh,
        )

        _save_identity(identity=identity)
        return identity

    _clear_identity()
    return None


def _session_matches_request(
    *,
    identity: dict | None,
    request_email: str | None,
) -> bool:
    if not identity:
        return False

    session_email = identity.get('email')

    if not session_email:
        return False

    if not request_email:
        return True

    return str(session_email).strip().lower() == str(request_email).strip().lower()


def _allow_local_identity() -> bool:
    return str(current_app.config.get('FLASK_ENV') or '').upper() == 'LOCAL'


def _build_local_identity() -> dict:
    return {
        'id': 'local-user',
        'name': 'Invitado',
        'email': 'invitado@local',
        'profile': Profile.LOCAL.value,
        'needs_registration': False,
    }


def _save_identity(identity: dict) -> None:
    session[SESSION_IDENTITY_KEY] = {
        'id': identity.get('id'),
        'name': identity.get('name'),
        'email': identity.get('email'),
        'profile': identity.get('profile'),
        'photo_bytes': identity.get('photo_bytes'),
        'needs_registration': bool(identity.get('needs_registration', False)),
    }

    session.modified = True
    g.identity = session[SESSION_IDENTITY_KEY]


def _clear_identity() -> None:
    session.pop(SESSION_IDENTITY_KEY, None)
    session.modified = True
    g.identity = None


def _assign_photo_profile(
    *,
    identity: dict,
    access_token: str | None,
    force_refresh: bool,
) -> dict:
    session_identity = session.get(SESSION_IDENTITY_KEY, {})
    session_photo_bytes = session_identity.get('photo_bytes', None)

    if not force_refresh and session_photo_bytes:
        identity['photo_bytes'] = session_photo_bytes
        return identity

    if not access_token:
        identity['photo_bytes'] = get_default_photo()
        return identity

    identity['photo_bytes'] = get_profile_photo_bytes(
        access_token=access_token,
    )

    return identity
