from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from .ids import AlarmRuleVisualizationIds


def build_visual_target_card(
    *,
    target: dict[str, Any],
    index: str = 'integrated_operations',
    component_options: list[dict[str, str]] | None = None,
    subcomponent_options: list[dict[str, str]] | None = None,
):
    selected_component_keys = _ensure_list(
        value=target.get('affected_component_keys'),
    )

    return dbc.Card(
        className='mb-3',
        children=[
            dbc.CardHeader('ADA Operaciones Integradas'),
            dbc.CardBody(
                children=[
                    dbc.Row(
                        className='g-3',
                        children=[
                            dbc.Col(
                                md=6,
                                children=[
                                    dbc.Label('Componentes afectados'),
                                    dcc.Dropdown(
                                        id={
                                            'type': (
                                                AlarmRuleVisualizationIds
                                                .AFFECTED_COMPONENTS_TYPE
                                            ),
                                            'index': index,
                                        },
                                        value=selected_component_keys,
                                        options=component_options or [],
                                        multi=True,
                                        placeholder='Selecciona componentes padre',
                                    ),
                                    html.Div(
                                        (
                                            'Los componentes padre definen agrupación, '
                                            'posición principal y filtran los subcomponentes disponibles.'
                                        ),
                                        className='text-muted small mt-1',
                                    ),
                                ],
                            ),
                            dbc.Col(
                                md=6,
                                children=[
                                    dbc.Label('Subcomponentes afectados / resaltados'),
                                    dcc.Dropdown(
                                        id={
                                            'type': (
                                                AlarmRuleVisualizationIds
                                                .AFFECTED_SUBCOMPONENTS_TYPE
                                            ),
                                            'index': index,
                                        },
                                        value=_ensure_list(
                                            value=target.get('affected_subcomponent_keys'),
                                        ),
                                        options=subcomponent_options or [],
                                        multi=True,
                                        placeholder=(
                                            'Selecciona primero uno o más componentes padre'
                                        ),
                                        disabled=not bool(selected_component_keys),
                                    ),
                                    html.Div(
                                        (
                                            'Solo se muestran subcomponentes pertenecientes '
                                            'a los componentes padre seleccionados.'
                                        ),
                                        className='text-muted small mt-1',
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ],
    )


def _ensure_list(
    *,
    value: Any,
) -> list[str]:
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item or '').strip()
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(';')
            if item.strip()
        ]

    return []