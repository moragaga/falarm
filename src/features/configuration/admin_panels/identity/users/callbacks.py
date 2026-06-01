"""
Registers a callback for the identity users admin operations.

This function sets up a callback mechanism for the identity users admin
definition, using the `register_admin_callback` function. A custom `after_save`
callback is provided to handle actions that need to occur after saving data,
such as invalidating the identity sync service.

The function leverages dependencies such as `get_config_service`,
`get_configuration_sharepoint_repository`, and `get_identity_sync_service` to
configure the required services and repositories for the callback registration.

Notes
-----
The `after_save` callback is responsible for invalidating the identity sync
service after saving, ensuring that any cached identity configurations are
refreshed.

Functions
---------
register_identity_users_admin_callback
    Registers a callback for identity users admin with a specific definition,
    data service, and a custom `after_save` logic.

"""

from __future__ import annotations

from src.app.dependencies import (
    get_config_service,
    get_configuration_sharepoint_repository,
    get_identity_sync_service,
)
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService

from .definition import IDENTITY_USERS_ADMIN_DEFINITION


def register_identity_users_admin_callback() -> None:
    def _after_save(_definition, _normalized_rows: list[dict]) -> list[str]:
        get_identity_sync_service().invalidate()
        return []

    register_admin_callback(
        definition_factory=lambda: IDENTITY_USERS_ADMIN_DEFINITION,
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=_after_save,
    )
