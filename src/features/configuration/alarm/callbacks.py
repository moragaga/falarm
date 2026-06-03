from __future__ import annotations

from .components.callbacks import register_alarm_components_admin_callback
from .diagnostics.callbacks import register_alarm_diagnostics_callbacks
from .family.callbacks import register_alarm_family_admin_callback
from .rules.callbacks import register_alarm_rules_admin_callback
from .subcomponents.callbacks import register_alarm_subcomponents_admin_callback
from .tools.callbacks import register_alarm_tools_admin_callback
from .rules.editor.header_callbacks import register_alarm_rule_editor_header_callbacks

def register_alarm_configuration_callbacks() -> None:
    register_alarm_family_admin_callback()
    register_alarm_tools_admin_callback()
    register_alarm_components_admin_callback()
    register_alarm_subcomponents_admin_callback()
    register_alarm_rules_admin_callback()
    register_alarm_diagnostics_callbacks()
    register_alarm_rule_editor_header_callbacks()