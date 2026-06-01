"""
Builds the navigation links admin layout.

This function orchestrates the retrieval of configuration data, the creation
of group options, the definition of navigation links, and finally, the assembly
of the admin layout.

Returns
-------
Any
    The constructed admin layout representing the navigation links.

"""

from __future__ import annotations

from src.app.dependencies import get_configuration_sharepoint_repository
from src.features.admin_framework.services import build_admin_layout

from .definition import build_navigation_links_admin_definition
from .group_options import build_navigation_group_options


def build_navigation_links_admin_layout():
    group_rows = get_configuration_sharepoint_repository().load_rows(
        filename='navigation_groups.json.gz',
        relative_path='navigation',
    )

    definition = build_navigation_links_admin_definition(
        parent_group_options=build_navigation_group_options(group_rows),
    )

    return build_admin_layout(definition)
