"""Defines a constant DashboardShellDefinition instance for configuring the dashboard.

This module contains a single instance of `DashboardShellDefinition` called
`DASHBOARD_DEFINITION`, which is configured with default parameters to define
the behavior of a dashboard. It is primarily used to set the refresh interval
for the dashboard in milliseconds.
"""

from __future__ import annotations

from src.shared.ui.app_dashboard_shell.models import DashboardShellDefinition

DASHBOARD_DEFINITION = DashboardShellDefinition(
    dashboard_interval_ms=10_000,
)
