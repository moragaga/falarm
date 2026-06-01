from __future__ import annotations

import dash

from src.features.configuration.alarm.family.layout import build_alarm_family_admin_layout
from src.features.configuration.alarm.paths import ALARM_FAMILY_PATH

dash.register_page(
    __name__,
    path=ALARM_FAMILY_PATH,
    name='Familias de alarmas',
)


def layout():
    return build_alarm_family_admin_layout()
