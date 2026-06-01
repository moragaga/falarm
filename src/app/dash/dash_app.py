"""
This module initializes and configures a Dash application, enabling integration
with a Flask server. It provides helper functions to resolve directory paths
and retrieve application versioning.

Functions
---------
init_dash_app(app: Flask, settings: EnvConfiguration) -> Dash
    Initializes and configures a Dash application using the provided Flask
    server and application settings.

_resolve_root_path() -> tuple[Path, Path]
    Resolves and returns the paths for assets and pages directories relative
    to the project's root directory.

_get_app_version() -> str
    Reads the application version from the version file in the assets directory.
    If unavailable or an error is raised, it defaults to 'V0'.

_get_root_path() -> Path
    Retrieves the root directory of the project based on the path ending
    with 'src'. Raises a ValueError if the root path cannot be resolved.
"""

from __future__ import annotations

from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask

from src.shared.time.timestamps import parse_utc_datetime

from ..bootstrap.callback_registry import register_dash_callbacks
from ..env_configuration import EnvConfiguration
from .layouts.root_layout import RootLayout
from .runtime import set_dash_app
from .templates.index_string import get_index_page_string


def init_dash_app(app: Flask, settings: EnvConfiguration) -> Dash:
    ASSETS_DIR, PAGES_DIR = _resolve_root_path()
    app_version = _get_app_version()
    dash_app = Dash(
        name=__name__,
        server=app,
        use_pages=True,
        title=settings.app_name.replace('"', ''),
        update_title='Updating...',
        index_string=get_index_page_string(
            appinsights_connection_string=settings.application_insights_connection_string,
            app_short_name=settings.app_short_name.replace('"', ''),
            user_session_tracking_enabled=not settings.is_local,
            app_version=app_version,
        ),
        assets_folder=str(ASSETS_DIR),
        pages_folder=str(PAGES_DIR),
        meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],
        suppress_callback_exceptions=not settings.is_local,
        external_stylesheets=[
            dbc.icons.BOOTSTRAP,
        ],
    )
    dash_app.layout = RootLayout.render(version=app_version)

    set_dash_app(dash_app=dash_app)
    register_dash_callbacks()

    return dash_app


def _resolve_root_path() -> tuple[Path, Path]:
    BASE_DIR = _get_root_path()
    return BASE_DIR / 'assets', BASE_DIR / 'pages'


def _get_app_version() -> str:
    try:
        BASE_DIR = _get_root_path()
        BASE_DIR = BASE_DIR / 'assets' / 'version.txt'
        with open(BASE_DIR, 'r') as file:
            version = file.read().strip()

        version = parse_utc_datetime(value=version)
        version = version.strftime('%Y.%m.%d-%H%M')
        version = f'V{version}'
    except Exception:
        # print('[ERROR] Error initializing read version: ', e)
        version = 'V0'

    return version


def _get_root_path() -> Path:
    paths = Path(__file__).resolve().parents
    BASE_DIR = next((path for path in paths if str(path).endswith('src')), None)
    if not BASE_DIR:
        raise ValueError('[ERROR] Could not resolve root path')
    return BASE_DIR
