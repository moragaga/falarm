from __future__ import annotations

import dash

from src.features.configuration.alarm.components_n0.layout import (
    build_alarm_components_n0_admin_layout,
)
from src.features.configuration.alarm.paths import ALARM_COMPONENTS_N0_PATH

dash.register_page(
    __name__,
    path=ALARM_COMPONENTS_N0_PATH,
    name='Componentes Nivel 0',
)


def layout():
    return build_alarm_components_n0_admin_layout()
