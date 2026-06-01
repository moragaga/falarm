"""
This module provides the `ConfigStatusService` class responsible for fetching the status
of configuration artifacts by combining data from a manifest and a publication state.

Classes
-------
ConfigStatusService
    A service for retrieving the status of configuration artifacts.
"""

from __future__ import annotations

from ..models import (
    ConfigArtifactStatusView,
)
from ..repositories import ConfigManifestRepository, ConfigPublicationStateRepository


class ConfigStatusService:
    def __init__(
        self,
        manifest_repository: ConfigManifestRepository,
        publication_state_repository: ConfigPublicationStateRepository,
    ) -> None:
        self._manifest_repository = manifest_repository
        self._publication_state_repository = publication_state_repository

    def get_status(self) -> list[ConfigArtifactStatusView]:
        manifest = self._manifest_repository.load_manifest()
        publication_state = self._publication_state_repository.load_state()

        published_by_key = {
            artifact.artifact_key: artifact for artifact in publication_state.artifacts
        }

        views: list[ConfigArtifactStatusView] = []

        for artifact in manifest.artifacts:
            published = published_by_key.get(artifact.artifact_key)

            if published is None:
                status = 'unpublished'
            elif (
                published.published_revision == artifact.revision
                and published.published_hash == artifact.content_hash
            ):
                status = 'published'
            else:
                status = 'pending_publish'

            views.append(
                ConfigArtifactStatusView(
                    artifact_key=artifact.artifact_key,
                    display_name=artifact.display_name,
                    category=artifact.category,
                    sharepoint_revision=artifact.revision,
                    sharepoint_hash=artifact.content_hash,
                    sharepoint_updated_at=artifact.updated_at,
                    sharepoint_updated_by=artifact.updated_by,
                    published_revision=published.published_revision if published else None,
                    published_hash=published.published_hash if published else None,
                    published_at=published.published_at if published else None,
                    published_by=published.published_by if published else None,
                    status=status,
                )
            )

        views.sort(key=lambda item: (item.category, item.display_name, item.artifact_key))
        return views
