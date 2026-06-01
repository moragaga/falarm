from __future__ import annotations

from typing import Any


class AlarmConfigurationValidationService:
    @staticmethod
    def validate_rule_draft(*, draft: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        if not str(draft.get('family_key') or '').strip():
            errors.append('La regla debe tener familia.')

        if not str(draft.get('rule_key') or '').strip():
            errors.append('La regla debe tener ID.')

        if not str(draft.get('rule_name') or '').strip():
            errors.append('La regla debe tener nombre.')

        if not str(draft.get('display_name') or '').strip():
            errors.append('La regla debe tener nombre visible.')

        if not str(draft.get('content_key') or '').strip():
            errors.append('La regla debe tener ID de contenido automático.')

        if not str(draft.get('scope_key') or '').strip():
            errors.append('La regla debe tener grupo prioridad/gestión.')

        if str(draft.get('color') or '') not in {'red', 'yellow'}:
            errors.append('El color de la regla debe ser Rojo o Amarillo.')

        origin_tool_key = str(draft.get('origin_tool_key') or '').strip()
        if not origin_tool_key:
            errors.append('La regla debe tener herramienta inicial.')

        risk_level = str(draft.get('risk_level') or '3')
        escalation_targets = _active_escalation_targets(draft=draft)

        if risk_level == '1' and not _has_level_one_immediate_target(draft=draft, targets=escalation_targets):
            errors.append('Riesgo 1 requiere destino de nivel 1 inmediato con 0 minutos.')

        if risk_level == '3' and escalation_targets:
            errors.append('Riesgo 3 no debe tener destinos de escalamiento activos.')

        if draft.get('reappear_if_still_active_enabled') and not draft.get(
            'reappear_after_management_minutes'
        ):
            errors.append('Si reaparece por no normalización, debe indicar minutos de espera desde la gestión.')

        seen_orders: set[int] = set()
        seen_tools: set[str] = set()
        for target in escalation_targets:
            target_tool_key = str(target.get('target_tool_key') or '').strip()
            if not target_tool_key:
                errors.append('Existe un destino de escalamiento sin herramienta.')
                continue

            if target_tool_key == origin_tool_key:
                errors.append(f'El destino {target_tool_key} no puede ser igual a la herramienta inicial.')

            if target_tool_key in seen_tools:
                errors.append(f'El destino {target_tool_key} está duplicado.')
            seen_tools.add(target_tool_key)

            try:
                step_order = int(target.get('step_order') or 0)
            except Exception:
                step_order = 0

            if step_order <= 0:
                errors.append(f'El destino {target_tool_key} debe tener orden mayor a 0.')
            elif step_order in seen_orders:
                errors.append(f'El orden {step_order} está duplicado en escalamiento.')
            seen_orders.add(step_order)

            wait_minutes = target.get('wait_minutes_from_previous_stage')
            if wait_minutes is None:
                errors.append(f'El destino {target_tool_key} debe tener minutos desde etapa anterior.')
                continue

            try:
                if int(wait_minutes) < 0:
                    errors.append(f'El destino {target_tool_key} no puede tener minutos negativos.')
            except Exception:
                errors.append(f'El destino {target_tool_key} tiene minutos inválidos.')

        _validate_n0_visualization(draft=draft, errors=errors)

        return errors


def _validate_n0_visualization(*, draft: dict[str, Any], errors: list[str]) -> None:
    requires_n0_visual = _requires_n0_visual(draft=draft)
    visual_targets = [
        target
        for target in draft.get('visual_targets') or []
        if isinstance(target, dict)
    ]

    if not requires_n0_visual:
        if visual_targets:
            errors.append('La visualización Nivel 0 solo aplica cuando la regla escala o aparece en Nivel 0.')
        return

    if len(visual_targets) != 1:
        errors.append('La regla debe tener una única visualización Nivel 0.')
        return

    visual_target = visual_targets[0]
    if not _is_level_one_tool(draft=draft, tool_key=str(visual_target.get('tool_key') or '')):
        errors.append('La visualización de la regla debe apuntar únicamente a la herramienta de nivel 1.')

    affected_component_keys = _ensure_list(visual_target.get('affected_component_keys'))
    affected_subcomponent_keys = _ensure_list(visual_target.get('affected_subcomponent_keys'))

    if not affected_component_keys:
        errors.append('La visualización Nivel 0 requiere al menos un componente padre afectado.')

    if not affected_subcomponent_keys:
        errors.append('La visualización Nivel 0 requiere al menos un subcomponente afectado/resaltado.')

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
    if component_rows or subcomponent_rows:
        component_keys = {
            str(row.get('component_key') or '')
            for row in component_rows
        }
        subcomponent_parent_by_key = {
            str(row.get('subcomponent_key') or ''): str(row.get('parent_component_key') or '')
            for row in subcomponent_rows
        }

        for component_key in affected_component_keys:
            if component_key not in component_keys:
                errors.append(f'El componente Nivel 0 {component_key} no existe o no es componente padre.')

        for subcomponent_key in affected_subcomponent_keys:
            parent_component_key = subcomponent_parent_by_key.get(subcomponent_key)
            if not parent_component_key:
                errors.append(f'El subcomponente Nivel 0 {subcomponent_key} no existe.')
                continue

            if parent_component_key not in affected_component_keys:
                errors.append(
                    f'El subcomponente {subcomponent_key} pertenece a {parent_component_key}, '
                    'pero ese componente padre no está seleccionado.'
                )


def _active_escalation_targets(*, draft: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        target
        for target in draft.get('escalation_targets') or []
        if isinstance(target, dict) and bool(target.get('is_enabled'))
    ]


def _has_level_one_immediate_target(
    *,
    draft: dict[str, Any],
    targets: list[dict[str, Any]],
) -> bool:
    for target in targets:
        if not _is_level_one_tool(draft=draft, tool_key=str(target.get('target_tool_key') or '')):
            continue

        try:
            return int(target.get('wait_minutes_from_previous_stage') or 0) == 0
        except Exception:
            return False

    return False


def _requires_n0_visual(*, draft: dict[str, Any]) -> bool:
    if str(draft.get('risk_level') or '') == '1':
        return True

    for target in _active_escalation_targets(draft=draft):
        if _is_level_one_tool(draft=draft, tool_key=str(target.get('target_tool_key') or '')):
            return True

    return False



def _is_level_one_tool(*, draft: dict[str, Any], tool_key: str) -> bool:
    catalogs = draft.get('_catalogs') or {}
    tool_level_by_key = catalogs.get('tool_level_by_key') or {}
    configured = str(catalogs.get('level_one_tool_key') or '').strip()
    return (
        _normalize_tool_level(value=tool_level_by_key.get(tool_key)) == '1'
        or (configured and tool_key == configured)
        or tool_key == 'nivel_0'
    )


def _normalize_tool_level(*, value: Any) -> str:
    normalized = str(value or '').strip().lower()
    aliases = {
        '1': '1',
        'n0': '1',
        'nivel_0': '1',
        'nivel 0': '1',
        'sala': '1',
        '2': '2',
        'executive': '2',
        'ejecutiva': '2',
        'ejecutivo': '2',
        '3': '3',
        'n1': '3',
        'ada_n1': '3',
    }
    return aliases.get(normalized, normalized if normalized in {'1', '2', '3'} else '')


def _ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item or '').strip()]

    if isinstance(value, str):
        return [item.strip() for item in value.split(';') if item.strip()]

    return []
