"""
Defines the SharepointFileType enumeration for categorizing SharePoint file types.

This module contains an enumeration `SharepointFileType` to classify specific types
of SharePoint files, such as configuration files and modals.

Classes
-------
SharepointFileType
    An enumeration representing different types of SharePoint files.
"""

from __future__ import annotations

from enum import Enum


class SharepointFileType(Enum):
    CONFIGURATION = 'configuration'
