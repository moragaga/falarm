"""
Provides a function to build a UI shell for app information display.

This module contains a function that creates a Dash HTML `Div` component
with a specific class name. The component serves as a container for
displaying app-related information.

Functions
---------
- build_app_information_shell: Constructs an HTML container with
  predefined styling for app information.
"""

from __future__ import annotations

from dash import html


def build_app_information_shell(*, content=None) -> html.Div:
    content = content or []
    return html.Div(className='app-information-shell', children=content)
