"""
A utility function to build an inline row component for displaying a label, value, and optional unit
in a structured layout using Dash components.

This function generates a `Div` element with flexible styling and includes options for customizing
the text, colors, and layout of the label, value, and unit fields. Primarily used for creating
Dash application UI elements.

Parameters
----------
label : str or Component
    The label to display in the row. It can be a string or a Dash Component.
value : str, html.Img, or None
    The primary value to display in the row. It can be a string, an image component, or None.
unit : str, Component, or None, optional
    The unit or additional text to display adjacent to the value. This can be a string, a Dash Component,
    or None. Default is None.
color : str or None, optional
    The color key for styling the value text. This is resolved by the `resolve_color_class` utility
    to apply a corresponding CSS class. Default is None.
value_class_name : str or None, optional
    Additional custom CSS class(es) for styling the value text. Default is None.
container_class_name : str, optional
    CSS class(es) for styling the outer container of the row. Default is
    'app-border-bottom pt-1'.
font_size_class_name : str, optional
    CSS class(es) for controlling the font size of the components. Default is 'font-size-200'.

Returns
-------
html.Div
    A Dash `Div` component structured with a customizable label, value, and unit displayed in a
    flexible inline row layout.
"""

from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from ..theme import resolve_color_class


def build_inline_value_row(
    label: str | Component,
    value: str | html.Img | None,
    unit: str | Component | None = None,
    color: str | None = None,
    value_class_name: str | None = None,
    container_class_name: str = 'app-border-bottom pt-1',
    font_size_class_name: str = 'font-size-200',
) -> html.Div:
    return html.Div(
        className=f'd-flex justify-content-between {container_class_name} {font_size_class_name}',
        children=[
            html.P(children=[label]),
            html.Div(
                className='d-flex',
                children=[
                    html.P(
                        className=f'fw-bold '
                        f'{resolve_color_class(value=color)} '
                        f'{value_class_name or ""}',
                        children=[value],
                    ),
                    html.P(style={'paddingLeft': '.1rem'}, children=[unit])
                    if unit is not None
                    else None,
                ],
            ),
        ],
    )
