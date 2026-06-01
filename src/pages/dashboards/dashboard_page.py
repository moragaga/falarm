from __future__ import annotations

import dash

from src.features.dashboards.home.layout import build_dashboard_initial_layout

dash.register_page(__name__, path='/', name='Dashboard principal')
layout = build_dashboard_initial_layout
