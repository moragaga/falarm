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
                FieldOption(label='Componente padre', value='component'),
                FieldOption(label='Subcomponente', value='subcomponent'),
            ),
            default_value='component',
            help_text='Los componentes padre definen posiciones de Nivel 0. Los subcomponentes cuelgan de un componente padre.',
        ),
        FieldDefinition(
            name='parent_component_key',
            label='Componente padre',
            field_type='text',
            required=False,
            help_text='Solo aplica para subcomponentes. Ejemplo: flotacion_selectiva.',
        ),
        FieldDefinition(
            name='position_index',
            label='Posición Nivel 0',
            field_type='number',
            required=False,
            default_value=None,
            help_text='Solo aplica a componentes padre. Define la posición principal en Nivel 0.',
        ),
        FieldDefinition(
            name='additional_position_keys',
            label='Posiciones adicionales afectadas',
            field_type='semicolon_list',
            required=False,
            help_text='Solo aplica a componentes padre. IDs de otros componentes/posiciones afectados, separados por ;.',
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
