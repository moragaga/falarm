from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.components_n0.definition import (
    ALARM_COMPONENTS_N0_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.definition import ALARM_RULES_ADMIN_DEFINITION
from src.features.configuration.alarm.rules.editor.escalation.definition import (
    ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.visualization.definition import (
    ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.row_factory_service import AlarmRuleRowFactoryService
from src.features.configuration.alarm.services.admin_manifest_save_service import (
    AlarmAdminManifestSaveService,
)
from src.features.configuration.alarm.services.alarm_configuration_validation_service import (
    AlarmConfigurationValidationService,
)
from src.features.configuration.alarm.services.alarm_rule_summary_service import AlarmRuleSummaryService
from src.features.configuration.alarm.tools.definition import ALARM_TOOLS_ADMIN_DEFINITION


_INTERNAL_DRAFT_KEYS = {
    'escalation_targets',
    'visual_targets',
    'diagnostics',
    '_catalogs',
}

_RULE_ROW_KEYS = {
    'rule_key',
    'family_key',
    'rule_name',
    'display_name',
    'title_template',
    'cause_template',
    'content_key',
    'kind',
    'risk_level',
    'scope_key',
    'priority_order',
    'origin_tool_key',
    'operator_bucket',
    'color',
    'hide_all_tools_when_managed',
    'reappear_if_still_active_enabled',
    'reappear_after_management_minutes',
    'continue_escalation_clock_when_hidden',
    'use_message_management_override',
    'escalation_summary',
    'visual_summary',
    'is_active',
}

_ALLOWED_COLORS = {'red', 'yellow'}


class AlarmRuleEditorService:
    def __init__(self, *, data_service: AdminDataService) -> None:
        self._data_service = data_service

    def load_draft(
        self,
        *,
        rule_key: str | None,
        family_key: str | None,
    ) -> dict[str, Any]:
        rules = self._data_service.load(ALARM_RULES_ADMIN_DEFINITION)
        escalation_targets = self._data_service.load(ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION)
        visual_targets = self._data_service.load(ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION)

        rule = _find_row(rows=rules, key_field='rule_key', key_value=rule_key)
        if rule is None:
            rule = AlarmRuleRowFactoryService.build_new_row(current_rows=rules)
            if family_key:
                rule['family_key'] = family_key

        draft = dict(rule)
        draft['escalation_targets'] = [
            dict(target)
            for target in escalation_targets
            if str(target.get('rule_key') or '') == str(draft.get('rule_key') or '')
        ]
        draft['visual_targets'] = [
            dict(target)
            for target in visual_targets
            if str(target.get('rule_key') or '') == str(draft.get('rule_key') or '')
        ]
        draft = self.normalize_runtime_draft(draft=draft)
        draft['_catalogs'] = self._build_catalogs()
        draft['diagnostics'] = AlarmConfigurationValidationService.validate_rule_draft(draft=draft)

        return draft

    def save_draft(self, *, draft: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
        normalized_draft = self.normalize_runtime_draft(draft=draft)
        errors = AlarmConfigurationValidationService.validate_rule_draft(draft=normalized_draft)
        if errors:
            normalized_draft['diagnostics'] = errors
            return False, errors, normalized_draft

        rule_rows = self._upsert_rule_row(draft=normalized_draft)
        ok, save_errors, saved_rule_rows = self._data_service.save(
            ALARM_RULES_ADMIN_DEFINITION,
            rule_rows,
        )
        if not ok:
            return False, save_errors, normalized_draft

        AlarmAdminManifestSaveService.register_update(
            definition=ALARM_RULES_ADMIN_DEFINITION,
            normalized_rows=saved_rule_rows,
        )

        escalation_rows = self._replace_child_rows(
            definition_rows=self._data_service.load(ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION),
            rule_key=str(normalized_draft.get('rule_key') or ''),
            child_rows=normalized_draft.get('escalation_targets') or [],
            allowed_keys={
                'rule_key',
                'target_tool_key',
                'is_enabled',
                'step_order',
                'wait_minutes_from_previous_stage',
            },
        )
        ok, save_errors, saved_escalation_rows = self._data_service.save(
            ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
            escalation_rows,
        )
        if not ok:
            return False, save_errors, normalized_draft

        AlarmAdminManifestSaveService.register_update(
            definition=ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
            normalized_rows=saved_escalation_rows,
        )

        visual_rows = self._replace_child_rows(
            definition_rows=self._data_service.load(ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION),
            rule_key=str(normalized_draft.get('rule_key') or ''),
            child_rows=normalized_draft.get('visual_targets') or [],
            allowed_keys={
                'rule_key',
                'tool_key',
                'visualization_mode',
                'main_component_key',
                'affected_component_keys',
                'affected_subcomponent_keys',
                'highlight_target_key',
                'position_group_key',
                'min_position',
                'max_position',
                'is_complete',
            },
        )
        ok, save_errors, saved_visual_rows = self._data_service.save(
            ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
            visual_rows,
        )
        if not ok:
            return False, save_errors, normalized_draft

        AlarmAdminManifestSaveService.register_update(
            definition=ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
            normalized_rows=saved_visual_rows,
        )

        return True, [], self.load_draft(
            rule_key=str(normalized_draft.get('rule_key') or ''),
            family_key=str(normalized_draft.get('family_key') or ''),
        )

    def _upsert_rule_row(self, *, draft: dict[str, Any]) -> list[dict[str, Any]]:
        rules = self._data_service.load(ALARM_RULES_ADMIN_DEFINITION)
        rule_key = str(draft.get('rule_key') or '').strip()
        normalized_draft = self.normalize_runtime_draft(draft=draft)
        rule_row = {
            key: normalized_draft.get(key)
            for key in _RULE_ROW_KEYS
            if key in normalized_draft
        }
        rule_row['escalation_summary'] = AlarmRuleSummaryService.build_escalation_summary(
            targets=normalized_draft.get('escalation_targets') or [],
        )
        rule_row['visual_summary'] = AlarmRuleSummaryService.build_visual_summary(
            targets=normalized_draft.get('visual_targets') or [],
        )

        updated_rows: list[dict[str, Any]] = []
        replaced = False

        for row in rules:
            if str(row.get('rule_key') or '') == rule_key:
                updated_rows.append(rule_row)
                replaced = True
                continue

            updated_rows.append(row)

        if not replaced:
            updated_rows.append(rule_row)

        return updated_rows

    @staticmethod
    def _replace_child_rows(
        *,
        definition_rows: list[dict[str, Any]],
        rule_key: str,
        child_rows: list[dict[str, Any]],
        allowed_keys: set[str],
    ) -> list[dict[str, Any]]:
        retained_rows = [
            row
            for row in definition_rows
            if str(row.get('rule_key') or '') != rule_key
        ]

        prepared_children = []
        for child in child_rows:
            if not isinstance(child, dict):
                continue

            prepared_child = {
                key: value
                for key, value in child.items()
                if key in allowed_keys
            }
            prepared_child['rule_key'] = rule_key
            prepared_children.append(prepared_child)

        return [*retained_rows, *prepared_children]

    def _build_catalogs(self) -> dict[str, Any]:
        tools = [
            row
            for row in self._data_service.load(ALARM_TOOLS_ADMIN_DEFINITION)
            if bool(row.get('is_active', True))
        ]
        components = [
            row
            for row in self._data_service.load(ALARM_COMPONENTS_N0_ADMIN_DEFINITION)
            if bool(row.get('is_active', True))
        ]

        return {
            'tools': tools,
            'tool_options': _build_options(rows=tools, label_field='tool_name', value_field='tool_key'),
            'components': components,
            'component_options': _build_options(
                rows=[row for row in components if str(row.get('component_type') or '') == 'component'],
                label_field='component_name',
                value_field='component_key',
            ),
            'subcomponent_options': _build_options(
                rows=[row for row in components if str(row.get('component_type') or '') == 'subcomponent'],
                label_field='component_name',
                value_field='component_key',
            ),
        }

    @staticmethod
    def normalize_runtime_draft(*, draft: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(draft or {})
        normalized['risk_level'] = str(normalized.get('risk_level') or '3')
        normalized['kind'] = str(normalized.get('kind') or 'risk')
        normalized['content_key'] = _ensure_content_key(value=normalized.get('content_key'))
        normalized['scope_key'] = _resolve_scope_key(draft=normalized)
        # El runtime debe manejar relojes por ocurrencia/scope/gestión;
        # este flag queda forzado para compatibilidad con filas antiguas.
        normalized['continue_escalation_clock_when_hidden'] = True

        color = str(normalized.get('color') or '').strip().lower()
        normalized['color'] = color if color in _ALLOWED_COLORS else 'yellow'

        # Clean deprecated fields from the editor draft. Existing files may still have them,
        # but the new model keeps a single operational scope.
        normalized.pop('priority_scope_key', None)
        normalized.pop('management_scope_key', None)
        normalized.pop('reappear_tool_policy', None)
        normalized.pop('reappear_tool_key', None)
        normalized.pop('reappear_if_unmanaged_enabled', None)
        normalized.pop('reappear_after_unmanaged_minutes', None)

        escalation_targets = [
            dict(target)
            for target in normalized.get('escalation_targets') or []
            if isinstance(target, dict)
        ]

        risk_level = str(normalized.get('risk_level') or '3')
        if risk_level == '1':
            escalation_targets = _ensure_n0_immediate_target(targets=escalation_targets)
        elif risk_level == '3':
            escalation_targets = []

        normalized['escalation_targets'] = _deduplicate_targets(targets=escalation_targets)

        visual_targets = [
            _normalize_visual_target(target=target)
            for target in normalized.get('visual_targets') or []
            if isinstance(target, dict)
        ]
        normalized['visual_targets'] = _deduplicate_visual_targets(targets=visual_targets)

        return normalized


def _find_row(
    *,
    rows: list[dict],
    key_field: str,
    key_value: str | None,
) -> dict | None:
    normalized_key = str(key_value or '').strip()
    if not normalized_key or normalized_key == 'new':
        return None

    for row in rows:
        if str(row.get(key_field) or '').strip() == normalized_key:
            return dict(row)

    return None


def _build_options(*, rows: list[dict[str, Any]], label_field: str, value_field: str) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []

    for row in sorted(rows, key=lambda item: int(item.get('display_order') or 0)):
        label = str(row.get(label_field) or '').strip()
        value = str(row.get(value_field) or '').strip()
        if not label or not value:
            continue

        options.append({'label': label, 'value': value})

    return options


def _ensure_content_key(*, value: Any) -> str:
    normalized = str(value or '').strip()
    if normalized:
        return normalized

    return f'alarm_content_{uuid4().hex}'


def _resolve_scope_key(*, draft: dict[str, Any]) -> str:
    candidates = (
        draft.get('scope_key'),
        draft.get('management_scope_key'),
        draft.get('priority_scope_key'),
    )

    for candidate in candidates:
        normalized = str(candidate or '').strip()
        if normalized:
            return normalized

    return ''


def _ensure_n0_immediate_target(*, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    updated: list[dict[str, Any]] = []
    found_n0 = False

    for target in targets:
        normalized_target = dict(target)
        if str(normalized_target.get('target_tool_key') or '') == 'nivel_0':
            normalized_target['is_enabled'] = True
            normalized_target['step_order'] = 1
            normalized_target['wait_minutes_from_previous_stage'] = 0
            found_n0 = True

        updated.append(normalized_target)

    if not found_n0:
        updated.append(
            {
                'target_tool_key': 'nivel_0',
                'is_enabled': True,
                'step_order': 1,
                'wait_minutes_from_previous_stage': 0,
            }
        )

    return updated


def _deduplicate_targets(*, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_tool: dict[str, dict[str, Any]] = {}

    for target in targets:
        tool_key = str(target.get('target_tool_key') or '').strip()
        if not tool_key:
            continue

        prepared = dict(target)
        prepared['target_tool_key'] = tool_key
        prepared['is_enabled'] = bool(prepared.get('is_enabled', True))
        prepared['step_order'] = _to_int_or_none(prepared.get('step_order'))
        if prepared['step_order'] is None:
            prepared['step_order'] = len(by_tool) + 1

        prepared['wait_minutes_from_previous_stage'] = _to_int_or_none(
            prepared.get('wait_minutes_from_previous_stage')
            if prepared.get('wait_minutes_from_previous_stage') not in (None, '')
            else prepared.get('show_after_active_minutes')
        )
        prepared.pop('show_after_active_minutes', None)
        by_tool[tool_key] = prepared

    return sorted(by_tool.values(), key=lambda item: int(item.get('step_order') or 0))


def _normalize_visual_target(*, target: dict[str, Any]) -> dict[str, Any]:
    prepared = dict(target)
    prepared['affected_component_keys'] = _ensure_list(prepared.get('affected_component_keys'))
    prepared['affected_subcomponent_keys'] = _ensure_list(prepared.get('affected_subcomponent_keys'))
    prepared['min_position'] = _to_int_or_none(prepared.get('min_position'))
    prepared['max_position'] = _to_int_or_none(prepared.get('max_position'))
    prepared['is_complete'] = bool(prepared.get('is_complete', False))
    return prepared


def _deduplicate_visual_targets(*, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_tool: dict[str, dict[str, Any]] = {}

    for target in targets:
        tool_key = str(target.get('tool_key') or '').strip()
        if not tool_key:
            continue

        prepared = dict(target)
        prepared['tool_key'] = tool_key
        by_tool[tool_key] = prepared

    return list(by_tool.values())


def _ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item or '').strip()]

    if isinstance(value, str):
        return [item.strip() for item in value.split(';') if item.strip()]

    return []


def _to_int_or_none(value: Any) -> int | None:
    if value in (None, ''):
        return None

    try:
        return int(value)
    except Exception:
        return None
