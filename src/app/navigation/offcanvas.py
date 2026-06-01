"""
Builds the application navigation off-canvas component.

This module defines a function to construct a Bootstrap-styled off-canvas
navigation menu for use in a Dash application. The off-canvas menu includes
a title and a placeholder for menu content.

Functions
---------
build_app_navigation_offcanvas : dbc.Offcanvas
    Constructs and returns the off-canvas navigation menu component.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from .ids import AppNavigationIds
from .offcanvas_title import build_navigation_offcanvas_title


def build_app_navigation_offcanvas() -> dbc.Offcanvas:
    return dbc.Offcanvas(
        id=AppNavigationIds.HEADER_OFFCANVAS,
        title=build_navigation_offcanvas_title(),
        is_open=False,
        placement='end',
        className='dashboard-main-offcanvas app-navigation-offcanvas',
        children=[
            html.Div(
                id=AppNavigationIds.HEADER_MENU_CONTENT,
                className='app-navigation-offcanvas-content',
            )
        ],
    )
