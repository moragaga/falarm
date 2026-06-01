from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .ids import AlarmRuleManagementIds


def build_management_tab_layout(*, draft: dict[str, Any] | None):
    draft = draft or {}

    return html.Div(
        children=[
            dbc.Alert(
                color='info',
                className='mb-3',
                children=(
                    'La gestión oculta la alarma de todas las herramientas. Si la condición sigue activa '
                    'después del tiempo configurado, el motor la vuelve a mostrar y recalcula dónde debe '
                    'verse según su riesgo, cascadas activas y escalamiento. No se configura una herramienta fija '
                    'de reaparición.'
                ),
            ),
            dbc.Alert(
                color='secondary',
                className='mb-3',
                children=(
                    'Importante: el motor debe usar relojes por ocurrencia, gestión y scope operativo. '
                    'No se debe usar un único reloj global para toda la regla.'
                ),
            ),
            dbc.Row(
                className='g-3',
                children=[
                    dbc.Col(
                        md=6,
                        children=[
                            _checkbox(
                                'Ocultar de todas las herramientas al gestionar',
                                AlarmRuleManagementIds.HIDE_ALL_TOOLS_WHEN_MANAGED,
                                draft.get('hide_all_tools_when_managed', True),
                            ),
                            _checkbox(
                                'Reaparece si sigue activa',
                                AlarmRuleManagementIds.REAPPEAR_IF_STILL_ACTIVE_ENABLED,
                                draft.get('reappear_if_still_active_enabled', True),
                            ),
                            _number(
                                'Reaparecer después de gestión (minutos)',
                                AlarmRuleManagementIds.REAPPEAR_AFTER_MANAGEMENT_MINUTES,
                                draft.get('reappear_after_management_minutes') or 60,
                            ),
                        ],
                    ),
                    dbc.Col(
                        md=6,
                        children=[
                            _checkbox(
                                'Usar reglas del mensaje si existen',
                                AlarmRuleManagementIds.USE_MESSAGE_MANAGEMENT_OVERRIDE,
                                draft.get('use_message_management_override', True),
                                help_text=(
                                    'Cuando exista un mensaje global con override, sus tiempos pueden pisar '
                                    'la configuración de reaparición de la regla.'
                                ),
                            ),
                            html.Div(
                                className='text-muted small mt-2',
                                children=(
                                    'Si una alarma gestionada no normaliza, reaparece en el flujo que corresponda: '
                                    'base, Nivel 0 inmediato para riesgo 1, destinos progresivos para riesgo 2, '
                                    'o solo su herramienta inicial para riesgo 3.'
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _checkbox(label: str, component_id: str, value, help_text: str | None = None):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Checkbox(id=component_id, label=label, value=bool(value)),
            html.Div(help_text, className='text-muted small mt-1') if help_text else None,
        ],
    )


def _number(label: str, component_id: str, value):
    return html.Div(
        className='mb-3',
        children=[dbc.Label(label), dbc.Input(id=component_id, value=value, type='number', min=0)],
    )
