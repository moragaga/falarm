"""
Builds a Div component for the application alarm shell.

This function creates an HTML Div element using the Dash library with a specific
CSS class for styling (`app-alarm-shell`). It accepts optional child components
to be included within the Div element.

Parameters
----------
children : list, optional
    A list of child components or elements to be rendered within the Div. If no
    children are provided, an empty list is used by default.

Returns
-------
dash.html.Div
    A Div element with the specified class and child components.
"""

from __future__ import annotations

from dash import html


def build_app_alarm_shell(*, children=None) -> html.Div:
    children = children or []

    return html.Div(className='app-alarm-shell', children=children)
