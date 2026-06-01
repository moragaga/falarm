"""
A service for synchronizing the first local projection with a SharePoint identity repository.

This module defines a single class, `IdentityFirstProjectionSyncService`, responsible for
coordinating the publication of the first local projection of identity data to a SharePoint
repository. It interacts with a `SharePointIdentityRepository` to load and save identity
information.

Classes
-------
IdentityFirstProjectionSyncService
    A service to manage the synchronization of the first local projection.
"""

from __future__ import annotations

from ..registry.identity_registry import IDENTITIES_FALLBACK
from ..repositories.sharepoint_identity_repository import SharePointIdentityRepository


class IdentityFirstProjectionSyncService:
    def __init__(self, sharepoint_identity_repository: SharePointIdentityRepository):
        self._sharepoint_identity_repository = sharepoint_identity_repository

    def sync_first_local_projection(self):
        rows = self._sharepoint_identity_repository.load_rows()
        if rows:
            print('[INFO] First projection is already published')
            return

        print('[INFO] There is first projection, publishing it...')
        rows = [identity.to_sharepoint_row() for identity in IDENTITIES_FALLBACK]
        ok = self._sharepoint_identity_repository.save_rows(rows)
        if not ok:
            print('[ERROR] Failed to save first projection')
            return
        print('[INFO] First projection is already published')
