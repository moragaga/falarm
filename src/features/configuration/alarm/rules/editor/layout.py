from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from .ids import AlarmRuleEditorIds, AlarmRuleEditorTabs


def build_alarm_rule_editor_layout(
    *,
    family_key: str | None,
    rule_key: str | None,
    active_tab: str | None,
):
    selected_tab = (
        active_tab
        if active_tab in AlarmRuleEditorTabs.ALL
        else AlarmRuleEditorTabs.IDENTITY
    )

    return html.Div(
        className='p-3',
        children=[
            dcc.Store(id=AlarmRuleEditorIds.ORIGINAL_STORE),
            dcc.Store(id=AlarmRuleEditorIds.DRAFT_STORE),
            dcc.Store(id=AlarmRuleEditorIds.VALIDATION_STORE),
            dcc.Store(id=AlarmRuleEditorIds.DIRTY_STORE, data=False),
            dbc.Card(
                className='mb-3',
                children=[
                    dbc.CardBody(
                        children=[
                            html.Div(id=AlarmRuleEditorIds.HEADER),
                            html.Div(
                                className='d-flex justify-content-end gap-2 mt-3',
                                children=[
                                    dbc.Button(
                                        'Volver al listado',
                                        id=AlarmRuleEditorIds.CANCEL_BUTTON,
                                        color='secondary',
                                        outline=True,
                                        n_clicks=0,
                                    ),
                                    dbc.Button(
                                        'Guardar regla',
                                        id=AlarmRuleEditorIds.SAVE_BUTTON,
                                        color='dark',
                                        n_clicks=0,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            dbc.Tabs(
                                id=AlarmRuleEditorIds.TABS,
                                active_tab=selected_tab,
                                children=[
                                    dbc.Tab(
                                        label='Identidad',
                                        tab_id=AlarmRuleEditorTabs.IDENTITY,
                                    ),
                                    dbc.Tab(
                                        label='Gestión y reaparición',
                                        tab_id=AlarmRuleEditorTabs.MANAGEMENT,
                                    ),
                                    dbc.Tab(
                                        label='Escalamiento',
                                        tab_id=AlarmRuleEditorTabs.ESCALATION,
                                    ),
                                    dbc.Tab(
                                        label='Visualización',
                                        tab_id=AlarmRuleEditorTabs.VISUALIZATION,
                                    ),
                                    dbc.Tab(
                                        label='Resumen',
                                        tab_id=AlarmRuleEditorTabs.SUMMARY,
                                    ),
                                ],
                            ),
                            html.Div(
                                id=AlarmRuleEditorIds.TAB_CONTENT,
                                className='pt-3',
                            ),
                        ],
                    ),
                ],
            ),
            dcc.Store(
                id='alarm-rule-editor-route-context',
                data={
                    'family_key': family_key,
                    'rule_key': rule_key,
                    'active_tab': selected_tab,
                },
            ),
        ],
    )