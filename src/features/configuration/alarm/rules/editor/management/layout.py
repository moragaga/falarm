from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .ids import AlarmRuleManagementIds


def build_management_tab_layout(
    *,
    draft: dict[str, Any] | None,
):
    draft = draft or {}

    return html.Div(
        children=[
            dbc.Alert(
                color='info',
                className='mb-3',
                children=(
                    'La gestión aceptada oculta la ocurrencia gestionada como '
                    'comportamiento base del motor. Esta opción no se configura '
                    'por regla.'
                ),
            ),
            dbc.Alert(
                color='secondary',
                className='mb-3',
                children=(
                    'Si la condición sigue activa después del tiempo configurado, '
                    'el core recalcula prioridad, escalamiento y visibilidad según '
                    'la configuración base de la regla.'
                ),
            ),
            dbc.Row(
                className='g-3',
                children=[
                    dbc.Col(
                        md=6,
                        children=[
                            _checkbox(
                                label='Reaparece si sigue activa',
                                component_id=(
                                    AlarmRuleManagementIds
                                    .REAPPEAR_IF_STILL_ACTIVE_ENABLED
                                ),
                                value=draft.get(
                                    'reappear_if_still_active_enabled',
                                    True,
                                ),
                            ),
                            _number(
                                label='Reaparecer después de gestión (minutos)',
                                component_id=(
                                    AlarmRuleManagementIds
                                    .REAPPEAR_AFTER_MANAGEMENT_MINUTES
                                ),
                                value=(
                                    draft.get('reappear_after_management_minutes')
                                    or 60
                                ),
                            ),
                        ],
                    ),
                    dbc.Col(
                        md=6,
                        children=[
                            _checkbox(
                                label='Usar reglas del mensaje si existen',
                                component_id=(
                                    AlarmRuleManagementIds
                                    .USE_MESSAGE_MANAGEMENT_OVERRIDE
                                ),
                                value=draft.get(
                                    'use_message_management_override',
                                    True,
                                ),
                                help_text=(
                                    'Cuando exista un mensaje global con override, '
                                    'sus tiempos pueden pisar la configuración de '
                                    'reaparición de la regla.'
                                ),
                            ),
                            html.Div(
                                className='text-muted small mt-2',
                                children=(
                                    'C1 usa visibilidad inmediata, C2 usa '
                                    'escalamiento progresivo y C3 permanece en su '
                                    'herramienta principal.'
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _checkbox(
    *,
    label: str,
    component_id: str,
    value,
    help_text: str | None = None,
):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Checkbox(id=component_id, label=label, value=bool(value)),
            html.Div(help_text, className='text-muted small mt-1') if help_text else None,
        ],
    )


def _number(
    *,
    label: str,
    component_id: str,
    value,
):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Input(id=component_id, value=value, type='number', min=0),
        ],
    )