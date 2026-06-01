from __future__ import annotations

import dash

from src.features.configuration.admin_panels.publication_manager.layout import (
    build_publication_manager_layout,
)

dash.register_page(__name__, path='/admin/publication-manager', name='Publication-Manager')
layout = build_publication_manager_layout
