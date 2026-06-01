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

from .row_factory_service import AlarmRuleRowFactoryService
from .schema import ALARM_RULES_ADMIN_SCHEMA

ALARM_RULES_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_rules',
    title='Reglas de alarmas',
    schema=ALARM_RULES_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_rules.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_rules',
        display_name='Reglas de alarmas',
        category=ALARM_CONFIGURATION_CATEGORY,
        schema_key=ALARM_RULES_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
            document_id='alarm_rules',
            partition_key='alarm_rules',
        ),
    ),
    row_id_field='rule_key',
    row_factory=AlarmRuleRowFactoryService.build_new_row,
)
