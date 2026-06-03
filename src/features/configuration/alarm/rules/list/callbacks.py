from __future__ import annotations

from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.app.dependencies import get_config_service, get_configuration_sharepoint_repository
from src.features.admin_framework.services import AdminDataService, AdminFeedbackService
from src.features.configuration.alarm.services.alarm_configuration_query_service import (
    AlarmConfigurationQueryService,
)

from ..ids import AlarmRulesMode, AlarmRulesPageIds
from .filters import filter_rule_rows
from .grid import build_alarm_rules_grid_rows
from .ids import AlarmRulesListIds


def register_alarm_rules_list_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AlarmRulesListIds.FAMILY_SELECT, component_property='options'),
        Output(component_id=AlarmRulesListIds.FAMILY_SELECT, component_property='value'),
        Output(component_id=AlarmRulesListIds.GRID, component_property='rowData'),
        Input(component_id=AlarmRulesListIds.INIT, component_property='n_intervals'),
        Input(component_id=AlarmRulesListIds.REFRESH_BUTTON, component_property='n_clicks'),
        Input(component_id=AlarmRulesListIds.FAMILY_SELECT, component_property='value'),
    )
    def load_rule_rows(
        _init_intervals,
        _refresh_clicks,
        family_key: str | None,
    ):
        service = _build_query_service()

        family_rows = service.load_families()

        options = [
            {
                'label': row.get('family_name') or row.get('family_key'),
                'value': row.get('family_key'),
            }
            for row in family_rows
            if row.get('family_key')
        ]

        safe_family = (
            family_key
            if _option_exists(options=options, value=family_key)
            else None
        )

        if not safe_family:
            return options, None, []

        tool_rows = service.load_tools()
        rule_rows = service.load_rules()

        filtered_rows = filter_rule_rows(
            rows=rule_rows,
            family_key=safe_family,
        )

        grid_rows = build_alarm_rules_grid_rows(
            rows=filtered_rows,
            families=family_rows,
            tools=tool_rows,
        )

        return options, safe_family, grid_rows

    @app.callback(
        Output(
            component_id=AlarmRulesPageIds.PAGE_STATE,
            component_property='data',
            allow_duplicate=True,
        ),
        Output(
            component_id=AlarmRulesPageIds.TOAST_HOST,
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmRulesListIds.NEW_BUTTON, component_property='n_clicks'),
        Input(component_id=AlarmRulesListIds.EDIT_BUTTON, component_property='n_clicks'),
        State(component_id=AlarmRulesListIds.FAMILY_SELECT, component_property='value'),
        State(component_id=AlarmRulesListIds.GRID, component_property='selectedRows'),
        prevent_initial_call=True,
    )
    def navigate_from_rules_list(
        _new_clicks,
        _edit_clicks,
        family_key: str | None,
        selected_rows,
    ):
        triggered = ctx.triggered_id

        if triggered is None:
            raise PreventUpdate

        if triggered == AlarmRulesListIds.NEW_BUTTON and not _new_clicks:
            raise PreventUpdate

        if triggered == AlarmRulesListIds.EDIT_BUTTON and not _edit_clicks:
            raise PreventUpdate

        if triggered == AlarmRulesListIds.NEW_BUTTON:
            if not family_key:
                return (
                    no_update,
                    AdminFeedbackService.build_warning(
                        'Selecciona una familia antes de crear una regla.',
                    ),
                )

            return (
                _build_edit_state(
                    family_key=family_key,
                    rule_key='new',
                    tab='identity',
                ),
                None,
            )

        if triggered == AlarmRulesListIds.EDIT_BUTTON:
            selected_rule = _get_selected_rule(
                selected_rows=selected_rows,
            )

            if not selected_rule:
                return (
                    no_update,
                    AdminFeedbackService.build_warning(
                        'Selecciona una regla para editar.',
                    ),
                )

            return (
                _build_edit_state(
                    family_key=selected_rule.get('family_key') or family_key,
                    rule_key=selected_rule.get('rule_key'),
                    tab='identity',
                ),
                None,
            )

        raise PreventUpdate


def _build_query_service() -> AlarmConfigurationQueryService:
    return AlarmConfigurationQueryService(
        data_service=AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        )
    )


def _option_exists(
    *,
    options: list[dict],
    value: str | None,
) -> bool:
    if not value:
        return False

    return any(option.get('value') == value for option in options)


def _get_selected_rule(
    *,
    selected_rows,
) -> dict | None:
    if not selected_rows:
        return None

    selected = selected_rows[0]

    if isinstance(selected, dict):
        return selected

    return None


def _build_edit_state(
    *,
    family_key: str | None,
    rule_key: str | None,
    tab: str,
) -> dict:
    return {
        'mode': AlarmRulesMode.EDIT,
        'family_key': family_key,
        'rule_key': rule_key or 'new',
        'active_tab': tab,
    }