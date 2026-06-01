from __future__ import annotations

import dash

from src.features.configuration.admin_panels.navigation.groups.layout import (
    build_navigation_groups_admin_layout,
)

dash.register_page(
    __name__,
    path='/admin/navigation/groups',
    name='Grupos de navegación',
)


def layout():
    return build_navigation_groups_admin_layout()
