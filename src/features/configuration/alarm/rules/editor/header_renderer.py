from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html


def build_alarm_rule_editor_header(
    *,
    draft: dict[str, Any] | None,
):
    draft = draft or {}
    diagnostics = _resolve_diagnostics(draft=draft)
    diagnostic_count = len(diagnostics)

    badge_label, badge_color = _resolve_badge(
        diagnostic_count=diagnostic_count,
    )

    return html.Div(
        className='d-flex justify-content-between align-items-start gap-3',
        children=[
            html.Div(
                children=[
                    html.H4(
                        _resolve_title(draft=draft),
                        className='mb-1',
                    ),
                    html.Div(
                        _resolve_subtitle(draft=draft),
                        className='text-muted small',
                    ),
                ],
            ),
            dbc.Badge(
                badge_label,
                color=badge_color,
                pill=True,
                className='px-3 py-2',
            ),
        ],
    )


def _resolve_title(
    *,
    draft: dict[str, Any],
) -> str:
    display_name = str(draft.get('display_name') or '').strip()

    if display_name:
        return display_name

    return 'Nueva regla'


def _resolve_subtitle(
    *,
    draft: dict[str, Any],
) -> str:
    family_label = _resolve_family_label(draft=draft)
    rule_name = str(draft.get('rule_name') or '').strip()
    rule_key = str(draft.get('rule_key') or '').strip()

    rule_label = rule_name or rule_key

    parts = [
        value
        for value in (family_label, rule_label)
        if value
    ]

    if not parts:
        return 'Sin identificadores configurados'

    return ' · '.join(parts)


def _resolve_family_label(
    *,
    draft: dict[str, Any],
) -> str:
    family_key = str(draft.get('family_key') or '').strip()

    if not family_key:
        return ''

    catalogs = draft.get('_catalogs') or {}
    family_by_key = catalogs.get('family_by_key') or {}
    family = family_by_key.get(family_key)

    if isinstance(family, dict):
        family_name = str(family.get('family_name') or '').strip()

        if family_name:
            return family_name

    return family_key


def _resolve_badge(
    *,
    diagnostic_count: int,
) -> tuple[str, str]:
    if diagnostic_count == 0:
        return 'Sin diagnóstico', 'success'

    if diagnostic_count == 1:
        return '1 diagnóstico', 'warning'

    return f'{diagnostic_count} diagnósticos', 'warning'


def _resolve_diagnostics(
    *,
    draft: dict[str, Any],
) -> list[Any]:
    return [
        diagnostic
        for diagnostic in draft.get('diagnostics') or []
        if str(diagnostic or '').strip()
    ]