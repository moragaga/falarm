from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, FieldOption

ALARM_TOOLS_ADMIN_SCHEMA = AdminSchema(
    key='alarm_tools',
    title='Herramientas de alarmas',
    fields=(
        FieldDefinition(
            name='tool_key',
            label='ID herramienta',
            field_type='text',
            required=True,
            editable=False,
        ),
        FieldDefinition(
            name='tool_name',
            label='Herramienta',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='tool_level',
            label='Nivel herramienta',
            field_type='select',
            required=True,
            options=(
                FieldOption(label='Nivel 1 · Nivel 0 / Sala', value='1'),
                FieldOption(label='Nivel 2 · Ejecutiva', value='2'),
                FieldOption(label='Nivel 3 · ADA N1', value='3'),
            ),
            default_value='3',
            help_text='Define la jerarquía de escalamiento. Nivel 1 es el destino crítico final; debe existir una sola herramienta activa nivel 1.',
        ),
        FieldDefinition(
            name='visualization_mode',
            label='Visualización base',
            field_type='select',
            required=True,
            options=(
                FieldOption(label='Genérica', value='generic'),
                FieldOption(label='Distribuida', value='distributed'),
                FieldOption(label='Cola / posicionamiento', value='queue_for_queue'),
            ),
            default_value='generic',
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
        ),
    ),
)
