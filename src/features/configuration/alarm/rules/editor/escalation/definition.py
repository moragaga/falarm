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

from .schema import ALARM_RULE_ESCALATION_TARGETS_SCHEMA

ALARM_RULE_ESCALATION_TARGETS_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_rule_escalation_targets',
    title='Destinos de escalamiento de reglas',
    schema=ALARM_RULE_ESCALATION_TARGETS_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_rule_escalation_targets.json.gz',
        relative_path=ALARM_CONFIGURATION_RELATIVE_PATH,
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_rule_escalation_targets',
        display_name='Destinos de escalamiento de reglas',
        category=ALARM_CONFIGURATION_CATEGORY,
        schema_key=ALARM_RULE_ESCALATION_TARGETS_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name=ALARM_CONFIGURATION_CONTAINER_NAME,
            document_id='alarm_rule_escalation_targets',
            partition_key='alarm_rule_escalation_targets',
        ),
    ),
    row_id_field='rule_key',
)
