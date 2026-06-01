from __future__ import annotations

from flask import session

from src.app.dependencies import get_config_manifest_service
from src.features.admin_framework.models import AdminDefinition


class AlarmAdminManifestSaveService:
    @staticmethod
    def register_update(
        *,
        definition: AdminDefinition,
        normalized_rows: list[dict],
    ) -> list[str]:
        updated_by = (session.get('identity') or {}).get('email')

        ok = get_config_manifest_service().register_update(
            definition=definition,
            rows=normalized_rows,
            updated_by=updated_by,
        )

        if ok:
            return []

        return ['El archivo se guardó, pero no se pudo actualizar el config manifest.']
