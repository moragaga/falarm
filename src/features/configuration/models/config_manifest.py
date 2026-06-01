"""
Represents configuration artifacts and their associated metadata in a manifest.

This module contains the `ConfigManifestArtifact` and `ConfigManifest` classes.
`ConfigManifestArtifact` encapsulates metadata about an individual artifact,
such as file information, content type, and revision data.
`ConfigManifest` provides a collection of such artifacts and operations to
serialize and deserialize their representation.

Classes
-------
- ConfigManifestArtifact
- ConfigManifest
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ConfigManifestArtifact:
    artifact_key: str
    display_name: str
    category: str
    filename: str
    relative_path: str | None
    content_type: str
    schema_key: str | None
    revision: int
    content_hash: str
    updated_at: str
    updated_by: str | None
    is_active: bool = True
    target_container_name: str | None = None
    target_document_id: str | None = None
    target_partition_key: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfigManifestArtifact:
        return cls(
            artifact_key=str(data.get('artifact_key') or ''),
            display_name=str(data.get('display_name') or ''),
            category=str(data.get('category') or ''),
            filename=str(data.get('filename') or ''),
            relative_path=cls._normalize_optional_text(data.get('relative_path')),
            content_type=str(data.get('content_type') or 'application/json+gzip'),
            schema_key=cls._normalize_optional_text(data.get('schema_key')),
            revision=int(data.get('revision') or 0),
            content_hash=str(data.get('content_hash') or ''),
            updated_at=str(data.get('updated_at') or ''),
            updated_by=cls._normalize_optional_text(data.get('updated_by')),
            is_active=cls._to_bool(data.get('is_active'), default=True),
            target_container_name=cls._normalize_optional_text(data.get('target_container_name')),
            target_document_id=cls._normalize_optional_text(data.get('target_document_id')),
            target_partition_key=cls._normalize_optional_text(data.get('target_partition_key')),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'artifact_key': self.artifact_key,
            'display_name': self.display_name,
            'category': self.category,
            'filename': self.filename,
            'relative_path': self.relative_path,
            'content_type': self.content_type,
            'schema_key': self.schema_key,
            'revision': self.revision,
            'content_hash': self.content_hash,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by,
            'is_active': self.is_active,
            'target_container_name': self.target_container_name,
            'target_document_id': self.target_document_id,
            'target_partition_key': self.target_partition_key,
        }

    @staticmethod
    def _normalize_optional_text(value: Any) -> str | None:
        if value is None:
            return None

        normalized = str(value).strip()

        if not normalized:
            return None

        if normalized.lower() == 'none':
            return None

        return normalized

    @staticmethod
    def _to_bool(value: Any, *, default: bool) -> bool:
        if value is None:
            return default

        if isinstance(value, bool):
            return value

        normalized = str(value).strip().lower()

        if normalized in {'true', '1', 'yes', 'si', 'sí'}:
            return True

        if normalized in {'false', '0', 'no'}:
            return False

        return default


@dataclass(frozen=True)
class ConfigManifest:
    artifacts: tuple[ConfigManifestArtifact, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | list[dict[str, Any]] | None) -> ConfigManifest:
        if data is None:
            return cls()

        if isinstance(data, dict):
            raw_artifacts = data.get('artifacts') or []
        elif isinstance(data, list):
            raw_artifacts = data
        else:
            raw_artifacts = []

        artifacts = tuple(
            ConfigManifestArtifact.from_dict(item)
            for item in raw_artifacts
            if isinstance(item, dict)
        )

        return cls(artifacts=artifacts)

    def to_dict(self) -> dict[str, Any]:
        return {'artifacts': [artifact.to_dict() for artifact in self.artifacts]}
