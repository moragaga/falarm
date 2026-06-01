from __future__ import annotations

from typing import Any


def build_options_from_rows(
    *,
    rows: list[dict[str, Any]],
    label_field: str,
    value_field: str,
) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []

    for row in rows:
        label = str(row.get(label_field) or '').strip()
        value = str(row.get(value_field) or '').strip()

        if not label or not value:
            continue

        options.append(
            {
                'label': label,
                'value': value,
            }
        )

    return options
