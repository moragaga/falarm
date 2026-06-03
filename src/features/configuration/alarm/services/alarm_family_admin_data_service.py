from __future__ import annotations

from typing import Any

from src.features.admin_framework.models import AdminDefinition
from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.services.alarm_family_row_normalization_service import (
    AlarmFamilyRowNormalizationService,
)


class AlarmFamilyAdminDataService:
    def __init__(
        self,
        *,
        delegate: AdminDataService,
    ) -> None:
        self._delegate = delegate

    def load(
        self,
        definition: AdminDefinition,
    ) -> list[dict[str, Any]]:
        rows = self._delegate.load(definition)

        return AlarmFamilyRowNormalizationService.normalize_rows(
            rows=rows,
        )

    def save(
        self,
        definition: AdminDefinition,
        rows: list[dict[str, Any]],
    ):
        normalized_rows = AlarmFamilyRowNormalizationService.normalize_rows(
            rows=rows,
        )

        return self._delegate.save(
            definition,
            normalized_rows,
        )