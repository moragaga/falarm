from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.features.admin_framework.models import AdminDefinition
from src.features.admin_framework.services import AdminDataService


class AlarmGuardedAdminDataService:
    def __init__(
        self,
        *,
        delegate: AdminDataService,
        validate_rows: Callable[
            [list[dict[str, Any]], list[dict[str, Any]]],
            list[str],
        ],
        normalize_rows: Callable[..., list[dict[str, Any]]] | None = None,
    ) -> None:
        self._delegate = delegate
        self._validate_rows = validate_rows
        self._normalize_rows = normalize_rows

    def load(
        self,
        definition: AdminDefinition,
    ) -> list[dict[str, Any]]:
        rows = self._delegate.load(definition)

        prepared_rows = [
            row
            for row in rows or []
            if isinstance(row, dict)
        ]

        if self._normalize_rows is None:
            return prepared_rows

        return self._normalize_rows(rows=prepared_rows)

    def save(
        self,
        definition: AdminDefinition,
        rows: list[dict[str, Any]],
    ):
        previous_rows = self.load(definition)

        next_rows = [
            row
            for row in rows or []
            if isinstance(row, dict)
        ]

        if self._normalize_rows is not None:
            next_rows = self._normalize_rows(rows=next_rows)

        errors = self._validate_rows(
            previous_rows,
            next_rows,
        )

        if errors:
            return False, errors, previous_rows

        return self._delegate.save(
            definition,
            next_rows,
        )