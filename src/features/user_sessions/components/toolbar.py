from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component

from ..constants import (
    DEFAULT_DEVICE_FILTER,
    DEFAULT_DEVICE_OPTIONS,
    DEFAULT_PROFILE_FILTER,
    DEFAULT_RESOLUTION_FILTER,
    DEFAULT_RESOLUTION_OPTIONS,
    DEFAULT_SORT_ORDER,
    EXCLUDE_ADMIN_VALUE,
    PROFILE_OPTIONS,
    SORT_OPTIONS,
)
from ..ids import UserSessionAnalyticsPageIds


def build_user_session_analytics_toolbar() -> html.Div:
    return html.Div(
        className='user-session-analytics-toolbar',
        children=[
            _build_profile_filter(),
            _build_device_filter(),
            _build_resolution_filter(),
            _build_exclude_admin_switch(),
            _build_search_control(),
            _build_sort_control(),
        ],
    )


def _build_profile_filter() -> html.Div:
    return html.Div(
        className='user-session-analytics-control',
        children=[
            html.Label(
                htmlFor=UserSessionAnalyticsPageIds.PROFILE_SELECT,
                className='user-session-analytics-control-label',
                children=['Perfil'],
            ),
            dbc.Select(
                id=UserSessionAnalyticsPageIds.PROFILE_SELECT,
                size='sm',
                value=DEFAULT_PROFILE_FILTER,
                options=PROFILE_OPTIONS,
                placeholder='Seleccionar perfil',
                className='user-session-analytics-select',
            ),
        ],
    )


def _build_device_filter() -> html.Div:
    return html.Div(
        className='user-session-analytics-control',
        children=[
            html.Label(
                htmlFor=UserSessionAnalyticsPageIds.DEVICE_SELECT,
                className='user-session-analytics-control-label',
                children=['Dispositivo'],
            ),
            dbc.Select(
                id=UserSessionAnalyticsPageIds.DEVICE_SELECT,
                size='sm',
                value=DEFAULT_DEVICE_FILTER,
                options=DEFAULT_DEVICE_OPTIONS,
                placeholder='Seleccionar dispositivo',
                className='user-session-analytics-select',
            ),
        ],
    )


def _build_resolution_filter() -> html.Div:
    return html.Div(
        className='user-session-analytics-control',
        children=[
            html.Label(
                htmlFor=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
                className='user-session-analytics-control-label',
                children=['Resolución'],
            ),
            dbc.Select(
                id=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
                size='sm',
                value=DEFAULT_RESOLUTION_FILTER,
                options=DEFAULT_RESOLUTION_OPTIONS,
                placeholder='Seleccionar resolución',
                className='user-session-analytics-select',
            ),
        ],
    )


def _build_exclude_admin_switch() -> html.Div:
    return html.Div(
        className='user-session-analytics-control user-session-analytics-switch-control',
        children=[
            html.Label(
                className='user-session-analytics-control-label',
                children=['Administrador'],
            ),
            dbc.Checklist(
                id=UserSessionAnalyticsPageIds.EXCLUDE_ADMIN_SWITCH,
                options=[
                    {
                        'label': 'Excluir administrador',
                        'value': EXCLUDE_ADMIN_VALUE,
                    },
                ],
                value=[EXCLUDE_ADMIN_VALUE],
                switch=True,
                className='user-session-analytics-switch',
            ),
        ],
    )


def _build_search_control() -> html.Div:
    return html.Div(
        className='user-session-analytics-control user-session-analytics-search-control',
        children=[
            html.Label(
                htmlFor=UserSessionAnalyticsPageIds.SEARCH_INPUT,
                children=['Buscar usuario'],
                className='user-session-analytics-control-label',
            ),
            dbc.InputGroup(
                size='sm',
                className='user-session-analytics-search',
                children=[
                    dbc.InputGroupText(html.I(className='bi bi-search')),
                    dbc.Input(
                        id=UserSessionAnalyticsPageIds.SEARCH_INPUT,
                        type='text',
                        debounce=False,
                        placeholder='Buscar por nombre o correo...',
                    ),
                ],
            ),
        ],
    )


def _build_sort_control() -> html.Div:
    return html.Div(
        className='user-session-analytics-control',
        children=[
            html.Label(
                htmlFor=UserSessionAnalyticsPageIds.SORT_SELECT,
                className='user-session-analytics-control-label',
                children=['Ordenar por'],
            ),
            dbc.Select(
                id=UserSessionAnalyticsPageIds.SORT_SELECT,
                size='sm',
                value=DEFAULT_SORT_ORDER,
                options=SORT_OPTIONS,
                placeholder='Seleccionar orden',
                className='user-session-analytics-select',
            ),
        ],
    )

def build_refresh_button_content() -> list[Component]:
    return [
        html.I(className='bi bi-arrow-clockwise me-2'),
        html.Span(children=['Actualizar']),
    ]