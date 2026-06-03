from __future__ import annotations

from typing import Any

from src.features.configuration.alarm.options import AlarmOperationalArea
from src.features.configuration.alarm.services.alarm_identifier_normalization_service import (
    AlarmIdentifierNormalizationService,
)


class AlarmFamilyRowNormalizationService:
    @staticmethod
    def normalize_rows(
        *,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        return [
            AlarmFamilyRowNormalizationService.normalize_row(row=row)
            for row in rows or []
            if isinstance(row, dict)
        ]

    @staticmethod
    def normalize_row(
        *,
        row: dict[str, Any],
    ) -> dict[str, Any]:
        normalized = dict(row)

        normalized['family_key'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('family_key'),
            )
        )

        normalized['family_name'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('family_name'),
            )
        )

        normalized['description'] = str(normalized.get('description') or '').strip()

        normalized['operational_area'] = _normalize_operational_area(
            value=normalized.get('operational_area'),
        )

        normalized['display_order'] = _to_int(
            value=normalized.get('display_order'),
            default_value=0,
        )

        normalized['is_active'] = bool(normalized.get('is_active', True))

        return normalized


def _normalize_operational_area(
    *,
    value: Any,
) -> str:
    normalized = str(value or '').strip()

    allowed_values = {
        item.value
        for item in AlarmOperationalArea
    }

    if normalized in allowed_values:
        return normalized

    return AlarmOperationalArea.PLANTA.value


def _to_int(
    *,
    value: Any,
    default_value: int,
) -> int:
    try:
        return int(value)
    except Exception:
        return default_value