"""
This module provides utility functions to retrieve application services from Flask's
`app.extensions`. If a requested service is not registered, a RuntimeError will be raised.

These functions are designed to streamline access to specific services required for
application logic, ensuring they are properly initialized and registered.

Functions
---------
get_cosmos_service()
    Retrieves the CosmosService instance from Flask's `app.extensions`.

get_identity_sync_service()
    Retrieves the IdentitySyncService instance from Flask's `app.extensions`.

get_configuration_sharepoint_repository()
    Retrieves the ConfigurationSharepointRepository instance from Flask's `app.extensions`.

get_config_service()
    Retrieves the ConfigService instance from Flask's `app.extensions`.

get_config_manifest_service()
    Retrieves the ConfigManifestService instance from Flask's `app.extensions`.

get_navigation_cache_service()
    Retrieves the NavigationCacheService instance from Flask's `app.extensions`.

get_dashboard_context_service()
    Retrieves the DashboardContextService instance from Flask's `app.extensions`.

get_distributed_alarm_context_service()
    Retrieves the DistributedAlarmContextService instance from Flask's `app.extensions`.

get_publication_manager_action_service()
    Retrieves the PublicationManagerActionService instance from Flask's `app.extensions`.

get_alarm_message_admin_service()
    Retrieves the AlarmMessageAdminService instance from Flask's `app.extensions`.

get_alarm_management_use_case_service()
    Retrieves the AlarmManagementUseCaseService instance from Flask's `app.extensions`.

get_user_session_tracking_service()
    Retrieves the UserSessionTrackingService instance from Flask's `app.extensions`.
"""

from __future__ import annotations

from flask import current_app

from src.features.configuration.admin_panels.publication_manager.services import (
    PublicationManagerActionService,
)
from src.features.configuration.repositories import ConfigurationSharepointRepository
from src.features.configuration.services import (
    ConfigManifestService,
    ConfigService,
)
from src.features.identity.services import IdentitySyncService
from src.features.navigation.services import NavigationCacheService
from src.features.user_sessions.services import UserSessionTrackingService
from src.shared.infrastructure.cosmos import CosmosService


def get_cosmos_service() -> CosmosService:
    service = current_app.extensions.get('cosmos_service')
    if service is None:
        raise RuntimeError('[ERROR] CosmosService is not registered in app.extensions')
    return service


def get_identity_sync_service() -> IdentitySyncService:
    service = current_app.extensions.get('identity_sync_service')
    if service is None:
        raise RuntimeError('[ERROR] IdentitySyncService is not registered in app.extensions')
    return service


def get_configuration_sharepoint_repository() -> ConfigurationSharepointRepository:
    service = current_app.extensions.get('configuration_sharepoint_repository')
    if service is None:
        raise RuntimeError('[ERROR] ConfigurationRepository is not registered in app.extensions')
    return service


def get_config_service() -> ConfigService:
    service = current_app.extensions.get('config_service')
    if service is None:
        raise RuntimeError('[ERROR] ConfigService is not registered in app.extensions')
    return service


def get_config_manifest_service() -> ConfigManifestService:
    service = current_app.extensions.get('config_manifest_service')
    if service is None:
        raise RuntimeError('[ERROR] ConfigManifestService is not registered in app.extensions')
    return service


def get_navigation_cache_service() -> NavigationCacheService:
    service = current_app.extensions.get('navigation_cache_service')
    if service is None:
        raise RuntimeError('[ERROR] NavigationCacheService is not registered in app.extensions')
    return service



def get_publication_manager_action_service() -> PublicationManagerActionService:
    service = current_app.extensions.get('publication_manager_action_service')
    if service is None:
        raise RuntimeError(
            '[ERROR] PublicationManagerActionService is not registered in app.extensions'
        )
    return service


def get_user_session_tracking_service() -> UserSessionTrackingService:
    service = current_app.extensions['user_session_tracking_service']
    if service is None:
        raise RuntimeError('[ERROR] UserSessionTrackingService is not registered in app.extensions')
    return service
