from __future__ import annotations

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.app.dependencies import get_config_service, get_configuration_sharepoint_repository
from src.features.admin_framework.services import AdminDataService, AdminFeedbackService
from src.features.configuration.alarm.services.alarm_rule_editor_service import AlarmRuleEditorService

from ..ids import AlarmRulesMode, AlarmRulesPageIds
from .escalation.callbacks import register_alarm_rule_escalation_callbacks
from .escalation.layout import build_escalation_tab_layout
from .identity.callbacks import register_alarm_rule_identity_callbacks
from .identity.layout import build_identity_tab_layout
from .ids import AlarmRuleEditorIds, AlarmRuleEditorTabs
from .management.callbacks import register_alarm_rule_management_callbacks
from .management.layout import build_management_tab_layout
from .summary.layout import build_summary_tab_layout
from .visualization.callbacks import register_alarm_rule_visualization_callbacks
from .visualization.layout import build_visualization_tab_layout


def register_alarm_rule_editor_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.ORIGINAL_STORE, component_property='data'),
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data'),
        Input(component_id='alarm-rule-editor-route-context', component_property='data'),
    )
    def load_rule_editor(route_context: dict | None):
        if not route_context:
            raise PreventUpdate

        service = _build_editor_service()
        draft = service.load_draft(
            rule_key=route_context.get('rule_key'),
            family_key=route_context.get('family_key'),
        )
        diagnostics = draft.get('diagnostics') or []

        return (
            draft,
            draft,
            {'diagnostics': diagnostics},
        )

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.TAB_CONTENT, component_property='children'),
        Input(component_id=AlarmRuleEditorIds.TABS, component_property='active_tab'),
        Input(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
    )
    def render_rule_editor_tab(active_tab: str | None, draft: dict | None):
        selected_tab = active_tab if active_tab in AlarmRuleEditorTabs.ALL else AlarmRuleEditorTabs.IDENTITY

        if selected_tab == AlarmRuleEditorTabs.MANAGEMENT:
            return build_management_tab_layout(draft=draft)

        if selected_tab == AlarmRuleEditorTabs.ESCALATION:
            return build_escalation_tab_layout(draft=draft)

        if selected_tab == AlarmRuleEditorTabs.VISUALIZATION:
            return build_visualization_tab_layout(draft=draft)

        if selected_tab == AlarmRuleEditorTabs.SUMMARY:
            return build_summary_tab_layout(draft=draft)

        return build_identity_tab_layout(draft=draft)

    @app.callback(
        Output(
            component_id=AlarmRulesPageIds.PAGE_STATE,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmRuleEditorIds.CANCEL_BUTTON, component_property='n_clicks'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def return_to_rules_list(clicks, draft: dict | None):
        if not clicks or ctx.triggered_id is None:
            raise PreventUpdate

        return {
            'mode': AlarmRulesMode.LIST,
            'family_key': (draft or {}).get('family_key'),
            'rule_key': None,
            'active_tab': None,
        }

    @app.callback(
        Output(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRuleEditorIds.VALIDATION_STORE, component_property='data', allow_duplicate=True),
        Output(component_id=AlarmRulesPageIds.TOAST_HOST, component_property='children', allow_duplicate=True),
        Input(component_id=AlarmRuleEditorIds.SAVE_BUTTON, component_property='n_clicks'),
        State(component_id=AlarmRuleEditorIds.DRAFT_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def save_rule_editor(clicks, draft: dict | None):
        if not clicks or ctx.triggered_id is None:
            raise PreventUpdate

        if not draft:
            return draft, {'diagnostics': ['No hay datos para guardar.']}, AdminFeedbackService.build_error(
                'No hay datos para guardar.'
            )

        ok, errors, saved_draft = _build_editor_service().save_draft(draft=draft)
        if not ok:
            return saved_draft, {'diagnostics': errors}, AdminFeedbackService.build_error(errors)

        return saved_draft, {'diagnostics': []}, AdminFeedbackService.build_success(
            'La regla fue guardada correctamente.'
        )

    register_alarm_rule_identity_callbacks()
    register_alarm_rule_management_callbacks()
    register_alarm_rule_escalation_callbacks()
    register_alarm_rule_visualization_callbacks()


def _build_editor_service() -> AlarmRuleEditorService:
    return AlarmRuleEditorService(
        data_service=AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        )
    )

