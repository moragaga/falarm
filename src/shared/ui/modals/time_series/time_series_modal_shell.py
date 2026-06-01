"""
Module for building the structure and components of a time series modal.

This module contains functions to create a modal using Dash and Dash Bootstrap
Components, designed for displaying operational indicators in real-time. It
includes the layout and various subcomponents, such as headers, body content,
filters, and graph areas.

Functions
---------
build_time_series_modal_shell :
    Creates the main modal structure, including header, body, and footer.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import Component

from .definitions import MODAL_VARIANTS
from .ids import TimeSeriesModalIds


def build_time_series_modal_shell():
    return dbc.Modal(
        id=TimeSeriesModalIds.MODAL,
        is_open=False,
        className='time-series-modal',
        backdrop=MODAL_VARIANTS.backdrop,
        centered=MODAL_VARIANTS.centered,
        keyboard=MODAL_VARIANTS.keyboard,
        style={'--bs-modal-width': MODAL_VARIANTS.width},
        children=[_header(), _body(), _footer()],
    )


def _header():
    return dbc.ModalHeader(
        className='p-2 {0}'.format(MODAL_VARIANTS.header_class_name),
        close_button=MODAL_VARIANTS.close_button,
        children=[
            html.Div(
                className='d-flex justify-content-between align-items-center w-100',
                children=[
                    html.Div(
                        className='d-flex align-items-center',
                        children=[
                            html.P(
                                className='ps-3 text-start {0} {1}'.format(
                                    MODAL_VARIANTS.header_font_color_class_name,
                                    MODAL_VARIANTS.font_size_class_name,
                                ),
                                children=['Indicadores operacionales:'],
                            ),
                            html.P(
                                id=TimeSeriesModalIds.TITLE,
                                className='fw-bold ps-1 {0} {1}'.format(
                                    MODAL_VARIANTS.header_font_color_class_name,
                                    MODAL_VARIANTS.font_size_class_name,
                                ),
                            ),
                        ],
                    ),
                    html.I(
                        id=TimeSeriesModalIds.CLOSE,
                        className='bi bi-x-lg pe-3 active-cursor {0}'.format(
                            MODAL_VARIANTS.header_font_color_class_name
                        ),
                        n_clicks=0,
                    ),
                ],
            )
        ],
    )


def _body():
    return dbc.ModalBody(
        className='p-2 {0}'.format(MODAL_VARIANTS.body_class_name),
        children=[
            dbc.Container(
                className='time-series-modal-graph-container',
                fluid=True,
                children=[
                    _information(),
                    _filter_turn(),
                    _graph_content(),
                ],
            )
        ],
    )


def _information() -> html.Div:
    return html.Div(
        className='time-series-modal-title-wrapper',
        children=[
            html.P(
                className='fst-italic fw-semibold {0} {1}'.format(
                    MODAL_VARIANTS.body_font_color_class_name, MODAL_VARIANTS.font_size_class_name
                ),
                children=['Evolución en tiempo real'],
            ),
            dbc.Button(
                id=TimeSeriesModalIds.REFRESH_BUTTON,
                className='app-running-button-host time-series-modal-refresh-button',
                color='dark',
                children=['Actualizar'],
            ),
        ],
    )


def _filter_turn() -> html.Div:
    return html.Div(
        className='d-flex justify-content-center align-items-center',
        children=[
            html.Div(
                className='time-series-modal-control',
                children=[
                    html.Label(
                        htmlFor=TimeSeriesModalIds.FILTER_SELECT_TURN_SCOPE,
                        className='time-series-modal-control-label',
                        children=['Turno'],
                    ),
                    dbc.Select(
                        id=TimeSeriesModalIds.FILTER_SELECT_TURN_SCOPE,
                        className='time-series-modal-control-filter',
                        placeholder='Filtrar por turno',
                        size='sm',
                        value='current',
                        options=[
                            {
                                'label': 'Actual',
                                'value': 'current',
                            },
                            {
                                'label': 'Anterior',
                                'value': 'previous',
                            },
                            {
                                'label': 'Ambos',
                                'value': 'all',
                            },
                        ],
                    ),
                ],
            ),
        ],
    )


def _graph_content() -> Component:
    return dcc.Loading(
        id=TimeSeriesModalIds.GRAPH_LOADING,
        type='default',
        display='auto',
        delay_show=150,
        delay_hide=150,
        target_components={
            TimeSeriesModalIds.GRAPH: 'children',
        },
        parent_className='time-series-modal-loading-parent',
        className='time-series-modal-loading loading-component-spinner',
        overlay_style={
            'visibility': 'visible',
        },
        children=[
            html.Div(
                className='time-series-modal-graph p-3',
                id=TimeSeriesModalIds.GRAPH,
            ),
        ],
    )


def _footer():
    return dbc.ModalFooter(
        className='p-1 {0}'.format(MODAL_VARIANTS.footer_class_name),
        children=[
            html.Div(
                className='d-flex justify-content-start align-items-center w-100',
                children=[
                    html.P(
                        className='ps-3 {0} {1}'.format(
                            MODAL_VARIANTS.footer_font_color_class_name,
                            MODAL_VARIANTS.font_size_class_name,
                        ),
                        children=['Última actualización:'],
                    ),
                    html.P(
                        className='fw-bold ps-1 {0} {1}'.format(
                            MODAL_VARIANTS.footer_font_color_class_name,
                            MODAL_VARIANTS.font_size_class_name,
                        ),
                        id=TimeSeriesModalIds.LAST_UPDATE,
                    ),
                ],
            )
        ],
    )
