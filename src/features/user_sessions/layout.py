from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from .components import (
    build_initial_state,
    build_user_session_analytics_toolbar,
    build_user_session_user_table_shell,
    build_user_session_analytics_footer
)
from .components.toolbar import build_refresh_button_content
from .graphs import build_empty_weekly_comparison_figure
from .ids import UserSessionAnalyticsPageIds
from ...shared.ui.app_header_shell.app_header_analytics_shell import build_app_header_analytics_shell


def build_user_session_analytics_layout() -> html.Div:
    return html.Div(
        id=UserSessionAnalyticsPageIds.ROOT,
        className='user-session-analytics-root',
        children=[
            dcc.Interval(
                id=UserSessionAnalyticsPageIds.INIT_TRIGGER,
                interval=250,
                n_intervals=0,
                max_intervals=1,
            ),
            dcc.Store(
                id=UserSessionAnalyticsPageIds.SNAPSHOT_STORE,
                storage_type='memory',
            ),
            dcc.Store(
                id=UserSessionAnalyticsPageIds.USERS_PAGE_STORE,
                data=1,
                storage_type='memory',
            ),
            build_app_header_analytics_shell(title='Uso del dashboard principal'),
            html.Main(
                className='user-session-analytics-page-main',
                children=[
                    _build_information(),
                    build_user_session_analytics_toolbar(),
                    dcc.Loading(
                        id=UserSessionAnalyticsPageIds.MAIN_LOADER,
                        type='default',
                        delay_show=0,
                        show_initially=True,
                        display='show',
                        className='loading-component-spinner',
                        parent_className='user-session-analytics-loader',
                        children=[
                            _build_content_shell(),
                        ],
                    ),
                    build_user_session_analytics_footer()
                ],
            ),
        ],
    )


def _build_information() -> html.Div:
    return html.Div(
        className='user-session-analytics-page-header',
        children=[
            html.Div(
                className='user-session-analytics-page-title-block',
                children=[
                    html.H4(
                        className='user-session-analytics-title',
                        children=['Uso del dashboard principal'],
                    ),
                    html.Div(
                        className='user-session-analytics-description',
                        children=['Resumen de actividad y uso comparado entre semana actual y semana anterior.'],
                    ),
                    html.Div(
                        className='user-session-analytics-window-note',
                        children=[
                            html.I(className='bi bi-calendar-week'),
                            html.Span(
                                children=['Datos de los últimos 14 días · semana anterior + semana actual.']
                            ),
                        ],
                    ),
                    html.Div(
                        className='user-session-analytics-updated-wrapper',
                        children=[
                            html.I(className='bi bi-clock'),
                            html.Span(
                                id=UserSessionAnalyticsPageIds.LAST_UPDATED_TEXT,
                                children='Sin actualización',
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='user-session-analytics-header-actions',
                children=[
                    dbc.Button(
                        id=UserSessionAnalyticsPageIds.REFRESH_BUTTON,
                        color='dark',
                        size='md',
                        outline=True,
                        className='user-session-analytics-refresh-button',
                        n_clicks=0,
                        children=build_refresh_button_content()
                    ),
                ],
            ),
        ],
    )


def _build_content_shell() -> html.Div:
    return html.Div(
        className='user-session-analytics-content-shell',
        children=[
            html.Div(
                className='user-session-analytics-main-column flex-fill h-100',
                children=[
                    html.Div(
                        id=UserSessionAnalyticsPageIds.KPI_CONTAINER,
                        className='user-session-analytics-kpi-grid',
                        children=[build_initial_state('Esperando métricas de uso.')],
                    ),
                    dbc.Card(
                        className='user-session-analytics-chart-card',
                        children=[
                            dbc.CardHeader(
                                className='user-session-analytics-panel-header',
                                children=[
                                    html.Div(
                                        className='user-session-analytics-panel-title-wrapper',
                                        children=[
                                            html.I(
                                                className='bi bi-graph-up-arrow user-session-analytics-panel-icon'
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        className='user-session-analytics-panel-title',
                                                        children=['Comparación semanal de sesiones y usuarios'],
                                                    ),
                                                    html.Div(
                                                        className='user-session-analytics-panel-subtitle',
                                                        children=['Semana anterior versus avance de semana actual.'],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            dcc.Graph(
                                id=UserSessionAnalyticsPageIds.WEEKLY_CHART,
                                className='user-session-analytics-weekly-chart',
                                config={
                                    'displayModeBar': False,
                                    'responsive': True,
                                },
                                figure=build_empty_weekly_comparison_figure(
                                    message='Esperando datos de tendencia.',
                                ),
                            ),
                        ],
                    ),
                    build_user_session_user_table_shell(),
                ],
            ),
            html.Div(
                className='user-session-analytics-side-column flex-fill h-100',
                children=[
                    dbc.Card(
                        className='user-session-analytics-context-card h-100',
                        children=[
                            dbc.CardHeader(
                                className='user-session-analytics-panel-header',
                                children=[
                                    html.Div(
                                        className='user-session-analytics-panel-title-wrapper',
                                        children=[
                                            html.I(
                                                className='bi bi-clipboard-data user-session-analytics-panel-icon'
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        'Resumen comparativo',
                                                        className='user-session-analytics-panel-title',
                                                    ),
                                                    html.Div(
                                                        'Hallazgos principales según filtros aplicados.',
                                                        className='user-session-analytics-panel-subtitle',
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Div(
                                id=UserSessionAnalyticsPageIds.SUMMARY_CONTAINER,
                                className='user-session-analytics-summary-list',
                                children=[build_initial_state('Esperando resumen.')],
                            ),
                        ],
                    ),
                    dbc.Card(
                        className='user-session-analytics-device-card h-100',
                        children=[
                            dbc.CardHeader(
                                className='user-session-analytics-panel-header',
                                children=[
                                    html.Div(
                                        className='user-session-analytics-panel-title-wrapper',
                                        children=[
                                            html.I(
                                                className='bi bi-display user-session-analytics-panel-icon'
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        'Dispositivos y resoluciones',
                                                        className='user-session-analytics-panel-title',
                                                    ),
                                                    html.Div(
                                                        'Distribución de uso del dashboard.',
                                                        className='user-session-analytics-panel-subtitle',
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Div(
                                id=UserSessionAnalyticsPageIds.DEVICE_RESOLUTION_CONTAINER,
                                className='user-session-analytics-device-resolution',
                                children=[build_initial_state('Esperando dispositivos.')],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )