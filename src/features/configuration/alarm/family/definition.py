from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)
from src.features.configuration.alarm.constants import (
    ALARM_CONFIGURATION_CATEGORY,
    ALARM_CONFIGURATION_CONTAINER_NAME,
    ALARM_CONFIGURATION_RELATIVE_PATH,
)

from .row_factory_service import AlarmFamilyRowFactoryService
from .schema import ALARM_FAMILY_ADMIN_SCHEMA

ALARM_FAMILY_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_families',
    title='Familias de alarmas',
    schema=ALARM_FAMILY_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_families.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_families',
        display_name='Familias de alarmas',
        category=ALARM_CONFIGURATION_CATEGORY,
        schema_key=ALARM_FAMILY_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
            document_id='alarm_families',
            partition_key='alarm_families',
        ),
    ),
    row_id_field='family_key',
    row_factory=AlarmFamilyRowFactoryService.build_new_row,
)
