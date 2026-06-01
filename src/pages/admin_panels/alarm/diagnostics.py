from __future__ import annotations

import dash

from src.features.configuration.alarm.diagnostics.layout import build_alarm_diagnostics_layout
from src.features.configuration.alarm.paths import ALARM_DIAGNOSTICS_PATH

dash.register_page(
    __name__,
    path=ALARM_DIAGNOSTICS_PATH,
    name='Diagnósticos de alarmas',
)


def layout():
    return build_alarm_diagnostics_layout()
