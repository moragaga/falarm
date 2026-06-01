"""
This module registers all necessary callbacks for the app's navigation system.

The callbacks manage the functionality of opening and closing various navigation elements such
as the off-canvas menu, navigation menu content rendering, and group toggles within the menu.
"""

from __future__ import annotations

from dash import MATCH, Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app

from .ids import AppNavigationIds
from .menu_content import build_navigation_menu_content


def register_app_navigation_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(component_id=AppNavigationIds.HEADER_OFFCANVAS, component_property='is_open'),
        Input(component_id=AppNavigationIds.HEADER_MOBILE_TOGGLE, component_property='n_clicks'),
        Input(component_id=AppNavigationIds.HEADER_DESKTOP_TOGGLE, component_property='n_clicks'),
        State(component_id=AppNavigationIds.HEADER_OFFCANVAS, component_property='is_open'),
        prevent_initial_call=True,
    )
    def toggle_navigation_offcanvas(
        _mobile_clicks,
        _desktop_clicks,
        is_open: bool,
    ):
        triggered = ctx.triggered_id

        if triggered in (
            AppNavigationIds.HEADER_MOBILE_TOGGLE,
            AppNavigationIds.HEADER_DESKTOP_TOGGLE,
        ):
            return not is_open

        return is_open

    @app.callback(
        Output(component_id=AppNavigationIds.HEADER_MENU_CONTENT, component_property='children'),
        Input(component_id=AppNavigationIds.HEADER_LOCATION, component_property='pathname'),
    )
    def render_navigation_menu(pathname: str | None):
        return build_navigation_menu_content(current_path=pathname)

    @app.callback(
        Output(
            component_id={
                'type': AppNavigationIds.NAVIGATION_GROUP_COLLAPSE,
                'group_key': MATCH,
            },
            component_property='is_open',
        ),
        Input(
            component_id={
                'type': AppNavigationIds.NAVIGATION_GROUP_TOGGLE,
                'group_key': MATCH,
            },
            component_property='n_clicks',
        ),
        State(
            component_id={
                'type': AppNavigationIds.NAVIGATION_GROUP_COLLAPSE,
                'group_key': MATCH,
            },
            component_property='is_open',
        ),
        prevent_initial_call=True,
    )
    def toggle_navigation_group(
        n_clicks,
        is_open: bool,
    ):
        if not n_clicks:
            raise PreventUpdate

        return not bool(is_open)
