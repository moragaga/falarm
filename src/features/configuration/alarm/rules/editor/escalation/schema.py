from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition

ALARM_RULE_ESCALATION_TARGETS_SCHEMA = AdminSchema(
    key='alarm_rule_escalation_targets',
    title='Destinos de escalamiento de reglas',
    fields=(
        FieldDefinition(
            name='rule_key',
            label='ID regla',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='step_order',
            label='Orden',
            field_type='number',
            required=True,
            default_value=1,
        ),
        FieldDefinition(
            name='target_tool_key',
            label='Herramienta destino',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='is_enabled',
            label='Activo',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
        FieldDefinition(
            name='wait_minutes_from_previous_stage',
            label='Minutos desde etapa anterior',
            field_type='number',
            required=False,
        ),
    ),
)
