"""
Defines functionality to build an HTML feedback container for an admin interface.

This module handles the creation of a container element for feedback
messages in the admin interface by utilizing dynamically constructed
component IDs.
"""

from __future__ import annotations

from dash import html

from ..services.admin_component_ids import (
    build_admin_component_ids,
)


def build_admin_feedback_host(admin_key: str) -> html.Div:
    ids = build_admin_component_ids(admin_key)
    return html.Div(id=ids['toast_host'])
