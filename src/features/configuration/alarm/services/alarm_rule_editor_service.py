from __future__ import annotations

import json
from typing import Any

from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.components.definition import (
    ALARM_COMPONENTS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.family.definition import (
    ALARM_FAMILY_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.options import (
    AlarmBusinessCategory,
    AlarmColor,
    AlarmCriticality,
    AlarmKind,
    AlarmToolTier,
    AlarmVisibilityMode,
)
from src.features.configuration.alarm.rules.definition import (
    ALARM_RULES_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.escalation.definition import (
    ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.visualization.definition import (
    ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.row_factory_service import (
    AlarmRuleRowFactoryService,
)
from src.features.configuration.alarm.services.admin_manifest_save_service import (
    AlarmAdminManifestSaveService,
)
from src.features.configuration.alarm.services.alarm_configuration_validation_service import (
    AlarmConfigurationValidationService,
)
from src.features.configuration.alarm.services.alarm_identifier_normalization_service import (
    AlarmIdentifierNormalizationService,
)
from src.features.configuration.alarm.services.alarm_rule_summary_service import (
    AlarmRuleSummaryService,
)
from src.features.configuration.alarm.subcomponents.definition import (
    ALARM_SUBCOMPONENTS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.tools.definition import (
    ALARM_TOOLS_ADMIN_DEFINITION,
)


_RULE_ROW_KEYS = {
    'rule_key',
    'family_key',
    'rule_name',
    'display_name',
    'title_template',
    'cause_template',
    'content_key',
    'kind',
    'criticality_code',
    'business_category',
    'visibility_mode',
    'scope_key',
    'priority_order',
    'origin_tool_key',
    'operator_bucket',
    'color',
    'reappear_if_still_active_enabled',
    'reappear_after_management_minutes',
    'continue_escalation_clock_when_hidden',
    'use_message_management_override',
    'escalation_summary',
    'visual_summary',
    'is_active',
}


class AlarmRuleEditorService:
    def __init__(
        self,
        *,
        data_service: AdminDataService,
    ) -> None:
        self._data_service = data_service

    def load_draft(
        self,
        *,
        rule_key: str | None,
        family_key: str | None,
    ) -> dict[str, Any]:
        rules = self._data_service.load(ALARM_RULES_ADMIN_DEFINITION)
        escalation_targets = self._data_service.load(
            ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
        )
        visual_targets = self._data_service.load(
            ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
        )

        rule = _find_row(
            rows=rules,
            key_field='rule_key',
            key_value=rule_key,
        )

        if rule is None:
            rule = AlarmRuleRowFactoryService.build_new_row(
                current_rows=rules,
            )

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

        draft = self.normalize_live_draft(
            draft=draft,
        )

        draft['_catalogs'] = self._build_catalogs()

        draft['diagnostics'] = (
            AlarmConfigurationValidationService.validate_rule_draft(
                draft=draft,
            )
        )

        return draft

    def save_draft(
        self,
        *,
        draft: dict[str, Any],
    ) -> tuple[bool, list[str], dict[str, Any]]:
        catalogs = self._build_catalogs()

        normalized_draft = self.normalize_runtime_draft(
            draft=draft,
        )
        normalized_draft['_catalogs'] = catalogs

        normalized_draft = self._with_summaries(
            draft=normalized_draft,
            catalogs=catalogs,
        )

        errors = AlarmConfigurationValidationService.validate_rule_draft(
            draft=normalized_draft,
        )

        if errors:
            normalized_draft['diagnostics'] = errors
            return False, errors, normalized_draft

        previous_rule_rows = self._load_rows(
            definition=ALARM_RULES_ADMIN_DEFINITION,
        )

        next_rule_rows = self._upsert_rule_row(
            current_rows=previous_rule_rows,
            draft=normalized_draft,
        )

        if not _rows_equal(previous_rule_rows, next_rule_rows):
            ok, save_errors, saved_rule_rows = self._data_service.save(
                ALARM_RULES_ADMIN_DEFINITION,
                next_rule_rows,
            )

            if not ok:
                return False, save_errors, normalized_draft

            AlarmAdminManifestSaveService.register_update(
                definition=ALARM_RULES_ADMIN_DEFINITION,
                normalized_rows=saved_rule_rows,
            )

        previous_escalation_rows = self._load_rows(
            definition=ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
        )

        next_escalation_rows = self._replace_child_rows(
            definition_rows=previous_escalation_rows,
            rule_key=str(normalized_draft.get('rule_key') or ''),
            child_rows=normalized_draft.get('escalation_targets') or [],
            allowed_keys={
                'rule_key',
                'target_tool_key',
                'is_enabled',
                'step_order',
                'wait_minutes_from_previous_step',
            },
        )

        if not _rows_equal(previous_escalation_rows, next_escalation_rows):
            ok, save_errors, saved_escalation_rows = self._data_service.save(
                ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
                next_escalation_rows,
            )

            if not ok:
                return False, save_errors, normalized_draft

            AlarmAdminManifestSaveService.register_update(
                definition=ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
                normalized_rows=saved_escalation_rows,
            )

        previous_visual_rows = self._load_rows(
            definition=ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
        )

        next_visual_rows = self._replace_child_rows(
            definition_rows=previous_visual_rows,
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

        if not _rows_equal(previous_visual_rows, next_visual_rows):
            ok, save_errors, saved_visual_rows = self._data_service.save(
                ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
                next_visual_rows,
            )

            if not ok:
                return False, save_errors, normalized_draft

            AlarmAdminManifestSaveService.register_update(
                definition=ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
                normalized_rows=saved_visual_rows,
            )

        return True, [], self._build_saved_draft_response(
            draft=normalized_draft,
            catalogs=catalogs,
        )

    def _load_rows(
        self,
        *,
        definition,
    ) -> list[dict[str, Any]]:
        rows = self._data_service.load(definition)

        return [
            row
            for row in rows or []
            if isinstance(row, dict)
        ]

    def _upsert_rule_row(
        self,
        *,
        current_rows: list[dict[str, Any]],
        draft: dict[str, Any],
    ) -> list[dict[str, Any]]:
        rule_key = str(draft.get('rule_key') or '').strip()

        rule_row = {
            key: draft.get(key)
            for key in _RULE_ROW_KEYS
            if key in draft
        }

        updated_rows: list[dict[str, Any]] = []
        replaced = False

        for row in current_rows:
            if str(row.get('rule_key') or '') == rule_key:
                updated_rows.append(rule_row)
                replaced = True
                continue

            updated_rows.append(row)

        if not replaced:
            updated_rows.append(rule_row)

        return updated_rows

    @staticmethod
    def normalize_live_draft(
        *,
        draft: dict[str, Any],
    ) -> dict[str, Any]:
        normalized = dict(draft)

        normalized['rule_key'] = str(normalized.get('rule_key') or '').strip()

        normalized['family_key'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('family_key'),
            )
        )

        normalized['rule_name'] = (
            AlarmIdentifierNormalizationService.normalize_live_identifier(
                normalized.get('rule_name'),
            )
        )

        normalized['display_name'] = str(normalized.get('display_name') or '')
        normalized['title_template'] = str(normalized.get('title_template') or '')
        normalized['cause_template'] = str(normalized.get('cause_template') or '')

        normalized['content_key'] = (
            AlarmIdentifierNormalizationService.normalize_live_identifier(
                normalized.get('content_key'),
            )
        )

        normalized['kind'] = _enum_value_or_default(
            value=normalized.get('kind'),
            allowed_values={item.value for item in AlarmKind},
            default_value=AlarmKind.RISK.value,
        )

        normalized['criticality_code'] = _enum_value_or_default(
            value=normalized.get('criticality_code'),
            allowed_values={item.value for item in AlarmCriticality},
            default_value=AlarmCriticality.C3.value,
        )

        normalized['business_category'] = _enum_value_or_default(
            value=normalized.get('business_category'),
            allowed_values={item.value for item in AlarmBusinessCategory},
            default_value=AlarmBusinessCategory.OPERATIONAL.value,
        )

        normalized['visibility_mode'] = _enum_value_or_default(
            value=normalized.get('visibility_mode'),
            allowed_values={item.value for item in AlarmVisibilityMode},
            default_value=AlarmVisibilityMode.VISIBLE.value,
        )

        normalized['scope_key'] = (
            AlarmIdentifierNormalizationService.normalize_live_identifier(
                normalized.get('scope_key'),
            )
        )

        normalized['origin_tool_key'] = str(
            normalized.get('origin_tool_key') or '',
        ).strip()

        normalized['operator_bucket'] = (
            AlarmIdentifierNormalizationService.normalize_live_identifier(
                normalized.get('operator_bucket'),
            )
        )

        normalized['color'] = _enum_value_or_default(
            value=normalized.get('color'),
            allowed_values={item.value for item in AlarmColor},
            default_value=AlarmColor.YELLOW.value,
        )

        normalized['priority_order'] = _to_int(
            normalized.get('priority_order'),
            default_value=100,
        )

        normalized['reappear_if_still_active_enabled'] = bool(
            normalized.get('reappear_if_still_active_enabled', True),
        )

        normalized['reappear_after_management_minutes'] = _to_optional_int(
            normalized.get('reappear_after_management_minutes'),
        )

        normalized['continue_escalation_clock_when_hidden'] = bool(
            normalized.get('continue_escalation_clock_when_hidden', True),
        )

        normalized['use_message_management_override'] = bool(
            normalized.get('use_message_management_override', True),
        )

        normalized['is_active'] = bool(normalized.get('is_active', True))

        normalized['escalation_targets'] = _normalize_escalation_targets(
            targets=normalized.get('escalation_targets') or [],
            criticality_code=str(normalized.get('criticality_code') or ''),
            visibility_mode=str(normalized.get('visibility_mode') or ''),
            origin_tool_key=str(normalized.get('origin_tool_key') or ''),
        )

        normalized['visual_targets'] = _normalize_visual_targets(
            targets=normalized.get('visual_targets') or [],
            visibility_mode=str(normalized.get('visibility_mode') or ''),
        )

        return normalized

    @staticmethod
    def normalize_runtime_draft(
        *,
        draft: dict[str, Any],
    ) -> dict[str, Any]:
        normalized = dict(draft)

        normalized['rule_key'] = str(normalized.get('rule_key') or '').strip()

        normalized['family_key'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('family_key'),
            )
        )

        normalized['rule_name'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('rule_name'),
            )
        )

        normalized['display_name'] = str(normalized.get('display_name') or '').strip()
        normalized['title_template'] = str(normalized.get('title_template') or '').strip()
        normalized['cause_template'] = str(normalized.get('cause_template') or '').strip()

        normalized['content_key'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('content_key'),
            )
        )

        normalized['kind'] = _enum_value_or_default(
            value=normalized.get('kind'),
            allowed_values={item.value for item in AlarmKind},
            default_value=AlarmKind.RISK.value,
        )

        normalized['criticality_code'] = _enum_value_or_default(
            value=normalized.get('criticality_code'),
            allowed_values={item.value for item in AlarmCriticality},
            default_value=AlarmCriticality.C3.value,
        )

        normalized['business_category'] = _enum_value_or_default(
            value=normalized.get('business_category'),
            allowed_values={item.value for item in AlarmBusinessCategory},
            default_value=AlarmBusinessCategory.OPERATIONAL.value,
        )

        normalized['visibility_mode'] = _enum_value_or_default(
            value=normalized.get('visibility_mode'),
            allowed_values={item.value for item in AlarmVisibilityMode},
            default_value=AlarmVisibilityMode.VISIBLE.value,
        )

        normalized['scope_key'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier(
                normalized.get('scope_key'),
            )
        )

        normalized['origin_tool_key'] = str(
            normalized.get('origin_tool_key') or '',
        ).strip()

        normalized['operator_bucket'] = (
            AlarmIdentifierNormalizationService.normalize_final_identifier_or_default(
                normalized.get('operator_bucket'),
                default_value='default',
            )
        )

        normalized['color'] = _enum_value_or_default(
            value=normalized.get('color'),
            allowed_values={item.value for item in AlarmColor},
            default_value=AlarmColor.YELLOW.value,
        )

        normalized['priority_order'] = _to_int(
            normalized.get('priority_order'),
            default_value=100,
        )

        normalized['reappear_if_still_active_enabled'] = bool(
            normalized.get('reappear_if_still_active_enabled', True),
        )

        normalized['reappear_after_management_minutes'] = _to_optional_int(
            normalized.get('reappear_after_management_minutes'),
        )

        normalized['continue_escalation_clock_when_hidden'] = bool(
            normalized.get('continue_escalation_clock_when_hidden', True),
        )

        normalized['use_message_management_override'] = bool(
            normalized.get('use_message_management_override', True),
        )

        normalized['is_active'] = bool(normalized.get('is_active', True))

        normalized['escalation_targets'] = _normalize_escalation_targets(
            targets=normalized.get('escalation_targets') or [],
            criticality_code=str(normalized.get('criticality_code') or ''),
            visibility_mode=str(normalized.get('visibility_mode') or ''),
            origin_tool_key=str(normalized.get('origin_tool_key') or ''),
        )

        normalized['visual_targets'] = _normalize_visual_targets(
            targets=normalized.get('visual_targets') or [],
            visibility_mode=str(normalized.get('visibility_mode') or ''),
        )

        return normalized

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

        prepared_children: list[dict[str, Any]] = []

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

    def _build_catalogs(
        self,
    ) -> dict[str, Any]:
        families = [
            row
            for row in self._data_service.load(ALARM_FAMILY_ADMIN_DEFINITION)
            if isinstance(row, dict)
        ]

        tools = [
            row
            for row in self._data_service.load(ALARM_TOOLS_ADMIN_DEFINITION)
            if isinstance(row, dict) and bool(row.get('is_active', True))
        ]

        components = [
            row
            for row in self._data_service.load(ALARM_COMPONENTS_ADMIN_DEFINITION)
            if isinstance(row, dict) and bool(row.get('is_active', True))
        ]

        subcomponents = [
            row
            for row in self._data_service.load(ALARM_SUBCOMPONENTS_ADMIN_DEFINITION)
            if isinstance(row, dict) and bool(row.get('is_active', True))
        ]

        return {
            'families': families,
            'family_by_key': {
                str(row.get('family_key') or ''): row
                for row in families
                if row.get('family_key')
            },
            'tools': tools,
            'tool_options': _build_tool_options(tools=tools),
            'tool_name_by_key': _build_name_map(
                rows=tools,
                key_field='tool_key',
                name_field='tool_name',
            ),
            'tool_tier_by_key': _build_tool_tier_map(tools=tools),
            'integrated_operations_tool_keys': _tool_keys_by_tier(
                tools=tools,
                tool_tier=AlarmToolTier.INTEGRATED_OPERATIONS.value,
            ),
            'strategic_tool_keys': _tool_keys_by_tier(
                tools=tools,
                tool_tier=AlarmToolTier.STRATEGIC.value,
            ),
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
            'subcomponent_parent_by_key': {
                str(row.get('subcomponent_key') or ''): str(
                    row.get('parent_component_key') or '',
                )
                for row in subcomponents
                if row.get('subcomponent_key')
            },
        }

    @staticmethod
    def _with_summaries(
        *,
        draft: dict[str, Any],
        catalogs: dict[str, Any],
    ) -> dict[str, Any]:
        prepared = dict(draft)

        prepared['escalation_summary'] = (
            AlarmRuleSummaryService.build_escalation_summary(
                criticality_code=str(prepared.get('criticality_code') or ''),
                visibility_mode=str(prepared.get('visibility_mode') or ''),
                targets=prepared.get('escalation_targets') or [],
                tool_name_by_key=catalogs.get('tool_name_by_key') or {},
            )
        )

        prepared['visual_summary'] = AlarmRuleSummaryService.build_visual_summary(
            visibility_mode=str(prepared.get('visibility_mode') or ''),
            targets=prepared.get('visual_targets') or [],
            component_name_by_key=catalogs.get('component_name_by_key') or {},
            subcomponent_name_by_key=catalogs.get('subcomponent_name_by_key') or {},
        )

        return prepared

    @staticmethod
    def _build_saved_draft_response(
        *,
        draft: dict[str, Any],
        catalogs: dict[str, Any],
    ) -> dict[str, Any]:
        prepared = dict(draft)
        prepared['_catalogs'] = catalogs
        prepared['diagnostics'] = (
            AlarmConfigurationValidationService.validate_rule_draft(
                draft=prepared,
            )
        )

        return prepared


def _normalize_escalation_targets(
    *,
    targets: list[Any],
    criticality_code: str,
    visibility_mode: str,
    origin_tool_key: str,
) -> list[dict[str, Any]]:
    if visibility_mode == AlarmVisibilityMode.TRACE_ONLY.value:
        return []

    if criticality_code != AlarmCriticality.C2.value:
        return []

    if not origin_tool_key:
        return []

    prepared_targets: list[dict[str, Any]] = []

    for target in targets:
        if not isinstance(target, dict):
            continue

        target_tool_key = str(target.get('target_tool_key') or '').strip()

        if not target_tool_key:
            continue

        prepared_targets.append(
            {
                'step_order': _to_int(
                    target.get('step_order'),
                    default_value=len(prepared_targets) + 1,
                ),
                'target_tool_key': target_tool_key,
                'is_enabled': bool(target.get('is_enabled', True)),
                'wait_minutes_from_previous_step': _to_optional_int(
                    target.get('wait_minutes_from_previous_step'),
                ),
            }
        )

    return sorted(
        prepared_targets,
        key=lambda item: int(item.get('step_order') or 0),
    )


def _normalize_visual_targets(
    *,
    targets: list[Any],
    visibility_mode: str,
) -> list[dict[str, Any]]:
    if visibility_mode == AlarmVisibilityMode.TRACE_ONLY.value:
        return []

    prepared_targets: list[dict[str, Any]] = []

    for target in targets:
        if not isinstance(target, dict):
            continue

        tool_key = str(target.get('tool_key') or '').strip()

        if not tool_key:
            continue

        prepared_targets.append(
            {
                'tool_key': tool_key,
                'affected_component_keys': _ensure_list(
                    target.get('affected_component_keys'),
                ),
                'affected_subcomponent_keys': _ensure_list(
                    target.get('affected_subcomponent_keys'),
                ),
                'is_complete': bool(target.get('is_complete')),
            }
        )

    return prepared_targets[:1]


def _build_tool_options(
    *,
    tools: list[dict[str, Any]],
) -> list[dict[str, str]]:
    return [
        {
            'label': str(row.get('tool_name') or row.get('tool_key') or ''),
            'value': str(row.get('tool_key') or ''),
        }
        for row in sorted(
            tools,
            key=lambda item: int(item.get('display_order') or 0),
        )
        if row.get('tool_key')
    ]


def _build_component_options(
    *,
    components: list[dict[str, Any]],
) -> list[dict[str, str]]:
    return [
        {
            'label': str(row.get('component_name') or row.get('component_key') or ''),
            'value': str(row.get('component_key') or ''),
        }
        for row in sorted(
            components,
            key=lambda item: int(item.get('display_order') or 0),
        )
        if row.get('component_key')
    ]


def _build_subcomponent_options(
    *,
    components: list[dict[str, Any]],
    subcomponents: list[dict[str, Any]],
) -> list[dict[str, str]]:
    component_name_by_key = _build_name_map(
        rows=components,
        key_field='component_key',
        name_field='component_name',
    )

    options: list[dict[str, str]] = []

    for row in sorted(
        subcomponents,
        key=lambda item: int(item.get('display_order') or 0),
    ):
        subcomponent_key = str(row.get('subcomponent_key') or '')

        if not subcomponent_key:
            continue

        parent_component_key = str(row.get('parent_component_key') or '')
        parent_name = component_name_by_key.get(parent_component_key, parent_component_key)
        subcomponent_name = str(row.get('subcomponent_name') or subcomponent_key)

        options.append(
            {
                'label': f'{parent_name} · {subcomponent_name}',
                'value': subcomponent_key,
            }
        )

    return options


def _build_name_map(
    *,
    rows: list[dict[str, Any]],
    key_field: str,
    name_field: str,
) -> dict[str, str]:
    return {
        str(row.get(key_field) or ''): str(row.get(name_field) or row.get(key_field) or '')
        for row in rows
        if row.get(key_field)
    }


def _build_tool_tier_map(
    *,
    tools: list[dict[str, Any]],
) -> dict[str, str]:
    return {
        str(row.get('tool_key') or ''): str(row.get('tool_tier') or '')
        for row in tools
        if row.get('tool_key')
    }


def _tool_keys_by_tier(
    *,
    tools: list[dict[str, Any]],
    tool_tier: str,
) -> tuple[str, ...]:
    return tuple(
        str(row.get('tool_key') or '')
        for row in sorted(
            tools,
            key=lambda item: int(item.get('display_order') or 0),
        )
        if str(row.get('tool_tier') or '') == tool_tier and row.get('tool_key')
    )


def _find_row(
    *,
    rows: list[dict[str, Any]],
    key_field: str,
    key_value: str | None,
) -> dict[str, Any] | None:
    normalized_key = str(key_value or '').strip()

    if not normalized_key or normalized_key == 'new':
        return None

    for row in rows:
        if str(row.get(key_field) or '').strip() == normalized_key:
            return row

    return None


def _enum_value_or_default(
    *,
    value: Any,
    allowed_values: set[str],
    default_value: str,
) -> str:
    normalized = str(value or '').strip()

    if normalized in allowed_values:
        return normalized

    return default_value


def _to_int(
    value: Any,
    *,
    default_value: int,
) -> int:
    try:
        return int(value)
    except Exception:
        return default_value


def _to_optional_int(
    value: Any,
) -> int | None:
    if value is None:
        return None

    if value == '':
        return None

    try:
        return int(value)
    except Exception:
        return None


def _ensure_list(
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


def _rows_equal(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
) -> bool:
    return _stable_json(left) == _stable_json(right)


def _stable_json(
    value: Any,
) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )