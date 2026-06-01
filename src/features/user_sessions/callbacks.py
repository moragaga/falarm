from __future__ import annotations

from typing import Any

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.basic_analytics_runtime.user_sessions.services import (
    get_user_session_analytics_runtime_service,
)

from .components import (
    build_device_resolution_panel,
    build_kpi_cards,
    build_summary_items,
    build_user_rows,
)
from .components.toolbar import build_refresh_button_content
from .constants import (
    DEFAULT_DEVICE_FILTER,
    DEFAULT_RESOLUTION_FILTER,
    PAGE_SIZE,
)
from .graphs import build_weekly_comparison_figure
from .ids import UserSessionAnalyticsPageIds
from .services import (
    build_dynamic_device_options,
    build_dynamic_resolution_options,
    build_page_view,
    build_user_session_page_snapshot,
    get_next_page,
    get_total_pages_for_users,
)
from ...shared.ui.status.running_button import build_running_button_children


def register_user_session_analytics_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=UserSessionAnalyticsPageIds.SNAPSHOT_STORE,
            component_property='data',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.LAST_UPDATED_TEXT,
            component_property='children',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.INIT_TRIGGER,
            component_property='n_intervals',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.REFRESH_BUTTON,
            component_property='n_clicks',
        ),
        running=[
            (Output(component_id=UserSessionAnalyticsPageIds.MAIN_LOADER, component_property='display'), 'show', 'auto'),
            (
                Output(component_id=UserSessionAnalyticsPageIds.REFRESH_BUTTON, component_property='children'),
                build_running_button_children(text='Actualizando'), build_refresh_button_content()
            )
        ],
        prevent_initial_call=True
    )
    def load_snapshot(
        init_intervals: int | None,
        refresh_clicks: int | None,
    ):
        triggered_id = ctx.triggered_id

        if triggered_id is None:
            raise PreventUpdate

        snapshot = _load_page_snapshot()

        return (
            snapshot,
            _build_last_updated_text(snapshot=snapshot),
        )

    @app.callback(
        Output(
            component_id=UserSessionAnalyticsPageIds.DEVICE_SELECT,
            component_property='options',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.DEVICE_SELECT,
            component_property='value',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
            component_property='options',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SNAPSHOT_STORE,
            component_property='data',
        ),
        State(
            component_id=UserSessionAnalyticsPageIds.DEVICE_SELECT,
            component_property='value',
        ),
        State(
            component_id=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
            component_property='value',
        ),
    )
    def hydrate_dynamic_options(
        snapshot: dict[str, Any] | None,
        current_device: str | None,
        current_resolution: str | None,
    ):
        device_options = build_dynamic_device_options(
            snapshot=snapshot,
        )
        resolution_options = build_dynamic_resolution_options(
            snapshot=snapshot,
        )

        safe_device = _resolve_safe_option_value(
            options=device_options,
            value=current_device,
            fallback=DEFAULT_DEVICE_FILTER,
        )
        safe_resolution = _resolve_safe_option_value(
            options=resolution_options,
            value=current_resolution,
            fallback=DEFAULT_RESOLUTION_FILTER,
        )

        return (
            device_options,
            safe_device,
            resolution_options,
            safe_resolution,
        )

    @app.callback(
        Output(
            component_id=UserSessionAnalyticsPageIds.USERS_PAGE_STORE,
            component_property='data',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.USERS_PREVIOUS_BUTTON,
            component_property='n_clicks',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.USERS_NEXT_BUTTON,
            component_property='n_clicks',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SNAPSHOT_STORE,
            component_property='data',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.PROFILE_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.DEVICE_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.EXCLUDE_ADMIN_SWITCH,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SEARCH_INPUT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SORT_SELECT,
            component_property='value',
        ),
        State(
            component_id=UserSessionAnalyticsPageIds.USERS_PAGE_STORE,
            component_property='data',
        ),
    )
    def update_users_page(
        previous_clicks: int | None,
        next_clicks: int | None,
        snapshot: dict[str, Any] | None,
        profile_filter: str | None,
        device_filter: str | None,
        resolution_filter: str | None,
        exclude_admin_values: list[str] | None,
        search_text: str | None,
        sort_order: str | None,
        current_page: int | None,
    ):
        triggered_id = ctx.triggered_id

        if triggered_id in {
            UserSessionAnalyticsPageIds.SNAPSHOT_STORE,
            UserSessionAnalyticsPageIds.PROFILE_SELECT,
            UserSessionAnalyticsPageIds.DEVICE_SELECT,
            UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
            UserSessionAnalyticsPageIds.EXCLUDE_ADMIN_SWITCH,
            UserSessionAnalyticsPageIds.SEARCH_INPUT,
            UserSessionAnalyticsPageIds.SORT_SELECT,
        }:
            return 1

        total_pages = get_total_pages_for_users(
            snapshot=snapshot,
            profile_filter=profile_filter,
            device_filter=device_filter,
            resolution_filter=resolution_filter,
            exclude_admin_values=exclude_admin_values,
            search_text=search_text,
            sort_order=sort_order,
            page_size=PAGE_SIZE,
        )

        if triggered_id == UserSessionAnalyticsPageIds.USERS_PREVIOUS_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='previous',
                total_pages=total_pages,
            )

        if triggered_id == UserSessionAnalyticsPageIds.USERS_NEXT_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='next',
                total_pages=total_pages,
            )

        return current_page or 1

    @app.callback(
        Output(
            component_id=UserSessionAnalyticsPageIds.KPI_CONTAINER,
            component_property='children',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.WEEKLY_CHART,
            component_property='figure',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.SUMMARY_CONTAINER,
            component_property='children',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.DEVICE_RESOLUTION_CONTAINER,
            component_property='children',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.USERS_TABLE_BODY,
            component_property='children',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.USERS_COUNT,
            component_property='children',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.USERS_PAGE_TEXT,
            component_property='children',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.USERS_PREVIOUS_BUTTON,
            component_property='disabled',
        ),
        Output(
            component_id=UserSessionAnalyticsPageIds.USERS_NEXT_BUTTON,
            component_property='disabled',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SNAPSHOT_STORE,
            component_property='data',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.PROFILE_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.DEVICE_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.RESOLUTION_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.EXCLUDE_ADMIN_SWITCH,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SEARCH_INPUT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.SORT_SELECT,
            component_property='value',
        ),
        Input(
            component_id=UserSessionAnalyticsPageIds.USERS_PAGE_STORE,
            component_property='data',
        ),
    )
    def render_page(
        snapshot: dict[str, Any] | None,
        profile_filter: str | None,
        device_filter: str | None,
        resolution_filter: str | None,
        exclude_admin_values: list[str] | None,
        search_text: str | None,
        sort_order: str | None,
        page: int | None,
    ):
        view = build_page_view(
            snapshot=snapshot,
            profile_filter=profile_filter,
            device_filter=device_filter,
            resolution_filter=resolution_filter,
            exclude_admin_values=exclude_admin_values,
            search_text=search_text,
            sort_order=sort_order,
            page=page,
            page_size=PAGE_SIZE,
        )

        total_items = int(view['total_items'])
        users_count = f'{total_items} usuario' if total_items == 1 else f'{total_items} usuarios'

        return (
            build_kpi_cards(
                kpis=view['kpis'],
            ),
            build_weekly_comparison_figure(
                weekly_comparison=view['weekly_comparison'],
            ),
            build_summary_items(
                summary=view['summary'],
            ),
            build_device_resolution_panel(
                device_resolution=view['device_resolution'],
            ),
            build_user_rows(
                items=view['users'],
                page_size=PAGE_SIZE,
                has_snapshot=bool(view['has_snapshot']),
                empty_by_filter=bool(view['empty_by_filter']),
            ),
            users_count,
            f'Página {view["page"]} de {view["total_pages"]}',
            not view['has_previous'],
            not view['has_next'],
        )


def _load_page_snapshot() -> dict[str, Any]:
    analytics_snapshot = get_user_session_analytics_runtime_service().get_snapshot()

    return build_user_session_page_snapshot(
        analytics_snapshot=analytics_snapshot,
    )


def _build_last_updated_text(
    *,
    snapshot: dict[str, Any] | None,
) -> str:
    if not snapshot:
        return 'Sin actualización'

    source_display = snapshot.get('source_snapshot_timestamp_display') or 'Sin fecha'
    captured_display = snapshot.get('captured_at_display') or 'Sin fecha'

    return f'Última actualización: {source_display} · Información obtenida: {captured_display}'


def _resolve_safe_option_value(
    *,
    options: list[dict[str, Any]],
    value: str | None,
    fallback: str,
) -> str:
    allowed_values = {
        str(option.get('value'))
        for option in options
    }

    if value and value in allowed_values:
        return value

    return fallback