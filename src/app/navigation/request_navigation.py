"""
Handles the loading of navigation runtime configuration for the current request.

This function interacts with the navigation cache service to retrieve and
store the runtime configuration in the Flask session. If necessary, it can
force a refresh of the configuration data.

Parameters
----------
force_refresh : bool, optional
    Indicates whether to force a refresh of the navigation runtime configuration.
    Defaults to False.

Returns
-------
NavigationRuntimeConfig
    The runtime configuration of the navigation loaded from the cache service.
"""

from __future__ import annotations

from flask import session

from src.features.navigation.models import (
    NavigationRuntimeConfig,
)

from ..dependencies import get_navigation_cache_service


def load_request_navigation(
    force_refresh: bool = False,
) -> NavigationRuntimeConfig:
    config = get_navigation_cache_service().get_navigation(
        force_refresh=force_refresh,
    )

    session['navigation_runtime_config'] = config.to_dict()
    session.modified = True

    return config
