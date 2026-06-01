from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, FieldOption

ALARM_COMPONENTS_N0_ADMIN_SCHEMA = AdminSchema(
    key='alarm_components_n0',
    title='Componentes Nivel 0',
    fields=(
        FieldDefinition(
            name='component_key',
            label='ID componente',
            field_type='text',
            required=True,
            editable=False,
        ),
        FieldDefinition(
            name='component_name',
            label='Componente',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='component_type',
            label='Tipo',
            field_type='select',
            required=True,
            options=(
                FieldOption(label='Componente', value='component'),
                FieldOption(label='Subcomponente', value='subcomponent'),
            ),
            default_value='component',
        ),
        FieldDefinition(
            name='parent_component_key',
            label='Componente padre',
            field_type='text',
            required=False,
            help_text='Solo aplica para subcomponentes. Ejemplo: flotacion_selectiva.',
        ),
        FieldDefinition(
            name='tool_level',
            label='Nivel aplica',
            field_type='select',
            required=True,
            options=(
                FieldOption(label='Nivel 0', value='n0'),
                FieldOption(label='Todos', value='all'),
            ),
            default_value='n0',
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
