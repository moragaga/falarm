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
from .ids import AlarmRuleEscalationIds


def register_alarm_rule_escalation_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data', allow_duplicate=True),
        Input(component_id=AlarmRuleEscalationIds.ADD_TARGET_BUTTON, component_property='n_clicks'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def add_escalation_target(clicks, draft: dict | None):
        if not clicks or ctx.triggered_id is None or not draft:
            raise PreventUpdate

        # Solo Riesgo 2 permite agregar destinos manuales.
        if str(draft.get('risk_level') or '3') != '2':
            raise PreventUpdate

        updated = dict(draft)
        targets = [
            dict(target)
            for target in updated.get('escalation_targets') or []
            if isinstance(target, dict)
        ]
        existing_tools = {str(target.get('target_tool_key') or '') for target in targets}
        target_tool_key = _resolve_next_linear_target_tool_key(
            draft=updated,
            existing_tools=existing_tools,
        )
        if not target_tool_key:
            target_tool_key = _fallback_target_tool_key(draft=updated, existing_tools=existing_tools)

        targets.append(
            {
                'step_order': _next_step_order(targets=targets),
                'target_tool_key': target_tool_key,
                'is_enabled': True,
                'wait_minutes_from_previous_stage': 15,
            }
        )
        updated['escalation_targets'] = targets

        return _finalize_draft(updated)

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data', allow_duplicate=True),
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
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data', allow_duplicate=True),
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
        if str(updated.get('risk_level') or '3') == '3':
            updated['escalation_targets'] = []
            return _finalize_draft(updated)

        targets = []
        for position, tool_id in enumerate(tool_ids or []):
            if not isinstance(tool_id, dict):
                continue

            step_order = _value_at(order_values, position)
            tool_key = _value_at(tool_values, position)
            is_enabled = bool(_value_at(enabled_values, position))
            minutes = _value_at(minutes_values, position)
            if not tool_key and not is_enabled:
                continue

            targets.append(
                {
                    'step_order': step_order,
                    'target_tool_key': tool_key or '',
                    'is_enabled': is_enabled,
                    'wait_minutes_from_previous_stage': minutes,
                }
            )

        updated['escalation_targets'] = targets
        return _finalize_draft(updated)


def _finalize_draft(draft: dict[str, Any]):
    normalized = AlarmRuleEditorService.normalize_runtime_draft(draft=draft)
    diagnostics = AlarmConfigurationValidationService.validate_rule_draft(draft=normalized)
    normalized['diagnostics'] = diagnostics
    return normalized, {'diagnostics': diagnostics}



def _resolve_next_linear_target_tool_key(*, draft: dict[str, Any], existing_tools: set[str]) -> str:
    catalogs = draft.get('_catalogs') or {}
    tools = [row for row in catalogs.get('tools') or [] if isinstance(row, dict)]
    origin_tool_key = str(draft.get('origin_tool_key') or '')
    current_tool_key = _resolve_current_stage_tool_key(
        origin_tool_key=origin_tool_key,
        targets=draft.get('escalation_targets') or [],
        existing_tools=existing_tools,
    )
    current_level = _tool_level(tool_key=current_tool_key, tools=tools)

    candidates = []
    for tool in tools:
        tool_key = str(tool.get('tool_key') or '')
        if not tool_key or tool_key in existing_tools or tool_key == origin_tool_key:
            continue

        level = _tool_level(tool_key=tool_key, tools=tools)
        if level <= 0:
            continue

        if current_level > 0 and level >= current_level:
            continue

        candidates.append(tool)

    candidates = sorted(
        candidates,
        key=lambda item: (-_tool_level(tool_key=str(item.get('tool_key') or ''), tools=tools), int(item.get('display_order') or 0)),
    )
    if candidates:
        return str(candidates[0].get('tool_key') or '')

    return ''


def _resolve_current_stage_tool_key(
    *,
    origin_tool_key: str,
    targets: list[dict[str, Any]],
    existing_tools: set[str],
) -> str:
    active_targets = [
        target
        for target in targets
        if isinstance(target, dict)
        and str(target.get('target_tool_key') or '') in existing_tools
        and bool(target.get('is_enabled', True))
    ]
    if not active_targets:
        return origin_tool_key

    active_targets = sorted(active_targets, key=lambda item: int(item.get('step_order') or 0))
    return str(active_targets[-1].get('target_tool_key') or origin_tool_key)


def _tool_level(*, tool_key: str, tools: list[dict[str, Any]]) -> int:
    for tool in tools:
        if str(tool.get('tool_key') or '') != tool_key:
            continue

        return _normalize_tool_level(value=tool.get('tool_level'))

    return 0


def _normalize_tool_level(*, value: Any) -> int:
    normalized = str(value or '').strip().lower()
    aliases = {
        '1': 1,
        'n0': 1,
        'nivel_0': 1,
        'nivel 0': 1,
        'sala': 1,
        '2': 2,
        'executive': 2,
        'ejecutiva': 2,
        'ejecutivo': 2,
        '3': 3,
        'n1': 3,
        'ada_n1': 3,
    }
    if normalized in aliases:
        return aliases[normalized]

    try:
        return int(normalized)
    except Exception:
        return 0



def _fallback_target_tool_key(*, draft: dict[str, Any], existing_tools: set[str]) -> str:
    catalogs = draft.get('_catalogs') or {}
    tools = [row for row in catalogs.get('tools') or [] if isinstance(row, dict)]
    origin_tool_key = str(draft.get('origin_tool_key') or '')

    # Prefer the first active level 2 tool, then level 1, excluding origin and duplicates.
    for desired_level in (2, 1):
        candidates = [
            tool
            for tool in tools
            if _normalize_tool_level(value=tool.get('tool_level')) == desired_level
            and str(tool.get('tool_key') or '') not in existing_tools
            and str(tool.get('tool_key') or '') != origin_tool_key
        ]
        candidates = sorted(candidates, key=lambda item: int(item.get('display_order') or 0))
        if candidates:
            return str(candidates[0].get('tool_key') or '')

    return ''

def _next_step_order(*, targets: list[dict[str, Any]]) -> int:
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
