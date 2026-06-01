"""
Provides functionality to build the admin layout for the application.

This module includes methods to construct an organized admin interface using
Dash and Dash Bootstrap Components. The generated layout comprises a page
header, toolbar, feedback mechanism, modal handling capabilities, and a grid
service for managing data tables.

Functions
---------
build_admin_layout(definition: AdminDefinition) -> html.Div
    Constructs and returns the admin layout as a Dash `html.Div` component.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.features.configuration.services import (
    SchemaBuilderService,
)

from ..components.admin_feedback_host import build_admin_feedback_host
from ..components.admin_modal_host import build_admin_component_ids, build_admin_modal_host
from ..components.admin_page_header import build_admin_page_header
from ..components.admin_toolbar import build_admin_toolbar
from ..models.admin_definition import AdminDefinition
from ..services.admin_grid_service import AdminGridService


def build_admin_layout(definition: AdminDefinition) -> html.Div:
    ids = build_admin_component_ids(definition.key)
    column_defs = SchemaBuilderService.build_column_defs(definition.schema)

    return html.Div(
        id=ids['container'],
        className='p-0',
        children=[
            build_admin_page_header(definition.title),
            html.Div(
                className='p-3',
                children=[
                    dcc.Interval(id=ids['init'], n_intervals=0, max_intervals=1, interval=250),
                    dbc.Card(
                        children=[
                            dbc.CardBody(
                                children=[
                                    build_admin_toolbar(admin_key=definition.key),
                                    dcc.Loading(
                                        id=ids['loading'],
                                        type='default',
                                        parent_className='loading-component-admin',
                                        className='loading-component-spinner',
                                        display='show',
                                        children=AdminGridService.create_table(
                                            table_id=ids['grid'],
                                            row_data=[],
                                            column_defs=column_defs,
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            ),
            build_admin_feedback_host(definition.key),
            build_admin_modal_host(definition.key),
        ],
    )
