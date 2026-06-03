from __future__ import annotations

from typing import Any

from src.features.configuration.alarm.options import (
    AlarmBusinessCategory,
    AlarmColor,
    AlarmCriticality,
    AlarmKind,
    AlarmToolTier,
    AlarmVisibilityMode,
)
from src.features.configuration.alarm.services.alarm_identifier_normalization_service import (
    AlarmIdentifierNormalizationService,
)


class AlarmConfigurationValidationService:
    @staticmethod
    def validate_rule_draft(
        *,
        draft: dict[str, Any],
    ) -> list[str]:
        errors: list[str] = []

        _validate_required_identity(
            draft=draft,
            errors=errors,
        )

        _validate_identifiers(
            draft=draft,
            errors=errors,
        )

        _validate_enums(
            draft=draft,
            errors=errors,
        )

        _validate_family(
            draft=draft,
            errors=errors,
        )

        _validate_origin_tool(
            draft=draft,
            errors=errors,
        )

        _validate_reappearance(
            draft=draft,
            errors=errors,
        )

        _validate_escalation(
            draft=draft,
            errors=errors,
        )

        _validate_integrated_operations_visualization(
            draft=draft,
            errors=errors,
        )

        return errors


def _validate_required_identity(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    if not _text(draft.get('family_key')):
        errors.append('La regla debe tener familia.')

    if not _text(draft.get('rule_key')):
        errors.append('La regla debe tener ID.')

    if not _final_identifier_text(draft.get('rule_name')):
        errors.append('La regla debe tener nombre.')

    if not _text(draft.get('display_name')):
        errors.append('La regla debe tener nombre visible.')

    if not _final_identifier_text(draft.get('content_key')):
        errors.append('La regla debe tener ID de contenido.')

    if not _final_identifier_text(draft.get('scope_key')):
        errors.append('La regla debe tener scope de prioridad/gestión.')

    if not _text(draft.get('origin_tool_key')):
        errors.append('La regla debe tener herramienta inicial.')

    try:
        priority_order = int(draft.get('priority_order') or 0)
    except Exception:
        priority_order = 0

    if priority_order <= 0:
        errors.append('La prioridad debe ser un número mayor a 0.')


def _validate_identifiers(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    identifier_fields = {
        'rule_name': 'Regla',
        'content_key': 'ID contenido',
        'scope_key': 'Scope prioridad/gestión',
        'operator_bucket': 'Bucket operador',
    }

    for field_name, label in identifier_fields.items():
        value = _text(draft.get(field_name))

        if not value:
            continue

        if not AlarmIdentifierNormalizationService.is_valid_live_identifier(value):
            errors.append(
                f'{label} solo permite minúsculas, números y guion bajo.',
            )


def _validate_enums(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    if _text(draft.get('kind')) not in {item.value for item in AlarmKind}:
        errors.append('El tipo de regla no es válido.')

    if _text(draft.get('criticality_code')) not in {
        item.value
        for item in AlarmCriticality
    }:
        errors.append('La criticidad no es válida.')

    if _text(draft.get('business_category')) not in {
        item.value
        for item in AlarmBusinessCategory
    }:
        errors.append('La categoría de negocio no es válida.')

    if _text(draft.get('visibility_mode')) not in {
        item.value
        for item in AlarmVisibilityMode
    }:
        errors.append('La visibilidad no es válida.')

    if _text(draft.get('color')) not in {item.value for item in AlarmColor}:
        errors.append('El color de la regla debe ser Rojo o Amarillo.')


def _validate_family(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    catalogs = draft.get('_catalogs') or {}
    family_by_key = catalogs.get('family_by_key') or {}

    if not family_by_key:
        return

    family_key = _text(draft.get('family_key'))
    family = family_by_key.get(family_key)

    if family is None:
        errors.append(f'La familia {family_key} no existe.')
        return

    if not bool(family.get('is_active', True)):
        errors.append(f'La familia {family_key} no está activa.')


def _validate_origin_tool(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    origin_tool_key = _text(draft.get('origin_tool_key'))

    if not origin_tool_key:
        return

    catalogs = draft.get('_catalogs') or {}
    tool_tier_by_key = catalogs.get('tool_tier_by_key') or {}

    if tool_tier_by_key and origin_tool_key not in tool_tier_by_key:
        errors.append(f'La herramienta inicial {origin_tool_key} no existe o no está activa.')


def _validate_reappearance(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    if not bool(draft.get('reappear_if_still_active_enabled')):
        return

    try:
        minutes = int(draft.get('reappear_after_management_minutes') or 0)
    except Exception:
        minutes = 0

    if minutes <= 0:
        errors.append(
            'Si la alarma reaparece por no normalización, debe indicar minutos de espera mayores a 0.',
        )


def _validate_escalation(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    visibility_mode = _text(draft.get('visibility_mode'))
    criticality_code = _text(draft.get('criticality_code'))
    origin_tool_key = _text(draft.get('origin_tool_key'))
    active_targets = _active_escalation_targets(draft=draft)

    if visibility_mode == AlarmVisibilityMode.TRACE_ONLY.value:
        if active_targets:
            errors.append('Una regla solo trazabilidad no debe tener escalamiento.')
        return

    if not origin_tool_key:
        if active_targets:
            errors.append('No se puede configurar escalamiento sin herramienta inicial.')
        return

    if criticality_code == AlarmCriticality.C1.value:
        if active_targets:
            errors.append('C1 no debe tener destinos manuales de escalamiento.')

        _validate_c1_required_tools(
            draft=draft,
            errors=errors,
        )
        return

    if criticality_code == AlarmCriticality.C3.value:
        if active_targets:
            errors.append('C3 no debe tener destinos de escalamiento.')
        return

    if criticality_code != AlarmCriticality.C2.value:
        return

    if not active_targets:
        if _has_available_escalation_target_from_current_tool(
            draft=draft,
            current_tool_key=origin_tool_key,
            excluded_tool_keys=set(),
        ):
            errors.append('C2 debe tener al menos un destino de escalamiento.')
        return

    _validate_c2_escalation_sequence(
        draft=draft,
        targets=active_targets,
        errors=errors,
    )


def _validate_c1_required_tools(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    catalogs = draft.get('_catalogs') or {}
    integrated_keys = catalogs.get('integrated_operations_tool_keys') or ()
    strategic_keys = catalogs.get('strategic_tool_keys') or ()

    if not integrated_keys:
        errors.append('C1 requiere al menos una herramienta ADA Operaciones Integradas activa.')

    if not strategic_keys:
        errors.append('C1 requiere al menos una herramienta ADA Estratégico activa.')


def _validate_c2_escalation_sequence(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
    errors: list[str],
) -> None:
    origin_tool_key = _text(draft.get('origin_tool_key'))

    current_tool_key = origin_tool_key
    seen_orders: set[int] = set()
    seen_tools: set[str] = set()

    ordered_targets = sorted(targets, key=_target_order)

    for target in ordered_targets:
        target_tool_key = _text(target.get('target_tool_key'))

        if not target_tool_key:
            errors.append('Existe un destino de escalamiento sin herramienta.')
            continue

        if target_tool_key == origin_tool_key:
            errors.append(
                f'El destino {target_tool_key} no puede ser igual a la herramienta inicial.',
            )

        if target_tool_key in seen_tools:
            errors.append(f'El destino {target_tool_key} está duplicado.')

        if not _is_allowed_next_escalation_target(
            draft=draft,
            current_tool_key=current_tool_key,
            target_tool_key=target_tool_key,
        ):
            errors.append(
                f'El destino {target_tool_key} no es válido para el eslabón actual.',
            )

        seen_tools.add(target_tool_key)
        current_tool_key = target_tool_key

        step_order = _target_order(target)

        if step_order <= 0:
            errors.append(f'El destino {target_tool_key} debe tener orden mayor a 0.')
        elif step_order in seen_orders:
            errors.append(f'El orden {step_order} está duplicado en escalamiento.')

        seen_orders.add(step_order)

        wait_minutes = target.get('wait_minutes_from_previous_step')

        if wait_minutes is None:
            errors.append(
                f'El destino {target_tool_key} debe tener minutos desde etapa anterior.',
            )
            continue

        try:
            if int(wait_minutes) < 0:
                errors.append(
                    f'El destino {target_tool_key} no puede tener minutos negativos.',
                )
        except Exception:
            errors.append(f'El destino {target_tool_key} tiene minutos inválidos.')


def _validate_integrated_operations_visualization(
    *,
    draft: dict[str, Any],
    errors: list[str],
) -> None:
    if not _requires_integrated_operations_visualization(draft=draft):
        if _visual_targets(draft=draft):
            errors.append(
                'La visualización ADA Operaciones Integradas solo aplica cuando la regla se muestra en esa herramienta.',
            )
        return

    visual_targets = _visual_targets(draft=draft)

    if len(visual_targets) != 1:
        errors.append('La regla debe tener una única visualización ADA Operaciones Integradas.')
        return

    visual_target = visual_targets[0]
    visual_tool_key = _text(visual_target.get('tool_key'))

    if not _is_integrated_operations_tool(
        draft=draft,
        tool_key=visual_tool_key,
    ):
        errors.append(
            'La visualización debe apuntar a una herramienta ADA Operaciones Integradas.',
        )

    affected_component_keys = _ensure_list(
        visual_target.get('affected_component_keys'),
    )
    affected_subcomponent_keys = _ensure_list(
        visual_target.get('affected_subcomponent_keys'),
    )

    if not affected_component_keys:
        errors.append(
            'La visualización requiere al menos un componente padre afectado.',
        )

    if not affected_subcomponent_keys:
        errors.append(
            'La visualización requiere al menos un subcomponente afectado/resaltado.',
        )

    _validate_component_subcomponent_consistency(
        draft=draft,
        affected_component_keys=affected_component_keys,
        affected_subcomponent_keys=affected_subcomponent_keys,
        errors=errors,
    )


def _validate_component_subcomponent_consistency(
    *,
    draft: dict[str, Any],
    affected_component_keys: list[str],
    affected_subcomponent_keys: list[str],
    errors: list[str],
) -> None:
    catalogs = draft.get('_catalogs') or {}
    component_rows = [
        row
        for row in catalogs.get('components') or []
        if isinstance(row, dict)
    ]
    subcomponent_rows = [
        row
        for row in catalogs.get('subcomponents') or []
        if isinstance(row, dict)
    ]

    if not component_rows and not subcomponent_rows:
        return

    component_keys = {
        _text(row.get('component_key'))
        for row in component_rows
        if _text(row.get('component_key'))
    }

    subcomponent_parent_by_key = {
        _text(row.get('subcomponent_key')): _text(row.get('parent_component_key'))
        for row in subcomponent_rows
        if _text(row.get('subcomponent_key'))
    }

    for component_key in affected_component_keys:
        if component_key not in component_keys:
            errors.append(f'El componente {component_key} no existe o no está activo.')

    for subcomponent_key in affected_subcomponent_keys:
        parent_component_key = subcomponent_parent_by_key.get(subcomponent_key)

        if not parent_component_key:
            errors.append(f'El subcomponente {subcomponent_key} no existe o no está activo.')
            continue

        if parent_component_key not in affected_component_keys:
            errors.append(
                f'El subcomponente {subcomponent_key} pertenece a {parent_component_key}, '
                'pero ese componente padre no está seleccionado.',
            )


def _requires_integrated_operations_visualization(
    *,
    draft: dict[str, Any],
) -> bool:
    if _text(draft.get('visibility_mode')) == AlarmVisibilityMode.TRACE_ONLY.value:
        return False

    origin_tool_key = _text(draft.get('origin_tool_key'))

    if origin_tool_key and _is_integrated_operations_tool(
        draft=draft,
        tool_key=origin_tool_key,
    ):
        return True

    if _text(draft.get('criticality_code')) == AlarmCriticality.C1.value:
        return True

    for target in _active_escalation_targets(draft=draft):
        if _is_integrated_operations_tool(
            draft=draft,
            tool_key=_text(target.get('target_tool_key')),
        ):
            return True

    return False


def _active_escalation_targets(
    *,
    draft: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        target
        for target in draft.get('escalation_targets') or []
        if isinstance(target, dict) and bool(target.get('is_enabled', True))
    ]


def _visual_targets(
    *,
    draft: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        target
        for target in draft.get('visual_targets') or []
        if isinstance(target, dict)
    ]


def _has_available_escalation_target_from_current_tool(
    *,
    draft: dict[str, Any],
    current_tool_key: str,
    excluded_tool_keys: set[str],
) -> bool:
    catalogs = draft.get('_catalogs') or {}

    for tool in catalogs.get('tools') or []:
        if not isinstance(tool, dict):
            continue

        target_tool_key = _text(tool.get('tool_key'))

        if not target_tool_key:
            continue

        if target_tool_key in excluded_tool_keys:
            continue

        if _is_allowed_next_escalation_target(
            draft=draft,
            current_tool_key=current_tool_key,
            target_tool_key=target_tool_key,
        ):
            return True

    return False


def _is_allowed_next_escalation_target(
    *,
    draft: dict[str, Any],
    current_tool_key: str,
    target_tool_key: str,
) -> bool:
    if not current_tool_key or not target_tool_key:
        return False

    if current_tool_key == target_tool_key:
        return False

    current_tier = _tool_tier_for_key(
        draft=draft,
        tool_key=current_tool_key,
    )

    target_tier = _tool_tier_for_key(
        draft=draft,
        tool_key=target_tool_key,
    )

    if current_tier == AlarmToolTier.PROCESS.value:
        return target_tier in {
            AlarmToolTier.INTEGRATED_OPERATIONS.value,
            AlarmToolTier.STRATEGIC.value,
        }

    if current_tier == AlarmToolTier.INTEGRATED_OPERATIONS.value:
        return target_tier == AlarmToolTier.STRATEGIC.value

    return False


def _is_integrated_operations_tool(
    *,
    draft: dict[str, Any],
    tool_key: str,
) -> bool:
    return (
        _tool_tier_for_key(
            draft=draft,
            tool_key=tool_key,
        )
        == AlarmToolTier.INTEGRATED_OPERATIONS.value
    )


def _tool_tier_for_key(
    *,
    draft: dict[str, Any],
    tool_key: str,
) -> str:
    catalogs = draft.get('_catalogs') or {}
    tool_tier_by_key = catalogs.get('tool_tier_by_key') or {}

    return _text(tool_tier_by_key.get(tool_key))


def _target_order(target: dict[str, Any]) -> int:
    try:
        return int(target.get('step_order') or 0)
    except Exception:
        return 0


def _ensure_list(
    value: Any,
) -> list[str]:
    if isinstance(value, list):
        return [
            _text(item)
            for item in value
            if _text(item)
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(';')
            if item.strip()
        ]

    return []


def _text(
    value: Any,
) -> str:
    return str(value or '').strip()


def _final_identifier_text(
    value: Any,
) -> str:
    return AlarmIdentifierNormalizationService.normalize_final_identifier(
        value=value,
    )