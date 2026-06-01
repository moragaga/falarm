from __future__ import annotations

from typing import Any

from src.features.admin_framework.services import AdminGridService
from src.shared.ui.grid.models import GridConfiguration, GridRowSelectionConfiguration

from .ids import AlarmRulesListIds


def build_alarm_rules_list_grid():
    return AdminGridService.create_table(
        table_id=AlarmRulesListIds.GRID,
        row_data=[],
        column_defs=_build_column_defs(),
        configuration=GridConfiguration(
            editable=False,
            pagination=True,
            pagination_page_size=20,
            row_selection=GridRowSelectionConfiguration(
                mode='singleRow',
                checkboxes=True,
                header_checkbox=False,
                enable_click_selection=True,
            ),
        ),
    )


def build_alarm_rules_grid_rows(*, rows: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    prepared_rows: list[dict[str, Any]] = []

    for row in rows or []:
        if not isinstance(row, dict):
            continue

        prepared_rows.append(
            {
                'rule_key': row.get('rule_key'),
                'family_key': row.get('family_key'),
                'rule_name': row.get('rule_name'),
                'display_name': row.get('display_name'),
                'kind': _format_kind(value=row.get('kind')),
                'risk_level': row.get('risk_level'),
                'scope_key': _resolve_scope_key(row=row),
                'priority_order': row.get('priority_order'),
                'origin_tool_key': row.get('origin_tool_key'),
                'color': _format_color(value=row.get('color')),
                'content_key': row.get('content_key'),
                'escalation_summary': row.get('escalation_summary'),
                'visual_summary': row.get('visual_summary'),
                'is_active': row.get('is_active'),
            }
        )

    return prepared_rows


def _build_column_defs() -> list[dict[str, Any]]:
    return [
        {'field': 'rule_key', 'headerName': 'ID regla', 'editable': False, 'minWidth': 180},
        {'field': 'family_key', 'headerName': 'Familia', 'editable': False, 'minWidth': 140},
        {'field': 'rule_name', 'headerName': 'Regla', 'editable': False, 'minWidth': 220},
        {'field': 'display_name', 'headerName': 'Nombre visible', 'editable': False, 'minWidth': 220},
        {'field': 'kind', 'headerName': 'Tipo', 'editable': False, 'minWidth': 110},
        {'field': 'risk_level', 'headerName': 'Riesgo', 'editable': False, 'minWidth': 110},
        {'field': 'scope_key', 'headerName': 'Scope operativo', 'editable': False, 'minWidth': 180},
        {'field': 'priority_order', 'headerName': 'Prioridad', 'editable': False, 'minWidth': 120},
        {'field': 'origin_tool_key', 'headerName': 'Herramienta inicial', 'editable': False, 'minWidth': 210},
        {'field': 'color', 'headerName': 'Color', 'editable': False, 'minWidth': 120},
        {'field': 'content_key', 'headerName': 'ID contenido', 'editable': False, 'minWidth': 190},
        {'field': 'escalation_summary', 'headerName': 'Escalamiento', 'editable': False, 'minWidth': 260},
        {'field': 'visual_summary', 'headerName': 'Visualización', 'editable': False, 'minWidth': 260},
        {
            'field': 'is_active',
            'headerName': 'Activa',
            'editable': False,
            'minWidth': 110,
            'cellRenderer': 'agCheckboxCellRenderer',
        },
    ]


def _format_kind(*, value: Any) -> str:
    if value == 'impact':
        return 'Impacto'

    return 'Riesgo'


def _format_color(*, value: Any) -> str:
    if value == 'red':
        return 'Rojo'

    if value == 'yellow':
        return 'Amarillo'

    return str(value or '')


def _resolve_scope_key(*, row: dict[str, Any]) -> str:
    return str(
        row.get('scope_key')
        or row.get('management_scope_key')
        or row.get('priority_scope_key')
        or ''
    )
