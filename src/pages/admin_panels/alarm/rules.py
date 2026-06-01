from __future__ import annotations

import dash

from src.features.configuration.alarm.paths import ALARM_RULES_PATH
from src.features.configuration.alarm.rules.layout import build_alarm_rules_admin_layout


dash.register_page(
    __name__,
    path=ALARM_RULES_PATH,
    name='Reglas de alarmas',
)


def layout(**_query_params):
    return build_alarm_rules_admin_layout()
