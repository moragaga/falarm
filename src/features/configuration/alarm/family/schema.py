from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition

ALARM_FAMILY_ADMIN_SCHEMA = AdminSchema(
    key='alarm_families',
    title='Familias de alarmas',
    fields=(
        FieldDefinition(
            name='family_key',
            label='ID familia',
            field_type='text',
            required=True,
            editable=False,
            help_text='Identificador técnico estable de la familia.',
        ),
        FieldDefinition(
            name='family_name',
            label='Familia',
            field_type='text',
            required=True,
            help_text='Nombre visible usado solo para agrupar y filtrar reglas.',
        ),
        FieldDefinition(
            name='description',
            label='Descripción',
            field_type='text',
            required=False,
            help_text='Texto breve de apoyo para el configurador.',
        ),
        FieldDefinition(
            name='display_order',
            label='Orden',
            field_type='number',
            required=True,
            default_value=0,
        ),
        FieldDefinition(
            name='is_available',
            label='Disponible',
            field_type='boolean',
            required=True,
            default_value=True,
            help_text='Permite usar la familia al crear o editar reglas. No define comportamiento operativo.',
        ),
    ),
)
