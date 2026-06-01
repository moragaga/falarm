"""
Provides initialization functions for app extensions, services, and configurations.

This module contains methods to initialize various extensions and services
used in a Flask application, such as Cosmos DB, SharePoint, login management,
identity services, configuration services, and several domain-specific
services (e.g., alarm management, KPI configuration, dashboard runtime).
Each initialization method sets up the necessary infrastructure and registers
services or extensions with the Flask application instance.
"""

from __future__ import annotations

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from ..features.admin_framework.services import AdminDataService
from ..features.configuration.admin_panels.publication_manager.services import (
    PublicationManagerActionService,
)
from ..features.configuration.repositories import (
    ConfigManifestRepository,
    ConfigPublicationStateRepository,
    ConfigurationSharepointRepository,
)
from ..features.configuration.services import (
    ConfigHashService,
    ConfigManifestService,
    ConfigManifestSyncService,
    ConfigPublicationService,
    ConfigService,
    ConfigStatusService,
    build_config_artifact_registry,
)
from ..features.configuration.services.config_first_projection_sync_service import (
    ConfigFirstProjectionSyncService,
)
from ..features.identity.repositories import (
    SharePointIdentityRepository,
)
from ..features.identity.services import IdentitySyncService
from ..features.identity.services.identity_first_projection_sync_service import (
    IdentityFirstProjectionSyncService,
)
from ..features.identity.settings import get_identity_settings
from ..features.navigation.repositories import (
    NavigationProjectionRepository,
)
from ..features.navigation.services import (
    NavigationCacheService,
    NavigationFirstProjectionSyncService,
    NavigationReadService,
)
from ..features.user_sessions.repositories import UserSessionRepository
from ..features.user_sessions.services import (
    UserSessionTrackingService,
    UserSessionTrackingSettings,
)
from ..shared.infrastructure.cosmos import (
    CosmosService,
    CosmosSettings,
    create_cosmos_client,
    ensure_required_containers,
    ensure_required_database,
)
from ..shared.infrastructure.sharepoint import SharepointService, SharepointSettings
from .env_configuration import EnvConfiguration


def init_extensions(app: Flask, settings: EnvConfiguration) -> None:
    app.extensions = getattr(app, 'extensions', {})

    _init_cosmos(app=app, settings=settings)
    _init_sharepoint(app=app, settings=settings)
    _init_base_extensions(app=app)
    _init_login_manager(app=app)
    _init_identity_services(app=app)
    _init_configuration_services(app=app)
    _init_publication_services(app=app)
    _init_navigation_cache_services(app=app, settings=settings)
    _init_user_session_tracking_service(app, settings=settings)
    # Evaluate to args
    if settings.is_first_load:
        _init_navigation_first_projection(app=app, settings=settings)
        _init_identity_first_projection(app=app)
        _init_configuration_first_projection(app=app, settings=settings)
    _init_cors(app=app)


def _init_cosmos(app: Flask, settings: EnvConfiguration) -> None:
    cosmos_settings = CosmosSettings.from_env(settings=settings)
    client = create_cosmos_client(settings=cosmos_settings)

    if not settings.is_remote_service:
        print('[INFO] Init with local runtime')
        ensure_required_database(client=client, settings=cosmos_settings)
        print(
            f'[INFO] local runtime - {cosmos_settings.database_name} database create successfully'
        )

    service = CosmosService(client=client, database_name=cosmos_settings.database_name)
    ensure_required_containers(cosmos_service=service, is_remote_service=settings.is_remote_service)

    app.extensions['cosmos_service'] = service


def _init_base_extensions(app: Flask) -> None:
    extensions = ()
    for extension in extensions:
        app.extensions[extension] = {}


def _init_login_manager(app: Flask) -> None:
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.extensions['login_manager'] = login_manager


def _init_identity_services(app: Flask) -> None:
    sharepoint_service: SharepointService | None = app.extensions.get('sharepoint_service')

    with app.app_context():
        identity_settings = get_identity_settings()

    configuration_repository = ConfigurationSharepointRepository(
        sharepoint_service=sharepoint_service,
    )

    sharepoint_repository = SharePointIdentityRepository(
        repository=configuration_repository,
        settings=identity_settings,
    )

    app.extensions['identity_sync_service'] = IdentitySyncService(
        sharepoint_repository=sharepoint_repository,
        settings=identity_settings,
    )
    app.extensions['sharepoint_identity_repository'] = sharepoint_repository


