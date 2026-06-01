"""Layout builder for the Publication Manager page.

This module provides a function to build the user interface layout for the
Publication Manager page. The layout includes a header, a toolbar, and a data
grid for managing publication artifacts and their statuses.

It leverages Dash and Dash Bootstrap Components (DBC) for UI components and
uses a grid-based interface for data representation.

"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.features.admin_framework.components import build_admin_page_header
from src.features.admin_framework.services import AdminGridService
from src.shared.ui.grid.models import (
    GridConfiguration,
    GridRowSelectionConfiguration,
)

from .ids import PUBLICATION_MANAGER_IDS


def build_publication_manager_layout() -> html.Div:
    column_defs = [
        {
            'field': 'artifact_key',
            'headerName': 'Artifact Key',
            'pinned': 'left',
            'minWidth': 220,
        },
        {
            'field': 'status',
            'headerName': 'Estado',
            'minWidth': 150,
            'cellClassRules': {
                'publication-status-published': 'params.value === "Publicado"',
                'publication-status-pending': 'params.value === "Pendiente"',
                'publication-status-unpublished': 'params.value === "No publicado"',
            },
        },
        {
            'field': 'display_name',
            'headerName': 'Nombre',
            'minWidth': 220,
        },
        {
            'field': 'category',
            'headerName': 'Categoría',
            'minWidth': 150,
        },
        {
            'field': 'sharepoint_revision',
            'headerName': 'Rev. SharePoint',
            'minWidth': 150,
        },
        {
            'field': 'published_revision',
            'headerName': 'Rev. Publicada',
            'minWidth': 150,
        },
        {
            'field': 'sharepoint_updated_at',
            'headerName': 'Actualizado en',
            'minWidth': 220,
        },
        {
            'field': 'sharepoint_updated_by',
            'headerName': 'Actualizado por',
            'minWidth': 200,
        },
        {
            'field': 'published_at',
            'headerName': 'Publicado en',
            'minWidth': 220,
        },
        {
            'field': 'published_by',
            'headerName': 'Publicado por',
            'minWidth': 200,
        },
        {
            'field': 'status_code',
            'headerName': 'Código Estado',
            'hide': True,
        },
    ]

    return html.Div(
        id=PUBLICATION_MANAGER_IDS['container'],
        className='p-0',
        children=[
            build_admin_page_header('Publication Manager'),
            dcc.Interval(
                id=PUBLICATION_MANAGER_IDS['init'], n_intervals=0, max_intervals=1, interval=250
            ),
            html.Div(
                className='p-3',
                children=[
                    dbc.Card(
                        children=[
                            dbc.CardBody(
                                children=[
                                    _build_toolbar(),
                                    dcc.Loading(
                                        id=PUBLICATION_MANAGER_IDS['loading'],
                                        type='default',
                                        parent_className='loading-component-publication-manager-admin',
                                        className='loading-component-spinner',
                                        display='show',
                                        children=AdminGridService.create_table(
                                            table_id=PUBLICATION_MANAGER_IDS['grid'],
                                            row_data=[],
                                            column_defs=column_defs,
                                            configuration=GridConfiguration(
                                                editable=False,
                                                pagination=True,
                                                pagination_page_size=20,
                                                pagination_page_size_selector=(
                                                    10,
                                                    20,
                                                    50,
                                                    100,
                                                ),
                                                row_selection=GridRowSelectionConfiguration(
                                                    mode='multiRow',
                                                    checkboxes=True,
                                                    header_checkbox=True,
                                                    enable_click_selection=True,
                                                ),
                                                animate_rows=False,
                                                stop_editing_when_cells_lose_focus=True,
                                                dash_grid_options_overrides={
                                                    'rowSelection': {
                                                        'selectAll': 'all',
                                                    },
                                                },
                                                class_name='ag-theme-alpine w-100 app-grid-shell publication-manager-configuration',
                                            ),
                                        ),
                                    ),
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id=PUBLICATION_MANAGER_IDS['toast'],
                        className='mt-3',
                    ),
                ],
            ),
        ],
    )


def _build_toolbar() -> html.Div:
    return html.Div(
        className='d-flex gap-2 align-items-center flex-wrap mb-3',
        children=[
            dbc.ButtonGroup(
                className='admin-toolbar-buttons-wrapper',
                children=[
                    dbc.Button(
                        id=PUBLICATION_MANAGER_IDS['refresh'],
                        color='secondary',
                        outline=True,
                        n_clicks=0,
                        children=['Recargar'],
                    ),
                    dbc.Button(
                        id=PUBLICATION_MANAGER_IDS['publish'],
                        color='primary',
                        outline=True,
                        n_clicks=0,
                        children=['Publicar seleccionados'],
                    ),
                    dbc.Button(
                        id=PUBLICATION_MANAGER_IDS['publish_pending'],
                        color='success',
                        outline=True,
                        n_clicks=0,
                        children=['Publicar pendientes'],
                    ),
                ],
            )
        ],
    )
