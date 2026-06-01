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

from .row_factory_service import AlarmComponentN0RowFactoryService
from .schema import ALARM_COMPONENTS_N0_ADMIN_SCHEMA

ALARM_COMPONENTS_N0_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_components_n0',
    title='Componentes Nivel 0',
    schema=ALARM_COMPONENTS_N0_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_components_n0.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_components_n0',
        display_name='Componentes Nivel 0',
        category=ALARM_CONFIGURATION_CATEGORY,
        schema_key=ALARM_COMPONENTS_N0_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
            document_id='alarm_components_n0',
            partition_key='alarm_components_n0',
        ),
    ),
    row_id_field='component_key',
    row_factory=AlarmComponentN0RowFactoryService.build_new_row,
)
