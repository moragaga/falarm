from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from src.features.configuration.alarm.options import (
    AlarmCriticality,
    AlarmToolTier,
    AlarmVisibilityMode,
)

from .ids import AlarmRuleEscalationIds
from .target_card import build_escalation_target_card


def build_escalation_tab_layout(
    *,
    draft: dict[str, Any] | None,
):
    draft = draft or {}
    criticality_code = str(draft.get('criticality_code') or AlarmCriticality.C3.value)
    visibility_mode = str(draft.get('visibility_mode') or AlarmVisibilityMode.VISIBLE.value)
    origin_tool_key = str(draft.get('origin_tool_key') or '')

    targets = [
        target
        for target in draft.get('escalation_targets') or []
        if isinstance(target, dict)
    ]

    catalogs = draft.get('_catalogs') or {}

    if visibility_mode == AlarmVisibilityMode.TRACE_ONLY.value:
        return dbc.Alert(
            'La regla está en modo solo trazabilidad. Se procesa y genera historia, pero no escala ni se proyecta a herramientas.',
            color='secondary',
        )

    allow_add = (
        criticality_code == AlarmCriticality.C2.value
        and bool(origin_tool_key)
        and _has_available_escalation_target(
            draft=draft,
            targets=targets,
            catalogs=catalogs,
        )
    )

    return html.Div(
        children=[
            _build_criticality_help(
                draft=draft,
                criticality_code=criticality_code,
                catalogs=catalogs,
            ),
            html.Div(
                className='d-flex justify-content-between align-items-center mb-3',
                children=[
                    html.Div(
                        children=[
                            html.H5('Escalamiento', className='mb-1'),
                            html.Div(
                                className='text-muted small',
                                children=(
                                    'C1 usa visibilidad inmediata. C2 escala hacia herramientas superiores. '
                                    'C3 no escala.'
                                ),
                            ),
                        ],
                    ),
                    dbc.Button(
                        'Agregar destino',
                        id=AlarmRuleEscalationIds.ADD_TARGET_BUTTON,
                        color='success',
                        outline=True,
                        n_clicks=0,
                        disabled=not allow_add,
                        className='' if allow_add else 'd-none',
                    ),
                ],
            ),
            html.Div(
                id=AlarmRuleEscalationIds.TARGETS_CONTAINER,
                children=_build_target_cards(
                    draft=draft,
                    targets=targets,
                    catalogs=catalogs,
                ),
            ),
        ],
    )


def _build_target_cards(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
    catalogs: dict[str, Any],
):
    criticality_code = str(draft.get('criticality_code') or AlarmCriticality.C3.value)
    origin_tool_key = str(draft.get('origin_tool_key') or '')

    if not origin_tool_key:
        return [
            dbc.Alert(
                'Selecciona una herramienta inicial antes de configurar escalamiento.',
                color='secondary',
            )
        ]

    if criticality_code == AlarmCriticality.C1.value:
        return [
            dbc.Alert(
                'C1 no guarda destinos manuales. El runtime la proyecta inmediatamente a herramienta inicial, ADA Operaciones Integradas y ADA Estratégico.',
                color='danger',
            )
        ]

    if criticality_code == AlarmCriticality.C3.value:
        return [
            dbc.Alert(
                'C3 no escala. Permanece en su herramienta inicial según la regla.',
                color='info',
            )
        ]

    if not targets:
        return [
            dbc.Alert(
                'C2 requiere una cadena de escalamiento si existe un destino superior disponible.',
                color='secondary',
            )
        ]

    return [
        build_escalation_target_card(
            target=target,
            index=str(index),
            tool_options=_build_allowed_target_options(
                draft=draft,
                target_index=index,
                catalogs=catalogs,
            ),
        )
        for index, target in enumerate(targets)
    ]


def _build_criticality_help(
    *,
    draft: dict[str, Any],
    criticality_code: str,
    catalogs: dict[str, Any],
):
    origin_tool_key = str(draft.get('origin_tool_key') or '')

    if not origin_tool_key:
        return dbc.Alert(
            'Primero selecciona herramienta inicial. Sin ella no se puede calcular la cadena de escalamiento.',
            color='secondary',
            className='mb-3',
        )

    if criticality_code == AlarmCriticality.C1.value:
        integrated_count = len(catalogs.get('integrated_operations_tool_keys') or ())
        strategic_count = len(catalogs.get('strategic_tool_keys') or ())

        return dbc.Alert(
            (
                'C1: visibilidad inmediata en herramienta inicial, ADA Operaciones Integradas '
                f'({integrated_count}) y ADA Estratégico ({strategic_count}).'
            ),
            color='danger',
            className='mb-3',
        )

    if criticality_code == AlarmCriticality.C2.value:
        return dbc.Alert(
            (
                'C2: escala hacia herramientas superiores. Desde ADA Proceso puede ir a '
                'ADA Operaciones Integradas o directo a ADA Estratégico. Desde ADA Operaciones '
                'Integradas solo puede ir a ADA Estratégico.'
            ),
            color='warning',
            className='mb-3',
        )

    return dbc.Alert(
        'C3: sin escalamiento.',
        color='info',
        className='mb-3',
    )


