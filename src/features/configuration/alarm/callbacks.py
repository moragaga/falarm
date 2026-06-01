from __future__ import annotations

from .components_n0.callbacks import register_alarm_components_n0_admin_callback
from .diagnostics.callbacks import register_alarm_diagnostics_callbacks
from .family.callbacks import register_alarm_family_admin_callback
from .rules.callbacks import register_alarm_rules_admin_callback
from .tools.callbacks import register_alarm_tools_admin_callback


def register_alarm_configuration_callbacks() -> None:
    register_alarm_family_admin_callback()
    register_alarm_tools_admin_callback()
    register_alarm_components_n0_admin_callback()
    register_alarm_rules_admin_callback()
    register_alarm_diagnostics_callbacks()
