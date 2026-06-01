from __future__ import annotations

from typing import Any
from uuid import uuid4


class AlarmComponentN0RowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]

        return {
            'component_key': f'n0_component_{uuid4().hex[:8]}',
            'component_name': '',
            'component_type': 'component',
            'parent_component_key': '',
            'position_index': None,
            'additional_position_keys': [],
            'tool_level': 'n0',
            'display_order': AlarmComponentN0RowFactoryService._resolve_next_order(rows=rows),
            'is_active': True,
        }

    @staticmethod
    def _resolve_next_order(*, rows: list[dict[str, Any]]) -> int:
        orders: list[int] = []

        for row in rows:
            try:
                order = int(row.get('display_order') or 0)
            except Exception:
                continue

            if order > 0:
                orders.append(order)

        if not orders:
            return 10

        return max(orders) + 10
