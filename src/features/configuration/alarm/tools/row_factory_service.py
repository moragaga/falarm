from __future__ import annotations

from typing import Any
from uuid import uuid4


class AlarmToolRowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]

        return {
            'tool_key': f'alarm_tool_{uuid4().hex[:8]}',
            'tool_name': '',
            'tool_level': 'n1',
            'visualization_mode': 'generic',
            'display_order': AlarmToolRowFactoryService._resolve_next_order(rows=rows),
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
