from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html


def build_alarm_rule_diagnostics_content(
    *,
    diagnostics: list[Any] | None,
):
    diagnostics = [
        diagnostic
        for diagnostic in diagnostics or []
        if str(diagnostic or '').strip()
    ]

    if not diagnostics:
        return dbc.Alert(
            'Sin diagnósticos bloqueantes.',
            color='success',
            className='mb-0',
        )

    return html.Div(
        children=[
            dbc.Alert(
                str(diagnostic),
                color='warning',
                className='mb-2',
            )
            for diagnostic in diagnostics
        ],
    )