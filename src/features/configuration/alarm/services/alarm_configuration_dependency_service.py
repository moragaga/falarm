from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.features.configuration.alarm.rules.definition import (
    ALARM_RULES_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.escalation.definition import (
    ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.visualization.definition import (
    ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.subcomponents.definition import (
    ALARM_SUBCOMPONENTS_ADMIN_DEFINITION,
)


@dataclass(frozen=True, slots=True)
class AlarmConfigurationDependency:
    source: str
    source_key: str
    field_name: str
    usage: str


class AlarmConfigurationDependencyService:
    def __init__(
        self,
        *,
        data_service,
    ) -> None:
        self._data_service = data_service

    def get_family_dependencies(
        self,
        *,
        family_key: str,
        active_only: bool = False,
    ) -> list[AlarmConfigurationDependency]:
        rules = self._load_rows(ALARM_RULES_ADMIN_DEFINITION)
        dependencies: list[AlarmConfigurationDependency] = []

        for rule in rules:
            if str(rule.get('family_key') or '') != family_key:
                continue

            if active_only and not bool(rule.get('is_active', True)):
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Reglas',
                    source_key=str(rule.get('rule_name') or rule.get('rule_key') or ''),
                    field_name='family_key',
                    usage='La regla pertenece a esta familia.',
                )
            )

        return dependencies

    def get_tool_dependencies(
        self,
        *,
        tool_key: str,
        active_only: bool = False,
    ) -> list[AlarmConfigurationDependency]:
        rules = self._load_rows(ALARM_RULES_ADMIN_DEFINITION)
        escalation_targets = self._load_rows(
            ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
        )
        visual_targets = self._load_rows(
            ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
        )

        active_rule_keys = self._resolve_active_rule_keys(rules=rules)
        dependencies: list[AlarmConfigurationDependency] = []

        for rule in rules:
            if active_only and not bool(rule.get('is_active', True)):
                continue

            if str(rule.get('origin_tool_key') or '') != tool_key:
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Reglas',
                    source_key=str(rule.get('rule_name') or rule.get('rule_key') or ''),
                    field_name='origin_tool_key',
                    usage='La herramienta está configurada como herramienta inicial.',
                )
            )

        for target in escalation_targets:
            rule_key = str(target.get('rule_key') or '')

            if active_only and rule_key not in active_rule_keys:
                continue

            if str(target.get('target_tool_key') or '') != tool_key:
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Escalamiento',
                    source_key=rule_key,
                    field_name='target_tool_key',
                    usage='La herramienta está configurada como destino de escalamiento.',
                )
            )

        for target in visual_targets:
            rule_key = str(target.get('rule_key') or '')

            if active_only and rule_key not in active_rule_keys:
                continue

            if str(target.get('tool_key') or '') != tool_key:
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Visualización',
                    source_key=rule_key,
                    field_name='tool_key',
                    usage='La herramienta está configurada como herramienta de visualización.',
                )
            )

        return dependencies

    def get_component_dependencies(
        self,
        *,
        component_key: str,
        active_only: bool = False,
    ) -> list[AlarmConfigurationDependency]:
        subcomponents = self._load_rows(ALARM_SUBCOMPONENTS_ADMIN_DEFINITION)
        visual_targets = self._load_rows(
            ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
        )
        rules = self._load_rows(ALARM_RULES_ADMIN_DEFINITION)
        active_rule_keys = self._resolve_active_rule_keys(rules=rules)

        dependencies: list[AlarmConfigurationDependency] = []

        for subcomponent in subcomponents:
            if active_only and not bool(subcomponent.get('is_active', True)):
                continue

            if str(subcomponent.get('parent_component_key') or '') != component_key:
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Subcomponentes',
                    source_key=str(
                        subcomponent.get('subcomponent_name')
                        or subcomponent.get('subcomponent_key')
                        or ''
                    ),
                    field_name='parent_component_key',
                    usage='El componente tiene subcomponentes asociados.',
                )
            )

        for target in visual_targets:
            rule_key = str(target.get('rule_key') or '')

            if active_only and rule_key not in active_rule_keys:
                continue

            affected_component_keys = _ensure_list(
                target.get('affected_component_keys'),
            )

            if component_key not in affected_component_keys:
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Visualización',
                    source_key=rule_key,
                    field_name='affected_component_keys',
                    usage='El componente está usado en una visualización de regla.',
                )
            )

        return dependencies

    def get_subcomponent_dependencies(
        self,
        *,
        subcomponent_key: str,
        active_only: bool = False,
    ) -> list[AlarmConfigurationDependency]:
        visual_targets = self._load_rows(
            ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
        )
        rules = self._load_rows(ALARM_RULES_ADMIN_DEFINITION)
        active_rule_keys = self._resolve_active_rule_keys(rules=rules)

        dependencies: list[AlarmConfigurationDependency] = []

        for target in visual_targets:
            rule_key = str(target.get('rule_key') or '')

            if active_only and rule_key not in active_rule_keys:
                continue

            affected_subcomponent_keys = _ensure_list(
                target.get('affected_subcomponent_keys'),
            )

            if subcomponent_key not in affected_subcomponent_keys:
                continue

            dependencies.append(
                AlarmConfigurationDependency(
                    source='Visualización',
                    source_key=rule_key,
                    field_name='affected_subcomponent_keys',
                    usage='El subcomponente está usado en una visualización de regla.',
                )
            )

        return dependencies

    def _load_rows(
        self,
        definition,
    ) -> list[dict[str, Any]]:
        rows = self._data_service.load(definition)

        return [
            row
            for row in rows or []
            if isinstance(row, dict)
        ]

    @staticmethod
    def _resolve_active_rule_keys(
        *,
        rules: list[dict[str, Any]],
    ) -> set[str]:
        return {
            str(rule.get('rule_key') or '')
            for rule in rules
            if bool(rule.get('is_active', True)) and rule.get('rule_key')
        }


def format_dependency_errors(
    *,
    action: str,
    entity_label: str,
    entity_key: str,
    dependencies: list[AlarmConfigurationDependency],
) -> list[str]:
    if not dependencies:
        return []

    detail = '; '.join(
        f'{dependency.source}: {dependency.source_key} ({dependency.usage})'
        for dependency in dependencies
    )

    return [
        (
            f'No se puede {action} {entity_label} "{entity_key}" porque tiene '
            f'dependencias activas: {detail}'
        )
    ]


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