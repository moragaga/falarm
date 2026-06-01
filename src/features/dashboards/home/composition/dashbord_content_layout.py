"""
Constructs the dashboard content layout configuration.

This function assembles various sections and modals of the dashboard content into a structured
layout dictionary. It generates a mapping of UI sections such as header, information, alarms,
and regional panels, as well as modal configurations.

Returns
-------
dict
    A dictionary defining the hierarchical structure of the dashboard content,
    including sections and modals.
"""

from __future__ import annotations

from src.shared.ui.modals.time_series.time_series_modal_shell import build_time_series_modal_shell

from ..sections import (
    build_center_region_section,
    build_header_section,
    build_information_section,
    build_left_region_section,
    build_right_region_section,
)


def build_dashboard_content_layout() -> dict:
    return {
        'header_children': [build_header_section()],
        'information_children': [build_information_section()],
        'alarms_children': [],
        'left_region_children': [build_left_region_section()],
        'center_region_children': [build_center_region_section()],
        'right_region_children': [build_right_region_section()],
        'modals_children': [
            build_time_series_modal_shell(),
        ],
    }
