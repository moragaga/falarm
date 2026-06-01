"""
Builds the identity users' admin layout.

This module constructs the admin layout for identity users by utilizing
a predefined definition and the `build_admin_layout` function from the
associated admin framework services module.

Functions
---------
build_identity_users_admin_layout:
    Builds and returns the identity users' admin layout based on the
    provided definition.
"""

from __future__ import annotations

from src.features.admin_framework.services import build_admin_layout

from .definition import IDENTITY_USERS_ADMIN_DEFINITION


def build_identity_users_admin_layout():
    return build_admin_layout(IDENTITY_USERS_ADMIN_DEFINITION)
