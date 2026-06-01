from __future__ import annotations

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.configuration.alarm.services.alarm_configuration_validation_service import (
    AlarmConfigurationValidationService,
)
from src.features.configuration.alarm.services.alarm_rule_editor_service import AlarmRuleEditorService

from ..ids import AlarmRuleEditorIds
from .ids import AlarmRuleManagementIds


def register_alarm_rule_management_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data', allow_duplicate=True),
        Input(component_id=AlarmRuleManagementIds.HIDE_ALL_TOOLS_WHEN_MANAGED, component_property='value'),
        Input(component_id=AlarmRuleManagementIds.REAPPEAR_IF_STILL_ACTIVE_ENABLED, component_property='value'),
        Input(component_id=AlarmRuleManagementIds.REAPPEAR_AFTER_MANAGEMENT_MINUTES, component_property='value'),
        Input(component_id=AlarmRuleManagementIds.USE_MESSAGE_MANAGEMENT_OVERRIDE, component_property='value'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def update_management_draft(
        hide_all_tools_when_managed,
        reappear_if_still_active_enabled,
        reappear_after_management_minutes,
        use_message_management_override,
        draft: dict | None,
    ):
        if ctx.triggered_id is None or not draft:
            raise PreventUpdate

        updated = dict(draft)
        updated.update(
            {
                'hide_all_tools_when_managed': bool(hide_all_tools_when_managed),
                'reappear_if_still_active_enabled': bool(reappear_if_still_active_enabled),
                'reappear_after_management_minutes': reappear_after_management_minutes,
                'use_message_management_override': bool(use_message_management_override),
            }
        )
        updated = AlarmRuleEditorService.normalize_runtime_draft(draft=updated)
        diagnostics = AlarmConfigurationValidationService.validate_rule_draft(draft=updated)
        updated['diagnostics'] = diagnostics

        return updated, {'diagnostics': diagnostics}