def _has_available_escalation_target(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
    catalogs: dict[str, Any],
) -> bool:
    current_tool_key = _resolve_current_tool_key(
        draft=draft,
        targets=targets,
    )

    if not current_tool_key:
        return False

    existing_tools = {
        str(target.get('target_tool_key') or '')
        for target in targets
        if isinstance(target, dict)
    }

    for tool in catalogs.get('tools') or []:
        if not isinstance(tool, dict):
            continue

        target_tool_key = str(tool.get('tool_key') or '')

        if not target_tool_key:
            continue

        if target_tool_key in existing_tools:
            continue

        if _is_allowed_next_escalation_target(
            catalogs=catalogs,
            current_tool_key=current_tool_key,
            target_tool_key=target_tool_key,
        ):
            return True

    return False


def _build_allowed_target_options(
    *,
    draft: dict[str, Any],
    target_index: int,
    catalogs: dict[str, Any],
) -> list[dict[str, str]]:
    tools = [
        tool
        for tool in catalogs.get('tools') or []
        if isinstance(tool, dict)
    ]

    current_tool_key = _resolve_current_tool_key_until_index(
        draft=draft,
        target_index=target_index,
    )

    existing_tools = {
        str(target.get('target_tool_key') or '')
        for index, target in enumerate(draft.get('escalation_targets') or [])
        if index != target_index and isinstance(target, dict)
    }

    options: list[dict[str, str]] = []

    for tool in sorted(tools, key=lambda item: int(item.get('display_order') or 0)):
        target_tool_key = str(tool.get('tool_key') or '')

        if not target_tool_key:
            continue

        if target_tool_key in existing_tools:
            continue

        if _is_allowed_next_escalation_target(
            catalogs=catalogs,
            current_tool_key=current_tool_key,
            target_tool_key=target_tool_key,
        ):
            options.append(
                {
                    'label': str(tool.get('tool_name') or target_tool_key),
                    'value': target_tool_key,
                }
            )

    return options


def _resolve_current_tool_key(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
) -> str:
    current_tool_key = str(draft.get('origin_tool_key') or '')

    for target in sorted(targets, key=lambda item: int(item.get('step_order') or 0)):
        if not bool(target.get('is_enabled', True)):
            continue

        target_tool_key = str(target.get('target_tool_key') or '')

        if target_tool_key:
            current_tool_key = target_tool_key

    return current_tool_key


def _resolve_current_tool_key_until_index(
    *,
    draft: dict[str, Any],
    target_index: int,
) -> str:
    current_tool_key = str(draft.get('origin_tool_key') or '')

    for index, target in enumerate(draft.get('escalation_targets') or []):
        if index >= target_index:
            break

        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        target_tool_key = str(target.get('target_tool_key') or '')

        if target_tool_key:
            current_tool_key = target_tool_key

    return current_tool_key


def _is_allowed_next_escalation_target(
    *,
    catalogs: dict[str, Any],
    current_tool_key: str,
    target_tool_key: str,
) -> bool:
    if not current_tool_key or not target_tool_key:
        return False

    if current_tool_key == target_tool_key:
        return False

    current_tier = _tool_tier_for_key(
        catalogs=catalogs,
        tool_key=current_tool_key,
    )
    target_tier = _tool_tier_for_key(
        catalogs=catalogs,
        tool_key=target_tool_key,
    )

    if current_tier == AlarmToolTier.PROCESS.value:
        return target_tier in {
            AlarmToolTier.INTEGRATED_OPERATIONS.value,
            AlarmToolTier.STRATEGIC.value,
        }

    if current_tier == AlarmToolTier.INTEGRATED_OPERATIONS.value:
        return target_tier == AlarmToolTier.STRATEGIC.value

    return False


def _tool_tier_for_key(
    *,
    catalogs: dict[str, Any],
    tool_key: str,
) -> str:
    tool_tier_by_key = catalogs.get('tool_tier_by_key') or {}
    return str(tool_tier_by_key.get(tool_key) or '')