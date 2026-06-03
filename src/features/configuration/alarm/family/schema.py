from __future__ import annotations

from src.features.configuration.alarm.options import (
    ALARM_OPERATIONAL_AREA_OPTIONS,
    AlarmOperationalArea,
)
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
            help_text=(
                'Identificador normalizado de familia. '
                'Al guardar se convierte a minúsculas, sin tildes, sin espacios y con guion bajo.'
            ),
        ),
        FieldDefinition(
            name='description',
            label='Descripción',
            field_type='text',
            required=False,
            help_text='Texto humano libre para describir la familia.',
        ),
        FieldDefinition(
            name='operational_area',
            label='Área operacional',
            field_type='select',
            required=True,
            options=ALARM_OPERATIONAL_AREA_OPTIONS,
            default_value=AlarmOperationalArea.PLANTA.value,
            help_text='Área operacional base que será resuelta hacia cada regla.',
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
            label='Activa',
            field_type='boolean',
            required=True,
            default_value=True,
            help_text='Si la familia no está activa, sus reglas no deben publicarse como ejecutables.',
        ),
    ),
)