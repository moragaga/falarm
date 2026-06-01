"""
Module for managing and synchronizing the first remote projection in a publication management system.

This service interacts with a Cosmos DB backend and triggers publication actions
via the PublicationManagerActionService. It ensures that the first remote projection
is correctly published and its state is recorded in the Cosmos DB.
"""

from __future__ import annotations

from src.app.env_configuration import EnvConfiguration
from src.features.configuration.admin_panels.publication_manager.services import (
    PublicationManagerActionService,
)
from src.shared.infrastructure.cosmos import CosmosService


class ConfigFirstProjectionSyncService:
    def __init__(
        self,
        cosmos_service: CosmosService,
        publication_manager_action_service: PublicationManagerActionService,
        settings: EnvConfiguration,
    ):
        self._cosmos_service = cosmos_service
        self._publication_manager_action_service = publication_manager_action_service
        self._container_name = 'publication_local_state'
        self._published_by = 'System'
        self._settings = settings

    def sync_first_remote_projection(self) -> None:
        is_published = False
        if not self._settings.is_remote_service:
            is_published = self._is_published_local_state()

        if not is_published:
            print('[INFO] There is first projection, publishing it...')
            self._sync()
            return
        print('[INFO] First projection is already published')

    def _is_published_local_state(self) -> bool:
        response = self._cosmos_service.query_items(self._container_name)

        if len(response) != 0:
            return response[0].get('is_published')
        return False

    def _sync(self):
        action_result = self._publication_manager_action_service.publish_pending(
            published_by=self._published_by
        )

        publish_state = True
        if action_result.has_errors:
            print(f'[ERROR] {action_result.errors}')
            publish_state = False
        else:
            print('[INFO] First remote projection published successfully')

        if not self._settings.is_remote_service:
            self._publish_cosmos_state(state=publish_state)

    def _publish_cosmos_state(self, state: bool):
        self._cosmos_service.upsert(
            container_name=self._container_name,
            item={
                'id': self._container_name,
                'is_published': state,
                'published_by': self._published_by,
            },
        )
