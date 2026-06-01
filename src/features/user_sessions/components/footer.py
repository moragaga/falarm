from __future__ import annotations

from dash import html

def build_user_session_analytics_footer() -> html.Div:
    return html.Div(
        className='user-session-analytics-footer',
        children=[
            html.Div(
                className='user-session-analytics-footer-note',
                children=[
                    html.I(className='bi bi-info-circle'),
                    html.Span('Perfil, dispositivo, resolución y administrador afectan toda la vista.'),
                ],
            ),
        ]
    )