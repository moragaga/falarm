"""
Dataclass representing the status view of a configuration artifact.

This class provides a structured representation and utility functions for handling
the status and metadata of a configuration artifact.

Attributes
----------
artifact_key : str
    A unique identifier for the artifact.
display_name : str
    The user-friendly name for the artifact.
category : str
    The category to which the artifact belongs.
sharepoint_revision : int
    The revision number of the artifact in SharePoint.
sharepoint_hash : str
    A hash representing the SharePoint version of the artifact.
sharepoint_updated_at : str
    A timestamp indicating when the artifact was last updated in SharePoint.
sharepoint_updated_by : str or None
    The user who last updated the artifact in SharePoint, or None if unavailable.
published_revision : int or None
    The published revision number, or None if the artifact is not published.
published_hash : str or None
    A hash representing the published version of the artifact, or None if unpublished.
published_at : str or None
    A timestamp indicating when the artifact was published, or None if unpublished.
published_by : str or None
    The user who published the artifact, or None if unpublished.
status : str
    The current status of the artifact (e.g., 'published', 'pending_publish', 'unpublished').

Methods
-------
to_row()
    Converts the artifact's attributes and status into a dictionary format, making it
    suitable for tabular or structured data representation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigArtifactStatusView:
    artifact_key: str
    display_name: str
    category: str
    sharepoint_revision: int
    sharepoint_hash: str
    sharepoint_updated_at: str
    sharepoint_updated_by: str | None
    published_revision: int | None
    published_hash: str | None
    published_at: str | None
    published_by: str | None
    status: str

    def to_row(self) -> dict:
        return {
            'artifact_key': self.artifact_key,
            'display_name': self.display_name,
            'category': self.category,
            'sharepoint_revision': self.sharepoint_revision,
            'sharepoint_updated_at': self.sharepoint_updated_at,
            'sharepoint_updated_by': self.sharepoint_updated_by,
            'published_revision': self.published_revision,
            'published_at': self.published_at,
            'published_by': self.published_by,
            'status': self._status_label(),
            'status_code': self.status,
        }

    def _status_label(self) -> str:
        if self.status == 'published':
            return 'Publicado'
        if self.status == 'pending_publish':
            return 'Pendiente'
        if self.status == 'unpublished':
            return 'No publicado'
        return self.status
