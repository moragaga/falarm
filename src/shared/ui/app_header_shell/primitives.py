"""
This module provides functionalities for building styled components using Dash and Dash Bootstrap Components.

The module includes functions to build buttons with specific themes and icons, as well as rendering logos
with customizable image paths for Dash applications.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html


def build_button_action(
    id_button: str,
    icon_button: str,
    class_name: str,
    title: str = 'Abrir menú',
    theme: str = 'dark',
) -> dbc.Button:
    class_name_theme = 'dark-theme' if theme == 'dark' else 'light-theme'
    return dbc.Button(
        id=id_button,
        className=f'{class_name} {class_name_theme}',
        color=theme,
        n_clicks=0,
        title=title,
        children=[
            html.I(className=icon_button),
        ],
    )


def build_logo(logo_src_name: str = 'logo_dashboard') -> html.Div:
    return html.Div(
        className='d-flex align-items-center justify-content-center h-100 app-header-shell-logo-wrapper',
        children=[
            html.Img(
                className='img-fluid',
                src='/assets/img/branding/logos/{0}.svg'.format(logo_src_name),
            )
        ],
    )
