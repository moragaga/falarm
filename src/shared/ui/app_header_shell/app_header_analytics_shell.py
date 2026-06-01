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


def build_app_header_analytics_shell(title: str) -> html.Div:
    return html.Div(
        className='app-header-analytics-shell position-relative',
        children=[
            dbc.Container(
                fluid=True,
                className='app-header-analytics-inner',
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
                                className='header-analytics-title-wrapper',
                                xs=12,
                                sm=10,
                                md=10,
                                lg=10,
                                xl=10,
                                xxl=10,
                                children=[
                                    html.Div(
                                        className='d-flex justify-content-center align-items-center h-100 header-analytics-title-wrapper',
                                        children=[
                                            html.Div(
                                                className='d-flex justify-content-center align-items-center gap-1',
                                                children=[
                                                    html.I(className='bi bi-pie-chart-fill header-analytics-title'),
                                                    html.P(
                                                        className='text-center header-analytics-title',
                                                        children=['Analítica Avanzada']
                                                    ),
                                                ]
                                            ),
                                            html.Hr(className='text-white text-center mb-0 mt-1 header-analytics-divider'),
                                            html.P(
                                                className='text-center header-analytics-subtitle',
                                                children=[title],
                                            ),
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

