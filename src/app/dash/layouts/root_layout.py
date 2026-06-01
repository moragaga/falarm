"""
Defines the RootLayout class responsible for rendering the root layout in a Dash application.

This module provides a static method to render the primary layout container, including URL
location tracking, page content rendering, and version information embedding.

Classes
-------
RootLayout: A utility class for rendering the root layout.
"""

from __future__ import annotations

from dash import dcc, html, page_container


class RootLayout:
    @staticmethod
    def render(version: str):
        return html.Div(
            children=[
                dcc.Location(id='url', refresh=False),
                html.Div(
                    id='page-content',
                    children=[
                        page_container,
                    ],
                ),
                html.Span(className='d-none', children=[version]),
            ]
        )
