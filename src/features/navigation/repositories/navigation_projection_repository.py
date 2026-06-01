"""
Module for handling navigation projection data storage and retrieval.

This module provides functionality to interact with a CosmosDB container for
storing and retrieving navigation configuration data, including navigation
groups and links. The data is read from specific documents within the database
and returned as structured rows suitable for further processing.

Classes
-------
NavigationProjectionRepository
    Repository for fetching navigation configuration data from a CosmosDB
    service.
"""

from __future__ import annotations

from typing import Any


class NavigationProjectionRepository:
    def __init__(
        self,
        cosmos_service,
        container_name: str = 'navigation_configuration',
        groups_document_id: str = 'navigation_groups',
        groups_partition_key: str = 'navigation_groups',
        links_document_id: str = 'navigation_links',
        links_partition_key: str = 'navigation_links',
    ) -> None:
        self._cosmos_service = cosmos_service
        self._container_name = container_name

        self._groups_document_id = groups_document_id
        self._groups_partition_key = groups_partition_key

        self._links_document_id = links_document_id
        self._links_partition_key = links_partition_key

    def load_group_rows(self) -> list[dict[str, Any]]:
        document = self._read_document(
            document_id=self._groups_document_id,
            partition_key_value=self._groups_partition_key,
        )

        return self._extract_rows(document=document)

    def load_link_rows(self) -> list[dict[str, Any]]:
        document = self._read_document(
            document_id=self._links_document_id,
            partition_key_value=self._links_partition_key,
        )

        return self._extract_rows(document=document)

    def _read_document(
        self,
        document_id: str,
        partition_key_value: str,
    ) -> dict[str, Any] | None:
        return self._cosmos_service.read_item(
            container_name=self._container_name,
            item_id=document_id,
            partition_key_value=partition_key_value,
        )

    @staticmethod
    def _extract_rows(document: dict[str, Any] | None) -> list[dict[str, Any]]:
        if not isinstance(document, dict):
            return []

        for key in ('rows', 'items', 'data'):
            value = document.get(key)

            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

        payload = document.get('payload')

        if isinstance(payload, dict):
            for key in ('rows', 'items', 'data'):
                value = payload.get(key)

                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]

        return []
