from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from .ids import AlarmRuleSummaryIds


def build_summary_tab_layout(*, draft: dict[str, Any] | None):
    draft = draft or {}
    diagnostics = draft.get('diagnostics') or []

    return html.Div(
        id=AlarmRuleSummaryIds.SUMMARY_CONTAINER,
        children=[
            dbc.Row(
                className='g-3 mb-3',
                children=[
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Regla',
                            value=draft.get('display_name') or draft.get('rule_name') or 'Sin nombre',
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Nivel riesgo',
                            value=str(draft.get('risk_level') or '3'),
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Scope operativo',
                            value=draft.get('scope_key') or 'No configurado',
                        ),
                    ),
                    dbc.Col(
                        md=3,
                        children=_summary_card(
                            title='Herramienta inicial',
                            value=draft.get('origin_tool_key') or 'No configurada',
                        ),
                    ),
                ],
            ),
            dbc.Card(
                children=[
                    dbc.CardHeader('Diagnóstico de edición'),
                    dbc.CardBody(
                        id=AlarmRuleSummaryIds.DIAGNOSTICS_CONTAINER,
                        children=_build_diagnostic_items(diagnostics=diagnostics),
                    ),
                ],
            ),
        ],
    )


def _summary_card(*, title: str, value: str):
    return dbc.Card(
        children=[
            dbc.CardBody(
                children=[
                    html.Div(title, className='text-muted small'),
                    html.Div(value, className='fw-semibold'),
                ],
            ),
        ],
    )


def _build_diagnostic_items(*, diagnostics: list[Any]):
    if not diagnostics:
        return dbc.Alert('Sin diagnósticos bloqueantes en el draft actual.', color='success')

    return [
        dbc.Alert(str(item), color='warning', className='mb-2')
        for item in diagnostics
    ]
