"""
Generates a Dash Bootstrap layout container for a section with configurable
title, content, and optional external links.

The function creates a layout structure using Dash and Dash Bootstrap
components. It allows for the inclusion of a section title, customizable
content, and an optional component for external links. Additional class names
can be provided to adjust the styling of different parts of the layout.

Parameters
----------
title : str
    The text to be displayed as the title of the section.
content_id : str
    The `id` attribute for the top-level container element, typically used for
    referencing or callback purposes in Dash applications.
children : list or None, optional
    A list of Dash components to be included as the content of the section.
    Defaults to an empty list if not provided.
external_links_component : Dash component or None, optional
    A Dash component containing external links or any additional content
    to be appended near the title. Defaults to None.
wrapper_class_name : str, default='p-0 d-flex flex-column h-100'
    The CSS class name(s) to be applied to the top-level container element.
title_wrapper_class_name : str, default='d-flex justify-content-center align-items-center'
    The CSS class name(s) to be applied to the container wrapping the title.
title_text_class_name : str, default='text-center text-white component-master-title'
    The CSS class name(s) to be applied to the text element displaying the title.
content_wrapper_class_name : str, default='d-flex flex-column gap-1 h-100'
    The CSS class name(s) to be applied to the container wrapping the content.

Returns
-------
dbc.Container
    A Dash Bootstrap `Container` component structured with title, content, and
    optional external links, styled as per the provided or default class names.
"""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html


def build_section_shell(
    *,
    title: str,
    content_id: str,
    children=None,
    external_links_component=None,
    wrapper_class_name: str = 'p-0 d-flex flex-column h-100',
    title_wrapper_class_name: str = 'd-flex justify-content-center align-items-center',
    title_text_class_name: str = 'text-center text-white component-master-title',
    content_wrapper_class_name: str = 'd-flex flex-column gap-1 h-100',
) -> dbc.Container:
    children = children or []

    header_children = [html.P(className=title_text_class_name, children=[title])]

    if external_links_component is not None:
        header_children.append(external_links_component)

    return dbc.Container(
        id=content_id,
        className=wrapper_class_name,
        fluid=True,
        children=[
            html.Div(className=title_wrapper_class_name, children=header_children),
            html.Div(className=content_wrapper_class_name, children=children),
        ],
    )
