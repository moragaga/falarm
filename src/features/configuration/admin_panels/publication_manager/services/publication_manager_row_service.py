"""
Provides services for preparing rows related to publications.

The module includes methods to transform and filter input data
to a standardized format for publication management.
"""

from __future__ import annotations

from typing import Any

from src.shared.ui.grid.constants import GRID_ROW_UID_FIELD


class PublicationManagerRowService:
    @staticmethod
    def prepare_rows(
        *,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        prepared_rows: list[dict[str, Any]] = []

        for row in rows:
            if not isinstance(row, dict):
                continue

            artifact_key = str(row.get('artifact_key') or '').strip()

            if not artifact_key:
                continue

            prepared_row = dict(row)
            prepared_row[GRID_ROW_UID_FIELD] = artifact_key
            prepared_rows.append(prepared_row)

        return prepared_rows
