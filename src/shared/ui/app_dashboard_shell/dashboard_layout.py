"""
Builds and returns the layout structure for a dashboard application.

This function generates a complete layout for a dashboard application using Dash
components. The layout includes a header, information displays, alarm regions (if
enabled), multiple configurable content regions, modal dialogs, and various data
stores for managing runtime state. Additionally, the layout incorporates loading
overlays and periodic interval updates for refreshing dashboard and alarms.

Parameters
----------
dashboard_definition : DashboardShellDefinition
    Configuration object defining dashboard settings, including refresh intervals.
alarm_definition : AlarmShellDefinition
    Configuration object defining alarm settings, including refresh intervals and
    visibility options.
header_children : list, optional
    List of Dash components to be included in the dashboard's header section. Defaults
    to an empty list.
information_children : list, optional
    List of Dash components for displaying information in the dedicated information
    section. Defaults to an empty list.
alarms_children : list, optional
    List of Dash components to be displayed in the alarms section, if alarms are
    enabled. Defaults to an empty list.
left_region_children : list, optional
    List of Dash components to be included in the left region of the dashboard. Defaults
    to an empty list.
center_region_children : list, optional
    List of Dash components to be included in the center region of the dashboard.
    Defaults to an empty list.
right_region_children : list, optional
    List of Dash components to be included in the right region of the dashboard.
    Defaults to an empty list.
modals_children : list, optional
    List of Dash modal components for overlays in the dashboard. Defaults to an
    empty list.

Returns
-------
list
    A list of Dash components forming the entire dashboard layout, including interval
    updaters, state stores, loading overlays, and the main content structure.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.features.dashboards.home.services.runtime_refresh import (
    build_released_lock as dashboard_build_released_lock,
)

from ..app_alarm_shell.ids import AlarmShellIds
from ..app_alarm_shell.models import AlarmShellDefinition
from ..modals.time_series.ids import TimeSeriesModalIds
from .ids import DashboardShellIds
from .models import DashboardShellDefinition
from .region_shell import build_region_shell


def build_dashboard_layout(
    *,
    dashboard_definition: DashboardShellDefinition,
    alarm_definition: AlarmShellDefinition,
    header_children=None,
    information_children=None,
    alarms_children=None,
    left_region_children=None,
    center_region_children=None,
    right_region_children=None,
    modals_children=None,
):
    header_children = header_children or []
    information_children = information_children or []
    alarms_children = alarms_children or []
    left_region_children = left_region_children or []
    center_region_children = center_region_children or []
    right_region_children = right_region_children or []
    modals_children = modals_children or []

    main_children = [
        html.Div(
            id=DashboardShellIds.INFORMATION,
            children=information_children,
        )
    ]

    regions = []
    for ids, content, width in (
        (DashboardShellIds.LEFT_REGION, left_region_children, 2),
        (DashboardShellIds.CENTER_REGION, center_region_children, 8),
        (DashboardShellIds.RIGHT_REGION, right_region_children, 2),
    ):
        regions.append(
            build_region_shell(
                region_id=ids,
                **dict.fromkeys(['width_sm', 'width_md', 'width_lg', 'width_xl'], width),
                children=content,
            )
        )

    main_children.append(
        html.Div(
            id=DashboardShellIds.BODY,
            children=[
                dbc.Container(
                    fluid=True,
                    className='px-2',
                    children=[dbc.Row(className='g-1', children=regions)],
                )
            ],
        )
    )

    dashboard_content = html.Div(
        id=DashboardShellIds.ROOT,
        children=[
            html.Header(
                id=DashboardShellIds.HEADER,
                children=header_children,
            ),
            html.Main(
                children=main_children,
            ),
        ],
    )

    dashboard_loader_scope = html.Div(
        id='main-page-loader-scope',
        className='page-loader-scope is-loading',
        **{
            'data-page-loader': 'true',
            'data-loader-key': 'main-dashboard',
        },
        children=[
            html.Div(
                className='page-loader-content',
                children=[
                    dashboard_content,
                    html.Span(children=modals_children),
                ],
            ),
            html.Div(
                className='page-loader-overlay',
                children=[
                    html.Div(
                        className='page-loader-media-frame',
                        children=[
                            html.Img(
                                className='page-loader-gif',
                                src='/assets/img/branding/loaders/loader.gif',
                            ),
                            html.Video(
                                className='page-loader-video',
                                autoPlay=True,
                                loop=True,
                                muted=True,
                                playsInline=True,
                                preload='auto',
                                children=[
                                    html.Source(
                                        src='/assets/img/branding/loaders/loader.mp4',
                                        type='video/mp4',
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ],
    )

    return [
        dcc.Interval(
            id=DashboardShellIds.INTERVAL_DASHBOARD,
            interval=dashboard_definition.dashboard_interval_ms,
            n_intervals=0,
            max_intervals=-1,
        ),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_HEADER_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_HEADER_TIME_SERIES_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_CENTER_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_CENTER_TIME_SERIES_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_RIGHT_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_RIGHT_TIME_SERIES_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_LEFT_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_LEFT_TIME_SERIES_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_RUNTIME_TIMESTAMPS_STORE, data=None),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_INFORMATION_STATUS_STORE, data=None),
        dcc.Store(
            id=DashboardShellIds.STORE_DASHBOARD_REFRESH_LOCK, data=dashboard_build_released_lock()
        ),
        dcc.Store(id=DashboardShellIds.STORE_DASHBOARD_REFRESH_SIGNAL, data=None),
        dcc.Store(id=AlarmShellIds.STORE_ALARM_RUNTIME_STORE, data=None),
        dcc.Store(id=AlarmShellIds.STORE_ALARM_RESUME_STORE, data=None),
        dcc.Store(id=AlarmShellIds.STORE_ALARM_REFRESH_SIGNAL, data=None),
        dcc.Store(id=TimeSeriesModalIds.TIME_SERIES_MODAL_STATE_STORE, data=None),
        dcc.Store(id=TimeSeriesModalIds.TIME_SERIES_MODAL_MIRROR_STORE, data=True),
        dashboard_loader_scope,
    ]
