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
            label='Nivel',
            field_type='select',
            required=True,
            options=(
                FieldOption(label='ADA N1', value='n1'),
                FieldOption(label='Ejecutivo', value='executive'),
                FieldOption(label='Nivel 0', value='n0'),
            ),
            default_value='n1',
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
