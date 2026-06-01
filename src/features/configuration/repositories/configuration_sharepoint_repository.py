"""
This module provides a repository for interacting with configuration files located
in a SharePoint environment. It offers functionality to load, save, upload, and
download configuration data in various formats.

Classes
-------
ConfigurationSharepointRepository
    A repository for managing configuration data in SharePoint.
"""

from __future__ import annotations

from typing import Any

from src.shared.infrastructure.sharepoint import SharepointFileType, SharepointService


class ConfigurationSharepointRepository:
    def __init__(self, sharepoint_service: SharepointService | None = None) -> None:
        self._sharepoint_service = sharepoint_service

    def load_rows(
        self,
        filename: str,
        relative_path: str | None,
    ) -> list[dict] | dict:
        document = self.load_document(
            filename=filename,
            relative_path=relative_path,
            default=[],
        )

        if isinstance(document, (list, dict)):
            return document

        return []

    def save_rows(
        self,
        filename: str,
        relative_path: str | None,
        rows: list[dict] | dict,
    ) -> bool:
        return self.save_document(
            filename=filename,
            relative_path=relative_path,
            document=rows,
        )

    def load_document(
        self,
        *,
        filename: str,
        relative_path: str | None,
        default: Any = None,
    ) -> Any:
        if self._sharepoint_service is None:
            raise RuntimeError('SharePointService no está inicializado.')

        return self._sharepoint_service.load_json(
            filename=filename,
            file_type=SharepointFileType.CONFIGURATION,
            relative_path=relative_path,
            default=default,
        )

    def save_document(
        self,
        *,
        filename: str,
        relative_path: str | None,
        document: Any,
    ) -> bool:
        if self._sharepoint_service is None:
            raise RuntimeError('SharePointService no está inicializado.')

        return self._sharepoint_service.save_json(
            filename=filename,
            data=document,
            file_type=SharepointFileType.CONFIGURATION,
            relative_path=relative_path,
        )

    def upload_file(
        self,
        filename: str,
        relative_path: str | None,
        content: bytes,
    ) -> bool:
        if self._sharepoint_service is None:
            raise RuntimeError('SharePointService no está inicializado.')

        return self._sharepoint_service.upload_file(
            filename=filename,
            content=content,
            file_type=SharepointFileType.CONFIGURATION,
            relative_path=relative_path,
        )

    def download_file(
        self,
        filename: str,
        relative_path: str | None,
    ) -> Any:
        if self._sharepoint_service is None:
            raise RuntimeError('SharePointService no está inicializado.')

        return self._sharepoint_service.download_file(
            filename=filename,
            file_type=SharepointFileType.CONFIGURATION,
            relative_path=relative_path,
        )
