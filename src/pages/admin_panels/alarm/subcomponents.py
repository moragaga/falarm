from __future__ import annotations

import dash

from src.features.configuration.alarm.paths import ALARM_SUBCOMPONENTS_PATH
from src.features.configuration.alarm.subcomponents.layout import build_alarm_subcomponents_admin_layout

dash.register_page(
    __name__,
    path=ALARM_SUBCOMPONENTS_PATH,
    name='Subcomponentes de alarmas',
)


def layout():
    return build_alarm_subcomponents_admin_layout()
