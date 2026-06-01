from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, FieldOption

ALARM_COMPONENTS_ADMIN_SCHEMA = AdminSchema(
    key='alarm_components',
    title='Componentes de alarmas',
    fields=(
        FieldDefinition(
            name='component_key',
            label='ID componente',
            field_type='text',
            required=True,
            editable=False,
            help_text='Identificador técnico automático de la fila.',
        ),
        FieldDefinition(
            name='component_code',
            label='Identificador normalizado',
            field_type='text',
            required=True,
            help_text=(
                'Código estable para integrar con el front. Usar minúsculas, números y guion bajo. '
                'Ejemplo: flotacion_selectiva.'
            ),
        ),
        FieldDefinition(
            name='component_name',
            label='Componente',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='position_index',
            label='Posición',
            field_type='number',
            required=True,
            default_value=0,
            help_text='Posición principal usada por Nivel 0.',
        ),
        FieldDefinition(
            name='applies_to_tool_level',
            label='Nivel aplica',
            field_type='select',
            required=True,
            options=(
                FieldOption(label='Nivel 0', value='1'),
                FieldOption(label='Todos', value='all'),
            ),
            default_value='1',
        ),
        FieldDefinition(
            name='display_order',
            label='Orden',
            field_type='number',
            required=True,
            default_value=0,
        ),
        FieldDefinition(
            name='is_active',
            label='Activo',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
    ),
)
