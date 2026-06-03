from __future__ import annotations

from src.features.configuration.alarm.options import (
    ALARM_TOOL_TIER_OPTIONS,
    ALARM_VISUALIZATION_MODE_OPTIONS,
    AlarmToolTier,
    AlarmVisualizationMode,
)
from src.features.configuration.models import AdminSchema, FieldDefinition

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
            name='tool_tier',
            label='Tipo herramienta',
            field_type='select',
            required=True,
            options=ALARM_TOOL_TIER_OPTIONS,
            default_value=AlarmToolTier.PROCESS.value,
            help_text='Jerarquía funcional: ADA Proceso → ADA Operaciones Integradas → ADA Estratégico.',
        ),
        FieldDefinition(
            name='visualization_mode',
            label='Modo de proyección',
            field_type='select',
            required=True,
            options=ALARM_VISUALIZATION_MODE_OPTIONS,
            default_value=AlarmVisualizationMode.GENERIC.value,
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