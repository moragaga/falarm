"""
This module provides the initial layout construction for the dashboard UI.

The main function in this module builds the dashboard's initial layout by
leveraging definitions and components imported from various sources. The
layout is dynamically structured based on the content and configuration
provided by predefined definitions and composition utilities.
"""

from __future__ import annotations

from dash import html

from src.shared.ui.app_dashboard_shell.dashboard_layout import build_dashboard_layout

from .composition.dashbord_content_layout import build_dashboard_content_layout
from .definition import DASHBOARD_DEFINITION
from .ids import DashboardIds


def build_dashboard_initial_layout():
    content = build_dashboard_content_layout()

    return html.Div(
        id=DashboardIds.PAGE_CONTAINER,
        children=build_dashboard_layout(
            dashboard_definition=DASHBOARD_DEFINITION,
            alarm_definition=None,
            header_children=content.get('header_children'),
            information_children=content.get('information_children'),
            alarms_children=content.get('alarms_children'),
            left_region_children=content.get('left_region_children'),
            center_region_children=content.get('center_region_children'),
            right_region_children=content.get('right_region_children'),
            modals_children=content.get('modals_children'),
        ),
    )
