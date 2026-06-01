from __future__ import annotations

import dash

from src.features.configuration.alarm.components.layout import build_alarm_components_admin_layout
from src.features.configuration.alarm.paths import ALARM_COMPONENTS_PATH

dash.register_page(
    __name__,
    path=ALARM_COMPONENTS_PATH,
    name='Componentes de alarmas',
)


def layout():
    return build_alarm_components_admin_layout()
