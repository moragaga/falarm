"""
Utility function for creating an error UI component with predefined styling.

This function generates a Dash HTML Div element that displays an error
message styled according to the provided size option. It is used in
user interfaces to indicate the unavailability of a component.

Parameters
----------
ui_size : UiSize, optional
    A predefined size for the component. It determines the padding
    and other size-related styles of the error component. Valid values are:
    'extra-small', 'small', 'medium', 'large', 'extra-large', 'full-width'.
    Defaults to 'small'.

Returns
-------
Component
    A Dash HTML Div element styled as an error message container.
"""

from __future__ import annotations

from typing import Literal

from dash import html
from dash.development.base_component import Component

UiSize = Literal['extra-small', 'small', 'medium', 'large', 'extra-large', 'full-width']


def build_error_component(ui_size: UiSize = 'small') -> Component:
    sizes = {
        'extra-small': 'py-0 px-2',
        'small': 'py-1 px-2',
        'medium': 'py-2 px-2',
        'large': 'py-3 px-2',
        'extra-large': 'py-4 px-2',
        'full-width': 'py-5 px-2',
    }

    return html.Div(
        style={
            'background': 'linear-gradient(180deg, rgba(5,4,4,0.44) 0%, rgba(5,4,4,0.34) 100%)',
            'border': '1px solid rgba(255, 255, 255, 0.05)',
            'borderRadius': '10px',
            'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.25)',
        },
        className=f'd-flex justify-content-center align-items-center '
        f'{sizes.get(ui_size, "p-1")} mb-2 w-100',
        children=[
            html.P(
                className='text-center text-white fw-semibold font-size-100 mb-0',
                children='Componente no disponible',
            )
        ],
    )
