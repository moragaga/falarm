"""
A service for caching navigation runtime configuration with time-to-live (TTL) support.

This module provides functionality to cache and manage navigation runtime configurations
using a specified TTL, reducing the need for frequent data fetching. It ensures thread-safe
access and supports manual invalidation or forced refreshing of the cache.

Classes
-------
NavigationCacheService
    A service class for caching and managing navigation runtime configurations.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from threading import Lock

import pytz

from ..models.navigation_runtime_config import (
    NavigationRuntimeConfig,
)
from .navigation_read_service import NavigationReadService


class NavigationCacheService:
    def __init__(
        self,
        read_service: NavigationReadService,
        ttl_seconds: int = 300,
    ) -> None:
        self._read_service = read_service
        self._ttl = timedelta(seconds=ttl_seconds)
        self._lock = Lock()
        self._cached_config = NavigationRuntimeConfig()
        self._cache_at: datetime | None = None

    def get_navigation(
        self,
        force_refresh: bool = False,
    ) -> NavigationRuntimeConfig:
        with self._lock:
            if force_refresh or self._is_expired():
                self._cached_config = self._read_service.load_navigation()
                self._cache_at = datetime.now(tz=pytz.utc)

            return self._cached_config

    def invalidate(self) -> None:
        with self._lock:
            self._cached_config = NavigationRuntimeConfig()
            self._cache_at = None

    def _is_expired(self) -> bool:
        if self._cache_at is None:
            return True

        return datetime.now(tz=pytz.utc) - self._cache_at > self._ttl
