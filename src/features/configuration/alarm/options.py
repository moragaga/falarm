from __future__ import annotations

from enum import StrEnum

from src.features.configuration.models import FieldOption


class AlarmKind(StrEnum):
    RISK = 'risk'
    IMPACT = 'impact'


class AlarmCriticality(StrEnum):
    C1 = 'C1'
    C2 = 'C2'
    C3 = 'C3'


class AlarmBusinessCategory(StrEnum):
    OPERATIONAL = 'operational'
    HEALTH_SAFETY = 'health_safety'
    ENVIRONMENT = 'environment'
    COST = 'cost'
    PRODUCTION = 'production'
    MAINTENANCE = 'maintenance'


class AlarmOperationalArea(StrEnum):
    MINA = 'mina'
    PLANTA = 'planta'


class AlarmToolTier(StrEnum):
    PROCESS = 'process'
    INTEGRATED_OPERATIONS = 'integrated_operations'
    STRATEGIC = 'strategic'


class AlarmComponentAppliesToToolTier(StrEnum):
    INTEGRATED_OPERATIONS = 'integrated_operations'
    ALL = 'all'


class AlarmVisualizationMode(StrEnum):
    GENERIC = 'generic'
    DISTRIBUTED = 'distributed'
    QUEUE_IN_QUEUE = 'queue_in_queue'


class AlarmVisibilityMode(StrEnum):
    VISIBLE = 'visible'
    TRACE_ONLY = 'trace_only'


class AlarmColor(StrEnum):
    RED = 'red'
    YELLOW = 'yellow'


ALARM_KIND_OPTIONS = (
    FieldOption(label='Riesgo', value=AlarmKind.RISK.value),
    FieldOption(label='Impacto', value=AlarmKind.IMPACT.value),
)

ALARM_CRITICALITY_OPTIONS = (
    FieldOption(label='C1 · Visibilidad inmediata', value=AlarmCriticality.C1.value),
    FieldOption(label='C2 · Escalamiento progresivo', value=AlarmCriticality.C2.value),
    FieldOption(label='C3 · Sin escalamiento', value=AlarmCriticality.C3.value),
)

ALARM_BUSINESS_CATEGORY_OPTIONS = (
    FieldOption(label='Operacional', value=AlarmBusinessCategory.OPERATIONAL.value),
    FieldOption(label='Salud y seguridad', value=AlarmBusinessCategory.HEALTH_SAFETY.value),
    FieldOption(label='Medio ambiente', value=AlarmBusinessCategory.ENVIRONMENT.value),
    FieldOption(label='Costos', value=AlarmBusinessCategory.COST.value),
    FieldOption(label='Producción', value=AlarmBusinessCategory.PRODUCTION.value),
    FieldOption(label='Mantención', value=AlarmBusinessCategory.MAINTENANCE.value),
)

ALARM_OPERATIONAL_AREA_OPTIONS = (
    FieldOption(label='Mina', value=AlarmOperationalArea.MINA.value),
    FieldOption(label='Planta', value=AlarmOperationalArea.PLANTA.value),
)

ALARM_TOOL_TIER_OPTIONS = (
    FieldOption(label='ADA Proceso', value=AlarmToolTier.PROCESS.value),
    FieldOption(
        label='ADA Operaciones Integradas',
        value=AlarmToolTier.INTEGRATED_OPERATIONS.value,
    ),
    FieldOption(label='ADA Estratégico', value=AlarmToolTier.STRATEGIC.value),
)

ALARM_COMPONENT_APPLIES_TO_TOOL_TIER_OPTIONS = (
    FieldOption(
        label='ADA Operaciones Integradas',
        value=AlarmComponentAppliesToToolTier.INTEGRATED_OPERATIONS.value,
    ),
    FieldOption(label='Todos', value=AlarmComponentAppliesToToolTier.ALL.value),
)

ALARM_VISUALIZATION_MODE_OPTIONS = (
    FieldOption(label='Genérica', value=AlarmVisualizationMode.GENERIC.value),
    FieldOption(label='Distribuida', value=AlarmVisualizationMode.DISTRIBUTED.value),
    FieldOption(label='Queue in queue', value=AlarmVisualizationMode.QUEUE_IN_QUEUE.value),
)

ALARM_VISIBILITY_MODE_OPTIONS = (
    FieldOption(label='Visible en herramientas', value=AlarmVisibilityMode.VISIBLE.value),
    FieldOption(label='Solo trazabilidad', value=AlarmVisibilityMode.TRACE_ONLY.value),
)

ALARM_COLOR_OPTIONS = (
    FieldOption(label='Rojo', value=AlarmColor.RED.value),
    FieldOption(label='Amarillo', value=AlarmColor.YELLOW.value),
)


def build_dash_options(
    *,
    options: tuple[FieldOption, ...],
) -> list[dict[str, str]]:
    return [
        {
            'label': option.label,
            'value': option.value,
        }
        for option in options
    ]


def get_option_label(
    *,
    value: object,
    options: tuple[FieldOption, ...],
) -> str:
    normalized = str(value or '').strip()

    for option in options:
        if option.value == normalized:
            return option.label

    return normalized