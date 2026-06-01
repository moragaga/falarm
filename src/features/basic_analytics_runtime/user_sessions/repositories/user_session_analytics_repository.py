from __future__ import annotations

from typing import Any

from src.app.dependencies import get_cosmos_service

from ..constants import (
    COSMOS_CONTAINER_NAME,
    DOCUMENT_ID,
    PARTITION_KEY,
)


class UserSessionAnalyticsRepository:
    @staticmethod
    def get_snapshot() -> dict[str, Any]:
        try:
            item = get_cosmos_service().read_item(
                container_name=COSMOS_CONTAINER_NAME,
                item_id=DOCUMENT_ID,
                partition_key_value=PARTITION_KEY,
            )

            if isinstance(item, dict):
                return item

            return {}

        except Exception:
            return {}