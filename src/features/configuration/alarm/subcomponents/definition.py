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
from src.features.configuration.models import FieldOption

from .row_factory_service import AlarmSubcomponentRowFactoryService
from .schema import ALARM_SUBCOMPONENTS_ADMIN_SCHEMA, build_alarm_subcomponents_admin_schema


def build_alarm_subcomponents_admin_definition(
    *,
    parent_component_options: tuple[FieldOption, ...],
) -> AdminDefinition:
    schema = build_alarm_subcomponents_admin_schema(
        parent_component_options=parent_component_options,
    )

    return AdminDefinition(
        key='alarm_subcomponents',
        title='Subcomponentes de alarmas',
        schema=schema,
        remote=AdminRemoteDefinition(
            sharepoint_filename='alarm_subcomponents.json.gz',
            relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
        ),
        artifact=AdminArtifactDefinition(
            artifact_key='alarm_subcomponents',
            display_name='Subcomponentes de alarmas',
            category=ALARM_CONFIGURATION_CATEGORY,
            schema_key=schema.key,
            projection=AdminArtifactProjectionDefinition(
                container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
                document_id='alarm_subcomponents',
                partition_key='alarm_subcomponents',
            ),
        ),
        row_id_field='subcomponent_key',
        row_factory=AlarmSubcomponentRowFactoryService.build_new_row,
    )


ALARM_SUBCOMPONENTS_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_subcomponents',
    title='Subcomponentes de alarmas',
    schema=ALARM_SUBCOMPONENTS_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_subcomponents.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_subcomponents',
        display_name='Subcomponentes de alarmas',
        category=ALARM_CONFIGURATION_CATEGORY,
        schema_key=ALARM_SUBCOMPONENTS_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
            document_id='alarm_subcomponents',
            partition_key='alarm_subcomponents',
        ),
    ),
    row_id_field='subcomponent_key',
    row_factory=AlarmSubcomponentRowFactoryService.build_new_row,
)
