from __future__ import annotations

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.configuration.alarm.options import (
    AlarmBusinessCategory,
    AlarmColor,
    AlarmCriticality,
    AlarmKind,
    AlarmVisibilityMode,
)
from src.features.configuration.alarm.services.alarm_configuration_validation_service import (
    AlarmConfigurationValidationService,
)
from src.features.configuration.alarm.services.alarm_rule_editor_service import (
    AlarmRuleEditorService,
)

from ..ids import AlarmRuleEditorIds
from .ids import AlarmRuleIdentityIds


def register_alarm_rule_identity_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=AlarmRuleEditorIds.DRAFT_STORE,
            component_property='data',
            allow_duplicate=True,
        ),
        Output(
            component_id=AlarmRuleEditorIds.VALIDATION_STORE,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmRuleIdentityIds.RULE_NAME, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.DISPLAY_NAME, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.TITLE_TEMPLATE, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.CAUSE_TEMPLATE, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.CONTENT_KEY, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.KIND, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.CRITICALITY_CODE, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.BUSINESS_CATEGORY, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.VISIBILITY_MODE, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.SCOPE_KEY, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.PRIORITY_ORDER, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.ORIGIN_TOOL_KEY, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.OPERATOR_BUCKET, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.COLOR, component_property='value'),
        Input(component_id=AlarmRuleIdentityIds.IS_ACTIVE, component_property='value'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def update_identity_draft(
        rule_name,
        display_name,
        title_template,
        cause_template,
        content_key,
        kind,
        criticality_code,
        business_category,
        visibility_mode,
        scope_key,
        priority_order,
        origin_tool_key,
        operator_bucket,
        color,
        is_active,
        draft: dict | None,
    ):
        if ctx.triggered_id is None or not draft:
            raise PreventUpdate

        previous_origin_tool_key = str(draft.get('origin_tool_key') or '').strip()

        updated = dict(draft)
        updated.update(
            {
                'rule_name': rule_name or '',
                'display_name': display_name or '',
                'title_template': title_template or '',
                'cause_template': cause_template or '',
                'content_key': content_key or '',
                'kind': kind or AlarmKind.RISK.value,
                'criticality_code': criticality_code or AlarmCriticality.C3.value,
                'business_category': (
                    business_category or AlarmBusinessCategory.OPERATIONAL.value
                ),
                'visibility_mode': visibility_mode or AlarmVisibilityMode.VISIBLE.value,
                'scope_key': scope_key or '',
                'priority_order': priority_order,
                'origin_tool_key': origin_tool_key or previous_origin_tool_key,
                'operator_bucket': operator_bucket or '',
                'color': color or AlarmColor.YELLOW.value,
                'is_active': bool(is_active),
            }
        )

        updated = AlarmRuleEditorService.normalize_live_draft(draft=updated)
        diagnostics = AlarmConfigurationValidationService.validate_rule_draft(
            draft=updated,
        )
        updated['diagnostics'] = diagnostics

        return updated, {'diagnostics': diagnostics}