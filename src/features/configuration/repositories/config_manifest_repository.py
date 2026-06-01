"""
This module provides a repository for managing configuration manifests
within a SharePoint-like system. It offers methods to load and save
configuration manifests to and from a remote repository using a specific
JSON-based file format.

Classes
-------
ConfigManifestRepository
    Handles operations for persisting and retrieving configuration
    manifests.
"""

from __future__ import annotations

from ..models.config_manifest import ConfigManifest
from .configuration_sharepoint_repository import ConfigurationSharepointRepository


class ConfigManifestRepository:
    FILENAME = 'config_manifest.json.gz'
    RELATIVE_PATH = None

    def __init__(self, repository: ConfigurationSharepointRepository) -> None:
        self._repository = repository

    def load_manifest(self) -> ConfigManifest:
        data = self._repository.load_document(
            filename=self.FILENAME,
            relative_path=self.RELATIVE_PATH,
            default=None,
        )

        if data is None:
            return ConfigManifest()

        if isinstance(data, dict):
            return ConfigManifest.from_dict(data)

        if isinstance(data, list):
            return ConfigManifest.from_dict({'artifacts': data})

        raise ValueError(
            'config_manifest.json.gz tiene un formato inválido. '
            'Debe ser un objeto JSON o una lista de artefactos.'
        )

    def save_manifest(self, manifest: ConfigManifest) -> bool:
        return self._repository.save_document(
            filename=self.FILENAME,
            relative_path=self.RELATIVE_PATH,
            document=manifest.to_dict(),
        )
