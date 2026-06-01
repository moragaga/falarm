from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from ..ids import UserSessionAnalyticsPageIds
from .states import build_empty_state, build_initial_state


def build_user_session_user_table_shell() -> dbc.Card:
    return dbc.Card(
        className='user-session-analytics-users-card',
        children=[
            dbc.CardHeader(
                className='user-session-analytics-panel-header',
                children=[
                    html.Div(
                        className='user-session-analytics-panel-title-wrapper',
                        children=[
                            html.I(className='bi bi-person-lines-fill user-session-analytics-panel-icon'),
                            html.Div(
                                children=[
                                    html.Div(
                                        'Usuarios',
                                        className='user-session-analytics-panel-title',
                                    ),
                                    html.Div(
                                        'Detalle de actividad del dashboard principal.',
                                        className='user-session-analytics-panel-subtitle',
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Span(
                        id=UserSessionAnalyticsPageIds.USERS_COUNT,
                        className='user-session-analytics-panel-count',
                        children='0 usuarios',
                    ),
                ],
            ),
            html.Div(
                className='user-session-analytics-table-scroll',
                children=[
                    html.Div(
                        className='user-session-analytics-table-header',
                        children=[
                            html.Div(className='user-session-col-user', children='Usuario'),
                            html.Div(className='user-session-col-profile', children='Perfil'),
                            html.Div(className='user-session-col-sessions', children='Sesiones'),
                            html.Div(className='user-session-col-active-time', children='Tiempo visualizado'),
                            html.Div(className='user-session-col-last-seen', children='Último acceso'),
                            html.Div(className='user-session-col-resolution', children='Resolución más usada'),
                            html.Div(className='user-session-col-device', children='Dispositivo'),
                            html.Div(className='user-session-col-average', children='Promedio'),
                        ],
                    ),
                    html.Div(
                        id=UserSessionAnalyticsPageIds.USERS_TABLE_BODY,
                        className='user-session-analytics-table-body',
                        children=[build_initial_state('Esperando usuarios.')],
                    ),
                ],
            ),
            html.Div(
                className='user-session-analytics-pagination',
                children=[
                    dbc.Button(
                        html.I(className='bi bi-chevron-left'),
                        id=UserSessionAnalyticsPageIds.USERS_PREVIOUS_BUTTON,
                        color='light',
                        size='sm',
                        className='user-session-analytics-pagination-button',
                        n_clicks=0,
                        disabled=True,
                    ),
                    html.Div(
                        id=UserSessionAnalyticsPageIds.USERS_PAGE_TEXT,
                        className='user-session-analytics-pagination-text',
                        children='Página 1 de 1',
                    ),
                    dbc.Button(
                        html.I(className='bi bi-chevron-right'),
                        id=UserSessionAnalyticsPageIds.USERS_NEXT_BUTTON,
                        color='light',
                        size='sm',
                        className='user-session-analytics-pagination-button',
                        n_clicks=0,
                        disabled=True,
                    ),
                ],
            ),
        ],
    )


def build_user_rows(
    *,
    items: list[dict[str, Any]],
    page_size: int,
    has_snapshot: bool,
    empty_by_filter: bool,
) -> list[Any]:
    if not has_snapshot:
        return [build_initial_state('Esperando snapshot de usuarios.')]

    if not items:
        return [build_empty_state(empty_by_filter=empty_by_filter)]

    rows = [_build_user_row(item=item) for item in items]

    filler_count = max(0, page_size - len(items))
    rows.extend(_build_filler_row(index=index) for index in range(filler_count))

    return rows


def _build_user_row(
    *,
    item: dict[str, Any],
) -> html.Div:
    initials = _build_initials(
        display_name=item.get('display_name'),
        email=item.get('email'),
    )

    return html.Div(
        className='user-session-analytics-table-row',
        children=[
            html.Div(
                className='user-session-col-user',
                children=[
                    html.Div(initials, className='user-session-avatar'),
                    html.Div(
                        className='user-session-user-text',
                        children=[
                            html.Div(
                                item.get('display_name') or 'Usuario sin nombre',
                                className='user-session-user-name',
                            ),
                            html.Div(
                                item.get('email') or '',
                                className='user-session-user-email',
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                item.get('profile') or 'Sin perfil',
                className='user-session-col-profile',
            ),
            html.Div(
                str(item.get('sessions') or 0),
                className='user-session-col-sessions',
            ),
            html.Div(
                item.get('active_time_label') or '0s',
                className='user-session-col-active-time',
            ),
            html.Div(
                item.get('last_seen_display') or 'Sin fecha',
                className='user-session-col-last-seen',
            ),
            html.Div(
                item.get('primary_resolution') or 'Sin dato',
                className='user-session-col-resolution',
            ),
            html.Div(
                item.get('primary_device') or 'Sin dato',
                className='user-session-col-device',
            ),
            html.Div(
                item.get('avg_session_label') or '0s',
                className='user-session-col-average',
            ),
        ],
    )


def _build_filler_row(
    *,
    index: int,
) -> html.Div:
    return html.Div(
        key=f'user-session-filler-{index}',
        className='user-session-analytics-table-row user-session-analytics-table-row-filler',
    )


def _build_initials(
    *,
    display_name: object,
    email: object,
) -> str:
    text = str(display_name or '').strip()

    if not text:
        text = str(email or '').split('@')[0].strip()

    if not text:
        return '--'

    parts = [part for part in text.split(' ') if part]

    if len(parts) == 1:
        return parts[0][:2].upper()

    return f'{parts[0][0]}{parts[1][0]}'.upper()