from __future__ import annotations

from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.components.definition import ALARM_COMPONENTS_ADMIN_DEFINITION
from src.features.configuration.alarm.family.definition import ALARM_FAMILY_ADMIN_DEFINITION
from src.features.configuration.alarm.rules.definition import ALARM_RULES_ADMIN_DEFINITION
from src.features.configuration.alarm.rules.editor.escalation.definition import (
    ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.rules.editor.visualization.definition import (
    ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.subcomponents.definition import ALARM_SUBCOMPONENTS_ADMIN_DEFINITION
from src.features.configuration.alarm.tools.definition import ALARM_TOOLS_ADMIN_DEFINITION

class AlarmConfigurationQueryService:
    def __init__(self, *, data_service: AdminDataService) -> None:
        self._data_service = data_service

    def load_families(self) -> list[dict]:
        return self._data_service.load(ALARM_FAMILY_ADMIN_DEFINITION)

    def load_tools(self) -> list[dict]:
        return self._data_service.load(ALARM_TOOLS_ADMIN_DEFINITION)

    def load_components(self) -> list[dict]:
        return self._data_service.load(ALARM_COMPONENTS_ADMIN_DEFINITION)

    def load_subcomponents(self) -> list[dict]:
        return self._data_service.load(ALARM_SUBCOMPONENTS_ADMIN_DEFINITION)

    def load_rules(self) -> list[dict]:
        return self._data_service.load(ALARM_RULES_ADMIN_DEFINITION)

    def load_escalation_targets(self) -> list[dict]:
        return self._data_service.load(ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION)

    def load_visual_targets(self) -> list[dict]:
        return self._data_service.load(ALARM_RULE_VISUAL_TARGETS_ADMIN_DEFINITION)
