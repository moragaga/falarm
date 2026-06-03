from __future__ import annotations

from typing import Any

from src.features.configuration.alarm.services.alarm_configuration_dependency_service import (
    AlarmConfigurationDependencyService,
    format_dependency_errors,
)


class AlarmAdminReferenceGuardService:
    def __init__(
        self,
        *,
        dependency_service: AlarmConfigurationDependencyService,
    ) -> None:
        self._dependency_service = dependency_service

    def validate_family_rows(
        self,
        *,
        previous_rows: list[dict[str, Any]],
        next_rows: list[dict[str, Any]],
    ) -> list[str]:
        return self._validate_rows(
            previous_rows=previous_rows,
            next_rows=next_rows,
            row_key_field='family_key',
            entity_label='familia',
            get_dependencies=lambda key, active_only: (
                self._dependency_service.get_family_dependencies(
                    family_key=key,
                    active_only=active_only,
                )
            ),
        )

    def validate_tool_rows(
        self,
        *,
        previous_rows: list[dict[str, Any]],
        next_rows: list[dict[str, Any]],
    ) -> list[str]:
        return self._validate_rows(
            previous_rows=previous_rows,
            next_rows=next_rows,
            row_key_field='tool_key',
            entity_label='herramienta',
            get_dependencies=lambda key, active_only: (
                self._dependency_service.get_tool_dependencies(
                    tool_key=key,
                    active_only=active_only,
                )
            ),
        )

    def validate_component_rows(
        self,
        *,
        previous_rows: list[dict[str, Any]],
        next_rows: list[dict[str, Any]],
    ) -> list[str]:
        return self._validate_rows(
            previous_rows=previous_rows,
            next_rows=next_rows,
            row_key_field='component_key',
            entity_label='componente',
            get_dependencies=lambda key, active_only: (
                self._dependency_service.get_component_dependencies(
                    component_key=key,
                    active_only=active_only,
                )
            ),
        )

    def validate_subcomponent_rows(
        self,
        *,
        previous_rows: list[dict[str, Any]],
        next_rows: list[dict[str, Any]],
    ) -> list[str]:
        return self._validate_rows(
            previous_rows=previous_rows,
            next_rows=next_rows,
            row_key_field='subcomponent_key',
            entity_label='subcomponente',
            get_dependencies=lambda key, active_only: (
                self._dependency_service.get_subcomponent_dependencies(
                    subcomponent_key=key,
                    active_only=active_only,
                )
            ),
        )

    @staticmethod
    def _validate_rows(
        *,
        previous_rows: list[dict[str, Any]],
        next_rows: list[dict[str, Any]],
        row_key_field: str,
        entity_label: str,
        get_dependencies,
    ) -> list[str]:
        errors: list[str] = []

        previous_by_key = _build_row_map(
            rows=previous_rows,
            row_key_field=row_key_field,
        )
        next_by_key = _build_row_map(
            rows=next_rows,
            row_key_field=row_key_field,
        )

        deleted_keys = set(previous_by_key) - set(next_by_key)

        for deleted_key in sorted(deleted_keys):
            dependencies = get_dependencies(deleted_key, False)

            errors.extend(
                format_dependency_errors(
                    action='eliminar',
                    entity_label=entity_label,
                    entity_key=deleted_key,
                    dependencies=dependencies,
                )
            )

        for key, previous_row in previous_by_key.items():
            next_row = next_by_key.get(key)

            if next_row is None:
                continue

            was_active = bool(previous_row.get('is_active', True))
            is_active = bool(next_row.get('is_active', True))

            if not was_active or is_active:
                continue

            dependencies = get_dependencies(key, True)

            errors.extend(
                format_dependency_errors(
                    action='desactivar',
                    entity_label=entity_label,
                    entity_key=key,
                    dependencies=dependencies,
                )
            )

        return errors


def _build_row_map(
    *,
    rows: list[dict[str, Any]],
    row_key_field: str,
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}

    for row in rows or []:
        if not isinstance(row, dict):
            continue

        row_key = str(row.get(row_key_field) or '').strip()

        if not row_key:
            continue

        result[row_key] = row

    return result