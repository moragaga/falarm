"""
Middleware module for handling request validation, user session, identity
management, and navigation permissions in a Flask application.

This module provides functionality to register middlewares such as session
management, request validation, identity loading, and navigation access control
for a Flask application. It ensures that public and internal paths are allowed
unrestricted access, handles authenticated requests, and enforces navigation
permissions based on the user's profile and configured access controls.

Functions
---------
register_middlewares(app)
    Registers middleware functions to handle session permanence and request
    validation for the provided Flask application instance.
"""

from __future__ import annotations

from flask import (
    Flask,
    g,
    redirect,
    request,
    session,
)

from ..features.navigation.services import NavigationService
from .auth.identity_context import get_current_profile
from .auth.request_identity import load_request_identity
from .navigation import load_request_navigation

PUBLIC_PATHS = {
    '/health',
    '/api/session',
    '/service-worker.js',
    '/manifest.webmanifest',
}

AUTHENTICATED_PATHS_WITHOUT_NAVIGATION = {
    '/api/identity/register-current-user',
    '/api/user-session/touch',
}

IDENTITY_REFRESH_PATHS = {
    '/api/identity/register-current-user',
}

PUBLIC_PREFIXES = (
    '/assets/',
    '/_dash-',
    '/_dash-component-suites/',
    '/favicon.ico',
    '/apple-touch-icon',
)


def register_middlewares(app: Flask) -> None:
    @app.before_request
    def make_session_permanent():
        session.permanent = False

    @app.before_request
    def validate_requests():
        if _is_public_request(path=request.path):
            return None

        force_refresh = _should_refresh_identity(path=request.path)

        identity = load_request_identity(
            force_refresh=force_refresh,
        )

        g.identity = identity

        if identity is None:
            return _unauthorized_response()

        if _is_authenticated_request_without_navigation(path=request.path):
            return None

        profile = get_current_profile()

        if not profile:
            return _unauthorized_response()

        navigation_config = load_request_navigation(
            force_refresh=force_refresh,
        )

        if NavigationService.can_access_path(
            config=navigation_config,
            profile=profile,
            path=request.path,
        ):
            return None

        if request.path != '/':
            return redirect('/')

        return _unauthorized_response()


def _is_public_request(path: str) -> bool:
    if path in PUBLIC_PATHS:
        return True

    return any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)


def _is_authenticated_request_without_navigation(path: str) -> bool:
    return path in AUTHENTICATED_PATHS_WITHOUT_NAVIGATION


def _should_refresh_identity(path: str) -> bool:
    if path in IDENTITY_REFRESH_PATHS:
        return True

    if _is_internal_request(path=path):
        return False

    return True


def _is_internal_request(path: str) -> bool:
    if path in PUBLIC_PATHS:
        return True

    if path.startswith('/api/'):
        return True

    return any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)


def _unauthorized_response():
    if request.path != '/':
        return redirect('/')

    return 'Unauthorized access', 401
