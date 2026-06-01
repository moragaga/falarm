"""
This module provides the `EnvConfiguration` data class to manage environment
variables required for application configuration. It validates the presence of
all required environment variables and offers utility methods for interacting
with configurations in Flask applications.

Classes
-------
EnvConfiguration :
    A frozen dataclass that holds configuration values loaded from environment
    variables, with utilities to validate, query, and transform the configuration.

Functions
---------
No standalone functions are included in this module.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv

REQUIRED_ENV_VARS = (
    'APPLICATION_INSIGHTS_CONNECTION_STRING',
    'COSMOS_DATABASE_NAME',
    'COSMOS_ACCOUNT_KEY',
    'COSMOS_ACCOUNT_URI',
    'COSMOS_CONNECTION_MODE',
    'APP_NAME',
    'APP_SHORT_NAME',
    'SHAREPOINT_ROOT_PATH',
    'SECRET_KEY',
    'FLASK_ENV',
)


@dataclass(frozen=True)
class EnvConfiguration:
    application_insights_connection_string: str
    cosmos_database_name: str
    cosmos_account_key: str
    cosmos_account_uri: str
    cosmos_connection_mode: str
    app_name: str
    app_short_name: str
    secret_key: str
    sharepoint_root_path: str
    flask_env: str
    first_load: bool = False

    @classmethod
    def from_env(cls) -> EnvConfiguration:
        load_dotenv()

        env = {key: os.getenv(key) for key in REQUIRED_ENV_VARS}
        missing = [key for key, value in env.items() if not value]

        if missing:
            missing_vars = ', '.join(missing)
            raise ValueError(f'[ERROR] Missing required environment variables: {missing_vars}')

        return cls(
            application_insights_connection_string=env.get(
                'APPLICATION_INSIGHTS_CONNECTION_STRING'
            ),
            cosmos_database_name=env.get('COSMOS_DATABASE_NAME'),
            cosmos_account_key=env.get('COSMOS_ACCOUNT_KEY'),
            cosmos_account_uri=env.get('COSMOS_ACCOUNT_URI'),
            cosmos_connection_mode=env.get('COSMOS_CONNECTION_MODE'),
            app_name=cls._resolve_text(value=env.get('APP_NAME')),
            app_short_name=cls._resolve_text(value=env.get('APP_SHORT_NAME')),
            secret_key=cls._resolve_text(value=env.get('SECRET_KEY')),
            sharepoint_root_path=env.get('SHAREPOINT_ROOT_PATH'),
            flask_env=env.get('FLASK_ENV'),
            first_load=cls._is_first_load(),
        )

    @property
    def is_local(self) -> bool:
        return self.flask_env == 'LOCAL'

    @property
    def is_first_load(self) -> bool:
        return self.first_load

    @property
    def is_remote_service(self):
        return self.cosmos_connection_mode == 'REMOTE'

    def to_flask_configuration(self) -> dict:
        return {
            'APPLICATION_INSIGHTS_CONNECTION_STRING': self.application_insights_connection_string,
            'COSMOS_DATABASE_NAME': self.cosmos_database_name,
            'COSMOS_ACCOUNT_KEY': self.cosmos_account_key,
            'COSMOS_ACCOUNT_URI': self.cosmos_account_uri,
            'COSMOS_CONNECTION_MODE': self.cosmos_connection_mode,
            'APP_NAME': self.app_name,
            'APP_SHORT_NAME': self.app_short_name,
            'SECRET_KEY': self.secret_key,
            'SHAREPOINT_ROOT_PATH': self.sharepoint_root_path,
            'FLASK_ENV': self.flask_env,
            'FIRST_LOAD': self.first_load,
        }

    @staticmethod
    def _is_first_load():
        return '--first-load' in sys.argv

    @staticmethod
    def _resolve_text(value: str) -> str:
        return str(value).strip().replace('"', '')
