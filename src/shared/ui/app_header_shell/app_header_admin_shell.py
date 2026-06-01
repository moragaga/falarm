"""
Provides a function to build the app header for the admin shell, including logo, title, navigation buttons, and
popover-based information details.

This module is responsible for constructing a specific layout for the app's admin header, which incorporates
navigation-related components and additional informational popovers.

Functions
---------
build_app_header_admin_shell(title: str) -> html.Div
    Builds the admin shell header with a logo, title, navigation buttons, and contextual pop-over information.
"""

from __future__ import annotations

from uuid import uuid4

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import Component

from src.app.navigation.ids import AppNavigationIds
from src.app.navigation.offcanvas import build_app_navigation_offcanvas

from ..feedback.popover.popover import build_popover
from .primitives import build_button_action, build_logo


def build_app_header_admin_shell(title: str) -> html.Div:
    id_information = uuid4().__str__()
    return html.Div(
        className='app-header-admin-shell position-relative',
        children=[
            dbc.Container(
                fluid=True,
                className='app-header-admin-inner',
                children=[
                    dbc.Row(
                        className='g-0 align-items-stretch',
                        children=[
                            dbc.Col(
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                children=[build_logo(logo_src_name='app-web-admin')],
                            ),
                            dbc.Col(
                                className='header-admin-title-wrapper',
                                xs=12,
                                sm=10,
                                md=10,
                                lg=10,
                                xl=10,
                                xxl=10,
                                children=[
                                    html.Div(
                                        className='d-flex justify-content-center align-items-center h-100',
                                        children=[
                                            html.I(
                                                id=id_information,
                                                className='bi bi-info-square-fill header-admin-title pe-2 active-cursor',
                                            ),
                                            html.P(
                                                className='text-center header-admin-title',
                                                children=[title],
                                            ),
                                            _build_information(id_information=id_information),
                                        ],
                                    )
                                ],
                            ),
                            dbc.Col(xs=12, sm=1, md=1, lg=1, xl=1, xxl=1),
                            dbc.Col(
                                className='app-header-mobile-toggle',
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                children=[
                                    build_button_action(
                                        id_button=AppNavigationIds.HEADER_MOBILE_TOGGLE,
                                        icon_button='bi bi-list',
                                        class_name='dashboard-menu-btn-mobile',
                                        theme='light',
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
            build_button_action(
                id_button=AppNavigationIds.HEADER_DESKTOP_TOGGLE,
                icon_button='bi bi-chevron-left',
                class_name='dashboard-menu-btn-desktop d-none d-md-flex',
                theme='light',
            ),
            dcc.Location(
                id=AppNavigationIds.HEADER_LOCATION,
                refresh=False,
            ),
            build_app_navigation_offcanvas(),
        ],
    )


def _build_information(id_information: str) -> Component:
    custom_class_name = 'header-admin-information-text-secondary fst-italic fw-semibold'
    return build_popover(
        target=id_information,
        placement='bottom',
        children=[
            html.Div(
                className='p-2',
                children=[
                    html.P(
                        className='header-admin-information-title fw-semibold',
                        children=['Considerar lo siguiente:'],
                    ),
                    _build_wrapper(
                        children=[
                            html.P(
                                className='header-admin-information-text-primary',
                                children=['- Realizar cambios con precaución.'],
                            ),
                            html.P(
                                className='header-admin-information-text-primary',
                                children=[
                                    '- No olvides pasar por el gestor de publicaciones '
                                    'para generar la proyección de cosmos para el ambiente donde '
                                    'desees visualizar los cambios.'
                                ],
                            ),
                        ]
                    ),
                    _build_wrapper(
                        class_name='pt-2',
                        children=[
                            html.P(
                                className=custom_class_name,
                                children=[
                                    '** El administrador de perfiles de usuario no necesita proyección '
                                    'de cosmos.'
                                ],
                            ),
                            html.P(
                                className=custom_class_name,
                                children=[
                                    '** El administrador de imágenes de alarmas no necesita proyección '
                                    'de cosmos.'
                                ],
                            ),
                            html.P(
                                className=custom_class_name,
                                children=[
                                    '** La información contenida '
                                    'alimenta los diferentes ambientes de ADA.'
                                ],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


def _build_wrapper(children: list[html.Div], class_name: str = 'pt-1'):
    return html.Div(className='d-flex flex-column {0}'.format(class_name), children=children)
