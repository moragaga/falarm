from __future__ import annotations

from typing import Any

from dash import ALL, Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.configuration.alarm.options import (
    AlarmCriticality,
    AlarmToolTier,
    AlarmVisibilityMode,
)
from src.features.configuration.alarm.services.alarm_configuration_validation_service import (
    AlarmConfigurationValidationService,
)
from src.features.configuration.alarm.services.alarm_rule_editor_service import (
    AlarmRuleEditorService,
)

from ..ids import AlarmRuleEditorIds
from .ids import AlarmRuleEscalationIds


def register_alarm_rule_escalation_callbacks() -> None:
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
        Input(component_id=AlarmRuleEscalationIds.ADD_TARGET_BUTTON, component_property='n_clicks'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def add_escalation_target(clicks, draft: dict | None):
        if not clicks or ctx.triggered_id is None or not draft:
            raise PreventUpdate

        if str(draft.get('visibility_mode') or '') == AlarmVisibilityMode.TRACE_ONLY.value:
            raise PreventUpdate

        if str(draft.get('criticality_code') or '') != AlarmCriticality.C2.value:
            raise PreventUpdate

        if not str(draft.get('origin_tool_key') or '').strip():
            raise PreventUpdate

        updated = dict(draft)
        targets = [
            dict(target)
            for target in updated.get('escalation_targets') or []
            if isinstance(target, dict)
        ]

        target_tool_key = _resolve_next_target_tool_key(
            draft=updated,
            targets=targets,
        )

        if not target_tool_key:
            raise PreventUpdate

        targets.append(
            {
                'step_order': _next_step_order(targets=targets),
                'target_tool_key': target_tool_key,
                'is_enabled': True,
                'wait_minutes_from_previous_step': 15,
            }
        )

        updated['escalation_targets'] = targets

        return _finalize_draft(updated)

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
        Input({'type': AlarmRuleEscalationIds.TARGET_REMOVE_TYPE, 'index': ALL}, 'n_clicks'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def remove_escalation_target(clicks, draft: dict | None):
        triggered = ctx.triggered_id

        if not any(clicks or []) or not isinstance(triggered, dict) or not draft:
            raise PreventUpdate

        target_index = str(triggered.get('index') or '')

        targets = [
            dict(target)
            for index, target in enumerate(draft.get('escalation_targets') or [])
            if str(index) != target_index and isinstance(target, dict)
        ]

        updated = dict(draft)
        updated['escalation_targets'] = targets

        return _finalize_draft(updated)

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
        Input({'type': AlarmRuleEscalationIds.TARGET_ORDER_TYPE, 'index': ALL}, 'value'),
        Input({'type': AlarmRuleEscalationIds.TARGET_TOOL_TYPE, 'index': ALL}, 'value'),
        Input({'type': AlarmRuleEscalationIds.TARGET_ENABLED_TYPE, 'index': ALL}, 'value'),
        Input({'type': AlarmRuleEscalationIds.TARGET_MINUTES_TYPE, 'index': ALL}, 'value'),
        State({'type': AlarmRuleEscalationIds.TARGET_TOOL_TYPE, 'index': ALL}, 'id'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def update_escalation_targets(
        order_values,
        tool_values,
        enabled_values,
        minutes_values,
        tool_ids,
        draft: dict | None,
    ):
        if ctx.triggered_id is None or not draft:
            raise PreventUpdate

        updated = dict(draft)

        if str(updated.get('visibility_mode') or '') == AlarmVisibilityMode.TRACE_ONLY.value:
            updated['escalation_targets'] = []
            return _finalize_draft(updated)

        if str(updated.get('criticality_code') or '') != AlarmCriticality.C2.value:
            updated['escalation_targets'] = []
            return _finalize_draft(updated)

        if not str(updated.get('origin_tool_key') or '').strip():
            updated['escalation_targets'] = []
            return _finalize_draft(updated)

        targets: list[dict[str, Any]] = []

        for position, tool_id in enumerate(tool_ids or []):
            if not isinstance(tool_id, dict):
                continue

            tool_key = _value_at(tool_values, position)
            is_enabled = bool(_value_at(enabled_values, position))

            if not tool_key and not is_enabled:
                continue

            targets.append(
                {
                    'step_order': _value_at(order_values, position),
                    'target_tool_key': tool_key or '',
                    'is_enabled': is_enabled,
                    'wait_minutes_from_previous_step': _value_at(
                        minutes_values,
                        position,
                    ),
                }
            )

        updated['escalation_targets'] = targets

        return _finalize_draft(updated)


def _finalize_draft(draft: dict[str, Any]):
    normalized = AlarmRuleEditorService.normalize_runtime_draft(draft=draft)
    diagnostics = AlarmConfigurationValidationService.validate_rule_draft(
        draft=normalized,
    )
    normalized['diagnostics'] = diagnostics

    return normalized, {'diagnostics': diagnostics}


def _resolve_next_target_tool_key(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
) -> str:
    catalogs = draft.get('_catalogs') or {}
    tools = [
        tool
        for tool in catalogs.get('tools') or []
        if isinstance(tool, dict)
    ]

    current_tool_key = _resolve_current_tool_key(
        draft=draft,
        targets=targets,
    )

    if not current_tool_key:
        return ''

    existing_tools = {
        str(target.get('target_tool_key') or '')
        for target in targets
        if isinstance(target, dict)
    }

    for tool in sorted(tools, key=lambda item: int(item.get('display_order') or 0)):
        target_tool_key = str(tool.get('tool_key') or '')

        if not target_tool_key:
            continue

        if target_tool_key in existing_tools:
            continue

        if _is_allowed_next_escalation_target(
            catalogs=catalogs,
            current_tool_key=current_tool_key,
            target_tool_key=target_tool_key,
        ):
            return target_tool_key

    return ''


def _resolve_current_tool_key(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
) -> str:
    current_tool_key = str(draft.get('origin_tool_key') or '')

    for target in sorted(targets, key=lambda item: int(item.get('step_order') or 0)):
        if not bool(target.get('is_enabled', True)):
            continue

        target_tool_key = str(target.get('target_tool_key') or '')

        if target_tool_key:
            current_tool_key = target_tool_key

    return current_tool_key


def _is_allowed_next_escalation_target(
    *,
    catalogs: dict[str, Any],
    current_tool_key: str,
    target_tool_key: str,
) -> bool:
    if not current_tool_key or not target_tool_key:
        return False

    if current_tool_key == target_tool_key:
        return False

    current_tier = _tool_tier_for_key(
        catalogs=catalogs,
        tool_key=current_tool_key,
    )
    target_tier = _tool_tier_for_key(
        catalogs=catalogs,
        tool_key=target_tool_key,
    )

    if current_tier == AlarmToolTier.PROCESS.value:
        return target_tier in {
            AlarmToolTier.INTEGRATED_OPERATIONS.value,
            AlarmToolTier.STRATEGIC.value,
        }

    if current_tier == AlarmToolTier.INTEGRATED_OPERATIONS.value:
        return target_tier == AlarmToolTier.STRATEGIC.value

    return False


def _tool_tier_for_key(
    *,
    catalogs: dict[str, Any],
    tool_key: str,
) -> str:
    tool_tier_by_key = catalogs.get('tool_tier_by_key') or {}
    return str(tool_tier_by_key.get(tool_key) or '')


def _next_step_order(
    *,
    targets: list[dict[str, Any]],
) -> int:
    orders: list[int] = []

    for target in targets:
        try:
            order = int(target.get('step_order') or 0)
        except Exception:
            continue

        if order > 0:
            orders.append(order)

    if not orders:
        return 1

    return max(orders) + 1


def _value_at(values, position: int):
    if not isinstance(values, list):
        return None

    if position >= len(values):
        return None

    return values[position]