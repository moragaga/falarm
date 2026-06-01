"""Registers all Dash callbacks for the application.

This module initializes and registers the required callbacks for various
features and functionalities within a Dash-based web application. The
callbacks are split across multiple areas such as navigation, dashboards,
alarm monitoring, administration panels, and alarm management.

The registration process involves importing the required callback functions
from specific modules and executing them to associate them with the
application's event-driven architecture. This modular approach ensures
that each feature's callbacks are encapsulated and independently manageable.
"""

from __future__ import annotations


def register_dash_callbacks() -> None:
    _register_navigation_callbacks()
    _register_dashboard_modules_callbacks()
    _register_admin_callbacks()
    _register_alarm_configuration_callbacks()
    _register_time_series_modal_callback()
    _register_identity_users_admin_callbacks()
    _register_user_sessions_analytics_page_callbacks()


def _register_navigation_callbacks() -> None:
    from src.app.navigation import (
        register_app_navigation_callbacks,
    )

    register_app_navigation_callbacks()



def _register_admin_callbacks() -> None:
    from src.features.configuration.admin_panels.navigation.groups.callbacks import (
        register_navigation_groups_admin_callback,
    )
    from src.features.configuration.admin_panels.navigation.links.callbacks import (
        register_navigation_links_admin_callback,
    )
    from src.features.configuration.admin_panels.publication_manager.callbacks import (
        register_publication_manager_callback,
    )

    register_navigation_groups_admin_callback()
    register_navigation_links_admin_callback()
    register_publication_manager_callback()


def _register_alarm_configuration_callbacks() -> None:
    from src.features.configuration.alarm.callbacks import (
        register_alarm_configuration_callbacks,
    )

    register_alarm_configuration_callbacks()


def _register_dashboard_modules_callbacks():
    # Importar cada dashboard para registrar sus callbacks
    # from src.features.dashboards.{project_name}.areas import (
    #     register_dashboard_modules_callbacks,
    # )
    #
    # register_dashboard_modules_callbacks()
    pass


def _register_time_series_modal_callback():
    # Importar cada dashboard para registrar sus callbacks
    # from src.features.dashboards.{project_name}.time_series.callbacks.time_series_modal_callback import (
    #     register_time_series_modal_callback,
    # )
    #
    # register_time_series_modal_callback()
    pass


def _register_identity_users_admin_callbacks():
    from src.features.configuration.admin_panels.identity.users.callbacks import (
        register_identity_users_admin_callback,
    )

    register_identity_users_admin_callback()

def _register_user_sessions_analytics_page_callbacks():
    from src.features.user_sessions.callbacks import (
        register_user_session_analytics_callbacks,
    )
    register_user_session_analytics_callbacks()