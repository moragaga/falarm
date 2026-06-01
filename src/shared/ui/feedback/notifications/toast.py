"""
Utility function for creating a styled toast notification in a Dash application.

This function generates a Dash Bootstrap Components (dbc) Toast used to display
a message in a fixed position on the screen. The toast includes customizable
header text, a message, and an icon. The content of the message can be a string,
a list of strings, or a fully constructed Dash HTML component such as a Div or Ul.

Parameters
----------
header : str
    The text to be displayed in the header of the toast.
message : str | list[str] | html.Div | html.Ul
    The content to be displayed in the body of the toast. If a list of strings is
    provided, it is converted to an unordered list (html.Ul) with up to 8 items.
icon : str, optional
    The visual theme of the toast icon. Defaults to 'primary'.

Returns
-------
dbc.Toast
    A styled toast notification component ready for display in the Dash layout.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html


def build_toast(
    *,
    header: str,
    message: str | list[str] | html.Div | html.Ul,
    icon: str = 'primary',
) -> dbc.Toast:
    content = message

    if isinstance(message, list):
        content = html.Ul(
            [html.Li(item) for item in message[:8]],
            className='mb-0 ps-3',
        )

    return dbc.Toast(
        header=header,
        children=content,
        icon=icon,
        duration=5000,
        dismissable=True,
        is_open=True,
        style={
            'position': 'fixed',
            'top': 66,
            'right': 10,
            'width': 420,
            'zIndex': 2000,
        },
    )
