from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, FieldOption


def build_alarm_subcomponents_admin_schema(
    *,
    parent_component_options: tuple[FieldOption, ...],
) -> AdminSchema:
    return AdminSchema(
        key='alarm_subcomponents',
        title='Subcomponentes de alarmas',
        fields=(
            FieldDefinition(
                name='subcomponent_key',
                label='ID subcomponente',
                field_type='text',
                required=True,
                editable=False,
                help_text='Identificador técnico automático de la fila.',
            ),
            FieldDefinition(
                name='subcomponent_code',
                label='Identificador normalizado',
                field_type='text',
                required=True,
                help_text=(
                    'Código estable para integrar con el front. Usar minúsculas, números y guion bajo. '
                    'Ejemplo: selectiva.'
                ),
            ),
            FieldDefinition(
                name='subcomponent_name',
                label='Subcomponente',
                field_type='text',
                required=True,
            ),
            FieldDefinition(
                name='parent_component_key',
                label='Componente padre',
                field_type='select',
                required=True,
                options=parent_component_options,
                help_text='Selecciona un componente activo configurado en Componentes.',
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


ALARM_SUBCOMPONENTS_ADMIN_SCHEMA = build_alarm_subcomponents_admin_schema(
    parent_component_options=(),
)
