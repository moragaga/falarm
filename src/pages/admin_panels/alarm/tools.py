from __future__ import annotations

import dash

from src.features.configuration.alarm.paths import ALARM_TOOLS_PATH
from src.features.configuration.alarm.tools.layout import build_alarm_tools_admin_layout

dash.register_page(
    __name__,
    path=ALARM_TOOLS_PATH,
    name='Herramientas de alarmas',
)


def layout():
    return build_alarm_tools_admin_layout()
