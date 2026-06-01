from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from .ids import AlarmRuleVisualizationIds


def build_visual_target_card(
    *,
    target: dict[str, Any],
    index: str = 'nivel_0',
    component_options: list[dict[str, str]] | None = None,
    subcomponent_options: list[dict[str, str]] | None = None,
):
    return dbc.Card(
        className='mb-3',
        children=[
            dbc.CardHeader('Nivel 0'),
            dbc.CardBody(
                children=[
                    dbc.Row(
                        className='g-3',
                        children=[
                            dbc.Col(
                                md=6,
                                children=[
                                    dbc.Label('Componentes Nivel 0 afectados'),
                                    dcc.Dropdown(
                                        id={
                                            'type': AlarmRuleVisualizationIds.AFFECTED_COMPONENTS_TYPE,
                                            'index': index,
                                        },
                                        value=target.get('affected_component_keys') or [],
                                        options=component_options or [],
                                        multi=True,
                                        placeholder='Selecciona componentes padre',
                                    ),
                                    html.Div(
                                        'La posición principal y posiciones adicionales se toman desde la configuración del componente padre.',
                                        className='text-muted small mt-1',
                                    ),
                                ],
                            ),
                            dbc.Col(
                                md=6,
                                children=[
                                    dbc.Label('Subcomponentes Nivel 0 afectados / resaltados'),
                                    dcc.Dropdown(
                                        id={
                                            'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE,
                                            'index': index,
                                        },
                                        value=target.get('affected_subcomponent_keys') or [],
                                        options=subcomponent_options or [],
                                        multi=True,
                                        placeholder='Selecciona subcomponentes',
                                    ),
                                    html.Div(
                                        'Los subcomponentes seleccionados serán los elementos resaltados por el front.',
                                        className='text-muted small mt-1',
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ],
    )
