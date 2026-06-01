"""
This module provides configuration management for identity settings in a Flask application.

The module includes functionality for retrieving and handling identity-related configuration
values, such as environment, user-related paths and filenames, and cache time-to-live settings.
"""

from __future__ import annotations

from dataclasses import dataclass

from flask import current_app

LOCAL_ENVIRONMENT = 'LOCAL'


@dataclass(frozen=True)
class IdentitySettings:
    environment: str
    users_filename: str
    users_relative_path: str
    cache_ttl_seconds: int

    @property
    def should_write(self) -> bool:
        return self.environment.strip().upper() != LOCAL_ENVIRONMENT


def get_identity_settings() -> IdentitySettings:
    return IdentitySettings(
        environment=_get_config_value(
            key='FLASK_ENV',
            default='LOCAL',
        ),
        users_filename=_get_config_value(
            key='IDENTITY_USERS_FILENAME',
            default='identity_users.json.gz',
        ),
        users_relative_path=_get_config_value(
            key='IDENTITY_USERS_RELATIVE_PATH',
            default='identity',
        ),
        cache_ttl_seconds=_get_int_config_value(
            key='IDENTITY_USERS_CACHE_TTL_SECONDS',
            default=300,
        ),
    )


def _get_config_value(
    *,
    key: str,
    default: str,
) -> str:
    value = current_app.config.get(key)

    if value is None:
        return default

    return str(value)


def _get_int_config_value(
    *,
    key: str,
    default: int,
) -> int:
    value = current_app.config.get(key)

    if value is None:
        return default

    try:
        return int(value)
    except TypeError, ValueError:
        return default
