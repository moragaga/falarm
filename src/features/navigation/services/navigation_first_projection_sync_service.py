"""
Provides functionality for synchronizing the first projection configuration for navigation setup.

This module handles the synchronization of navigation groups and links by leveraging
fallback definitions from configuration files and ensuring they are properly stored
within the administration framework. It integrates multiple services such as
configuration, navigation registry, SharePoint repository, and administrative data handling.

Classes
-------
NavigationFirstProjectionSyncService
"""

from __future__ import annotations

from typing import Any

from src.features.admin_framework.models import AdminDefinition
from src.features.admin_framework.services import AdminDataService
from src.features.configuration.admin_panels.navigation.groups.definition import (
    NAVIGATION_GROUPS_ADMIN_DEFINITION,
)
from src.features.configuration.admin_panels.navigation.links.definition import (
    build_navigation_links_admin_definition,
)
from src.features.configuration.admin_panels.navigation.links.group_options import (
    build_navigation_group_options,
)
from src.features.configuration.repositories import ConfigurationSharepointRepository
from src.features.configuration.services import ConfigManifestService, ConfigService

from ..models import NavigationGroup, NavigationLink
from ..registry.navigation_registry import build_navigation_registry


class NavigationFirstProjectionSyncService:
    def __init__(
        self,
        sharepoint_repository: ConfigurationSharepointRepository,
        config_service: ConfigService,
        config_manifest_service: ConfigManifestService,
        app_name: str | None = None,
    ):
        self._config_manifest_service = config_manifest_service
        self._admin_data_service = AdminDataService(
            repository=sharepoint_repository,
            config_service=config_service,
        )
        self._app_name = app_name

    def sync_first_local_projection(self) -> bool:
        groups_fallback, links_fallback = build_navigation_registry(app_name=self._app_name)
        group_rows = self._ensure_navigation_groups(groups_fallback=groups_fallback)

        if group_rows is None:
            return False

        return self._ensure_navigation_links(
            group_rows=group_rows,
            fallback_links=links_fallback,
        )

    def _ensure_navigation_groups(
        self,
        *,
        groups_fallback: tuple[NavigationGroup, ...],
    ) -> list[dict[str, Any]] | None:
        group_rows = (
            self._admin_data_service.load(
                definition=NAVIGATION_GROUPS_ADMIN_DEFINITION,
            )
            or []
        )

        if group_rows:
            print('[INFO] Navigation group configuration already saved')
            return group_rows

        group_rows = [group.to_dict() for group in groups_fallback]

        ok = self._save_and_register_configuration(
            definition=NAVIGATION_GROUPS_ADMIN_DEFINITION,
            rows=group_rows,
            label='Navigation group',
        )

        if not ok:
            return None

        return group_rows

    def _ensure_navigation_links(
        self,
        *,
        group_rows: list[dict[str, Any]],
        fallback_links: tuple[NavigationLink, ...],
    ) -> bool:
        links_definition = build_navigation_links_admin_definition(
            parent_group_options=build_navigation_group_options(group_rows),
        )

        link_rows = (
            self._admin_data_service.load(
                definition=links_definition,
            )
            or []
        )

        if link_rows:
            print('[INFO] Navigation link configuration already saved')
            return True

        link_rows = [link.to_dict() for link in fallback_links]

        return self._save_and_register_configuration(
            definition=links_definition,
            rows=link_rows,
            label='Navigation links',
        )

    def _save_and_register_configuration(
        self,
        *,
        definition: AdminDefinition,
        rows: list[dict[str, Any]],
        label: str,
    ) -> bool:
        ok, errors, _ = self._admin_data_service.save(
            definition=definition,
            rows=rows,
        )

        if not ok:
            print(errors)
            print(f'[ERROR] {label} configuration not saved')
            return False

        print(f'[INFO] {label} configuration saved successfully')

        ok = self._config_manifest_service.register_update(
            definition=definition,
            rows=rows,
            updated_by='System',
        )

        if not ok:
            print(f'[ERROR] {label} config manifest not saved')
            return False

        print(f'[INFO] {label} config manifest saved successfully')
        return True
