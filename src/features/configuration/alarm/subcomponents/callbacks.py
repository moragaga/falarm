from __future__ import annotations

from src.app.dependencies import get_config_service, get_configuration_sharepoint_repository
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService
from src.features.configuration.alarm.services.admin_manifest_save_service import (
    AlarmAdminManifestSaveService,
)
from src.features.configuration.alarm.services.alarm_admin_reference_guard_service import (
    AlarmAdminReferenceGuardService,
)
from src.features.configuration.alarm.services.alarm_configuration_dependency_service import (
    AlarmConfigurationDependencyService,
)
from src.features.configuration.alarm.services.alarm_guarded_admin_data_service import (
    AlarmGuardedAdminDataService,
)

from .definition import ALARM_SUBCOMPONENTS_ADMIN_DEFINITION


def register_alarm_subcomponents_admin_callback() -> None:
    register_admin_callback(
        definition_factory=lambda: ALARM_SUBCOMPONENTS_ADMIN_DEFINITION,
        data_service_factory=_build_data_service,
        after_save=lambda definition, normalized_rows: AlarmAdminManifestSaveService.register_update(
            definition=definition,
            normalized_rows=normalized_rows,
        ),
    )


def _build_data_service() -> AlarmGuardedAdminDataService:
    delegate = AdminDataService(
        repository=get_configuration_sharepoint_repository(),
        config_service=get_config_service(),
    )

    dependency_service = AlarmConfigurationDependencyService(
        data_service=delegate,
    )

    guard_service = AlarmAdminReferenceGuardService(
        dependency_service=dependency_service,
    )

    return AlarmGuardedAdminDataService(
        delegate=delegate,
        validate_rows=lambda previous_rows, next_rows: guard_service.validate_subcomponent_rows(
            previous_rows=previous_rows,
            next_rows=next_rows,
        ),
    )