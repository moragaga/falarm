from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from src.features.configuration.alarm.options import (
    AlarmCriticality,
    AlarmToolTier,
    AlarmVisibilityMode,
)

from .ids import AlarmRuleVisualizationIds
from .target_card import build_visual_target_card


def build_visualization_tab_layout(
    *,
    draft: dict[str, Any] | None,
):
    draft = draft or {}
    catalogs = draft.get('_catalogs') or {}

    component_options = catalogs.get('component_options') or []

    if not _requires_integrated_operations_visualization(draft=draft):
        return html.Div(
            children=[
                dbc.Alert(
                    (
                        'Esta regla no requiere visualización ADA Operaciones Integradas. '
                        'Se requiere cuando la regla se muestra en esa herramienta: C1, '
                        'herramienta inicial ADA Operaciones Integradas o escalamiento hacia ella.'
                    ),
                    color='secondary',
                    className='mb-0',
                )
            ],
        )

    target = _resolve_visual_target(
        draft=draft,
    )

    selected_component_keys = _ensure_list(
        value=target.get('affected_component_keys'),
    )

    filtered_subcomponent_options = _filter_subcomponent_options(
        catalogs=catalogs,
        selected_component_keys=selected_component_keys,
    )

    target = _prune_target_subcomponents(
        target=target,
        allowed_subcomponent_options=filtered_subcomponent_options,
    )

    return html.Div(
        children=[
            dbc.Alert(
                color='info',
                className='mb-3',
                children=(
                    'Configura una única visualización para ADA Operaciones Integradas. '
                    'Primero selecciona componentes padre; luego se habilitarán solo sus '
                    'subcomponentes asociados.'
                ),
            ),
            html.Div(
                className='d-flex justify-content-between align-items-center mb-3',
                children=[
                    html.H5('Visualización ADA Operaciones Integradas', className='mb-0'),
                    dbc.Badge('Única por regla', color='primary', pill=True),
                ],
            ),
            html.Div(
                id=AlarmRuleVisualizationIds.TARGETS_CONTAINER,
                children=[
                    build_visual_target_card(
                        target=target,
                        index='integrated_operations',
                        component_options=component_options,
                        subcomponent_options=filtered_subcomponent_options,
                    )
                ],
            ),
        ],
    )


def _requires_integrated_operations_visualization(
    *,
    draft: dict[str, Any],
) -> bool:
    if str(draft.get('visibility_mode') or '') == AlarmVisibilityMode.TRACE_ONLY.value:
        return False

    origin_tool_key = str(draft.get('origin_tool_key') or '')

    if origin_tool_key and _is_integrated_operations_tool(
        draft=draft,
        tool_key=origin_tool_key,
    ):
        return True

    if str(draft.get('criticality_code') or '') == AlarmCriticality.C1.value:
        return True

    for target in draft.get('escalation_targets') or []:
        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        if _is_integrated_operations_tool(
            draft=draft,
            tool_key=str(target.get('target_tool_key') or ''),
        ):
            return True

    return False


def _resolve_visual_target(
    *,
    draft: dict[str, Any],
) -> dict[str, Any]:
    integrated_operations_tool_key = _resolve_integrated_operations_tool_key(
        draft=draft,
    )

    for target in draft.get('visual_targets') or []:
        if not isinstance(target, dict):
            continue

        if str(target.get('tool_key') or '') == integrated_operations_tool_key:
            return dict(target)

    return {
        'tool_key': integrated_operations_tool_key,
        'affected_component_keys': [],
        'affected_subcomponent_keys': [],
        'is_complete': False,
    }


def _resolve_integrated_operations_tool_key(
    *,
    draft: dict[str, Any],
) -> str:
    origin_tool_key = str(draft.get('origin_tool_key') or '')

    if origin_tool_key and _is_integrated_operations_tool(
        draft=draft,
        tool_key=origin_tool_key,
    ):
        return origin_tool_key

    for target in draft.get('escalation_targets') or []:
        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        target_tool_key = str(target.get('target_tool_key') or '')

        if _is_integrated_operations_tool(
            draft=draft,
            tool_key=target_tool_key,
        ):
            return target_tool_key

    catalogs = draft.get('_catalogs') or {}

    for tool_key in catalogs.get('integrated_operations_tool_keys') or ():
        return str(tool_key or '')

    return ''


def _is_integrated_operations_tool(
    *,
    draft: dict[str, Any],
    tool_key: str,
) -> bool:
    catalogs = draft.get('_catalogs') or {}
    tool_tier_by_key = catalogs.get('tool_tier_by_key') or {}

    return (
        str(tool_tier_by_key.get(tool_key) or '')
        == AlarmToolTier.INTEGRATED_OPERATIONS.value
    )


def _filter_subcomponent_options(
    *,
    catalogs: dict[str, Any],
    selected_component_keys: list[str],
) -> list[dict[str, str]]:
    if not selected_component_keys:
        return []

    selected_component_key_set = set(selected_component_keys)
    subcomponent_parent_by_key = catalogs.get('subcomponent_parent_by_key') or {}
    subcomponent_options = catalogs.get('subcomponent_options') or []

    filtered_options: list[dict[str, str]] = []

    for option in subcomponent_options:
        if not isinstance(option, dict):
            continue

        subcomponent_key = str(option.get('value') or '')
        parent_component_key = str(
            subcomponent_parent_by_key.get(subcomponent_key) or '',
        )

        if parent_component_key not in selected_component_key_set:
            continue

        filtered_options.append(option)

    return filtered_options


def _prune_target_subcomponents(
    *,
    target: dict[str, Any],
    allowed_subcomponent_options: list[dict[str, str]],
) -> dict[str, Any]:
    allowed_subcomponent_keys = {
        str(option.get('value') or '')
        for option in allowed_subcomponent_options
        if isinstance(option, dict)
    }

    prepared = dict(target)
    prepared['affected_subcomponent_keys'] = [
        subcomponent_key
        for subcomponent_key in _ensure_list(
            value=target.get('affected_subcomponent_keys'),
        )
        if subcomponent_key in allowed_subcomponent_keys
    ]

    return prepared


def _ensure_list(
    *,
    value: Any,
) -> list[str]:
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item or '').strip()
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(';')
            if item.strip()
        ]

    return []