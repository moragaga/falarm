from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.features.configuration.alarm.options import (
    ALARM_BUSINESS_CATEGORY_OPTIONS,
    ALARM_COLOR_OPTIONS,
    ALARM_CRITICALITY_OPTIONS,
    ALARM_KIND_OPTIONS,
    ALARM_VISIBILITY_MODE_OPTIONS,
    AlarmBusinessCategory,
    AlarmColor,
    AlarmCriticality,
    AlarmKind,
    AlarmVisibilityMode,
    build_dash_options,
)

from .ids import AlarmRuleIdentityIds


def build_identity_tab_layout(
    *,
    draft: dict[str, Any] | None,
):
    draft = draft or {}
    catalogs = draft.get('_catalogs') or {}
    tool_options = catalogs.get('tool_options') or []

    return dbc.Row(
        className='g-3',
        children=[
            dbc.Col(
                md=6,
                children=[
                    _input(
                        label='Regla',
                        component_id=AlarmRuleIdentityIds.RULE_NAME,
                        value=draft.get('rule_name'),
                    ),
                    _input(
                        label='Nombre visible',
                        component_id=AlarmRuleIdentityIds.DISPLAY_NAME,
                        value=draft.get('display_name'),
                    ),
                    _input(
                        label='Título',
                        component_id=AlarmRuleIdentityIds.TITLE_TEMPLATE,
                        value=draft.get('title_template'),
                    ),
                    _textarea(
                        label='Causa',
                        component_id=AlarmRuleIdentityIds.CAUSE_TEMPLATE,
                        value=draft.get('cause_template'),
                    ),
                    _input(
                        label='ID contenido',
                        component_id=AlarmRuleIdentityIds.CONTENT_KEY,
                        value=draft.get('content_key'),
                        help_text=(
                            'ID reusable para mensajes, imágenes y contenido. '
                            'Varias reglas pueden compartirlo.'
                        ),
                    ),
                    _dropdown(
                        label='Categoría negocio',
                        component_id=AlarmRuleIdentityIds.BUSINESS_CATEGORY,
                        options=build_dash_options(options=ALARM_BUSINESS_CATEGORY_OPTIONS),
                        value=draft.get('business_category')
                        or AlarmBusinessCategory.OPERATIONAL.value,
                    ),
                ],
            ),
            dbc.Col(
                md=6,
                children=[
                    _dropdown(
                        label='Tipo',
                        component_id=AlarmRuleIdentityIds.KIND,
                        options=build_dash_options(options=ALARM_KIND_OPTIONS),
                        value=draft.get('kind') or AlarmKind.RISK.value,
                    ),
                    _dropdown(
                        label='Criticidad',
                        component_id=AlarmRuleIdentityIds.CRITICALITY_CODE,
                        options=build_dash_options(options=ALARM_CRITICALITY_OPTIONS),
                        value=draft.get('criticality_code') or AlarmCriticality.C3.value,
                    ),
                    _dropdown(
                        label='Visibilidad',
                        component_id=AlarmRuleIdentityIds.VISIBILITY_MODE,
                        options=build_dash_options(options=ALARM_VISIBILITY_MODE_OPTIONS),
                        value=draft.get('visibility_mode') or AlarmVisibilityMode.VISIBLE.value,
                        help_text=(
                            'Solo trazabilidad procesa la regla, pero no entra a colas '
                            'ni vistas del operador.'
                        ),
                    ),
                    _input(
                        label='Scope prioridad/gestión',
                        component_id=AlarmRuleIdentityIds.SCOPE_KEY,
                        value=draft.get('scope_key'),
                        help_text=(
                            'Scope donde la regla compite por prioridad y donde aplica '
                            'gestión/desactivación.'
                        ),
                    ),
                    _number(
                        label='Prioridad',
                        component_id=AlarmRuleIdentityIds.PRIORITY_ORDER,
                        value=draft.get('priority_order') or 100,
                    ),
                    _dropdown(
                        label='Herramienta inicial',
                        component_id=AlarmRuleIdentityIds.ORIGIN_TOOL_KEY,
                        options=tool_options,
                        value=draft.get('origin_tool_key') or None,
                        placeholder='Selecciona herramienta inicial',
                        clearable=False,
                        help_text='Campo obligatorio. Define dónde nace la alarma.',
                    ),
                    _input(
                        label='Bucket operador',
                        component_id=AlarmRuleIdentityIds.OPERATOR_BUCKET,
                        value=draft.get('operator_bucket'),
                    ),
                    _dropdown(
                        label='Color',
                        component_id=AlarmRuleIdentityIds.COLOR,
                        options=build_dash_options(options=ALARM_COLOR_OPTIONS),
                        value=draft.get('color') or AlarmColor.YELLOW.value,
                    ),
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


def _input(
    *,
    label: str,
    component_id: str,
    value,
    help_text: str | None = None,
):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Input(id=component_id, value=value or '', type='text'),
            html.Div(help_text, className='text-muted small mt-1') if help_text else None,
        ],
    )


def _number(
    *,
    label: str,
    component_id: str,
    value,
):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Input(id=component_id, value=value, type='number'),
        ],
    )


def _textarea(
    *,
    label: str,
    component_id: str,
    value,
):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dbc.Textarea(id=component_id, value=value or '', rows=4),
        ],
    )


def _dropdown(
    *,
    label: str,
    component_id: str,
    options: list[dict[str, str]],
    value,
    placeholder: str | None = None,
    clearable: bool = False,
    help_text: str | None = None,
):
    return html.Div(
        className='mb-3',
        children=[
            dbc.Label(label),
            dcc.Dropdown(
                id=component_id,
                options=options,
                value=value,
                placeholder=placeholder,
                clearable=clearable,
            ),
            html.Div(help_text, className='text-muted small mt-1') if help_text else None,
        ],
    )