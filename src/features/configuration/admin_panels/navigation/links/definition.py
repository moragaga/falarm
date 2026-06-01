"""
This module provides the functionality for building and managing the
administrative definition of navigation links, including schemas, artifacts,
and configuration options.

The primary purpose of the module is to define a reusable and configurable
framework for creating and managing navigation links' administrative definitions.
It is tailored to work with SharePoint files, navigation-related schema,
and data projections.

Attributes
----------
DEFAULT_PARENT_GROUP_OPTIONS : tuple of FieldOption
    A tuple containing the default option for a parent group used within the
    navigation links administrative definition. The default option is labeled
    'Sin grupo' with an empty string as the value.

NAVIGATION_LINKS_ADMIN_DEFINITION : AdminDefinition
    The pre-built administrative definition for navigation links, containing
    schema, artifact, remote definitions, and row factory details for navigation
    links management.

Functions
---------
build_navigation_links_admin_definition(*, parent_group_options: tuple[FieldOption, ...]) -> AdminDefinition
    Builds the administrative definition for navigation links, including its
    schema, artifact, and remote configurations. This function provides a reusable
    setup for managing navigation settings and artifacts.
"""

from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)
from src.features.configuration.models import FieldOption

from .row_factory_service import NavigationLinkRowFactoryService
from .schema import build_navigation_links_admin_schema

DEFAULT_PARENT_GROUP_OPTIONS: tuple[FieldOption, ...] = (
    FieldOption(
        label='Sin grupo',
        value='',
    ),
)


def build_navigation_links_admin_definition(
    *,
    parent_group_options: tuple[FieldOption, ...],
) -> AdminDefinition:
    schema = build_navigation_links_admin_schema(
        parent_group_options=parent_group_options,
    )

    return AdminDefinition(
        key='navigation_links',
        title='Administración de links de navegación',
        schema=schema,
        remote=AdminRemoteDefinition(
            sharepoint_filename='navigation_links.json.gz',
            relative_path='navigation',
        ),
        artifact=AdminArtifactDefinition(
            artifact_key='navigation_links',
            display_name='Links de navegación',
            category='navigation',
            content_type='application/json+gzip',
            schema_key=schema.key,
            projection=AdminArtifactProjectionDefinition(
                container_name='navigation_configuration',
                document_id='navigation_links',
                partition_key='navigation_links',
            ),
        ),
        row_id_field='link_id',
        row_factory=NavigationLinkRowFactoryService.build_new_row,
    )


NAVIGATION_LINKS_ADMIN_DEFINITION = build_navigation_links_admin_definition(
    parent_group_options=DEFAULT_PARENT_GROUP_OPTIONS,
)
