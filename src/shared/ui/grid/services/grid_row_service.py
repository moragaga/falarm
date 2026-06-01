"""
Provides services and utility functions for managing grid rows, including
operations like attaching unique IDs, cleaning up technical fields, and
manipulating rows.

This module is designed to operate on lists of dictionaries, often used as
representations of rows in a grid or table structure. It includes methods
to handle technical fields, manage unique identifiers, and perform CRUD-style
operations on rows.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4

from src.shared.ui.grid.constants import GRID_ROW_UID_FIELD


class GridRowService:
    @staticmethod
    def attach_row_uids(
        *,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        prepared_rows: list[dict[str, Any]] = []

        for row in rows or []:
            if not isinstance(row, dict):
                continue

            prepared_row = deepcopy(row)
            prepared_row[GRID_ROW_UID_FIELD] = prepared_row.get(GRID_ROW_UID_FIELD) or uuid4().hex
            prepared_rows.append(prepared_row)

        return prepared_rows

    @staticmethod
    def attach_uid_to_row(
        *,
        row: dict[str, Any],
    ) -> dict[str, Any]:
        prepared_row = deepcopy(row)
        prepared_row[GRID_ROW_UID_FIELD] = prepared_row.get(GRID_ROW_UID_FIELD) or uuid4().hex
        return prepared_row

    @staticmethod
    def strip_technical_fields(
        *,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        cleaned_rows: list[dict[str, Any]] = []

        for row in rows or []:
            if not isinstance(row, dict):
                continue

            cleaned_rows.append(
                {key: value for key, value in row.items() if key != GRID_ROW_UID_FIELD}
            )

        return cleaned_rows

    @staticmethod
    def append_row(
        *,
        rows: list[dict[str, Any]] | None,
        row: dict[str, Any],
    ) -> list[dict[str, Any]]:
        prepared_rows = GridRowService.attach_row_uids(rows=rows)
        prepared_rows.append(GridRowService.attach_uid_to_row(row=row))
        return prepared_rows

    @staticmethod
    def delete_selected_rows(
        *,
        rows: list[dict[str, Any]] | None,
        selected_rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        prepared_rows = GridRowService.attach_row_uids(rows=rows)

        selected_uids = {
            str(row.get(GRID_ROW_UID_FIELD) or '')
            for row in selected_rows or []
            if isinstance(row, dict)
        }

        if not selected_uids:
            return prepared_rows

        return [
            row
            for row in prepared_rows
            if str(row.get(GRID_ROW_UID_FIELD) or '') not in selected_uids
        ]

    @staticmethod
    def prepend_technical_uid_column(
        *,
        column_defs: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        has_uid_column = any(column.get('field') == GRID_ROW_UID_FIELD for column in column_defs)

        if has_uid_column:
            return column_defs

        return [
            {
                'field': GRID_ROW_UID_FIELD,
                'hide': True,
                'editable': False,
                'suppressColumnsToolPanel': True,
            },
            *column_defs,
        ]
