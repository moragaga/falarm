"""
Generates the HTML structure for the navigation offcanvas title.

This function constructs a `Div` component using the Dash HTML module. The
generated structure includes an icon, a heading, and a subtitle to compose
the title section of the navigation offcanvas.

Returns
-------
dash.html.Div
    A Div component containing the icon, heading, and subtitle for the
    navigation offcanvas title.
"""

from __future__ import annotations

from dash import html


def build_navigation_offcanvas_title() -> html.Div:
    return html.Div(
        className='app-navigation-offcanvas-title',
        children=[
            html.Div(
                className='app-navigation-offcanvas-title-icon',
                children=[
                    html.I(className='bi bi-app-indicator'),
                ],
            ),
            html.Div(
                className='app-navigation-offcanvas-title-text',
                children=[
                    html.H5(
                        className='app-navigation-offcanvas-title-heading',
                        children='ADA N1',
                    ),
                    html.P(
                        className='app-navigation-offcanvas-title-subtitle',
                        children='Navegación del proyecto',
                    ),
                ],
            ),
        ],
    )