def _init_configuration_services(app: Flask) -> None:
    sharepoint_service = app.extensions.get('sharepoint_service')

    configuration_sharepoint_repository = ConfigurationSharepointRepository(
        sharepoint_service=sharepoint_service,
    )
    config_service = ConfigService()

    config_manifest_repository = ConfigManifestRepository(
        repository=configuration_sharepoint_repository,
    )
    config_hash_service = ConfigHashService()
    config_artifact_registry = build_config_artifact_registry()

    config_manifest_service = ConfigManifestService(
        repository=config_manifest_repository,
        hash_service=config_hash_service,
    )

    config_manifest_sync_service = ConfigManifestSyncService(
        registry=config_artifact_registry,
        manifest_repository=config_manifest_repository,
        configuration_repository=configuration_sharepoint_repository,
        hash_service=config_hash_service,
    )

    app.extensions['configuration_sharepoint_repository'] = configuration_sharepoint_repository
    app.extensions['config_service'] = config_service
    app.extensions['config_manifest_repository'] = config_manifest_repository
    app.extensions['config_hash_service'] = config_hash_service
    app.extensions['config_artifact_registry'] = config_artifact_registry
    app.extensions['config_manifest_service'] = config_manifest_service
    app.extensions['config_manifest_sync_service'] = config_manifest_sync_service


def _init_publication_services(app: Flask) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    config_manifest_repository: ConfigManifestRepository = app.extensions.get(
        'config_manifest_repository'
    )
    configuration_repository: ConfigurationSharepointRepository = app.extensions.get(
        'configuration_sharepoint_repository'
    )
    config_manifest_sync_service = app.extensions.get('config_manifest_sync_service')

    config_publication_state_repository = ConfigPublicationStateRepository(
        cosmos_service=cosmos_service,
    )

    config_status_service = ConfigStatusService(
        manifest_repository=config_manifest_repository,
        publication_state_repository=config_publication_state_repository,
    )

    config_publication_service = ConfigPublicationService(
        manifest_repository=config_manifest_repository,
        publication_state_repository=config_publication_state_repository,
        configuration_repository=configuration_repository,
        cosmos_service=cosmos_service,
    )

    publication_manager_action_service = PublicationManagerActionService(
        status_service=config_status_service,
        publication_service=config_publication_service,
        manifest_sync_service=config_manifest_sync_service,
    )

    app.extensions['config_publication_state_repository'] = config_publication_state_repository
    app.extensions['config_status_service'] = config_status_service
    app.extensions['config_publication_service'] = config_publication_service
    app.extensions['publication_manager_action_service'] = publication_manager_action_service


def _init_navigation_cache_services(app: Flask, settings: EnvConfiguration) -> None:
    cosmos_service: CosmosService = app.extensions['cosmos_service']

    projection_repository = NavigationProjectionRepository(
        cosmos_service=cosmos_service,
    )

    read_service = NavigationReadService(
        projection_repository=projection_repository, app_name=settings.app_name
    )

    app.extensions['navigation_cache_service'] = NavigationCacheService(
        read_service=read_service,
        ttl_seconds=300,
    )


def _init_sharepoint(app: Flask, settings: EnvConfiguration) -> None:
    sharepoint_settings = SharepointSettings.from_env(settings=settings)
    service = SharepointService(settings=sharepoint_settings)
    app.extensions['sharepoint_service'] = service


def _init_user_session_tracking_service(app: Flask, settings: EnvConfiguration) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')

    user_session_tracking_settings = UserSessionTrackingSettings.from_env(settings=settings)

    repository = UserSessionRepository(
        cosmos_service=cosmos_service,
        settings=user_session_tracking_settings,
    )

    app.extensions['user_session_tracking_service'] = UserSessionTrackingService(
        repository=repository,
        settings=user_session_tracking_settings,
    )


def _init_configuration_first_projection(app: Flask, settings: EnvConfiguration) -> None:
    print('[INFO] Init configuration first remote projection')
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    publication_manager_action_service: PublicationManagerActionService = app.extensions[
        'publication_manager_action_service'
    ]

    ConfigFirstProjectionSyncService(
        cosmos_service=cosmos_service,
        publication_manager_action_service=publication_manager_action_service,
        settings=settings,
    ).sync_first_remote_projection()


def _init_navigation_first_projection(app: Flask, settings: EnvConfiguration) -> None:
    print('[INFO] Init navigation first local projection')
    configuration_repository: ConfigurationSharepointRepository = app.extensions.get(
        'configuration_sharepoint_repository'
    )
    config_service: ConfigService = app.extensions.get('config_service')
    config_manifest_service: ConfigManifestService = app.extensions.get('config_manifest_service')

    NavigationFirstProjectionSyncService(
        sharepoint_repository=configuration_repository,
        config_service=config_service,
        config_manifest_service=config_manifest_service,
        app_name=settings.app_name,
    ).sync_first_local_projection()


def _init_identity_first_projection(app: Flask) -> None:
    print('[INFO] Init identities first local projection')
    sharepoint_identity_repository: SharePointIdentityRepository = app.extensions[
        'sharepoint_identity_repository'
    ]

    IdentityFirstProjectionSyncService(
        sharepoint_identity_repository=sharepoint_identity_repository,
    ).sync_first_local_projection()


def _init_cors(app: Flask) -> None:
    CORS(
        app,
        resources={
            r'/logout': {'origins': '*'},
            r'/assets/manifest.json': {'origins': '*'},
            r'/api/*': {'origins': '*'},
        },
        supports_credentials=True,
    )
