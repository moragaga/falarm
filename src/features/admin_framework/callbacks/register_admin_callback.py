from __future__ import annotations

from typing import Callable

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.configuration.services import (
    SchemaBuilderService,
)
from src.shared.ui.status.running_button import build_running_button_children

from ..models.admin_definition import AdminDefinition
from ..services.admin_component_ids import build_admin_component_ids
from ..services.admin_data_service import AdminDataService
from ..services.admin_feedback_service import AdminFeedbackService
from ..services.admin_grid_service import AdminGridService


def register_admin_callback(
    definition_factory: Callable[[], AdminDefinition],
    data_service_factory: Callable[[], AdminDataService],
    after_save: Callable[[AdminDefinition, list[dict]], list[str]] | None = None,
) -> None:
    definition = definition_factory()
    ids = build_admin_component_ids(definition.key)
    app = get_dash_app()

    @app.callback(
        Output(component_id=ids['grid'], component_property='rowData', allow_duplicate=True),
        Output(component_id=ids['toast_host'], component_property='children', allow_duplicate=True),
        Input(component_id=ids['init'], component_property='n_intervals'),
        Input(component_id=ids['refresh_button'], component_property='n_clicks'),
        State(component_id=ids['grid'], component_property='rowData'),
        running=[
            (
                Output(component_id=ids['refresh_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['refresh_button'], component_property='children'),
                build_running_button_children(text='Recargando'),
                'Recargar',
            ),
            (Output(component_id=ids['add_button'], component_property='disabled'), True, False),
            (Output(component_id=ids['delete_button'], component_property='disabled'), True, False),
            (Output(component_id=ids['save_button'], component_property='disabled'), True, False),
            (Output(component_id=ids['add_button'], component_property='disabled'), True, False),
            (Output(component_id=ids['loading'], component_property='display'), 'show', 'auto'),
        ],
        prevent_initial_call=True,
    )
    def _handle_admin_init(
        _n_intervals,
        _refresh_clicks,
        row_data,
    ):
        current_definition = definition_factory()
        data_service = data_service_factory()
        triggered = ctx.triggered_id
        if triggered is None:
            raise PreventUpdate

        current_rows = [row for row in row_data or [] if isinstance(row, dict)]

        try:
            if triggered is None or triggered == ids['init'] or triggered == ids['refresh_button']:
                rows = data_service.load(current_definition)

                if current_definition.schema is not None:
                    rows = SchemaBuilderService.format_rows_for_grid(
                        schema=current_definition.schema,
                        rows=rows,
                    )

                prepared_rows = AdminGridService.prepare_rows_for_grid(
                    rows=rows,
                )

                return prepared_rows, None

            return current_rows, None

        except Exception as error:
            return current_rows, AdminFeedbackService.build_error(
                message=f'Error interno: {str(error)}'
            )

    @app.callback(
        Output(component_id=ids['grid'], component_property='rowData', allow_duplicate=True),
        Output(component_id=ids['toast_host'], component_property='children', allow_duplicate=True),
        Input(component_id=ids['save_button'], component_property='n_clicks'),
        State(component_id=ids['grid'], component_property='rowData'),
        running=[
            (Output(component_id=ids['save_button'], component_property='disabled'), True, False),
            (
                Output(component_id=ids['save_button'], component_property='children'),
                build_running_button_children(text='Guardando'),
                'Guardar',
            ),
            (Output(component_id=ids['add_button'], component_property='disabled'), True, False),
            (Output(component_id=ids['delete_button'], component_property='disabled'), True, False),
            (
                Output(component_id=ids['refresh_button'], component_property='disabled'),
                True,
                False,
            ),
            (Output(component_id=ids['loading'], component_property='display'), 'show', 'auto'),
        ],
        prevent_initial_call=True,
    )
    def _handle_admin_save(
        _save_clicks,
        row_data,
    ):
        current_definition = definition_factory()
        data_service = data_service_factory()
        triggered = ctx.triggered_id
        if triggered is None:
            raise PreventUpdate

        current_rows = [row for row in row_data or [] if isinstance(row, dict)]

        try:
            if triggered == ids['save_button']:
                clean_rows = AdminGridService.clean_rows_for_save(
                    rows=current_rows,
                )

                if current_definition.schema is not None:
                    clean_rows = SchemaBuilderService.normalize_rows_for_save(
                        schema=current_definition.schema,
                        rows=clean_rows,
                    )

                ok, errors, normalized_rows = data_service.save(
                    definition=current_definition,
                    rows=clean_rows,
                )

                if not ok:
                    return current_rows, AdminFeedbackService.build_error(errors)

                post_save_errors: list[str] = []

                if after_save is not None:
                    post_save_errors = after_save(
                        current_definition,
                        normalized_rows,
                    )

                rows_for_grid = normalized_rows

                if current_definition.schema is not None:
                    rows_for_grid = SchemaBuilderService.format_rows_for_grid(
                        schema=current_definition.schema,
                        rows=normalized_rows,
                    )

                prepared_rows = AdminGridService.prepare_rows_for_grid(
                    rows=rows_for_grid,
                )

                if post_save_errors:
                    return prepared_rows, AdminFeedbackService.build_error(
                        f'Error interno: {str(post_save_errors)}',
                    )

                return prepared_rows, AdminFeedbackService.build_success(
                    'Los cambios fueron persistidos correctamente.',
                )

            return current_rows, None

        except Exception as error:
            return current_rows, AdminFeedbackService.build_error(
                message=f'Error interno: {str(error)}'
            )

    @app.callback(
        Output(component_id=ids['grid'], component_property='rowData'),
        Output(component_id=ids['toast_host'], component_property='children'),
        Input(component_id=ids['add_button'], component_property='n_clicks'),
        Input(component_id=ids['delete_button'], component_property='n_clicks'),
        State(component_id=ids['grid'], component_property='rowData'),
        State(component_id=ids['grid'], component_property='selectedRows'),
        prevent_initial_call=True,
    )
    def _handle_admin_actions(
        _add_clicks,
        _delete_clicks,
        row_data,
        selected_rows,
    ):
        current_definition = definition_factory()
        data_service = data_service_factory()
        triggered = ctx.triggered_id
        if triggered is None:
            raise PreventUpdate

        current_rows = [row for row in row_data or [] if isinstance(row, dict)]

        try:
            if triggered == ids['add_button']:
                new_row = _build_new_row(
                    definition=current_definition,
                    current_rows=current_rows,
                )

                if current_definition.schema is not None:
                    formatted_new_rows = SchemaBuilderService.format_rows_for_grid(
                        schema=current_definition.schema,
                        rows=[new_row],
                    )

                    if formatted_new_rows:
                        new_row = formatted_new_rows[0]

                updated_rows = AdminGridService.append_row(
                    rows=current_rows,
                    row=new_row,
                )

                return updated_rows, None

            if triggered == ids['delete_button']:
                updated_rows = AdminGridService.delete_selected_rows(
                    rows=current_rows,
                    selected_rows=selected_rows or [],
                )

                return updated_rows, None

            return current_rows, None

        except Exception as error:
            return current_rows, AdminFeedbackService.build_error(
                message=f'Error interno: {str(error)}'
            )


def _build_new_row(
    *,
    definition: AdminDefinition,
    current_rows: list[dict],
) -> dict:
    if definition.row_factory is not None:
        return definition.row_factory(
            current_rows=current_rows,
        )

    if definition.schema is None:
        raise ValueError(
            f'No se puede crear una fila nueva para {definition.key}: '
            'la definición no tiene schema ni row_factory.',
        )

    return SchemaBuilderService.build_empty_row(
        definition.schema,
    )
