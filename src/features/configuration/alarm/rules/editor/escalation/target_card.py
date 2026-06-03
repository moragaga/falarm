from __future__ import annotations

from typing import Any
from uuid import uuid4

import dash_bootstrap_components as dbc
from dash import dcc, html

from .ids import AlarmRuleEscalationIds


def build_escalation_target_card(
    *,
    target: dict[str, Any],
    index: str | None = None,
    tool_options: list[dict[str, str]] | None = None,
):
    item_key = index or str(target.get('target_tool_key') or uuid4().hex[:8])
    is_enabled = bool(target.get('is_enabled', True))
    disabled = not is_enabled

    return dbc.Card(
        className='mb-3',
        children=[
            dbc.CardBody(
                children=[
                    dbc.Row(
                        className='g-3 align-items-end',
                        children=[
                            dbc.Col(
                                md=2,
                                children=[
                                    dbc.Label('Orden'),
                                    dbc.Input(
                                        id={
                                            'type': AlarmRuleEscalationIds.TARGET_ORDER_TYPE,
                                            'index': item_key,
                                        },
                                        value=target.get('step_order'),
                                        type='number',
                                        min=1,
                                        disabled=disabled,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                md=4,
                                children=[
                                    dbc.Label('Herramienta destino'),
                                    dcc.Dropdown(
                                        id={
                                            'type': AlarmRuleEscalationIds.TARGET_TOOL_TYPE,
                                            'index': item_key,
                                        },
                                        options=tool_options or [],
                                        value=target.get('target_tool_key') or None,
                                        placeholder='Selecciona destino',
                                        disabled=disabled,
                                        clearable=False,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                md=3,
                                children=[
                                    dbc.Label('Minutos desde etapa anterior'),
                                    dbc.Input(
                                        id={
                                            'type': AlarmRuleEscalationIds.TARGET_MINUTES_TYPE,
                                            'index': item_key,
                                        },
                                        value=target.get('wait_minutes_from_previous_step'),
                                        type='number',
                                        min=0,
                                        disabled=disabled,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                md=2,
                                children=[
                                    dbc.Checkbox(
                                        id={
                                            'type': AlarmRuleEscalationIds.TARGET_ENABLED_TYPE,
                                            'index': item_key,
                                        },
                                        label='Destino activo',
                                        value=is_enabled,
                                    ),
                                    html.Div(
                                        '0 minutos significa inmediato. Desactivado significa que no escala a ese destino.',
                                        className='text-muted small mt-2',
                                    ),
                                ],
                            ),
                            dbc.Col(
                                md=1,
                                className='text-end',
                                children=[
                                    dbc.Button(
                                        'Quitar',
                                        id={
                                            'type': AlarmRuleEscalationIds.TARGET_REMOVE_TYPE,
                                            'index': item_key,
                                        },
                                        color='danger',
                                        outline=True,
                                        n_clicks=0,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )