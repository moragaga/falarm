from __future__ import annotations

from typing import Any

from dash import ALL, Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.configuration.alarm.services.alarm_configuration_validation_service import (
    AlarmConfigurationValidationService,
)
from src.features.configuration.alarm.services.alarm_rule_editor_service import AlarmRuleEditorService

from ..ids import AlarmRuleEditorIds
from .ids import AlarmRuleVisualizationIds


def register_alarm_rule_visualization_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data', allow_duplicate=True),
        Input({'type': AlarmRuleVisualizationIds.AFFECTED_COMPONENTS_TYPE, 'index': ALL}, 'value'),
        Input({'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE, 'index': ALL}, 'value'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def update_n0_visual_target(
        affected_component_values,
        affected_subcomponent_values,
        draft: dict | None,
    ):
        if ctx.triggered_id is None or not draft:
            raise PreventUpdate

        updated = dict(draft)
        if not _requires_n0_visual(draft=updated):
            updated['visual_targets'] = []
            return _finalize_draft(updated)

        updated['visual_targets'] = [
            {
                'tool_key': _resolve_level_one_tool_key(draft=draft),
                'affected_component_keys': _value_at(affected_component_values, 0) or [],
                'affected_subcomponent_keys': _value_at(affected_subcomponent_values, 0) or [],
                'is_complete': True,
            }
        ]

        return _finalize_draft(updated)


def _finalize_draft(draft: dict[str, Any]):
    normalized = AlarmRuleEditorService.normalize_runtime_draft(draft=draft)
    diagnostics = AlarmConfigurationValidationService.validate_rule_draft(draft=normalized)
    normalized['diagnostics'] = diagnostics
    return normalized, {'diagnostics': diagnostics}


def _requires_n0_visual(*, draft: dict[str, Any]) -> bool:
    if str(draft.get('risk_level') or '') == '1':
        return True

    for target in draft.get('escalation_targets') or []:
        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        if _is_level_one_tool(draft=draft, tool_key=str(target.get('target_tool_key') or '')):
            return True

    return False


def _value_at(values, position: int):
    if not isinstance(values, list):
        return None

    if position >= len(values):
        return None

    return values[position]


def _resolve_level_one_tool_key(*, draft: dict[str, Any]) -> str:
    catalogs = draft.get('_catalogs') or {}
    configured = str(catalogs.get('level_one_tool_key') or '').strip()
    if configured:
        return configured

    for tool in catalogs.get('tools') or []:
        if not isinstance(tool, dict):
            continue
        if str(tool.get('tool_level') or '') == '1':
            return str(tool.get('tool_key') or '').strip()

    return 'nivel_0'


def _is_level_one_tool(*, draft: dict[str, Any], tool_key: str) -> bool:
    catalogs = draft.get('_catalogs') or {}
    tool_level_by_key = catalogs.get('tool_level_by_key') or {}
    return str(tool_level_by_key.get(tool_key) or '') == '1' or tool_key == _resolve_level_one_tool_key(draft=draft)
