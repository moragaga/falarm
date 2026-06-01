"""Service for managing the publication of configuration artifacts.

This module facilitates the publication of configuration artifacts to specified
target locations, such as Cosmos DB, while updating the publication state. The
service ensures validation of artifacts, manages consistency in the publication
state, and checks for destructive updates before committing changes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.shared.infrastructure.cosmos import CosmosService

from ..models import (
    ConfigManifestArtifact,
    ConfigPublicationState,
    PublishedArtifactState,
)
from ..repositories import (
    ConfigManifestRepository,
    ConfigPublicationStateRepository,
    ConfigurationSharepointRepository,
)


class ConfigPublicationService:
    def __init__(
        self,
        manifest_repository: ConfigManifestRepository,
        publication_state_repository: ConfigPublicationStateRepository,
        configuration_repository: ConfigurationSharepointRepository,
        cosmos_service: CosmosService | None = None,
    ) -> None:
        self._manifest_repository = manifest_repository
        self._publication_state_repository = publication_state_repository
        self._configuration_repository = configuration_repository
        self._cosmos_service = cosmos_service

    def publish_artifact(
        self,
        *,
        artifact_key: str,
        published_by: str | None,
    ) -> tuple[bool, str | None]:
        manifest = self._manifest_repository.load_manifest()

        artifact = next(
            (item for item in manifest.artifacts if item.artifact_key == artifact_key),
            None,
        )

        if artifact is None:
            return False, 'No se encontró el artefacto en el config manifest.'

        if not artifact.target_container_name:
            return False, 'El artefacto no tiene contenedor de destino configurado.'

        source_payload = self._configuration_repository.load_document(
            filename=artifact.filename,
            relative_path=artifact.relative_path,
            default=None,
        )

        if source_payload is None:
            return False, 'No se pudo cargar el artefacto fuente desde SharePoint.'

        copied, copy_error = self._copy_to_current_cosmos(
            artifact=artifact,
            source_payload=source_payload,
        )

        if not copied:
            return False, copy_error or 'No se pudo copiar el artefacto al Cosmos actual.'

        current_state = self._publication_state_repository.load_state()

        published_artifact = PublishedArtifactState(
            artifact_key=artifact.artifact_key,
            published_revision=artifact.revision,
            published_hash=artifact.content_hash,
            published_at=datetime.now(timezone.utc).isoformat(),
            published_by=published_by,
        )

        updated_state = self._upsert_published_artifact(
            state=current_state,
            artifact=published_artifact,
        )

        if self._looks_destructive(
            before=current_state,
            after=updated_state,
        ):
            return (
                False,
                'La actualización del publication state parece destructiva. '
                'No se guardó el estado publicado.',
            )

        saved = self._publication_state_repository.save_state(updated_state)

        if not saved:
            return (
                False,
                'El artefacto se publicó, pero no se pudo actualizar el publication state.',
            )

        return True, None

    def _copy_to_current_cosmos(
        self,
        *,
        artifact: ConfigManifestArtifact,
        source_payload: Any,
    ) -> tuple[bool, str | None]:
        if self._cosmos_service is None:
            return False, 'CosmosService no está inicializado.'

        container_name = artifact.target_container_name
        document_id = artifact.target_document_id or artifact.artifact_key
        partition_key = artifact.target_partition_key or document_id

        document = {
            'id': document_id,
            'partition_key': partition_key,
            'artifact_key': artifact.artifact_key,
            'revision': artifact.revision,
            'content_hash': artifact.content_hash,
            'data': source_payload,
        }

        upserted = self._cosmos_service.upsert(
            container_name=container_name,
            item=document,
        )

        if not upserted:
            return False, 'No se pudo persistir el documento publicado.'

        return True, None

    @staticmethod
    def _upsert_published_artifact(
        *,
        state: ConfigPublicationState,
        artifact: PublishedArtifactState,
    ) -> ConfigPublicationState:
        artifacts = list(state.artifacts)
        replaced = False

        for index, current in enumerate(artifacts):
            if current.artifact_key == artifact.artifact_key:
                artifacts[index] = artifact
                replaced = True
                break

        if not replaced:
            artifacts.append(artifact)

        artifacts.sort(key=lambda item: item.artifact_key)

        return ConfigPublicationState(
            artifacts=tuple(artifacts),
        )

    @staticmethod
    def _looks_destructive(
        *,
        before: ConfigPublicationState,
        after: ConfigPublicationState,
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
