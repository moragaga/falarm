"""
A module for managing Cosmos DB container settings and ensuring their existence.

This module provides a dataclass for defining Cosmos DB container configurations,
a dictionary to store the configurations for various containers, and a function
for ensuring the required containers are present in a Cosmos DB instance.
"""

from __future__ import annotations

from dataclasses import dataclass

from .service import CosmosService

DEFAULT_TTL_SECONDS = 60 * 60 * 24  # 24h


@dataclass(frozen=True, slots=True)
class CosmosContainerSettings:
    partition_key_path: str = '/id'
    default_ttl: int = DEFAULT_TTL_SECONDS
    is_remote_service: bool = True


COSMOS_CONTAINER_SETTINGS: dict[str, CosmosContainerSettings] = {
    'publication_state': CosmosContainerSettings(partition_key_path='/id', default_ttl=-1),
    'navigation_configuration': CosmosContainerSettings(partition_key_path='/id', default_ttl=-1),
    'active_user_sessions': CosmosContainerSettings(
        partition_key_path='/id', default_ttl=DEFAULT_TTL_SECONDS
    ),
    'basic_analytics': CosmosContainerSettings(partition_key_path='/id', default_ttl=-1),
    'publication_local_state': CosmosContainerSettings(
        partition_key_path='/id', default_ttl=-1, is_remote_service=False
    ),
}


def ensure_required_containers(
    cosmos_service: CosmosService, is_remote_service: bool = True
) -> None:
    for container, settings in COSMOS_CONTAINER_SETTINGS.items():
        if is_remote_service and not settings.is_remote_service:
            continue

        cosmos_service.ensure_container(
            container_name=container,
            ttl=settings.default_ttl,
            partition_key=settings.partition_key_path,
        )
