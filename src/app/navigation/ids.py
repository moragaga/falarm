"""
Constants and utility methods for managing navigation identifiers in the application.

This module provides a set of constants representing unique identifiers used throughout
the application's navigation system. It also includes utility methods for generating specific
navigation-related IDs.

Classes
-------
AppNavigationIds
    Contains constants for navigation identifiers and helper methods for generating dynamic
    navigation IDs.
"""

from __future__ import annotations


class AppNavigationIds:
    HEADER_LOCATION = 'app-header-location'
    HEADER_OFFCANVAS = 'app-header-offcanvas'
    HEADER_MENU_CONTENT = 'app-header-menu-content'
    HEADER_MOBILE_TOGGLE = 'app-header-mobile-toggle'
    HEADER_DESKTOP_TOGGLE = 'app-header-desktop-toggle'
    HEADER_CLOSE_TRIGGER = 'app-header-close-trigger'

    NAVIGATION_GROUP_TOGGLE = 'app-navigation-group-toggle'
    NAVIGATION_GROUP_COLLAPSE = 'app-navigation-group-collapse'

    @staticmethod
    def build_group_toggle_id(group_key: str) -> dict:
        return {
            'type': AppNavigationIds.NAVIGATION_GROUP_TOGGLE,
            'group_key': group_key,
        }

    @staticmethod
    def build_group_collapse_id(group_key: str) -> dict:
        return {
            'type': AppNavigationIds.NAVIGATION_GROUP_COLLAPSE,
            'group_key': group_key,
        }
