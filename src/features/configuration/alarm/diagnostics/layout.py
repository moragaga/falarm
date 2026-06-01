from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from src.features.admin_framework.components.admin_page_header import build_admin_page_header

from .ids import AlarmDiagnosticsIds


def build_alarm_diagnostics_layout():
    return html.Div(
        id=AlarmDiagnosticsIds.CONTAINER,
        className='p-0',
        children=[
            build_admin_page_header('Diagnósticos de configuración de alarmas'),
            html.Div(
                className='p-3',
                children=[
                    dbc.Alert(
                        children=(
                            'Este panel queda preparado para mostrar errores y advertencias de '
                            'validación cuando integremos el compilador de configuración de alarmas.'
                        ),
                        color='info',
                        className='mb-3',
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                html.H5('Sin diagnósticos cargados', className='mb-2'),
                                html.P(
                                    'La configuración publicada todavía no ha sido validada por el '
                                    'nuevo flujo de alarmas.',
                                    className='text-muted mb-0',
                                ),
                            ]
                        )
                    ),
                ],
            ),
        ],
    )
