from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.components.definition import ALARM_COMPONENTS_ADMIN_DEFINITION
from src.features.configuration.alarm.rules.definition import ALARM_RULES_ADMIN_DEFINITION
from src.features.configuration.alarm.rules.editor.escalation.definition import (
    ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.visualization.definition import (
    ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.row_factory_service import AlarmRuleRowFactoryService
from src.features.configuration.alarm.subcomponents.definition import ALARM_SUBCOMPONENTS_ADMIN_DEFINITION
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
                'affected_component_keys',
                'affected_subcomponent_keys',
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
        catalogs = self._build_catalogs()
        rule_row['escalation_summary'] = AlarmRuleSummaryService.build_escalation_summary(
            targets=normalized_draft.get('escalation_targets') or [],
            tool_name_by_key=catalogs.get('tool_name_by_key') or {},
        )
        rule_row['visual_summary'] = AlarmRuleSummaryService.build_visual_summary(
            targets=normalized_draft.get('visual_targets') or [],
            component_name_by_key=catalogs.get('component_name_by_key') or {},
            subcomponent_name_by_key=catalogs.get('subcomponent_name_by_key') or {},
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
            for row in self._data_service.load(ALARM_COMPONENTS_ADMIN_DEFINITION)
            if bool(row.get('is_active', True))
        ]
        subcomponents = [
            row
            for row in self._data_service.load(ALARM_SUBCOMPONENTS_ADMIN_DEFINITION)
            if bool(row.get('is_active', True))
        ]
        level_one_tool_key = _resolve_single_tool_key_by_level(tools=tools, tool_level='1')

        return {
            'tools': tools,
            'tool_options': _build_tool_options(tools=tools),
            'tool_name_by_key': _build_name_map(rows=tools, key_field='tool_key', name_field='tool_name'),
            'tool_level_by_key': _build_tool_level_map(tools=tools),
            'level_one_tool_key': level_one_tool_key,
            'components': components,
            'subcomponents': subcomponents,
            'component_options': _build_component_options(components=components),
            'subcomponent_options': _build_subcomponent_options(
                components=components,
                subcomponents=subcomponents,
            ),
            'component_name_by_key': _build_name_map(
                rows=components,
                key_field='component_key',
                name_field='component_name',
            ),
            'subcomponent_name_by_key': _build_name_map(
                rows=subcomponents,
                key_field='subcomponent_key',
                name_field='subcomponent_name',
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
            level_one_tool_key = _resolve_level_one_tool_key(draft=normalized)
            escalation_targets = _ensure_level_one_immediate_target(
                targets=escalation_targets,
                level_one_tool_key=level_one_tool_key,
            )
        elif risk_level == '3':
            escalation_targets = []

        normalized['escalation_targets'] = _deduplicate_targets(targets=escalation_targets)

        visual_targets = [
            _normalize_visual_target(target=target)
            for target in normalized.get('visual_targets') or []
            if isinstance(target, dict)
        ]
        normalized['visual_targets'] = _resolve_single_n0_visual_target(
            draft=normalized,
            targets=visual_targets,
        )

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



def _build_tool_options(*, tools: list[dict[str, Any]]) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []

    for row in sorted(tools, key=lambda item: int(item.get('display_order') or 0)):
        tool_name = str(row.get('tool_name') or '').strip()
        tool_key = str(row.get('tool_key') or '').strip()
        if not tool_name or not tool_key:
            continue

        tool_level = _normalize_tool_level_value(value=row.get('tool_level'))
        label = tool_name
        if tool_level:
            label = f'{tool_name} · Nivel {tool_level}'

        options.append({'label': label, 'value': tool_key})

    return options


def _build_tool_level_map(*, tools: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(row.get('tool_key') or '').strip(): _normalize_tool_level_value(value=row.get('tool_level'))
        for row in tools
        if str(row.get('tool_key') or '').strip()
    }


def _normalize_tool_level_value(*, value: Any) -> str:
    normalized = str(value or '').strip().lower()
    aliases = {
        '1': '1',
        'n0': '1',
        'nivel_0': '1',
        'nivel 0': '1',
        'sala': '1',
        '2': '2',
        'executive': '2',
        'ejecutiva': '2',
        'ejecutivo': '2',
        '3': '3',
        'n1': '3',
        'ada_n1': '3',
    }
    return aliases.get(normalized, normalized if normalized in {'1', '2', '3'} else '')


def _build_component_options(*, components: list[dict[str, Any]]) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []

    for row in sorted(components, key=lambda item: int(item.get('display_order') or 0)):
        component_name = str(row.get('component_name') or '').strip()
        component_code = str(row.get('component_code') or '').strip()
        component_key = str(row.get('component_key') or '').strip()
        if not component_name or not component_key:
            continue

        position = row.get('position_index')
        label_parts = [component_name]
        if component_code:
            label_parts.append(component_code)
        if position not in (None, ''):
            label_parts.append(f'posición {position}')

        options.append({'label': ' · '.join(label_parts), 'value': component_key})

    return options


def _build_subcomponent_options(
    *,
    components: list[dict[str, Any]],
    subcomponents: list[dict[str, Any]],
) -> list[dict[str, str]]:
    component_names = _build_name_map(
        rows=components,
        key_field='component_key',
        name_field='component_name',
    )
    options: list[dict[str, str]] = []

    for row in sorted(subcomponents, key=lambda item: int(item.get('display_order') or 0)):
        subcomponent_name = str(row.get('subcomponent_name') or '').strip()
        subcomponent_code = str(row.get('subcomponent_code') or '').strip()
        subcomponent_key = str(row.get('subcomponent_key') or '').strip()
        parent_name = component_names.get(str(row.get('parent_component_key') or '').strip())
        if not subcomponent_name or not subcomponent_key:
            continue

        label_parts = []
        if parent_name:
            label_parts.append(parent_name)
        label_parts.append(subcomponent_name)
        if subcomponent_code:
            label_parts.append(subcomponent_code)

        options.append({'label': ' · '.join(label_parts), 'value': subcomponent_key})

    return options


def _build_name_map(*, rows: list[dict[str, Any]], key_field: str, name_field: str) -> dict[str, str]:
    return {
        str(row.get(key_field) or '').strip(): str(row.get(name_field) or '').strip()
        for row in rows
        if str(row.get(key_field) or '').strip() and str(row.get(name_field) or '').strip()
    }


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



def _ensure_level_one_immediate_target(
    *,
    targets: list[dict[str, Any]],
    level_one_tool_key: str,
) -> list[dict[str, Any]]:
    target_tool_key = level_one_tool_key or 'nivel_0'
    updated: list[dict[str, Any]] = []
    found_target = False

    for target in targets:
        normalized_target = dict(target)
        if str(normalized_target.get('target_tool_key') or '') == target_tool_key:
            normalized_target['is_enabled'] = True
            normalized_target['step_order'] = 1
            normalized_target['wait_minutes_from_previous_stage'] = 0
            found_target = True

        updated.append(normalized_target)

    if not found_target:
        updated.append(
            {
                'target_tool_key': target_tool_key,
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
    affected_component_keys = _ensure_list(prepared.get('affected_component_keys'))
    if not affected_component_keys and prepared.get('main_component_key'):
        affected_component_keys = _ensure_list(prepared.get('main_component_key'))

    affected_subcomponent_keys = _ensure_list(prepared.get('affected_subcomponent_keys'))
    if not affected_subcomponent_keys and prepared.get('highlight_target_key'):
        affected_subcomponent_keys = _ensure_list(prepared.get('highlight_target_key'))

    return {
        'tool_key': str(prepared.get('tool_key') or '').strip(),
        'affected_component_keys': affected_component_keys,
        'affected_subcomponent_keys': affected_subcomponent_keys,
        'is_complete': bool(prepared.get('is_complete', False)),
    }


def _resolve_single_n0_visual_target(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not _requires_n0_visual(draft=draft):
        return []

    level_one_tool_key = _resolve_level_one_tool_key(draft=draft)
    for target in targets:
        if str(target.get('tool_key') or '') == level_one_tool_key:
            prepared = dict(target)
            prepared['tool_key'] = level_one_tool_key
            return [prepared]

    if targets:
        prepared = dict(targets[0])
        prepared['tool_key'] = level_one_tool_key
        return [prepared]

    return []



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


def _resolve_single_tool_key_by_level(*, tools: list[dict[str, Any]], tool_level: str) -> str:
    normalized_level = _normalize_tool_level_value(value=tool_level)
    matches = [
        row
        for row in tools
        if _normalize_tool_level_value(value=row.get('tool_level')) == normalized_level
    ]
    if not matches:
        return ''

    matches = sorted(matches, key=lambda item: int(item.get('display_order') or 0))
    return str(matches[0].get('tool_key') or '').strip()


def _resolve_level_one_tool_key(*, draft: dict[str, Any]) -> str:
    catalogs = draft.get('_catalogs') or {}
    configured = str(catalogs.get('level_one_tool_key') or draft.get('level_one_tool_key') or '').strip()
    if configured:
        return configured

    tools = catalogs.get('tools') or []
    if tools:
        resolved = _resolve_single_tool_key_by_level(tools=tools, tool_level='1')
        if resolved:
            return resolved

    return 'nivel_0'


def _is_level_one_tool(*, draft: dict[str, Any], tool_key: str) -> bool:
    catalogs = draft.get('_catalogs') or {}
    tool_level_by_key = catalogs.get('tool_level_by_key') or {}
    return _normalize_tool_level_value(value=tool_level_by_key.get(tool_key)) == '1' or tool_key == _resolve_level_one_tool_key(draft=draft)


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
