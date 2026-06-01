"""
Constructs the main shell structure for the application header.

This function builds a header component for a Dash application using Dash
and Dash Bootstrap Components. It contains a logo, optional content sections
(global indicators, status, and information), and mobile/desktop toggle buttons.
The header is responsive and adjusts to various screen sizes.

Parameters
----------
global_indicator_content : list, optional
    A list of content elements to be displayed in the global indicators section of the header.
    Defaults to an empty list if None is provided.
status_content : list, optional
    A list of content elements to be displayed in the status section of the header.
    Defaults to an empty list if None is provided.
information_content : list, optional
    A list of content elements to be displayed in the information section of the header.
    Defaults to an empty list if None is provided.

Returns
-------
html.Div
    The constructed Dash Div component containing the entire header structure.

"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.app.navigation.ids import AppNavigationIds
from src.app.navigation.offcanvas import build_app_navigation_offcanvas

from .primitives import build_button_action, build_logo


def build_app_header_shell(
    *,
    global_indicator_content=None,
    status_content=None,
    information_content=None,
) -> html.Div:
    global_indicator_content = global_indicator_content or []
    status_content = status_content or []
    information_content = information_content or []

    return html.Div(
        className='app-header-shell position-relative',
        children=[
            dbc.Container(
                fluid=True,
                className='app-header-inner',
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
                                children=[build_logo(logo_src_name='app-web-home')],
                            ),
                            dbc.Col(
                                xs=12,
                                sm=9,
                                md=9,
                                lg=9,
                                xl=9,
                                xxl=9,
                                children=html.Div(
                                    className='',
                                    children=global_indicator_content or [],
                                ),
                            ),
                            dbc.Col(
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                children=[
                                    html.Div(
                                        className='d-flex align-items-center '
                                        'justify-content-center h-100 status-border-right',
                                        children=status_content or [],
                                    )
                                ],
                            ),
                            dbc.Col(
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                className='d-flex align-items-center justify-content-center',
                                children=[
                                    html.Div(
                                        className='d-flex align-items-center justify-content-center w-100',
                                        children=information_content or [],
                                    )
                                ],
                            ),
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
            ),
            dcc.Location(
                id=AppNavigationIds.HEADER_LOCATION,
                refresh=False,
            ),
            build_app_navigation_offcanvas(),
        ],
    )
