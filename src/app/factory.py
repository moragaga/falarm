"""
Module for creating and configuring the Flask application.

This module defines the functions required to initialize and configure a Flask
application including setting up configurations, initializing extensions,
and registering blueprints. The application leverages environment-specific
configurations and ensures secure session handling.

Functions
---------
create_flask_app(settings: EnvConfiguration) -> Flask
    Initializes and configures the Flask application.

_internal
---------
_register_blueprint(app: Flask) -> None
    Registers blueprints with the Flask application.
"""

from __future__ import annotations

from datetime import timedelta

from flask import Flask

from .blueprints import auth_bp, views_bp
from .env_configuration import EnvConfiguration
from .extensions import init_extensions


def create_flask_app(settings: EnvConfiguration) -> Flask:
    app = Flask(__name__)

    app.config.from_mapping(settings.to_flask_configuration())
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.secret_key = settings.secret_key

    init_extensions(app=app, settings=settings)
    _register_blueprint(app=app)

    return app


def _register_blueprint(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
