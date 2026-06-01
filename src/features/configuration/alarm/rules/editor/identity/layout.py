from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from .ids import AlarmRuleIdentityIds


def build_identity_tab_layout(*, draft: dict[str, Any] | None):
    draft = draft or {}
    catalogs = draft.get('_catalogs') or {}
    tool_options = catalogs.get('tool_options') or []

    return dbc.Row(
        className='g-3',
        children=[
            dbc.Col(
                md=6,
                children=[
                    _input('Regla', AlarmRuleIdentityIds.RULE_NAME, draft.get('rule_name')),
                    _input('Nombre visible', AlarmRuleIdentityIds.DISPLAY_NAME, draft.get('display_name')),
                    _input('Título', AlarmRuleIdentityIds.TITLE_TEMPLATE, draft.get('title_template')),
                    _textarea('Causa', AlarmRuleIdentityIds.CAUSE_TEMPLATE, draft.get('cause_template')),
                    _readonly_input(
                        'ID contenido automático',
                        AlarmRuleIdentityIds.CONTENT_KEY,
                        draft.get('content_key'),
                        help_text='Se genera automáticamente y luego se usará para vincular mensajes e imágenes.',
                    ),
                ],
            ),
            dbc.Col(
                md=6,
                children=[
                    dbc.Label('Tipo'),
                    dcc.Dropdown(
                        id=AlarmRuleIdentityIds.KIND,
                        options=[
                            {'label': 'Riesgo', 'value': 'risk'},
                            {'label': 'Impacto', 'value': 'impact'},
                        ],
                        value=draft.get('kind') or 'risk',
                        clearable=False,
                    ),
                    html.Div(className='mb-3'),
                    dbc.Label('Nivel riesgo'),
                    dcc.Dropdown(
                        id=AlarmRuleIdentityIds.RISK_LEVEL,
                        options=[
                            {'label': '1 - Nivel 0 inmediato', 'value': '1'},
                            {'label': '2 - Escala por tiempo', 'value': '2'},
                            {'label': '3 - No escala', 'value': '3'},
                        ],
                        value=str(draft.get('risk_level') or '3'),
                        clearable=False,
                    ),
                    html.Div(className='mb-3'),
                    _input(
                        'Grupo prioridad/gestión',
                        AlarmRuleIdentityIds.SCOPE_KEY,
                        draft.get('scope_key'),
                        help_text='Grupo donde la regla compite por prioridad y donde aplica gestión/desactivación. Ej: rougher_01, h2s_planta, molienda_linea_1.',
                    ),
                    _number(
                        'Prioridad',
                        AlarmRuleIdentityIds.PRIORITY_ORDER,
                        draft.get('priority_order') or 100,
                    ),
                    dbc.Label('Herramienta inicial'),
                    dcc.Dropdown(
                        id=AlarmRuleIdentityIds.ORIGIN_TOOL_KEY,
                        options=tool_options,
                        value=draft.get('origin_tool_key') or None,
                        placeholder='Selecciona herramienta inicial',
                    ),
                    html.Div(className='mb-3'),
                    _input('Bucket operador', AlarmRuleIdentityIds.OPERATOR_BUCKET, draft.get('operator_bucket')),
                    dbc.Label('Color'),
                    dcc.Dropdown(
                        id=AlarmRuleIdentityIds.COLOR,
                        options=[
                            {'label': 'Rojo', 'value': 'red'},
                            {'label': 'Amarillo', 'value': 'yellow'},
                        ],
                        value=draft.get('color') or 'yellow',
                        clearable=False,
                    ),
                    html.Div(className='mb-3'),
                    dbc.Checkbox(
                        id=AlarmRuleIdentityIds.IS_ACTIVE,
                        label='Activa',
                        value=bool(draft.get('is_active', True)),
                        className='mt-2',
                    ),
                ],
            ),
        ],
    )


def _input(label: str, component_id: str, value, help_text: str | None = None):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Input(id=component_id, value=value or '', type='text'),
            html.Div(help_text, className='text-muted small mt-1') if help_text else None,
        ],
    )


def _readonly_input(label: str, component_id: str, value, help_text: str | None = None):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Input(id=component_id, value=value or '', type='text', disabled=True),
            html.Div(help_text, className='text-muted small mt-1') if help_text else None,
        ],
    )


def _number(label: str, component_id: str, value):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Input(id=component_id, value=value, type='number'),
        ],
    )


def _textarea(label: str, component_id: str, value):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Textarea(id=component_id, value=value or '', rows=4),
        ],
    )
