from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html


def build_kpi_cards(
    *,
    kpis: dict[str, Any],
) -> list[Any]:
    return [
        _build_kpi_card(
            label='Sesiones totales',
            value=_safe_str(kpis.get('sessions_total', {}).get('current_label')),
            delta=_safe_str(kpis.get('sessions_total', {}).get('delta_label')),
            icon_class_name='bi bi-door-open',
        ),
        _build_kpi_card(
            label='Usuarios únicos',
            value=_safe_str(kpis.get('unique_users', {}).get('current_label')),
            delta=_safe_str(kpis.get('unique_users', {}).get('delta_label')),
            icon_class_name='bi bi-people',
        ),
        _build_kpi_card(
            label='Tiempo promedio por sesión',
            value=_safe_str(kpis.get('avg_session_seconds', {}).get('current_label')),
            delta=_safe_str(kpis.get('avg_session_seconds', {}).get('delta_label')),
            icon_class_name='bi bi-stopwatch',
        ),
        _build_kpi_card(
            label='Tiempo total visualizado',
            value=_safe_str(kpis.get('total_active_seconds', {}).get('current_label')),
            delta=_safe_str(kpis.get('total_active_seconds', {}).get('delta_label')),
            icon_class_name='bi bi-clock-history',
        ),
        _build_kpi_card(
            label='Usuarios recurrentes',
            value=_safe_str(kpis.get('recurring_users_pct', {}).get('current_label')),
            delta=_safe_str(kpis.get('recurring_users_pct', {}).get('delta_label')),
            icon_class_name='bi bi-arrow-repeat',
        ),
    ]


def build_summary_items(
    *,
    summary: dict[str, Any],
) -> list[Any]:
    if not summary:
        return []

    return [
        _build_summary_row(
            icon_class_name='bi bi-calendar-check',
            label='Día con mayor actividad',
            value=_safe_str(summary.get('most_active_day', {}).get('value')),
        ),
        _build_summary_row(
            icon_class_name='bi bi-person-badge',
            label='Perfil más usado',
            value=_safe_str(summary.get('top_profile', {}).get('value')),
        ),
        _build_summary_row(
            icon_class_name='bi bi-display',
            label='Resolución más usada',
            value=_safe_str(summary.get('top_resolution', {}).get('value')),
        ),
        _build_summary_row(
            icon_class_name='bi bi-pc-display-horizontal',
            label='Dispositivo más usado',
            value=_safe_str(summary.get('top_device', {}).get('value')),
        ),
        _build_summary_row(
            icon_class_name='bi bi-clock',
            label='Mayor uso entre',
            value=_safe_str(summary.get('peak_usage_range', {}).get('value')),
        ),
    ]


def build_device_resolution_panel(
    *,
    device_resolution: dict[str, Any],
) -> list[Any]:
    devices = _as_list(device_resolution.get('devices'))
    resolutions = _as_list(device_resolution.get('resolutions'))

    return [
        html.Div(
            className='user-session-analytics-device-section',
            children=[
                html.Div(
                    'Por dispositivo',
                    className='user-session-analytics-small-title',
                ),
                html.Div(
                    className='user-session-analytics-ranking',
                    children=[
                        _build_distribution_row(
                            label=_safe_str(item.get('label')),
                            value=_safe_str(item.get('value_label')),
                            pct=_safe_str(item.get('pct_label')),
                        )
                        for item in devices
                    ],
                ),
            ],
        ),
        html.Div(
            className='user-session-analytics-resolution-section',
            children=[
                html.Div(
                    'Resoluciones más usadas',
                    className='user-session-analytics-small-title',
                ),
                html.Div(
                    className='user-session-analytics-ranking',
                    children=[
                        _build_distribution_row(
                            label=_safe_str(item.get('label')),
                            value=_safe_str(item.get('value_label')),
                            pct=_safe_str(item.get('pct_label')),
                        )
                        for item in resolutions
                    ],
                ),
            ],
        ),
    ]


def _build_kpi_card(
    *,
    label: str,
    value: str,
    delta: str,
    icon_class_name: str,
) -> dbc.Card:
    return dbc.Card(
        className='user-session-analytics-kpi-card',
        children=[
            html.Div(
                className='user-session-analytics-kpi-icon',
                children=[
                    html.I(className=icon_class_name),
                ],
            ),
            html.Div(
                className='user-session-analytics-kpi-content',
                children=[
                    html.Div(
                        value or '0',
                        className='user-session-analytics-kpi-value',
                    ),
                    html.Div(
                        label,
                        className='user-session-analytics-kpi-label',
                    ),
                    html.Div(
                        delta or 'Sin comparación',
                        className='user-session-analytics-kpi-delta',
                    ),
                ],
            ),
        ],
    )


def _build_summary_row(
    *,
    icon_class_name: str,
    label: str,
    value: str,
) -> html.Div:
    return html.Div(
        className='user-session-analytics-summary-row',
        children=[
            html.Div(
                className='user-session-analytics-summary-icon',
                children=[html.I(className=icon_class_name)],
            ),
            html.Div(
                className='user-session-analytics-summary-text',
                children=[
                    html.Div(label, className='user-session-analytics-summary-label'),
                    html.Div(value or 'Sin datos', className='user-session-analytics-summary-value'),
                ],
            ),
        ],
    )


def _build_distribution_row(
    *,
    label: str,
    value: str,
    pct: str,
) -> html.Div:
    return html.Div(
        className='user-session-analytics-distribution-row',
        children=[
            html.Div(label or 'Sin dato', className='user-session-analytics-distribution-label'),
            html.Div(
                className='user-session-analytics-distribution-values',
                children=[
                    html.Span(value or '0'),
                    html.Span(pct or '0%'),
                ],
            ),
        ],
    )


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []