"""
Service for managing configuration manifests.

This module provides methods to interact with configuration manifests,
including registering updates, retrieving manifests, and handling
artifacts within a manifest.

Classes
-------
ConfigManifestService
    A service class responsible for managing configuration manifests.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.features.admin_framework.models.admin_definition import AdminDefinition
from src.features.configuration.models import (
    ConfigManifest,
    ConfigManifestArtifact,
)
from src.features.configuration.repositories import (
    ConfigManifestRepository,
)
from src.features.configuration.services.config_hash_service import ConfigHashService


class ConfigManifestService:
    def __init__(
        self,
        repository: ConfigManifestRepository,
        hash_service: ConfigHashService | None = None,
    ) -> None:
        self._repository = repository
        self._hash_service = hash_service or ConfigHashService()

    def register_update(
        self,
        definition: AdminDefinition,
        rows: list[dict] | dict,
        updated_by: str | None,
    ) -> bool:
        if definition.remote is None or definition.artifact is None:
            return False

        manifest = self._repository.load_manifest()

        content_hash = self._hash_service.build_hash(rows)
        updated_at = datetime.now(timezone.utc).isoformat()

        existing = self._find_artifact(
            manifest=manifest,
            artifact_key=definition.artifact.artifact_key,
        )

        if existing is None:
            next_revision = 1
        elif existing.content_hash == content_hash:
            next_revision = existing.revision
        else:
            next_revision = existing.revision + 1

        projection = definition.artifact.projection

        artifact = ConfigManifestArtifact(
            artifact_key=definition.artifact.artifact_key,
            display_name=definition.artifact.display_name,
            category=definition.artifact.category,
            filename=definition.remote.sharepoint_filename,
            relative_path=definition.remote.relative_path,
            content_type=definition.artifact.content_type,
            schema_key=definition.artifact.schema_key,
            revision=next_revision,
            content_hash=content_hash,
            updated_at=updated_at,
            updated_by=updated_by,
            is_active=True,
            target_container_name=projection.container_name if projection else None,
            target_document_id=projection.document_id if projection else None,
            target_partition_key=projection.partition_key if projection else None,
        )

        updated_manifest = self._upsert_artifact(
            manifest=manifest,
            artifact=artifact,
        )

        if self._looks_destructive(
            before=manifest,
            after=updated_manifest,
        ):
            return False

        return self._repository.save_manifest(updated_manifest)

    def get_manifest(self) -> ConfigManifest:
        return self._repository.load_manifest()

    @staticmethod
    def _find_artifact(
        *,
        manifest: ConfigManifest,
        artifact_key: str,
    ) -> ConfigManifestArtifact | None:
        for artifact in manifest.artifacts:
            if artifact.artifact_key == artifact_key:
                return artifact

        return None

    @staticmethod
    def _upsert_artifact(
        *,
        manifest: ConfigManifest,
        artifact: ConfigManifestArtifact,
    ) -> ConfigManifest:
        artifacts = list(manifest.artifacts)
        replaced = False

        for index, current in enumerate(artifacts):
            if current.artifact_key == artifact.artifact_key:
                artifacts[index] = artifact
                replaced = True
                break

        if not replaced:
            artifacts.append(artifact)

        artifacts.sort(
            key=lambda item: (
                item.category,
                item.display_name,
                item.artifact_key,
            )
        )

        return ConfigManifest(
            artifacts=tuple(artifacts),
        )

    @staticmethod
    def _looks_destructive(
        *,
        before: ConfigManifest,
        after: ConfigManifest,
    ) -> bool:
        before_keys = {
            artifact.artifact_key for artifact in before.artifacts if artifact.artifact_key
        }

        after_keys = {
            artifact.artifact_key for artifact in after.artifacts if artifact.artifact_key
        }

        if not before_keys:
            return False

        return not before_keys.issubset(after_keys)
