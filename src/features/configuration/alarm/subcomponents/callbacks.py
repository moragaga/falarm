from __future__ import annotations

from src.app.dependencies import get_config_service, get_configuration_sharepoint_repository
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.constants import ALARM_CONFIGURATION_RELATIVE_PATH
from src.features.configuration.alarm.services.admin_manifest_save_service import (
    AlarmAdminManifestSaveService,
)

from .component_options import build_alarm_component_options
from .definition import build_alarm_subcomponents_admin_definition


def register_alarm_subcomponents_admin_callback() -> None:
    def _build_definition():
        component_rows = get_configuration_sharepoint_repository().load_rows(
            filename='alarm_components.json.gz',
            relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
        )

        return build_alarm_subcomponents_admin_definition(
            parent_component_options=build_alarm_component_options(component_rows),
        )

    register_admin_callback(
        definition_factory=_build_definition,
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=lambda definition, normalized_rows: AlarmAdminManifestSaveService.register_update(
            definition=definition,
            normalized_rows=normalized_rows,
        ),
    )
