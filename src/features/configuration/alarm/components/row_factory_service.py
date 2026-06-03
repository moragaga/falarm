from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.features.configuration.alarm.options import AlarmComponentAppliesToToolTier


class AlarmComponentRowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]
        next_order = AlarmComponentRowFactoryService._resolve_next_order(rows=rows)
        component_key = f'alarm_component_{uuid4().hex[:8]}'

        return {
            'component_key': component_key,
            'component_code': '',
            'component_name': '',
            'position_index': next_order,
            'applies_to_tool_tier': (
                AlarmComponentAppliesToToolTier.INTEGRATED_OPERATIONS.value
            ),
            'display_order': next_order,
            'is_active': True,
        }

    @staticmethod
    def _resolve_next_order(
        *,
        rows: list[dict[str, Any]],
    ) -> int:
        orders: list[int] = []

        for row in rows:
            try:
                order = int(row.get('display_order') or row.get('position_index') or 0)
            except Exception:
                continue

            if order > 0:
                orders.append(order)

        if not orders:
            return 10

        return max(orders) + 10