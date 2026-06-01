"""
A repository class for managing identity-related data in SharePoint.

This module provides functionality to load and save identity data from/to
SharePoint using a configured repository and identity settings.

Classes
-------
SharePointIdentityRepository
    Handles operations related to identity user data in SharePoint.
"""

from __future__ import annotations

import logging

from src.features.configuration.repositories import (
    ConfigurationSharepointRepository,
)

from ..settings import IdentitySettings

logger = logging.getLogger(__name__)


class SharePointIdentityRepository:
    def __init__(
        self,
        repository: ConfigurationSharepointRepository,
        settings: IdentitySettings,
    ) -> None:
        self._repository = repository
        self._settings = settings

    def load_rows(self) -> list[dict]:
        try:
            rows = self._repository.load_rows(
                filename=self._settings.users_filename,
                relative_path=self._settings.users_relative_path,
            )
        except Exception:
            logger.exception(
                '[IDENTITY] Could not load identity users from SharePoint. Using empty user list.'
            )
            return []

        if not isinstance(rows, list):
            return []

        return [row for row in rows if isinstance(row, dict)]

    def save_rows(
        self,
        rows: list[dict],
    ) -> bool:
        try:
            return bool(
                self._repository.save_rows(
                    filename=self._settings.users_filename,
                    relative_path=self._settings.users_relative_path,
                    rows=rows,
                )
            )
        except Exception:
            logger.exception('[IDENTITY] Could not save identity users to SharePoint.')
            return False
