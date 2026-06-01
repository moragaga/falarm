"""
Builds the header for an admin page.

This function integrates the application header for the admin shell with the
specified title.

Parameters
----------
title : str
    The title to be displayed in the admin page header.

Returns
-------
AppHeaderAdminShell
    An instance of AppHeaderAdminShell configured with the specified title.
"""

from __future__ import annotations

from src.shared.ui.app_header_shell.app_header_admin_shell import build_app_header_admin_shell


def build_admin_page_header(title: str):
    return build_app_header_admin_shell(
        title=title,
    )
