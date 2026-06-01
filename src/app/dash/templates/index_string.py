"""
Generates an HTML index page string with customizable parameters.

This module provides functionality for dynamically generating an HTML index
page string based on a provided template. The function `get_index_page_string`
replaces placeholders within the template using the given input parameters.

Attributes
----------
INDEX_PAGE_STRING : str
    A constant string containing the base HTML template with placeholder
    variables to be replaced using specified parameters.

Functions
---------
get_index_page_string(appinsights_connection_string, app_short_name,
                      user_session_tracking_enabled, app_version)
    Constructs and returns the HTML index page string with the placeholders
    replaced by the given parameters.
"""

from __future__ import annotations

import json
from urllib.parse import quote

INDEX_PAGE_STRING = """
<!DOCTYPE html>
<html lang="es">
    <head>
        {%metas%}

        <meta name="theme-color" content="#000000">
        <meta name="background-color" content="#ffffff">

        <meta name="application-name" content="__APP_SHORT_NAME__">
        <meta name="apple-mobile-web-app-title" content="__APP_SHORT_NAME__">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">

        <meta name="mobile-web-app-capable" content="yes">
        <meta name="format-detection" content="telephone=no">

        <title>{%title%}</title>

        <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" sizes="167x167" href="/apple-touch-icon-167x167.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" href="/apple-touch-icon.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-precomposed.png?v=__APP_VERSION__">

        <link rel="manifest" href="/manifest.webmanifest?v=__APP_VERSION__" crossorigin="use-credentials">

        <link rel="icon" sizes="192x192" href="/assets/img/branding/logos/web-app-manifest-192x192.png?v=__APP_VERSION__">
        <link rel="icon" sizes="512x512" href="/assets/img/branding/logos/web-app-manifest-512x512.png?v=__APP_VERSION__">
        <link rel="icon" href="/assets/favicon.ico?v=__APP_VERSION__" type="image/x-icon">

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">

        {%favicon%}
        {%css%}

        <script type="text/javascript">
            window.APPINSIGHTS_CONNECTION_STRING = __APPINSIGHTS_CONNECTION_STRING__;
        </script>

        <script type="text/javascript">
            window.ADA_RUNTIME_CONFIG = {
                userSessionTrackingEnabled: __USER_SESSION_TRACKING_ENABLED__
            };
        </script>

        <script type="text/javascript">
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js', {
                    scope: '/'
                }).then((registration) => {
                    registration.update().catch((error) => {
                        console.warn('Service worker update failed:', error);
                    });
                }).catch((error) => {
                    console.warn('Service worker registration failed:', error);
                });
            });
        }
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


def get_index_page_string(
    appinsights_connection_string: str,
    app_short_name: str,
    user_session_tracking_enabled: bool,
    app_version: str,
) -> str:
    safe_app_version = quote(
        str(app_version or 'local'),
        safe='',
    )

    parameters = {
        '__APP_SHORT_NAME__': app_short_name,
        '__APPINSIGHTS_CONNECTION_STRING__': json.dumps(appinsights_connection_string),
        '__USER_SESSION_TRACKING_ENABLED__': json.dumps(user_session_tracking_enabled),
        '__APP_VERSION__': safe_app_version,
    }

    index = INDEX_PAGE_STRING

    for key, value in parameters.items():
        index = index.replace(key, value)

    return index
