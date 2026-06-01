"""
Definition of the identity users administration component.

This module defines the administrative structure and schema for managing
identity users. It facilitates handling related SharePoint configurations,
remote paths, and row factory functionalities relevant to user management.
"""

from __future__ import annotations

from src.features.admin_framework.models import (
    AdminDefinition,
    AdminRemoteDefinition,
)

from .row_factory_service import IdentityUserRowFactoryService
from .schema import IDENTITY_USERS_ADMIN_SCHEMA

IDENTITY_USERS_ADMIN_DEFINITION = AdminDefinition(
    key='identity_users',
    title='Administración de usuarios',
    schema=IDENTITY_USERS_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='identity_users.json.gz',
        relative_path='identity',
    ),
    artifact=None,
    row_id_field='user_id',
    row_factory=IdentityUserRowFactoryService.build_new_row,
)
