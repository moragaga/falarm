"""
A module for building dynamic Dash display cards.

Provides utility functions to construct and render Bootstrap-based
display cards with optional footer elements such as identifiers and
definitions. The cards are modular and configurable, allowing for
custom children components and class names for styling.

Functions
---------
build_display_card:
    Constructs and returns a Dash `Row` containing a display card
    component with the given configuration.

_build_wrapper_class_name:
    Generates the class name string for the card's wrapping container.

_build_card_class_name:
    Generates the class name string for the card's main component.

_build_footer:
    Constructs the optional footer for the card, including identifier
    and definition elements if specified.
"""

from __future__ import annotations

from typing import Any, Sequence

import dash_bootstrap_components as dbc
from dash import html


def build_display_card(
    uuid: str,
    name: str,
    class_name_component: str,
    children: Sequence[Any] | None = None,
    class_name_wrapper: str | None = None,
    show_identifier: bool = False,
    show_definition: bool = False,
):
    children = list(children or [])
    class_name_wrapper = class_name_wrapper or ''

    card_component = dbc.Card(
        className=_build_card_class_name(class_name_component),
        children=[
            dbc.CardBody(
                className='d-flex flex-column justify-content-between h-100',
                children=[
                    html.Div(className='h-100 d-flex flex-column', children=children),
                    _build_footer(
                        uuid=uuid,
                        name=name,
                        show_identifier=show_identifier,
                        show_definition=show_definition,
                    ),
                ],
            )
        ],
    )

    return dbc.Row(
        className=_build_wrapper_class_name(class_name_wrapper=class_name_wrapper),
        children=[
            dbc.Col(className='p-0', xs=12, sm=12, md=12, lg=12, xl=12, children=[card_component])
        ],
    )


def _build_wrapper_class_name(class_name_wrapper: str) -> str:
    base_classes = ['g-0']
    if class_name_wrapper:
        base_classes.insert(0, class_name_wrapper)
    return ' '.join(base_classes)


def _build_card_class_name(class_name_component: str) -> str:
    base_classes = [class_name_component, 'position-relative', 'display-card-content-wrapper']
    return ' '.join(base_classes)


def _build_footer(*, uuid: str, name: str, show_identifier: bool, show_definition: bool):
    if not show_identifier and not show_definition:
        return html.Div()

    footer_children = []

    if show_identifier:
        footer_children.append(html.P(className='text-center fw-bold m-0', children=[name.upper()]))

    if show_definition:
        footer_children.append(
            html.Div(
                className='position-absolute bottom-0 end-0',
                children=[
                    html.I(
                        className='bi bi-info-circle pe-1 active-cursor',
                    )
                ],
            )
        )

    return html.Div(
        className='position-relative display-card-footer',
        children=footer_children,
    )
