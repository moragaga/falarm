from __future__ import annotations

from typing import Any

from src.features.admin_framework.services import AdminGridService
from src.features.configuration.alarm.options import (
    ALARM_BUSINESS_CATEGORY_OPTIONS,
    ALARM_COLOR_OPTIONS,
    ALARM_CRITICALITY_OPTIONS,
    ALARM_KIND_OPTIONS,
    ALARM_VISIBILITY_MODE_OPTIONS,
    get_option_label,
)
from src.shared.ui.grid.models import (
    GridConfiguration,
    GridRowSelectionConfiguration,
)

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


def build_alarm_rules_grid_rows(
    *,
    rows: list[dict[str, Any]] | None,
    families: list[dict[str, Any]] | None = None,
    tools: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    family_name_by_key = _build_name_map(
        rows=families or [],
        key_field='family_key',
        name_field='family_name',
    )

    tool_name_by_key = _build_name_map(
        rows=tools or [],
        key_field='tool_key',
        name_field='tool_name',
    )

    prepared_rows: list[dict[str, Any]] = []

    for row in rows or []:
        if not isinstance(row, dict):
            continue

        family_key = str(row.get('family_key') or '').strip()
        origin_tool_key = str(row.get('origin_tool_key') or '').strip()

        prepared_rows.append(
            {
                'rule_key': row.get('rule_key'),
                'family_key': family_key,
                'family_label': family_name_by_key.get(family_key, family_key),
                'rule_name': row.get('rule_name'),
                'display_name': row.get('display_name'),
                'kind': get_option_label(
                    value=row.get('kind'),
                    options=ALARM_KIND_OPTIONS,
                ),
                'criticality_code': get_option_label(
                    value=row.get('criticality_code'),
                    options=ALARM_CRITICALITY_OPTIONS,
                ),
                'business_category': get_option_label(
                    value=row.get('business_category'),
                    options=ALARM_BUSINESS_CATEGORY_OPTIONS,
                ),
                'visibility_mode': get_option_label(
                    value=row.get('visibility_mode'),
                    options=ALARM_VISIBILITY_MODE_OPTIONS,
                ),
                'scope_key': row.get('scope_key'),
                'priority_order': row.get('priority_order'),
                'origin_tool_key': origin_tool_key,
                'origin_tool_label': tool_name_by_key.get(
                    origin_tool_key,
                    origin_tool_key,
                ),
                'operator_bucket': row.get('operator_bucket'),
                'color': get_option_label(
                    value=row.get('color'),
                    options=ALARM_COLOR_OPTIONS,
                ),
                'content_key': row.get('content_key'),
                'escalation_summary': row.get('escalation_summary'),
                'visual_summary': row.get('visual_summary'),
                'is_active': row.get('is_active'),
            }
        )

    return prepared_rows


def _build_column_defs() -> list[dict[str, Any]]:
    return [
        {
            'field': 'rule_key',
            'headerName': 'ID regla',
            'editable': False,
            'minWidth': 180,
            'hide': True,
        },
        {
            'field': 'family_key',
            'headerName': 'ID familia',
            'editable': False,
            'minWidth': 160,
            'hide': True,
        },
        {
            'field': 'origin_tool_key',
            'headerName': 'ID herramienta inicial',
            'editable': False,
            'minWidth': 190,
            'hide': True,
        },
        {
            'field': 'family_label',
            'headerName': 'Familia',
            'editable': False,
            'minWidth': 180,
        },
        {
            'field': 'rule_name',
            'headerName': 'Regla',
            'editable': False,
            'minWidth': 220,
        },
        {
            'field': 'display_name',
            'headerName': 'Nombre visible',
            'editable': False,
            'minWidth': 240,
        },
        {
            'field': 'kind',
            'headerName': 'Tipo',
            'editable': False,
            'minWidth': 110,
        },
        {
            'field': 'criticality_code',
            'headerName': 'Criticidad',
            'editable': False,
            'minWidth': 170,
        },
        {
            'field': 'business_category',
            'headerName': 'Categoría',
            'editable': False,
            'minWidth': 170,
        },
        {
            'field': 'visibility_mode',
            'headerName': 'Visibilidad',
            'editable': False,
            'minWidth': 170,
        },
        {
            'field': 'scope_key',
            'headerName': 'Scope operativo',
            'editable': False,
            'minWidth': 190,
        },
        {
            'field': 'priority_order',
            'headerName': 'Prioridad',
            'editable': False,
            'minWidth': 120,
        },
        {
            'field': 'origin_tool_label',
            'headerName': 'Herramienta inicial',
            'editable': False,
            'minWidth': 230,
        },
        {
            'field': 'operator_bucket',
            'headerName': 'Bucket operador',
            'editable': False,
            'minWidth': 170,
        },
        {
            'field': 'color',
            'headerName': 'Color',
            'editable': False,
            'minWidth': 120,
        },
        {
            'field': 'content_key',
            'headerName': 'ID contenido',
            'editable': False,
            'minWidth': 190,
        },
        {
            'field': 'escalation_summary',
            'headerName': 'Escalamiento',
            'editable': False,
            'minWidth': 300,
        },
        {
            'field': 'visual_summary',
            'headerName': 'Visualización',
            'editable': False,
            'minWidth': 300,
        },
        {
            'field': 'is_active',
            'headerName': 'Activa',
            'editable': False,
            'minWidth': 110,
            'cellRenderer': 'agCheckboxCellRenderer',
        },
    ]


def _build_name_map(
    *,
    rows: list[dict[str, Any]],
    key_field: str,
    name_field: str,
) -> dict[str, str]:
    result: dict[str, str] = {}

    for row in rows or []:
        if not isinstance(row, dict):
            continue

        key = str(row.get(key_field) or '').strip()

        if not key:
            continue

        name = str(row.get(name_field) or key).strip()
        result[key] = name or key

    return result