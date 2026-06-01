from __future__ import annotations

from urllib.parse import parse_qs

from dash import dcc, html

from src.features.admin_framework.components.admin_page_header import build_admin_page_header

from .ids import AlarmRulesMode, AlarmRulesPageIds, AlarmRulesQueryParams
from .editor.layout import build_alarm_rule_editor_layout
from .list.layout import build_alarm_rules_list_layout


def build_alarm_rules_layout():
    return html.Div(
        className='p-0',
        children=[
            dcc.Location(id=AlarmRulesPageIds.LOCATION, refresh=False),
            dcc.Store(
                id=AlarmRulesPageIds.PAGE_STATE,
                data={
                    'mode': AlarmRulesMode.LIST,
                    'family_key': None,
                    'rule_key': None,
                    'active_tab': None,
                },
            ),
            build_admin_page_header('Reglas de alarmas'),
            html.Div(id=AlarmRulesPageIds.PAGE_CONTENT),
            html.Div(id=AlarmRulesPageIds.TOAST_HOST),
        ],
    )


def build_alarm_rules_page_content(
    *,
    page_state: dict | None,
    search: str | None,
):
    state = page_state or {}
    mode = state.get('mode') or AlarmRulesMode.LIST

    # La página parte limpia. Los query params solo se usan para preseleccionar familia.
    # Editar/crear regla se maneja por PAGE_STATE para evitar saltos entre listado/editor.
    family_key = state.get('family_key') or _parse_search(search=search).get(AlarmRulesQueryParams.FAMILY)

    if mode == AlarmRulesMode.EDIT:
        return build_alarm_rule_editor_layout(
            family_key=family_key,
            rule_key=state.get('rule_key'),
            active_tab=state.get('active_tab'),
        )

    return build_alarm_rules_list_layout(selected_family=family_key)


# Backward-compatible name used by the existing page module.
def build_alarm_rules_admin_layout():
    return build_alarm_rules_layout()


def _parse_search(*, search: str | None) -> dict[str, str]:
    raw_search = str(search or '').lstrip('?')
    parsed = parse_qs(raw_search)

    return {
        key: values[0]
        for key, values in parsed.items()
        if values
    }
