"""
Build a Dash HTML Div component representing a row with two inline values.

This function constructs a structured HTML row with two labeled values displayed
side-by-side. Additional styles and configurations such as color, units, and class
names can be applied to each value. The row label is also displayed prominently at the
start of the row. This function is commonly used in dashboards or data-driven layouts
to represent comparisons or paired metrics.

Parameters
----------
label : str | Component
    The label for the entire row.
first_label : str | None
    The label associated with the first value.
first_value : str | html.Img | None
    The value to be displayed for the first metric. It can be a string or an image.
second_label : str | None
    The label associated with the second value.
second_value : str | html.Img | None
    The value to be displayed for the second metric. It can be a string or an image.
first_color : str | None, optional
    Optional color category/style name to be applied to the first value.
first_unit : str | Component | None, optional
    Optional unit to append to the first value.
first_value_class_name : str | None, optional
    Additional CSS class name to style the first value.
second_color : str | None, optional
    Optional color category/style name to be applied to the second value.
second_unit : str | Component | None, optional
    Optional unit to append to the second value.
second_value_class_name : str | None, optional
    Additional CSS class name to style the second value.
container_class_name : str, optional
    CSS class names for the row container. Defaults to 'app-border-bottom pt-1'.
font_size_class_name : str, optional
    CSS class name for font size styling. Defaults to 'font-size-200'.

Returns
-------
html.Div
    A Dash HTML Div component structured with the given labels, values, and styles.
"""

from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from ..theme import resolve_color_class


def build_inline_two_values_row(
    label: str | Component,
    first_label: str | None,
    first_value: str | html.Img | None,
    second_label: str | None,
    second_value: str | html.Img | None,
    first_color: str | None = None,
    first_unit: str | Component | None = None,
    first_value_class_name: str | None = None,
    second_color: str | None = None,
    second_unit: str | Component | None = None,
    second_value_class_name: str | None = None,
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
                    html.P(className='pe-1', children=[first_label]),
                    html.P(
                        className=f'fw-bold '
                        f'{resolve_color_class(value=first_color or "0")} '
                        f'{first_value_class_name or ""}',
                        children=[first_value],
                    ),
                    html.P(style={'paddingLeft': '.1rem'}, children=[first_unit])
                    if first_unit is not None
                    else None,
                    html.P(className='px-1', children=['/']),
                    html.P(className='pe-1', children=[second_label]),
                    html.P(
                        className=f'fw-bold '
                        f'{resolve_color_class(value=second_color or "0")} '
                        f'{second_value_class_name or ""}',
                        children=[second_value],
                    ),
                    html.P(style={'paddingLeft': '.1rem'}, children=[second_unit])
                    if second_unit is not None
                    else None,
                ],
            ),
        ],
    )
