"""
Module for managing the state of published artifacts and their configurations.

This module defines dataclasses that represent the state of a published artifact
and a configuration publication which includes multiple artifacts. These classes
provide functionalities for serialization and deserialization between Python
objects and dictionaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PublishedArtifactState:
    artifact_key: str
    published_revision: int
    published_hash: str
    published_at: str
    published_by: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PublishedArtifactState:
        return cls(
            artifact_key=str(data.get('artifact_key') or ''),
            published_revision=int(data.get('published_revision') or 0),
            published_hash=str(data.get('published_hash') or ''),
            published_at=str(data.get('published_at') or ''),
            published_by=data.get('published_by'),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'artifact_key': self.artifact_key,
            'published_revision': self.published_revision,
            'published_hash': self.published_hash,
            'published_at': self.published_at,
            'published_by': self.published_by,
        }


@dataclass(frozen=True)
class ConfigPublicationState:
    artifacts: tuple[PublishedArtifactState, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(
        cls, data: dict[str, Any] | list[dict[str, Any]] | None
    ) -> ConfigPublicationState:
        if data is None:
            return cls()

        if isinstance(data, dict):
            raw_artifacts = data.get('artifacts') or []
        elif isinstance(data, list):
            raw_artifacts = data
        else:
            raw_artifacts = []

        artifacts = tuple(
            PublishedArtifactState.from_dict(item)
            for item in raw_artifacts
            if isinstance(item, dict)
        )

        return cls(artifacts=artifacts)

    def to_dict(self) -> dict[str, Any]:
        return {'artifacts': [artifact.to_dict() for artifact in self.artifacts]}
