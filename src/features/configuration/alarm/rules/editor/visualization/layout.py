from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .ids import AlarmRuleVisualizationIds
from .target_card import build_visual_target_card


def build_visualization_tab_layout(*, draft: dict[str, Any] | None):
    draft = draft or {}
    catalogs = draft.get('_catalogs') or {}
    component_options = catalogs.get('component_options') or []
    subcomponent_options = catalogs.get('subcomponent_options') or []

    requires_n0_visual = _requires_n0_visual(draft=draft)
    target = _resolve_n0_visual_target(draft=draft)

    if not requires_n0_visual:
        return html.Div(
            children=[
                dbc.Alert(
                    'Esta regla no escala a Nivel 0, por lo que no requiere configuración visual Nivel 0. '
                    'Si cambias el riesgo o agregas Nivel 0 en escalamiento, esta sección se habilitará automáticamente.',
                    color='secondary',
                    className='mb-0',
                )
            ],
        )

    return html.Div(
        children=[
            dbc.Alert(
                color='info',
                className='mb-3',
                children=(
                    'Configura una única visualización para Nivel 0. Los componentes padre definen posición; '
                    'los subcomponentes seleccionados serán también los elementos a resaltar en el front.'
                ),
            ),
            html.Div(
                className='d-flex justify-content-between align-items-center mb-3',
                children=[
                    html.H5('Visualización Nivel 0', className='mb-0'),
                    dbc.Badge('Única por regla', color='primary', pill=True),
                ],
            ),
            html.Div(
                id=AlarmRuleVisualizationIds.TARGETS_CONTAINER,
                children=[
                    build_visual_target_card(
                        target=target,
                        index='nivel_0',
                        component_options=component_options,
                        subcomponent_options=subcomponent_options,
                    )
                ],
            ),
        ],
    )


def _requires_n0_visual(*, draft: dict[str, Any]) -> bool:
    if str(draft.get('risk_level') or '') == '1':
        return True

    for target in draft.get('escalation_targets') or []:
        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        if _is_level_one_tool(draft=draft, tool_key=str(target.get('target_tool_key') or '')):
            return True

    return False


def _resolve_n0_visual_target(*, draft: dict[str, Any]) -> dict[str, Any]:
    for target in draft.get('visual_targets') or []:
        if not isinstance(target, dict):
            continue

        if str(target.get('tool_key') or '') == _resolve_level_one_tool_key(draft=draft):
            return dict(target)

    return {
        'tool_key': _resolve_level_one_tool_key(draft=draft),
        'affected_component_keys': [],
        'affected_subcomponent_keys': [],
        'is_complete': False,
    }


def _resolve_level_one_tool_key(*, draft: dict[str, Any]) -> str:
    catalogs = draft.get('_catalogs') or {}
    configured = str(catalogs.get('level_one_tool_key') or '').strip()
    if configured:
        return configured

    for tool in catalogs.get('tools') or []:
        if not isinstance(tool, dict):
            continue
        if str(tool.get('tool_level') or '') == '1':
            return str(tool.get('tool_key') or '').strip()

    return 'nivel_0'


def _is_level_one_tool(*, draft: dict[str, Any], tool_key: str) -> bool:
    catalogs = draft.get('_catalogs') or {}
    tool_level_by_key = catalogs.get('tool_level_by_key') or {}
    return str(tool_level_by_key.get(tool_key) or '') == '1' or tool_key == _resolve_level_one_tool_key(draft=draft)
