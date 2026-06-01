from __future__ import annotations

from dash import Input, Output

from src.app.dash import get_dash_app

from .editor.callbacks import register_alarm_rule_editor_callbacks
from .ids import AlarmRulesPageIds
from .layout import build_alarm_rules_page_content
from .list.callbacks import register_alarm_rules_list_callbacks


def register_alarm_rules_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AlarmRulesPageIds.PAGE_CONTENT, component_property='children'),
        Input(component_id=AlarmRulesPageIds.PAGE_STATE, component_property='data'),
        Input(component_id=AlarmRulesPageIds.LOCATION, component_property='search'),
    )
    def render_rules_page_content(page_state: dict | None, search: str | None):
        return build_alarm_rules_page_content(page_state=page_state, search=search)

    register_alarm_rules_list_callbacks()
    register_alarm_rule_editor_callbacks()


# Backward-compatible name used by the first patch registry.
def register_alarm_rules_admin_callback() -> None:
    register_alarm_rules_callbacks()
