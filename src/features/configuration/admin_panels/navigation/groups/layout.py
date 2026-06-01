"""
Build the admin layout for navigation groups.

This module provides a function to construct an admin interface layout
for navigation groups using predefined definitions and a layout building
service.
"""

from __future__ import annotations

from src.features.admin_framework.services import build_admin_layout

from .definition import NAVIGATION_GROUPS_ADMIN_DEFINITION


def build_navigation_groups_admin_layout():
    return build_admin_layout(NAVIGATION_GROUPS_ADMIN_DEFINITION)
