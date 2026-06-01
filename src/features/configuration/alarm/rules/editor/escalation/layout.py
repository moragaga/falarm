from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .ids import AlarmRuleEscalationIds
from .target_card import build_escalation_target_card


def build_escalation_tab_layout(*, draft: dict[str, Any] | None):
    draft = draft or {}
    risk_level = str(draft.get('risk_level') or '3')
    targets = draft.get('escalation_targets') or []
    catalogs = draft.get('_catalogs') or {}
    tool_options = catalogs.get('tool_options') or []

    allow_add = risk_level == '2'

    return html.Div(
        children=[
            _build_risk_help(risk_level=risk_level),
            html.Div(
                className='d-flex justify-content-between align-items-center mb-3',
                children=[
                    html.Div(
                        children=[
                            html.H5('Escalamiento lineal', className='mb-1'),
                            html.Div(
                                className='text-muted small',
                                children=(
                                    'La herramienta inicial se muestra desde el inicio. Cada destino agregado '
                                    'se suma después de los minutos indicados desde la etapa anterior.'
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
                    targets=targets,
                    tool_options=tool_options,
                    risk_level=risk_level,
                    catalogs=catalogs,
                ),
            ),
        ],
    )


def _build_target_cards(
    *,
    targets: list[Any],
    tool_options: list[dict[str, str]],
    risk_level: str,
    catalogs: dict[str, Any],
):
    prepared = [target for target in targets if isinstance(target, dict)]

    if risk_level == '3':
        return [
            dbc.Alert(
                'Riesgo 3 no escala. Solo reaparece en su flujo original si fue gestionada y no normaliza.',
                color='secondary',
            )
        ]

    if risk_level == '1':
        level_one_tool_key = str(catalogs.get('level_one_tool_key') or '').strip()
        level_one_tool_name = _resolve_tool_name(
            catalogs=catalogs,
            tool_key=level_one_tool_key,
        )
        if not level_one_tool_key:
            return [
                dbc.Alert(
                    'Riesgo 1 requiere una única herramienta activa con nivel 1. Configúrala en Herramientas antes de cerrar esta regla.',
                    color='danger',
                )
            ]

        n0_target = _resolve_level_one_target(
            targets=prepared,
            level_one_tool_key=level_one_tool_key,
        )
        return [
            dbc.Alert(
                f'Riesgo 1 agrega automáticamente {level_one_tool_name} de forma inmediata. No es necesario agregar destinos manuales.',
                color='danger',
            ),
            build_escalation_target_card(
                target=n0_target,
                index='risk-1-n0',
                tool_options=tool_options,
                read_only=True,
            ),
        ]

    if not prepared:
        return [
            dbc.Alert(
                'Aún no hay destinos. Presiona “Agregar destino” para crear la cadena: Ejecutivo, Nivel 0 u otro destino permitido.',
                color='secondary',
            )
        ]

    return [
        build_escalation_target_card(
            target=target,
            index=str(index),
            tool_options=tool_options,
        )
        for index, target in enumerate(prepared)
    ]


def _resolve_level_one_target(
    *,
    targets: list[dict[str, Any]],
    level_one_tool_key: str,
) -> dict[str, Any]:
    target_tool_key = level_one_tool_key or 'nivel_0'
    for target in targets:
        if str(target.get('target_tool_key') or '') == target_tool_key:
            prepared = dict(target)
            prepared['target_tool_key'] = target_tool_key
            prepared['step_order'] = 1
            prepared['is_enabled'] = True
            prepared['wait_minutes_from_previous_stage'] = 0
            return prepared

    return {
        'step_order': 1,
        'target_tool_key': target_tool_key,
        'is_enabled': True,
        'wait_minutes_from_previous_stage': 0,
    }


def _build_risk_help(*, risk_level: str):
    if risk_level == '1':
        return dbc.Alert(
            'Riesgo 1: aparece en su herramienta inicial y también en Nivel 0 inmediatamente. Si se gestiona y no normaliza, reaparece y vuelve a mostrarse en ambas según corresponda.',
            color='danger',
            className='mb-3',
        )

    if risk_level == '2':
        return dbc.Alert(
            'Riesgo 2: configura una cadena progresiva. Ejemplo: desde la base, después de 15 minutos se agrega Ejecutivo; después de 15 minutos más se agrega Nivel 0.',
            color='warning',
            className='mb-3',
        )

    return dbc.Alert(
        'Riesgo 3: no escala. Si se gestiona y no normaliza, puede reaparecer en su flujo original; si una alarma de mayor prioridad desaparece, el motor debe mostrar la siguiente activa del scope.',
        color='info',
        className='mb-3',
    )



def _resolve_tool_name(*, catalogs: dict[str, Any], tool_key: str) -> str:
    tool_name_by_key = catalogs.get('tool_name_by_key') or {}
    return str(tool_name_by_key.get(tool_key) or tool_key or 'herramienta de nivel 1')
