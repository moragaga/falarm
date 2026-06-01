"""
Callback registration for the publication manager feature.

This module includes the `register_publication_manager_callback` function, which sets
up the necessary Dash callbacks to handle user actions in the publication manager UI.
Callbacks include refreshing the publication grid, publishing selected items, and
publishing all pending items. These actions communicate with a back-end service for
performing the requested operation and update the UI accordingly.

Functions
---------
register_publication_manager_callback : None
    Registers Dash callbacks for managing publications.
"""

from __future__ import annotations

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from flask import session

from src.app.dash import get_dash_app
from src.app.dependencies import get_publication_manager_action_service
from src.features.admin_framework.services import AdminFeedbackService
from src.shared.ui.status.running_button import build_running_button_children

from .layout import PUBLICATION_MANAGER_IDS
from .models.publication_manager_action_result import PublicationManagerActionResult


def register_publication_manager_callback() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=PUBLICATION_MANAGER_IDS['grid'],
            component_property='rowData',
            allow_duplicate=True,
        ),
        Output(
            component_id=PUBLICATION_MANAGER_IDS['grid'],
            component_property='selectedRows',
            allow_duplicate=True,
        ),
        Output(
            component_id=PUBLICATION_MANAGER_IDS['toast'],
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=PUBLICATION_MANAGER_IDS['refresh'], component_property='n_clicks'),
        Input(component_id=PUBLICATION_MANAGER_IDS['init'], component_property='n_intervals'),
        running=[
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['refresh'], component_property='disabled'
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['refresh'], component_property='children'
                ),
                build_running_button_children(text='Recargando'),
                'Recargar',
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish'], component_property='disabled'
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish_pending'],
                    component_property='disabled',
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['loading'], component_property='display'
                ),
                'show',
                'auto',
            ),
        ],
        prevent_initial_call=True,
    )
    def handle_publication_manager(_refresh_clicks, _init):
        triggered = ctx.triggered_id
        if ctx.triggered_id is None:
            raise PreventUpdate
        current_user = (session.get('identity') or {}).get('email')
        service = get_publication_manager_action_service()

        try:
            if triggered in (PUBLICATION_MANAGER_IDS['init'], PUBLICATION_MANAGER_IDS['refresh']):
                result = service.refresh(
                    updated_by=current_user,
                )
                return result.rows, [], None

            raise PreventUpdate
        except Exception as error:
            result = service.refresh(
                updated_by=current_user,
            )
            return result.rows, [], AdminFeedbackService.build_error(str(error))

    @app.callback(
        Output(
            component_id=PUBLICATION_MANAGER_IDS['grid'],
            component_property='rowData',
            allow_duplicate=True,
        ),
        Output(
            component_id=PUBLICATION_MANAGER_IDS['grid'],
            component_property='selectedRows',
            allow_duplicate=True,
        ),
        Output(
            component_id=PUBLICATION_MANAGER_IDS['toast'],
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=PUBLICATION_MANAGER_IDS['publish'], component_property='n_clicks'),
        State(component_id=PUBLICATION_MANAGER_IDS['grid'], component_property='selectedRows'),
        running=[
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish'], component_property='disabled'
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish'], component_property='children'
                ),
                build_running_button_children(text='Publicando'),
                'Publicar seleccionados',
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['refresh'], component_property='disabled'
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish_pending'],
                    component_property='disabled',
                ),
                True,
                False,
            ),
        ],
        prevent_initial_call=True,
    )
    def handle_publish(
        _publish_clicks,
        selected_rows,
    ):
        triggered = ctx.triggered_id
        if ctx.triggered_id is None:
            raise PreventUpdate
        current_user = (session.get('identity') or {}).get('email')
        service = get_publication_manager_action_service()

        try:
            if triggered == PUBLICATION_MANAGER_IDS['publish']:
                result = service.publish_selected(
                    selected_rows=selected_rows or [],
                    published_by=current_user,
                )
                return result.rows, [], _build_feedback(result)

            raise PreventUpdate
        except Exception as error:
            result = service.refresh(
                updated_by=current_user,
            )
            return result.rows, [], AdminFeedbackService.build_error(str(error))

    @app.callback(
        Output(
            component_id=PUBLICATION_MANAGER_IDS['grid'],
            component_property='rowData',
            allow_duplicate=True,
        ),
        Output(
            component_id=PUBLICATION_MANAGER_IDS['grid'],
            component_property='selectedRows',
            allow_duplicate=True,
        ),
        Output(
            component_id=PUBLICATION_MANAGER_IDS['toast'],
            component_property='children',
            allow_duplicate=True,
        ),
        Input(
            component_id=PUBLICATION_MANAGER_IDS['publish_pending'], component_property='n_clicks'
        ),
        running=[
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish_pending'],
                    component_property='disabled',
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish_pending'],
                    component_property='children',
                ),
                build_running_button_children(text='Publicando'),
                'Publicar pendientes',
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['refresh'], component_property='disabled'
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=PUBLICATION_MANAGER_IDS['publish'], component_property='disabled'
                ),
                True,
                False,
            ),
        ],
        prevent_initial_call=True,
    )
    def handle_publish_pending(
        _publish_pending_clicks,
    ):
        triggered = ctx.triggered_id
        if ctx.triggered_id is None:
            raise PreventUpdate
        current_user = (session.get('identity') or {}).get('email')
        service = get_publication_manager_action_service()

        try:
            if triggered == PUBLICATION_MANAGER_IDS['publish_pending']:
                result = service.publish_pending(
                    published_by=current_user,
                )
                return result.rows, [], _build_feedback(result)

            raise PreventUpdate
        except Exception as error:
            result = service.refresh(
                updated_by=current_user,
            )
            return result.rows, [], AdminFeedbackService.build_error(str(error))


def _build_feedback(result: PublicationManagerActionResult):
    if result.has_errors:
        return AdminFeedbackService.build_error(list(result.errors))

    if result.success_message:
        return AdminFeedbackService.build_success(result.success_message)

    return None
