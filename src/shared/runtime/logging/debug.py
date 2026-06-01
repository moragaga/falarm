"""
Functions for debugging in a Flask application.

This module provides utility functions to determine if the application is in
debug mode and to log messages conditionally, based on the debug mode status.
"""

from __future__ import annotations

from flask import current_app


def debug_enabled() -> bool:
    try:
        return current_app.config['FLASK_ENV'] == 'LOCAL'
    except RuntimeError:
        return False


def debug_log(*args, **kwargs) -> None:
    if debug_enabled():
        print(*args, **kwargs)
