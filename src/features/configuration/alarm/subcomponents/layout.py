from __future__ import annotations

from src.app.dependencies import get_configuration_sharepoint_repository
from src.features.admin_framework.services import build_admin_layout
from src.features.configuration.alarm.constants import ALARM_CONFIGURATION_RELATIVE_PATH

from .component_options import build_alarm_component_options
from .definition import build_alarm_subcomponents_admin_definition


def build_alarm_subcomponents_admin_layout():
    component_rows = get_configuration_sharepoint_repository().load_rows(
        filename='alarm_components.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    )

    definition = build_alarm_subcomponents_admin_definition(
        parent_component_options=build_alarm_component_options(component_rows),
    )

    return build_admin_layout(definition)
