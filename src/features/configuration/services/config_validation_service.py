"""
Validation and normalization service for configurations.

This module provides a service to validate and normalize data rows based
on an `AdminSchema`. It includes normalization for various field types
and ensures data integrity by enforcing field constraints, such as required
fields and valid options for select or multiselect fields.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from ..models import AdminSchema, FieldDefinition


class ConfigValidationService:
    @staticmethod
    def validate_rows(
        *,
        schema: AdminSchema,
        rows: list[dict[str, Any]] | None,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        errors: list[str] = []
        normalized_rows: list[dict[str, Any]] = []

        for row_index, row in enumerate(rows or [], start=1):
            if not isinstance(row, dict):
                errors.append(f'row {row_index}: invalid row')
                continue

            normalized_row, row_errors = ConfigValidationService.validate_row(
                schema=schema,
                row=row,
                row_index=row_index,
            )

            normalized_rows.append(normalized_row)
            errors.extend(row_errors)

        return normalized_rows, errors

    @staticmethod
    def validate_row(
        *,
        schema: AdminSchema,
        row: dict[str, Any],
        row_index: int | None = None,
    ) -> tuple[dict[str, Any], list[str]]:
        errors: list[str] = []
        normalized_row = deepcopy(row)

        for field in schema.fields:
            value = normalized_row.get(field.name)

            normalized_value, error = ConfigValidationService.normalize_field_value(
                field=field,
                value=value,
            )

            normalized_row[field.name] = normalized_value

            if error:
                prefix = f'row {row_index}: ' if row_index is not None else ''
                errors.append(f'{prefix}{field.label}: {error}')

        return normalized_row, errors

    @staticmethod
    def normalize_field_value(
        *,
        field: FieldDefinition,
        value: Any,
    ) -> tuple[Any, str | None]:
        if field.required and _is_empty(value):
            return value, 'required'

        if field.field_type == 'text':
            return _normalize_text(value), None

        if field.field_type == 'number':
            return _normalize_number(
                value=value,
                required=field.required,
            )

        if field.field_type == 'boolean':
            return _normalize_boolean(value), None

        if field.field_type == 'select':
            return ConfigValidationService._normalize_select_field(
                field=field,
                value=value,
            )

        if field.field_type == 'multiselect':
            return ConfigValidationService._normalize_multiselect_field(
                field=field,
                value=value,
            )

        if field.field_type == 'semicolon_list':
            return ConfigValidationService._normalize_semicolon_list_field(
                field=field,
                value=value,
            )

        return value, None

    @staticmethod
    def _normalize_select_field(
        *,
        field: FieldDefinition,
        value: Any,
    ) -> tuple[str, str | None]:
        normalized = field.normalize_option_value(value)

        if field.required and _is_empty(normalized):
            return normalized, 'required'

        if field.options and not field.is_valid_option_value(normalized):
            return normalized, 'invalid option'

        return normalized, None

    @staticmethod
    def _normalize_multiselect_field(
        *,
        field: FieldDefinition,
        value: Any,
    ) -> tuple[list[str], str | None]:
        normalized = _normalize_list(value)

        if field.required and not normalized:
            return normalized, 'required'

        if not field.options:
            return normalized, None

        valid_options = set(field.get_option_values())

        invalid = [item for item in normalized if item not in valid_options]

        if invalid:
            return normalized, f'invalid options: {invalid}'

        return normalized, None

    @staticmethod
    def _normalize_semicolon_list_field(
        *,
        field: FieldDefinition,
        value: Any,
    ) -> tuple[list[str], str | None]:
        normalized = _normalize_list(value)

        if field.required and not normalized:
            return normalized, 'required'

        if not field.options:
            return normalized, None

        valid_options = set(field.get_option_values())

        invalid = [item for item in normalized if item not in valid_options]

        if invalid:
            return normalized, f'invalid options: {invalid}'

        return normalized, None

    @staticmethod
    def validate(
        *,
        schema: AdminSchema,
        rows: list[dict[str, Any]] | None,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        return ConfigValidationService.validate_rows(
            schema=schema,
            rows=rows,
        )

    @staticmethod
    def normalize_rows(
        *,
        schema: AdminSchema,
        rows: list[dict[str, Any]] | None,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        return ConfigValidationService.validate_rows(
            schema=schema,
            rows=rows,
        )


def _normalize_text(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _normalize_number(
    *,
    value: Any,
    required: bool,
) -> tuple[int | float | None, str | None]:
    if _is_empty(value):
        if required:
            return None, 'required'

        return None, None

    try:
        number = float(value)
    except TypeError, ValueError:
        return value, 'must be numeric'

    if number.is_integer():
        return int(number), None

    return number, None


def _normalize_boolean(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value == 1

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {'true', '1', 'yes', 'y', 'si', 'sí'}:
            return True

        if normalized in {'false', '0', 'no', 'n'}:
            return False

    return False


def _normalize_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return [item.strip() for item in value.split(';') if item and item.strip()]

    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if item is not None and str(item).strip()]

    return []


def _is_empty(value: Any) -> bool:
    if value is None:
        return True

    if isinstance(value, str):
        return not value.strip()

    if isinstance(value, list):
        return len(value) == 0

    return False
