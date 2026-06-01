from __future__ import annotations

from typing import Any

from src.features.configuration.models import FieldOption


def build_alarm_component_options(
    rows: list[dict[str, Any]] | None,
) -> tuple[FieldOption, ...]:
    options: list[FieldOption] = []

    for row in sorted(rows or [], key=_component_sort_key):
        if not isinstance(row, dict):
            continue

        component_key = str(row.get('component_key') or '').strip()
        component_name = str(row.get('component_name') or '').strip()
        component_code = str(row.get('component_code') or '').strip()
        is_active = bool(row.get('is_active', True))

        if not component_key or not component_name or not is_active:
            continue

        label = component_name
        if component_code:
            label = f'{component_name} · {component_code}'

        options.append(
            FieldOption(
                label=label,
                value=component_key,
            )
        )

    return tuple(options)


def _component_sort_key(row: dict[str, Any]) -> tuple[int, str]:
    try:
        order = int(row.get('display_order') or row.get('position_index') or 0)
    except Exception:
        order = 0

    return order, str(row.get('component_name') or '')
