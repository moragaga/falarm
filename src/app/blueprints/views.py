"""Blueprint providing view-related routes for the application.

This module handles the routing of view-related endpoints using Flask's
Blueprint functionality. It includes routes for managing user-related
actions, such as logging out.

Blueprint:
    views_bp: The Blueprint object for view-related routes.
"""

from __future__ import annotations

from flask import Blueprint, current_app, redirect, request, session

views_bp = Blueprint('views_bp', __name__)


@views_bp.route('/logout')
def logout():
    session.clear()
    if current_app.config.get('FLASK_ENV') == 'LOCAL':
        return redirect('/')

    return redirect('https://{0}/.auth/logout'.format(request.host))
