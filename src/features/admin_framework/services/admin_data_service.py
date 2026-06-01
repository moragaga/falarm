"""
This module provides functionality for handling and managing administrative
data services. It integrates configuration repositories with admin definitions
to perform data loading, validation, and saving tasks.
"""

from __future__ import annotations

from src.features.configuration.repositories import (
    ConfigurationSharepointRepository,
)
from src.features.configuration.services import ConfigService

from ..models.admin_definition import AdminDefinition


class AdminDataService:
    def __init__(
        self,
        repository: ConfigurationSharepointRepository | None = None,
        config_service: ConfigService | None = None,
    ) -> None:
        self._repository = repository
        self._config_service = config_service or ConfigService()

    def load(self, definition: AdminDefinition) -> list[dict]:
        if self._repository is None or definition.remote is None:
            return []

        rows = self._repository.load_rows(
            filename=definition.remote.sharepoint_filename,
            relative_path=definition.remote.relative_path,
        )

        return self._prepare_rows_for_ui(definition=definition, rows=rows)

    def save(
        self, definition: AdminDefinition, rows: list[dict]
    ) -> tuple[bool, list[str], list[dict]]:
        normalized_rows = list(rows or [])
        errors: list[str] = []

        if definition.schema is not None:
            normalized_rows, errors = self._config_service.validate_and_normalize(
                schema=definition.schema,
                rows=normalized_rows,
            )

        if errors:
            return False, errors, normalized_rows

        if self._repository is None or definition.remote is None:
            return False, ['Configuration repository is not created'], normalized_rows

        ok = self._repository.save_rows(
            filename=definition.remote.sharepoint_filename,
            relative_path=definition.remote.relative_path,
            rows=normalized_rows,
        )

        if not ok:
            return False, ['Configuration could not be persisted'], normalized_rows

        ui_rows = self._prepare_rows_for_ui(definition=definition, rows=normalized_rows)
        return True, [], ui_rows

    @staticmethod
    def _prepare_rows_for_ui(definition: AdminDefinition, rows: list[dict]) -> list[dict]:
        if definition.schema is None:
            return list(rows or [])

        prepared_rows: list[dict] = []

        for row in rows or []:
            prepared_row = dict(row)

            for field in definition.schema.fields:
                if field.field_type == 'semicolon_list':
                    value = prepared_row.get(field.name)

                    if isinstance(value, list):
                        prepared_row[field.name] = ';'.join(
                            str(item).strip()
                            for item in value
                            if item is not None and str(item).strip()
                        )

            prepared_rows.append(prepared_row)

        return prepared_rows
