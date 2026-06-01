"""PublicationManagerActionService handles actions related to publication management.

This service provides functionality to refresh artifact statuses, publish selected
artifacts, and publish pending artifacts. It interacts with other services for status
synchronization, artifact publication, and preparation of status rows. The results
are encapsulated in a `PublicationManagerActionResult` object, which includes rows
and optionally error messages or success messages.

Attributes
----------
PUBLISHABLE_STATUS_CODES : set[str]
    A set of status codes indicating that artifacts are eligible for publication.

"""

from __future__ import annotations

from typing import Any

from src.features.configuration.services import (
    ConfigManifestSyncService,
    ConfigPublicationService,
    ConfigStatusService,
)

from ..models.publication_manager_action_result import PublicationManagerActionResult
from .publication_manager_row_service import PublicationManagerRowService

PUBLISHABLE_STATUS_CODES = {
    'unpublished',
    'pending_publish',
}


class PublicationManagerActionService:
    def __init__(
        self,
        *,
        status_service: ConfigStatusService,
        publication_service: ConfigPublicationService,
        manifest_sync_service: ConfigManifestSyncService,
    ) -> None:
        self._status_service = status_service
        self._publication_service = publication_service
        self._manifest_sync_service = manifest_sync_service

    def refresh(
        self,
        *,
        updated_by: str | None,
    ) -> PublicationManagerActionResult:
        self._manifest_sync_service.sync_registered_artifacts(
            updated_by=updated_by,
        )

        return PublicationManagerActionResult(
            rows=self._build_status_rows(),
        )

    def publish_selected(
        self,
        *,
        selected_rows: list[dict[str, Any]] | None,
        published_by: str | None,
    ) -> PublicationManagerActionResult:
        self._manifest_sync_service.sync_registered_artifacts(
            updated_by=published_by,
        )

        artifact_keys = self._resolve_selected_artifact_keys(
            selected_rows=selected_rows or [],
        )

        if not artifact_keys:
            return PublicationManagerActionResult(
                rows=self._build_status_rows(),
                errors=('Debes seleccionar al menos un artefacto válido para publicar.',),
            )

        return self._publish_artifact_keys(
            artifact_keys=artifact_keys,
            published_by=published_by,
            success_message='Los artefactos seleccionados fueron publicados correctamente.',
        )

    def publish_pending(
        self,
        *,
        published_by: str | None,
    ) -> PublicationManagerActionResult:
        self._manifest_sync_service.sync_registered_artifacts(
            updated_by=published_by,
        )

        status_rows = self._build_status_rows()

        artifact_keys = [
            str(row.get('artifact_key') or '').strip()
            for row in status_rows
            if row.get('status_code') in PUBLISHABLE_STATUS_CODES
            and str(row.get('artifact_key') or '').strip()
        ]

        if not artifact_keys:
            return PublicationManagerActionResult(
                rows=status_rows,
                errors=('No existen artefactos pendientes para publicar.',),
            )

        return self._publish_artifact_keys(
            artifact_keys=artifact_keys,
            published_by=published_by,
            success_message='Todos los artefactos pendientes fueron publicados correctamente.',
        )

    def _publish_artifact_keys(
        self,
        *,
        artifact_keys: list[str],
        published_by: str | None,
        success_message: str,
    ) -> PublicationManagerActionResult:
        errors: list[str] = []

        for artifact_key in artifact_keys:
            ok, error = self._publication_service.publish_artifact(
                artifact_key=artifact_key,
                published_by=published_by,
            )

            if not ok:
                errors.append(f'{artifact_key}: {error or "No se pudo publicar el artefacto."}')

        rows = self._build_status_rows()

        if errors:
            return PublicationManagerActionResult(
                rows=rows,
                errors=tuple(errors),
            )

        return PublicationManagerActionResult(
            rows=rows,
            success_message=success_message,
        )

    def _build_status_rows(self) -> list[dict[str, Any]]:
        rows = [item.to_row() for item in self._status_service.get_status()]

        return PublicationManagerRowService.prepare_rows(
            rows=rows,
        )

    @staticmethod
    def _resolve_selected_artifact_keys(
        *,
        selected_rows: list[dict[str, Any]],
    ) -> list[str]:
        artifact_keys: list[str] = []
        seen: set[str] = set()

        for row in selected_rows:
            if not isinstance(row, dict):
                continue

            artifact_key = str(row.get('artifact_key') or '').strip()

            if not artifact_key:
                continue

            if artifact_key in seen:
                continue

            seen.add(artifact_key)
            artifact_keys.append(artifact_key)

        return artifact_keys
