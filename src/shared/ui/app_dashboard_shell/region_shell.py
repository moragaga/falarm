"""
Creates a responsive column layout component for a specific region.

This function utilizes the `dbc.Col` component from Dash Bootstrap
Components to create a responsive region shell with customizable column
widths for various screen sizes. The component can also accept children
elements to be rendered inside the column and a custom CSS class for
styling.

Parameters
----------
region_id : str
    The ID to be assigned to the region column.
children : list or None, optional
    A list of child elements to be rendered inside the created column.
    Defaults to an empty list if not provided.
width_xs : int, optional
    The column width for extra small screens (XS). Defaults to 12.
width_sm : int, optional
    The column width for small screens (SM). Defaults to 4.
width_md : int, optional
    The column width for medium screens (MD). Defaults to 4.
width_lg : int, optional
    The column width for large screens (LG). Defaults to 4.
width_xl : int, optional
    The column width for extra large screens (XL). Defaults to 4.
class_name : str, optional
    The CSS class name to be applied to the column. Defaults to 'd-flex'.

Returns
-------
dbc.Col
    A responsive column component configured with the provided parameters.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc


def build_region_shell(
    *,
    region_id: str,
    children=None,
    width_xs: int = 12,
    width_sm: int = 4,
    width_md: int = 4,
    width_lg: int = 4,
    width_xl: int = 4,
    class_name: str = 'd-flex',
) -> dbc.Col:
    children = children or []

    return dbc.Col(
        id=region_id,
        className=class_name,
        xs=width_xs,
        sm=width_sm,
        md=width_md,
        lg=width_lg,
        xl=width_xl,
        children=children,
    )
