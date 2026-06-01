"""
A module for managing user session data in a Cosmos DB repository.

The module provides functionality for retrieving and upserting
documents related to user sessions using the Cosmos DB service.
"""

from __future__ import annotations

from typing import Any

from ..settings import UserSessionTrackingSettings


class UserSessionRepository:
    def __init__(self, *, cosmos_service, settings: UserSessionTrackingSettings) -> None:
        self._cosmos_service = cosmos_service
        self._container_name = settings.container_name

    def get_by_id(
        self,
        *,
        document_id: str,
    ) -> dict[str, Any] | None:
        return self._cosmos_service.read_item(
            container_name=self._container_name,
            item_id=document_id,
            partition_key_value=document_id,
        )

    def upsert(
        self,
        *,
        item: dict[str, Any],
    ) -> None:
        self._cosmos_service.upsert(
            container_name=self._container_name,
            item=item,
        )
