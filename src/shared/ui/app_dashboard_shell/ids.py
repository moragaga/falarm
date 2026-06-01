"""
A class containing a collection of constant identifiers used for defining
and categorizing dashboard shell components.

This class provides a centralized location for storing string constants
representing various elements of a dashboard shell layout. These constants
can be used as unique identifiers or keys in different parts of the
application, such as components, regions, and data stores.
"""

from __future__ import annotations


class DashboardShellIds:
    INTERVAL_DASHBOARD = 'dashboard-shell-interval-dashboard'

    STORE_DASHBOARD_RUNTIME_HEADER_STORE = 'dashboard-shell-runtime-header-store'
    STORE_DASHBOARD_RUNTIME_CENTER_STORE = 'dashboard-shell-runtime-body-store'
    STORE_DASHBOARD_RUNTIME_RIGHT_STORE = 'dashboard-shell-runtime-right-store'
    STORE_DASHBOARD_RUNTIME_LEFT_STORE = 'dashboard-shell-runtime-alarms-store'

    STORE_DASHBOARD_RUNTIME_HEADER_TIME_SERIES_STORE = (
        'dashboard-shell-runtime-header-time-series-store'
    )
    STORE_DASHBOARD_RUNTIME_CENTER_TIME_SERIES_STORE = (
        'dashboard-shell-runtime-body-time-series-store'
    )
    STORE_DASHBOARD_RUNTIME_RIGHT_TIME_SERIES_STORE = (
        'dashboard-shell-runtime-right-time-series-store'
    )
    STORE_DASHBOARD_RUNTIME_LEFT_TIME_SERIES_STORE = (
        'dashboard-shell-runtime-alarms-time-series-store'
    )
    STORE_DASHBOARD_RUNTIME_TIMESTAMPS_STORE = 'dashboard-shell-runtime-timestamps-store'

    STORE_DASHBOARD_INFORMATION_STATUS_STORE = 'dashboard-shell-information-status-store'
    STORE_DASHBOARD_REFRESH_LOCK = 'dashboard-shell-refresh-lock-store'
    STORE_DASHBOARD_REFRESH_SIGNAL = 'dashboard-shell-refresh-signal-store'

    ROOT = 'dashboard-shell-root'
    HEADER = 'dashboard-shell-header'
    INFORMATION = 'dashboard-shell-information'
    ALARMS = 'dashboard-shell-alarms'
    BODY = 'dashboard-shell-body'

    LEFT_REGION = 'dashboard-shell-left-region'
    CENTER_REGION = 'dashboard-shell-center-region'
    RIGHT_REGION = 'dashboard-shell-right-region'
