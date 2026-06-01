"""
A data class for configuring user session tracking settings.

This class provides configuration parameters for enabling and managing the
user session tracking system. It supports creating settings from environment
configuration while applying default values for certain attributes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from src.app.env_configuration import EnvConfiguration


@dataclass(frozen=True, slots=True)
class UserSessionTrackingSettings:
    DEFAULT_CONTAINER_NAME: ClassVar[str] = 'active_user_sessions'
    DEFAULT_MAX_ACTIVE_DELTA_SECONDS: ClassVar[int] = 10 * 60

    enabled: bool
    container_name: str = DEFAULT_CONTAINER_NAME
    max_active_delta_seconds: int = 10 * 60

    @classmethod
    def from_env(cls, settings: EnvConfiguration) -> UserSessionTrackingSettings:
        return cls(
            enabled=not settings.is_local,
            container_name=cls.DEFAULT_CONTAINER_NAME,
            max_active_delta_seconds=cls.DEFAULT_MAX_ACTIVE_DELTA_SECONDS,
        )
