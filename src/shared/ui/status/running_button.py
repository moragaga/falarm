"""
Provides a utility function to build the contents of a running button
component for use with Dash web applications.

This module contains a function for constructing a Dash HTML `Span`
component with customized child elements for a running button, including
a spinner and a text label. The generated component is intended to be
used as part of a Dash web application's user interface.
"""

from __future__ import annotations

from dash import html
from dash.development.base_component import Component


def build_running_button_children(
    *,
    text: str,
) -> Component:
    return html.Span(
        className='app-running-button-content',
        children=[
            html.Span(
                className='spinner-border spinner-border-sm app-running-button-spinner',
                role='status',
                **{
                    'aria-hidden': 'true',
                },
            ),
            html.Span(
                className='app-running-button-label',
                children=text,
            ),
        ],
    )
