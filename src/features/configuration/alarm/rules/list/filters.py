from __future__ import annotations

from typing import Any


def filter_rule_rows(
    *,
    rows: list[dict[str, Any]] | None,
    family_key: str | None,
) -> list[dict[str, Any]]:
    normalized_family = str(family_key or '').strip()
    filtered_rows: list[dict[str, Any]] = []

    for row in rows or []:
        if not isinstance(row, dict):
            continue

        if normalized_family and str(row.get('family_key') or '').strip() != normalized_family:
            continue

        filtered_rows.append(row)

    return filtered_rows
