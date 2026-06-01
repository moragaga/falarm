"""
Contains constants for managing the publication process in a user interface.

This module defines a dictionary of element IDs used throughout the
publication manager interface. These IDs are utilized for locating
HTML elements tied to various publication-related operations such as
refreshing content, publishing, and handling pending publications.
"""

from __future__ import annotations

PUBLICATION_MANAGER_IDS = {
    'container': 'publication-manager-container',
    'refresh': 'publication-manager-refresh',
    'publish': 'publication-manager-publish',
    'publish_pending': 'publication-manager-publish-pending',
    'grid': 'publication-manager-grid',
    'toast': 'publication-manager-toast',
    'init': 'publication-manager-init',
    'loading': 'publication-manager-loading',
}
