from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from .grid import build_alarm_rules_list_grid
from .ids import AlarmRulesListIds


def build_alarm_rules_list_layout(*, selected_family: str | None = None):
    return html.Div(
        className='p-3',
        children=[
            dcc.Interval(
                id=AlarmRulesListIds.INIT,
                n_intervals=0,
                max_intervals=1,
                interval=250,
            ),
            dbc.Card(
                className='mb-3',
                children=[
                    dbc.CardBody(
                        children=[
                            html.Div(
                                className='d-flex justify-content-between align-items-start gap-3 flex-wrap mb-3',
                                children=[
                                    html.Div(
                                        children=[
                                            html.H5('Reglas por familia', className='mb-1'),
                                            html.Div(
                                                className='text-muted small',
                                                children=(
                                                    'La familia solo filtra reglas. La configuración completa vive '
                                                    'en el editor guiado de cada regla.'
                                                ),
                                            ),
                                        ],
                                    ),
                                    dbc.ButtonGroup(
                                        children=[
                                            dbc.Button(
                                                'Recargar',
                                                id=AlarmRulesListIds.REFRESH_BUTTON,
                                                color='secondary',
                                                outline=True,
                                                n_clicks=0,
                                            ),
                                            dbc.Button(
                                                'Nueva regla',
                                                id=AlarmRulesListIds.NEW_BUTTON,
                                                color='success',
                                                outline=True,
                                                n_clicks=0,
                                            ),
                                            dbc.Button(
                                                'Editar regla',
                                                id=AlarmRulesListIds.EDIT_BUTTON,
                                                color='dark',
                                                outline=True,
                                                n_clicks=0,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            dbc.Row(
                                className='g-3',
                                children=[
                                    dbc.Col(
                                        md=5,
                                        children=[
                                            dbc.Label('Familia'),
                                            dcc.Dropdown(
                                                id=AlarmRulesListIds.FAMILY_SELECT,
                                                value=selected_family,
                                                clearable=True,
                                                placeholder='Todas las familias',
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            dcc.Loading(
                                id=AlarmRulesListIds.LOADING,
                                type='default',
                                children=build_alarm_rules_list_grid(),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
