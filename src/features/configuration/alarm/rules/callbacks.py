from __future__ import annotations

from src.app.dependencies import get_config_service, get_configuration_sharepoint_repository
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.services.admin_manifest_save_service import (
    AlarmAdminManifestSaveService,
)

from .definition import ALARM_RULES_ADMIN_DEFINITION


def register_alarm_rules_admin_callback() -> None:
    register_admin_callback(
        definition_factory=lambda: ALARM_RULES_ADMIN_DEFINITION,
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=lambda definition, normalized_rows: AlarmAdminManifestSaveService.register_update(
            definition=definition,
            normalized_rows=normalized_rows,
        ),
    )
