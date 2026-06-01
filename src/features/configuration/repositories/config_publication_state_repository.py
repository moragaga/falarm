"""
Repository for managing the state of configuration publications in a Cosmos DB
container.

This module provides functionality to load and save the current publication
state of configurations. The state is stored in a Cosmos DB container and is
identified by a specific document ID and partition key.

Classes
-------
ConfigPublicationStateRepository
    A repository to handle operations related to the configuration publication
    state in Cosmos DB.
"""

from __future__ import annotations

from src.shared.infrastructure.cosmos import CosmosService

from ..models.config_publication_state import ConfigPublicationState


class ConfigPublicationStateRepository:
    DOCUMENT_ID = 'publication_state'
    PARTITION_KEY_VALUE = 'publication_state'

    def __init__(
        self,
        cosmos_service: CosmosService | None = None,
        container_name: str = 'publication_state',
    ) -> None:
        self._cosmos_service = cosmos_service
        self._container_name = container_name

    def load_state(self) -> ConfigPublicationState:
        if self._cosmos_service is None:
            return ConfigPublicationState()

        document = self._cosmos_service.read_item(
            container_name=self._container_name,
            item_id=self.DOCUMENT_ID,
            partition_key_value=self.PARTITION_KEY_VALUE,
        )

        if document is None:
            return ConfigPublicationState()

        if not isinstance(document, dict):
            raise ValueError('config_publication_state tiene un formato inválido en Cosmos.')

        return ConfigPublicationState.from_dict(document)

    def save_state(self, state: ConfigPublicationState) -> bool:
        if self._cosmos_service is None:
            return False

        payload = {
            'id': self.DOCUMENT_ID,
            'partition_key': self.PARTITION_KEY_VALUE,
            **state.to_dict(),
        }

        return self._cosmos_service.upsert(
            container_name=self._container_name,
            item=payload,
        )
