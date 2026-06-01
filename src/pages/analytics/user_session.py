from __future__ import annotations

import dash

from src.features.user_sessions.layout import build_user_session_analytics_layout

dash.register_page(__name__, path='/analytics/user-session', name='User Session Analytics')
layout = build_user_session_analytics_layout
