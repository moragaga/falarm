"""
Provides a service for interacting with an Azure CosmosDB instance.

This module defines the `CosmosService` class, which facilitates common operations
such as querying, inserting, updating, and deleting items within a CosmosDB database.
It allows for streamlined data retrieval, manipulation, and management of database containers.

Classes
-------
CosmosService
    A service class to encapsulate CosmosDB operations.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd
from azure.cosmos import CosmosClient, PartitionKey

TTL = 60 * 60 * 24  # 24 horas


class CosmosService:
    META_DATA = {'_rid', '_ts', '_self', '_etag', '_attachments'}

    def __init__(self, client: CosmosClient, database_name: str) -> None:
        if client is None:
            raise ValueError('[ERROR] CosmosClient cannot be None')
        if not database_name:
            raise ValueError('[ERROR] Database name is required')

        self._client = client
        self._database_name = database_name
        self._database = self._client.get_database_client(database_name)

    def _get_container(self, container_name: str):
        if not container_name:
            raise ValueError('[ERROR] Container name is required')
        return self._database.get_container_client(container_name)

    def ensure_container(
        self, container_name: str, ttl: int = None, partition_key: str = '/id'
    ) -> None:
        self._database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path=partition_key),
            default_ttl=ttl or TTL,
        )

    def upsert(self, container_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        container = self._get_container(container_name)
        return container.upsert_item(body=item)

    def query_items(
        self,
        container_name: str,
        query: str = 'SELECT * FROM c',
        *,
        parameters: Optional[List[Dict[str, Any]]] = None,
        cross_partition: bool = True,
        strip_metadata: bool = True,
        unique_value: bool = False,
    ) -> List[Dict[str, Any]]:
        container = self._get_container(container_name)
        items = list(
            container.query_items(
                query=query,
                parameters=parameters or [],
                enable_cross_partition_query=cross_partition,
            )
        )
        if not strip_metadata:
            return items

        if unique_value:
            return items

        return [
            {key: value for key, value in item.items() if key not in self.META_DATA}
            for item in items
        ]

    def query_df(
        self,
        container_name: str,
        query: str = 'SELECT * FROM c',
        *,
        parameters: Optional[List[Dict[str, Any]]] = None,
    ) -> pd.DataFrame:
        items = self.query_items(
            container_name=container_name,
            query=query,
            parameters=parameters,
        )

        return pd.DataFrame(items)

    def delete_item(self, container_name: str, item_id: str, partition_key: str) -> None:
        container = self._get_container(container_name)
        container.delete_item(item=item_id, partition_key=partition_key)

    def delete_container(self, container_name: str) -> None:
        self._database.delete_container(container_name=container_name)

    def read_item(
        self,
        *,
        container_name: str,
        item_id: str,
        partition_key_value: str,
        strip_metadata: bool = True,
    ) -> dict[str, Any] | None:
        container = self._get_container(container_name)

        try:
            item = container.read_item(
                item=item_id,
                partition_key=partition_key_value,
            )
        except Exception as error:
            error_type_name = type(error).__name__

            if error_type_name in {
                'CosmosResourceNotFoundError',
                'ResourceNotFoundError',
            }:
                return None

            raise

        if not isinstance(item, dict):
            return None

        if not strip_metadata:
            return item

        return {key: value for key, value in item.items() if key not in self.META_DATA}
