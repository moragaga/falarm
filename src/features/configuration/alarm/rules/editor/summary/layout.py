from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from src.features.configuration.alarm.options import (
    ALARM_CRITICALITY_OPTIONS,
    ALARM_VISIBILITY_MODE_OPTIONS,
    get_option_label,
)
from src.features.configuration.alarm.rules.editor.diagnostics_renderer import (
    build_alarm_rule_diagnostics_content,
)

from .ids import AlarmRuleSummaryIds


def build_summary_tab_layout(
    *,
    draft: dict[str, Any] | None,
):
    draft = draft or {}
    diagnostics = draft.get('diagnostics') or []

    return html.Div(
        id=AlarmRuleSummaryIds.SUMMARY_CONTAINER,
        children=[
            dbc.Row(
                className='g-3 mb-3',
                children=[
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Regla',
                            value=(
                                draft.get('display_name')
                                or draft.get('rule_name')
                                or 'Sin nombre'
                            ),
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Criticidad',
                            value=(
                                get_option_label(
                                    value=draft.get('criticality_code'),
                                    options=ALARM_CRITICALITY_OPTIONS,
                                )
                                or 'No configurada'
                            ),
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Visibilidad',
                            value=(
                                get_option_label(
                                    value=draft.get('visibility_mode'),
                                    options=ALARM_VISIBILITY_MODE_OPTIONS,
                                )
                                or 'No configurada'
                            ),
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Scope operativo',
                            value=draft.get('scope_key') or 'No configurado',
                        ),
                    ),
                ],
            ),
            dbc.Row(
                className='g-3 mb-3',
                children=[
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Herramienta inicial',
                            value=_resolve_tool_label(
                                draft=draft,
                                tool_key=str(draft.get('origin_tool_key') or ''),
                            )
                            or 'No configurada',
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Familia',
                            value=_resolve_family_label(draft=draft)
                            or 'No configurada',
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Contenido',
                            value=draft.get('content_key') or 'No configurado',
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Estado',
                            value=(
                                'Activa'
                                if bool(draft.get('is_active', True))
                                else 'Inactiva'
                            ),
                        ),
                    ),
                ],
            ),
            dbc.Card(
                children=[
                    dbc.CardHeader('Diagnóstico de edición'),
                    dbc.CardBody(
                        id=AlarmRuleSummaryIds.DIAGNOSTICS_CONTAINER,
                        children=build_alarm_rule_diagnostics_content(
                            diagnostics=diagnostics,
                        ),
                    ),
                ],
            ),
        ],
    )


def _summary_card(
    *,
    title: str,
    value: str,
):
    return dbc.Card(
        children=[
            dbc.CardBody(
                children=[
                    html.Div(title, className='text-muted small'),
                    html.Div(value, className='fw-semibold'),
                ],
            ),
        ],
    )


def _resolve_family_label(
    *,
    draft: dict[str, Any],
) -> str:
    family_key = str(draft.get('family_key') or '').strip()

    if not family_key:
        return ''

    catalogs = draft.get('_catalogs') or {}
    family_by_key = catalogs.get('family_by_key') or {}
    family = family_by_key.get(family_key)

    if isinstance(family, dict):
        family_name = str(family.get('family_name') or '').strip()

        if family_name:
            return family_name

    return family_key


def _resolve_tool_label(
    *,
    draft: dict[str, Any],
    tool_key: str,
) -> str:
    tool_key = str(tool_key or '').strip()

    if not tool_key:
        return ''

    catalogs = draft.get('_catalogs') or {}
    tool_name_by_key = catalogs.get('tool_name_by_key') or {}

    tool_name = str(tool_name_by_key.get(tool_key) or '').strip()

    if tool_name:
        return tool_name

    return tool_key