"""
This module provides services for creating and managing navigation group rows,
allowing dynamic generation of navigation elements with unique attributes such as
group ID, label, icon, order, and visibility in menus.

Classes
-------
NavigationGroupRowFactoryService
    A service class for creating and managing rows in navigation groups.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4


class NavigationGroupRowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]

        return {
            'group_id': str(uuid4()),
            'label': '',
            'icon': '',
            'order': NavigationGroupRowFactoryService._resolve_next_order(
                rows=rows,
            ),
            'visible_in_menu': True,
            'is_active': True,
            'allow_profiles': '',
        }

    @staticmethod
    def _resolve_next_order(
        *,
        rows: list[dict[str, Any]],
    ) -> int:
        orders: list[int] = []

        for row in rows:
            try:
                order = int(row.get('order') or 0)
            except Exception:
                continue

            if order > 0:
                orders.append(order)

        if not orders:
            return 10

        return max(orders) + 10
