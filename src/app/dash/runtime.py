"""Module providing functionality to set and retrieve a Dash application instance.

This module facilitates the management of a global Dash application instance.
Functions are provided to set the instance of the Dash app and retrieve it when
needed. An error is raised if retrieval is attempted before initialization.
"""

from __future__ import annotations

from dash import Dash

_dash_app: Dash | None = None


def set_dash_app(dash_app: Dash):
    global _dash_app
    _dash_app = dash_app


def get_dash_app() -> Dash:
    if _dash_app is None:
        raise RuntimeError('Dash app has not been initialized yet')
    return _dash_app
