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
from .ids import AlarmRuleVisualizationIds


def register_alarm_rule_visualization_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            {
                'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE,
                'index': ALL,
            },
            'options',
        ),
        Output(
            {
                'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE,
                'index': ALL,
            },
            'value',
        ),
        Output(
            {
                'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE,
                'index': ALL,
            },
            'disabled',
        ),
        Input(
            {
                'type': AlarmRuleVisualizationIds.AFFECTED_COMPONENTS_TYPE,
                'index': ALL,
            },
            'value',
        ),
        State(
            {
                'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE,
                'index': ALL,
            },
            'value',
        ),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def update_available_subcomponents(
        affected_component_values,
        current_subcomponent_values,
        draft: dict | None,
    ):
        if ctx.triggered_id is None or not draft:
            raise PreventUpdate

        output_count = len(affected_component_values or [])

        if output_count == 0:
            raise PreventUpdate

        catalogs = draft.get('_catalogs') or {}

        options_payload: list[list[dict[str, str]]] = []
        values_payload: list[list[str]] = []
        disabled_payload: list[bool] = []

        for index, selected_component_keys in enumerate(affected_component_values or []):
            selected_components = _ensure_list(
                value=selected_component_keys,
            )

            filtered_options = _filter_subcomponent_options(
                catalogs=catalogs,
                selected_component_keys=selected_components,
            )

            allowed_subcomponent_keys = {
                str(option.get('value') or '')
                for option in filtered_options
                if isinstance(option, dict)
            }

            current_values = _ensure_list(
                value=_value_at(current_subcomponent_values, index),
            )

            pruned_values = [
                subcomponent_key
                for subcomponent_key in current_values
                if subcomponent_key in allowed_subcomponent_keys
            ]

            options_payload.append(filtered_options)
            values_payload.append(pruned_values)
            disabled_payload.append(not bool(selected_components))

        return options_payload, values_payload, disabled_payload

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
        Input({'type': AlarmRuleVisualizationIds.AFFECTED_COMPONENTS_TYPE, 'index': ALL}, 'value'),
        Input({'type': AlarmRuleVisualizationIds.AFFECTED_SUBCOMPONENTS_TYPE, 'index': ALL}, 'value'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def update_visual_target(
        affected_component_values,
        affected_subcomponent_values,
        draft: dict | None,
    ):
        if ctx.triggered_id is None or not draft:
            raise PreventUpdate

        updated = dict(draft)

        if not _requires_integrated_operations_visualization(draft=updated):
            updated['visual_targets'] = []
            return _finalize_draft(updated)

        selected_component_keys = _ensure_list(
            value=_value_at(affected_component_values, 0),
        )

        catalogs = updated.get('_catalogs') or {}

        filtered_subcomponent_options = _filter_subcomponent_options(
            catalogs=catalogs,
            selected_component_keys=selected_component_keys,
        )

        allowed_subcomponent_keys = {
            str(option.get('value') or '')
            for option in filtered_subcomponent_options
            if isinstance(option, dict)
        }

        selected_subcomponent_keys = [
            subcomponent_key
            for subcomponent_key in _ensure_list(
                value=_value_at(affected_subcomponent_values, 0),
            )
            if subcomponent_key in allowed_subcomponent_keys
        ]

        updated['visual_targets'] = [
            {
                'tool_key': _resolve_integrated_operations_tool_key(draft=updated),
                'affected_component_keys': selected_component_keys,
                'affected_subcomponent_keys': selected_subcomponent_keys,
                'is_complete': bool(
                    selected_component_keys
                    and selected_subcomponent_keys
                ),
            }
        ]

        return _finalize_draft(updated)


def _finalize_draft(draft: dict[str, Any]):
    normalized = AlarmRuleEditorService.normalize_runtime_draft(draft=draft)
    diagnostics = AlarmConfigurationValidationService.validate_rule_draft(
        draft=normalized,
    )
    normalized['diagnostics'] = diagnostics

    return normalized, {'diagnostics': diagnostics}


def _requires_integrated_operations_visualization(
    *,
    draft: dict[str, Any],
) -> bool:
    if str(draft.get('visibility_mode') or '') == AlarmVisibilityMode.TRACE_ONLY.value:
        return False

    origin_tool_key = str(draft.get('origin_tool_key') or '')

    if origin_tool_key and _is_integrated_operations_tool(
        draft=draft,
        tool_key=origin_tool_key,
    ):
        return True

    if str(draft.get('criticality_code') or '') == AlarmCriticality.C1.value:
        return True

    for target in draft.get('escalation_targets') or []:
        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        if _is_integrated_operations_tool(
            draft=draft,
            tool_key=str(target.get('target_tool_key') or ''),
        ):
            return True

    return False


def _resolve_integrated_operations_tool_key(
    *,
    draft: dict[str, Any],
) -> str:
    origin_tool_key = str(draft.get('origin_tool_key') or '')

    if origin_tool_key and _is_integrated_operations_tool(
        draft=draft,
        tool_key=origin_tool_key,
    ):
        return origin_tool_key

    for target in draft.get('escalation_targets') or []:
        if not isinstance(target, dict):
            continue

        if not bool(target.get('is_enabled', True)):
            continue

        target_tool_key = str(target.get('target_tool_key') or '')

        if _is_integrated_operations_tool(
            draft=draft,
            tool_key=target_tool_key,
        ):
            return target_tool_key

    catalogs = draft.get('_catalogs') or {}

    for tool_key in catalogs.get('integrated_operations_tool_keys') or ():
        return str(tool_key or '')

    return ''


def _is_integrated_operations_tool(
    *,
    draft: dict[str, Any],
    tool_key: str,
) -> bool:
    catalogs = draft.get('_catalogs') or {}
    tool_tier_by_key = catalogs.get('tool_tier_by_key') or {}

    return (
        str(tool_tier_by_key.get(tool_key) or '')
        == AlarmToolTier.INTEGRATED_OPERATIONS.value
    )


def _filter_subcomponent_options(
    *,
    catalogs: dict[str, Any],
    selected_component_keys: list[str],
) -> list[dict[str, str]]:
    if not selected_component_keys:
        return []

    selected_component_key_set = set(selected_component_keys)
    subcomponent_parent_by_key = catalogs.get('subcomponent_parent_by_key') or {}
    subcomponent_options = catalogs.get('subcomponent_options') or []

    filtered_options: list[dict[str, str]] = []

    for option in subcomponent_options:
        if not isinstance(option, dict):
            continue

        subcomponent_key = str(option.get('value') or '')
        parent_component_key = str(
            subcomponent_parent_by_key.get(subcomponent_key) or '',
        )

        if parent_component_key not in selected_component_key_set:
            continue

        filtered_options.append(option)

    return filtered_options


def _ensure_list(
    *,
    value: Any,
) -> list[str]:
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item or '').strip()
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(';')
            if item.strip()
        ]

    return []


def _value_at(values, position: int):
    if not isinstance(values, list):
        return None

    if position >= len(values):
        return None

    return values[position]