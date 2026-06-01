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

        if not str(draft.get('priority_scope_key') or '').strip():
            errors.append('La regla debe tener scope de prioridad.')

        if not str(draft.get('management_scope_key') or '').strip():
            errors.append('La regla debe tener scope de gestión.')

        origin_tool_key = str(draft.get('origin_tool_key') or '').strip()
        if not origin_tool_key:
            errors.append('La regla debe tener herramienta inicial.')

        risk_level = str(draft.get('risk_level') or '3')
        escalation_targets = _active_escalation_targets(draft=draft)

        if risk_level == '1' and not _has_n0_immediate_target(targets=escalation_targets):
            errors.append('Riesgo 1 requiere destino Nivel 0 inmediato con 0 minutos.')

        if risk_level == '3' and escalation_targets:
            errors.append('Riesgo 3 no debe tener destinos de escalamiento activos.')

        if draft.get('reappear_if_still_active_enabled') and not draft.get(
            'reappear_after_management_minutes'
        ):
            errors.append('Si reaparece por no normalización, debe indicar minutos de espera.')

        if str(draft.get('reappear_tool_policy') or '') == 'fixed_tool' and not str(
            draft.get('reappear_tool_key') or ''
        ).strip():
            errors.append('Si la reaparición usa herramienta fija, debe indicar la herramienta.')

        for target in escalation_targets:
            target_tool_key = str(target.get('target_tool_key') or '').strip()
            if not target_tool_key:
                errors.append('Existe un destino de escalamiento sin herramienta.')
                continue

            if target.get('show_after_active_minutes') is None:
                errors.append(f'El destino {target_tool_key} debe tener minutos.')
                continue

            try:
                if int(target.get('show_after_active_minutes') or 0) < 0:
                    errors.append(f'El destino {target_tool_key} no puede tener minutos negativos.')
            except Exception:
                errors.append(f'El destino {target_tool_key} tiene minutos inválidos.')

        required_visual_tools = _required_visual_tools(draft=draft)
        visual_targets = _visual_targets_by_tool(draft=draft)
        for tool_key in required_visual_tools:
            if tool_key not in visual_targets:
                errors.append(f'Falta visualización para la herramienta {tool_key}.')

        for visual_target in draft.get('visual_targets') or []:
            if not isinstance(visual_target, dict):
                continue

            tool_key = str(visual_target.get('tool_key') or '').strip()
            if not tool_key:
                errors.append('Existe una visualización sin herramienta.')
                continue

            if not str(visual_target.get('main_component_key') or '').strip():
                errors.append(f'La visualización de {tool_key} debe tener componente principal.')

            visualization_mode = str(visual_target.get('visualization_mode') or '')
            if visualization_mode == 'queue_for_queue' or tool_key == 'nivel_0':
                if not visual_target.get('affected_component_keys'):
                    errors.append(f'{tool_key} requiere componentes afectados.')

                if not visual_target.get('highlight_target_key'):
                    errors.append(f'{tool_key} requiere elemento a resaltar.')

                if visual_target.get('min_position') is None or visual_target.get('max_position') is None:
                    errors.append(f'{tool_key} requiere posición mínima y máxima.')
                elif int(visual_target['min_position']) > int(visual_target['max_position']):
                    errors.append(f'{tool_key} tiene posición mínima mayor que posición máxima.')

        return errors


def _active_escalation_targets(*, draft: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        target
        for target in draft.get('escalation_targets') or []
        if isinstance(target, dict) and bool(target.get('is_enabled'))
    ]


def _has_n0_immediate_target(*, targets: list[dict[str, Any]]) -> bool:
    for target in targets:
        if str(target.get('target_tool_key') or '') != 'nivel_0':
            continue

        try:
            return int(target.get('show_after_active_minutes') or 0) == 0
        except Exception:
            return False

    return False


def _required_visual_tools(*, draft: dict[str, Any]) -> set[str]:
    tools: set[str] = set()
    origin_tool_key = str(draft.get('origin_tool_key') or '').strip()
    if origin_tool_key:
        tools.add(origin_tool_key)

    for target in _active_escalation_targets(draft=draft):
        target_tool_key = str(target.get('target_tool_key') or '').strip()
        if target_tool_key:
            tools.add(target_tool_key)

    if str(draft.get('risk_level') or '') == '1':
        tools.add('nivel_0')

    return tools


def _visual_targets_by_tool(*, draft: dict[str, Any]) -> dict[str, dict[str, Any]]:
    targets: dict[str, dict[str, Any]] = {}

    for target in draft.get('visual_targets') or []:
        if not isinstance(target, dict):
            continue

        tool_key = str(target.get('tool_key') or '').strip()
        if not tool_key:
            continue

        targets[tool_key] = target

    return targets
