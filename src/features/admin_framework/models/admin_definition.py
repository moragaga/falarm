"""
This module defines data structures and types used for managing admin-related configurations
and definitions, including schema, artifact details, and remote file definitions. It includes
immutable data classes for configuration purposes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from src.features.configuration.models import AdminSchema

AdminRowFactory = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class AdminRemoteDefinition:
    sharepoint_filename: str
    relative_path: str


@dataclass(frozen=True)
class AdminArtifactProjectionDefinition:
    container_name: str
    document_id: str | None = None
    partition_key: str | None = None


@dataclass(frozen=True)
class AdminArtifactDefinition:
    artifact_key: str
    display_name: str
    category: str
    content_type: str = 'application/json+gzip'
    schema_key: str | None = None
    projection: AdminArtifactProjectionDefinition | None = None


@dataclass(frozen=True)
class AdminDefinition:
    key: str
    title: str
    schema: AdminSchema | None = None
    remote: AdminRemoteDefinition | None = None
    artifact: AdminArtifactDefinition | None = None
    row_id_field: str | None = None
    row_factory: AdminRowFactory | None = None
