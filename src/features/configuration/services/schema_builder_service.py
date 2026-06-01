"""
Services for dynamically building and manipulating admin schemas.

Provides methods to create column definitions, format rows for grids,
normalize rows for saving, and build empty rows for a given schema.
Certain private utility functions are also included for internal processing
of schema and field data.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from ..models import AdminSchema, FieldDefinition


class SchemaBuilderService:
    @staticmethod
    def build_column_defs(schema: AdminSchema) -> list[dict[str, Any]]:
        column_defs: list[dict[str, Any]] = []

        for field in schema.fields:
            column: dict[str, Any] = {
                'field': field.name,
                'headerName': field.label,
                'editable': field.editable and field.field_type != 'multiselect',
                'filter': True,
                'sortable': True,
                'resizable': True,
            }

            if field.help_text:
                column['headerTooltip'] = field.help_text

            if field.field_type == 'boolean':
                column.update(
                    {
                        'cellEditor': 'agCheckboxCellEditor',
                        'cellRenderer': 'agCheckboxCellRenderer',
                    }
                )

            if field.field_type == 'select' and field.options:
                column.update(
                    SchemaBuilderService._build_select_column_options(
                        field=field,
                    )
                )

            if field.field_type == 'multiselect':
                column.update(
                    {
                        'editable': False,
                        'valueFormatter': {
                            'function': (
                                "Array.isArray(params.value) ? params.value.join(', ') : ''"
                            )
                        },
                    }
                )

            column_defs.append(column)

        return column_defs

    @staticmethod
    def build_empty_row(schema: AdminSchema) -> dict[str, Any]:
        row: dict[str, Any] = {}

        for field in schema.fields:
            row[field.name] = deepcopy(field.default_value)

        return row

    @staticmethod
    def format_rows_for_grid(
        *,
        schema: AdminSchema,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        formatted_rows: list[dict[str, Any]] = []

        select_fields = [
            field for field in schema.fields if field.field_type == 'select' and field.options
        ]

        for row in rows or []:
            if not isinstance(row, dict):
                continue

            formatted_row = deepcopy(row)

            for field in select_fields:
                formatted_row[field.name] = SchemaBuilderService._format_select_value_for_grid(
                    field=field,
                    value=formatted_row.get(field.name),
                )

            formatted_rows.append(formatted_row)

        return formatted_rows

    @staticmethod
    def normalize_rows_for_save(
        *,
        schema: AdminSchema,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        normalized_rows: list[dict[str, Any]] = []

        select_fields = [
            field for field in schema.fields if field.field_type == 'select' and field.options
        ]

        for row in rows or []:
            if not isinstance(row, dict):
                continue

            normalized_row = deepcopy(row)

            for field in select_fields:
                normalized_row[field.name] = field.normalize_option_value(
                    normalized_row.get(field.name)
                )

            normalized_rows.append(normalized_row)

        return normalized_rows

    @staticmethod
    def _format_select_value_for_grid(
        *,
        field: FieldDefinition,
        value: Any,
    ) -> str:
        raw_value = str(value or '').strip()
        label_by_value = field.get_option_label_by_value()

        return label_by_value.get(raw_value, raw_value)

    @staticmethod
    def _build_select_column_options(
        *,
        field: FieldDefinition,
    ) -> dict[str, Any]:
        option_labels = field.get_option_labels()
        label_by_value = field.get_option_label_by_value()
        value_by_label = field.get_option_value_by_label()

        return {
            'cellEditor': 'agSelectCellEditor',
            'cellEditorParams': {
                'values': option_labels,
            },
            'valueFormatter': {
                'function': _build_select_value_formatter(
                    label_by_value=label_by_value,
                ),
            },
            'valueParser': {
                'function': _build_select_value_parser(
                    value_by_label=value_by_label,
                ),
            },
        }


def _build_select_value_formatter(
    *,
    label_by_value: dict[str, str],
) -> str:
    serialized_labels = json.dumps(
        label_by_value,
        ensure_ascii=False,
    )

    value_expression = "(params.value == null ? '' : params.value)"

    return (
        f'Object.prototype.hasOwnProperty.call(({serialized_labels}), {value_expression}) '
        f'? ({serialized_labels})[{value_expression}] '
        f': {value_expression}'
    )


def _build_select_value_parser(
    *,
    value_by_label: dict[str, str],
) -> str:
    serialized_values = json.dumps(
        value_by_label,
        ensure_ascii=False,
    )

    value_expression = "(params.newValue == null ? '' : params.newValue)"

    return (
        f'Object.prototype.hasOwnProperty.call(({serialized_values}), {value_expression}) '
        f'? ({serialized_values})[{value_expression}] '
        f': {value_expression}'
    )
