from __future__ import annotations

from dash import html


def build_initial_state(message: str = 'Esperando datos.') -> html.Div:
    return html.Div(
        className='user-session-analytics-empty-state',
        children=[
            html.I(className='bi bi-hourglass-split'),
            html.Div(message),
        ],
    )


def build_empty_state(
    *,
    empty_by_filter: bool,
) -> html.Div:
    message = (
        'No hay usuarios que coincidan con los filtros aplicados.'
        if empty_by_filter
        else 'No hay datos de usuarios en la ventana analítica.'
    )

    return html.Div(
        className='user-session-analytics-empty-state',
        children=[
            html.I(className='bi bi-inbox'),
            html.Div(message),
        ],
    )