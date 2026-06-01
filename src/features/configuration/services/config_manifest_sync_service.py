"""
Service for synchronizing the configuration manifest artifacts.

This module provides functionality to synchronize and update registered
artifacts in a configuration manifest with the latest definitions and changes.
It ensures the manifest reflects the latest state of artifacts from the
configuration repository and artifact registry. The synchronization process
includes detecting changes in artifact definitions, updating metadata, and
persisting the updated manifest when necessary.

Classes
-------
ConfigManifestSyncService
    Service to handle synchronization of configuration manifest artifacts.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)

from ..models import (
    ConfigManifest,
    ConfigManifestArtifact,
)
from ..repositories import ConfigManifestRepository, ConfigurationSharepointRepository
from ..services.config_artifact_registry import ConfigArtifactRegistry
from ..services.config_hash_service import ConfigHashService


class ConfigManifestSyncService:
    def __init__(
        self,
        *,
        registry: ConfigArtifactRegistry,
        manifest_repository: ConfigManifestRepository,
        configuration_repository: ConfigurationSharepointRepository,
        hash_service: ConfigHashService,
    ) -> None:
        self._registry = registry
        self._manifest_repository = manifest_repository
        self._configuration_repository = configuration_repository
        self._hash_service = hash_service

    def sync_registered_artifacts(
        self,
        *,
        updated_by: str | None,
    ) -> ConfigManifest:
        manifest = self._manifest_repository.load_manifest()
        artifacts_by_key = self._index_manifest_artifacts(manifest=manifest)

        changed = False
        now = datetime.now(timezone.utc).isoformat()

        for definition in self._registry.get_definitions():
            if definition.remote is None or definition.artifact is None:
                continue

            source_payload = self._configuration_repository.load_document(
                filename=definition.remote.sharepoint_filename,
                relative_path=definition.remote.relative_path,
                default=None,
            )

            if source_payload is None:
                continue

            content_hash = self._hash_service.build_hash(source_payload)
            artifact_key = definition.artifact.artifact_key
            existing = artifacts_by_key.get(artifact_key)

            next_artifact, artifact_changed = self._build_next_artifact(
                definition=definition,
                existing=existing,
                content_hash=content_hash,
                updated_at=now,
                updated_by=updated_by,
            )

            if artifact_changed:
                artifacts_by_key[artifact_key] = next_artifact
                changed = True

        if not changed:
            return manifest

        updated_manifest = ConfigManifest(
            artifacts=tuple(
                sorted(
                    artifacts_by_key.values(),
                    key=lambda item: (
                        item.category,
                        item.display_name,
                        item.artifact_key,
                    ),
                )
            )
        )

        self._manifest_repository.save_manifest(updated_manifest)
        return updated_manifest

    @staticmethod
    def _index_manifest_artifacts(
        *,
        manifest: ConfigManifest,
    ) -> dict[str, ConfigManifestArtifact]:
        return {
            artifact.artifact_key: artifact
            for artifact in manifest.artifacts
            if artifact.artifact_key
        }

    @staticmethod
    def _build_next_artifact(
        *,
        definition: AdminDefinition,
        existing: ConfigManifestArtifact | None,
        content_hash: str,
        updated_at: str,
        updated_by: str | None,
    ) -> tuple[ConfigManifestArtifact, bool]:
        artifact: AdminArtifactDefinition = definition.artifact
        projection = artifact.projection
        remote: AdminRemoteDefinition = definition.remote

        if existing is None:
            revision = 1
            effective_updated_at = updated_at
            effective_updated_by = updated_by
            changed = True
        elif existing.content_hash != content_hash:
            revision = existing.revision + 1
            effective_updated_at = updated_at
            effective_updated_by = updated_by
            changed = True
        else:
            revision = existing.revision
            effective_updated_at = existing.updated_at
            effective_updated_by = existing.updated_by
            changed = ConfigManifestSyncService._metadata_changed(
                existing=existing,
                definition=definition,
            )

        artifact = ConfigManifestArtifact(
            artifact_key=artifact.artifact_key,
            display_name=artifact.display_name,
            category=artifact.category,
            filename=remote.sharepoint_filename,
            relative_path=remote.relative_path,
            content_type=artifact.content_type,
            schema_key=artifact.schema_key,
            revision=revision,
            content_hash=content_hash,
            updated_at=effective_updated_at,
            updated_by=effective_updated_by,
            is_active=True,
            target_container_name=projection.container_name if projection else None,
            target_document_id=projection.document_id if projection else None,
            target_partition_key=projection.partition_key if projection else None,
        )

        return artifact, changed

    @staticmethod
    def _metadata_changed(
        *,
        existing: ConfigManifestArtifact,
        definition: AdminDefinition,
    ) -> bool:
        artifact: AdminArtifactDefinition = definition.artifact
        projection = artifact.projection
        remote: AdminRemoteDefinition = definition.remote
        return any(
            (
                existing.display_name != artifact.display_name,
                existing.category != artifact.category,
                existing.filename != remote.sharepoint_filename,
                existing.relative_path != remote.relative_path,
                existing.content_type != artifact.content_type,
                existing.schema_key != artifact.schema_key,
                existing.target_container_name
                != (projection.container_name if projection else None),
                existing.target_document_id != (projection.document_id if projection else None),
                existing.target_partition_key != (projection.partition_key if projection else None),
            )
        )
