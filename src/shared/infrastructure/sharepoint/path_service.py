"""
A service class for constructing relative paths for SharePoint file types.

This module provides the `SharepointPathService` class, which allows building
relative paths based on predefined SharePoint file types. The mapping between
file types and base paths is predefined within the class.

Classes
-------
SharepointPathService
    A service class to build relative paths for SharePoint files.
"""

from __future__ import annotations

from .file_type import SharepointFileType


class SharepointPathService:
    _TYPE_PATHS: dict[SharepointFileType, str] = {
        SharepointFileType.CONFIGURATION: 'configuration',
    }

    @classmethod
    def build_relative_path(
        cls, file_type: SharepointFileType, relative_path: str | None = None
    ) -> str:
        base_path = cls._TYPE_PATHS.get(
            file_type, cls._TYPE_PATHS[SharepointFileType.CONFIGURATION]
        )

        if not relative_path:
            return base_path

        normalized_relative = relative_path.strip('/\\')
        return f'{base_path}/{normalized_relative}'
