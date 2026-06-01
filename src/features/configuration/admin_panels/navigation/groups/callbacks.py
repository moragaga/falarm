"""
Defines functionality for registering navigation groups admin callback.

This module provides an implementation to register a specific admin callback
related to navigation groups. It handles saving the administrative operations
and invalidating cached navigation data upon successful updates while utilizing
associated services for configuration handling and administrative processing.
"""

from __future__ import annotations

from flask import session

from src.app.dependencies import (
    get_config_manifest_service,
    get_config_service,
    get_configuration_sharepoint_repository,
    get_navigation_cache_service,
)
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService

from .definition import NAVIGATION_GROUPS_ADMIN_DEFINITION


def register_navigation_groups_admin_callback() -> None:
    def _after_save(definition, normalized_rows: list[dict]) -> list[str]:
        updated_by = (session.get('identity') or {}).get('email')

        ok = get_config_manifest_service().register_update(
            definition=definition,
            rows=normalized_rows,
            updated_by=updated_by,
        )

        if not ok:
            return ['El archivo se guardó, pero no se pudo actualizar el config manifest.']

        get_navigation_cache_service().invalidate()
        return []

    register_admin_callback(
        definition_factory=lambda: NAVIGATION_GROUPS_ADMIN_DEFINITION,
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=_after_save,
    )
