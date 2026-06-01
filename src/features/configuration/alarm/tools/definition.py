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

from .row_factory_service import AlarmToolRowFactoryService
from .schema import ALARM_TOOLS_ADMIN_SCHEMA

ALARM_TOOLS_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_tools',
    title='Herramientas de alarmas',
    schema=ALARM_TOOLS_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_tools.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_tools',
        display_name='Herramientas de alarmas',
        category=ALARM_CONFIGURATION_CATEGORY,
        schema_key=ALARM_TOOLS_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
            document_id='alarm_tools',
            partition_key='alarm_tools',
        ),
    ),
    row_id_field='tool_key',
    row_factory=AlarmToolRowFactoryService.build_new_row,
)
