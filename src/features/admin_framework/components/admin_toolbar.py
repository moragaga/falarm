"""
Provides functionality for building an admin toolbar with Dash and
Dash Bootstrap Components.

The module defines a function to create a toolbar for admin interfaces,
which includes a grouped set of buttons for common administrative actions
such as refresh, add, delete, and save.

Functions
---------
build_admin_toolbar(admin_key)
    Constructs an admin toolbar component with specific functionalities.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ..services.admin_component_ids import (
    build_admin_component_ids,
)


def build_admin_toolbar(admin_key: str) -> html.Div:
    ids = build_admin_component_ids(admin_key)

    return html.Div(
        className='d-flex justify-content-between align-items-center gap-2 flex-wrap mb-3',
        children=[
            html.Div(),
            dbc.ButtonGroup(
                className='admin-toolbar-buttons-wrapper',
                children=[
                    dbc.Button(
                        id=ids['refresh_button'],
                        color='secondary',
                        outline=True,
                        n_clicks=0,
                        children=['Recargar'],
                    ),
                    dbc.Button(
                        id=ids['add_button'],
                        color='success',
                        outline=True,
                        n_clicks=0,
                        children=['Agregar fila'],
                    ),
                    dbc.Button(
                        id=ids['delete_button'],
                        color='danger',
                        outline=True,
                        n_clicks=0,
                        children=['Eliminar seleccionadas'],
                    ),
                    dbc.Button(
                        id=ids['save_button'],
                        color='dark',
                        outline=True,
                        n_clicks=0,
                        children=['Guardar'],
                    ),
                ],
            ),
        ],
    )
