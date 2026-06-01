from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition

ALARM_RULE_VISUAL_TARGETS_SCHEMA = AdminSchema(
    key='alarm_rule_visual_targets',
    title='Visualización Nivel 0 por regla',
    fields=(
        FieldDefinition(
            name='rule_key',
            label='ID regla',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='tool_key',
            label='Herramienta',
            field_type='text',
            required=True,
            help_text='Siempre debe ser nivel_0. Se conserva como campo técnico para el runtime.',
        ),
        FieldDefinition(
            name='affected_component_keys',
            label='Componentes Nivel 0 afectados',
            field_type='semicolon_list',
            required=False,
        ),
        FieldDefinition(
            name='affected_subcomponent_keys',
            label='Subcomponentes Nivel 0 afectados',
            field_type='semicolon_list',
            required=False,
        ),
        FieldDefinition(
            name='is_complete',
            label='Completa',
            field_type='boolean',
            required=True,
            default_value=False,
        ),
    ),
)
