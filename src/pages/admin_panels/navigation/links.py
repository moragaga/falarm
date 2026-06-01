from __future__ import annotations

import dash

from src.features.configuration.admin_panels.navigation.links.layout import (
    build_navigation_links_admin_layout,
)

dash.register_page(
    __name__,
    path='/admin/navigation/links',
    name='Links de navegación',
)


def layout():
    return build_navigation_links_admin_layout()
