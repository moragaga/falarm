from __future__ import annotations

from typing import Any

from dash import Input, Output

from src.app.dash import get_dash_app

from .header_renderer import build_alarm_rule_editor_header
from .ids import AlarmRuleEditorIds


def register_alarm_rule_editor_header_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=AlarmRuleEditorIds.HEADER,
            component_property='children',
        ),
        Input(
            component_id=AlarmRuleEditorIds.DRAFT_STORE,
            component_property='data',
        ),
    )
    def render_header_from_draft(
        draft: dict[str, Any] | None,
    ):
        return build_alarm_rule_editor_header(
            draft=draft,
        )