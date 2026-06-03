from __future__ import annotations

from typing import Any


class AlarmRuleSummaryService:
    @staticmethod
    def build_escalation_summary(
        *,
        criticality_code: str,
        visibility_mode: str,
        targets: list[dict[str, Any]] | None,
        tool_name_by_key: dict[str, str] | None = None,
    ) -> str:
        if visibility_mode == 'trace_only':
            return 'Solo trazabilidad'

        if criticality_code == 'C1':
            return 'Visibilidad inmediata: herramienta inicial, ADA Operaciones Integradas y ADA Estratégico'

        if criticality_code == 'C3':
            return 'No escala'

        active_targets = [
            target
            for target in targets or []
            if isinstance(target, dict) and bool(target.get('is_enabled', True))
        ]

        if not active_targets:
            return 'C2 sin destinos configurados'

        names = tool_name_by_key or {}
        parts: list[str] = []

        for target in sorted(active_targets, key=_target_order):
            tool_key = str(target.get('target_tool_key') or '').strip()
            if not tool_key:
                continue

            tool_name = names.get(tool_key, tool_key)
            minutes = target.get('wait_minutes_from_previous_step')

            if minutes in (0, '0'):
                parts.append(f'{tool_name}: inmediato')
                continue

            parts.append(f'{tool_name}: +{minutes} min desde etapa anterior')

        return ' · '.join(parts) if parts else 'C2 sin destinos configurados'

    @staticmethod
    def build_visual_summary(
        *,
        visibility_mode: str,
        targets: list[dict[str, Any]] | None,
        component_name_by_key: dict[str, str] | None = None,
        subcomponent_name_by_key: dict[str, str] | None = None,
    ) -> str:
        if visibility_mode == 'trace_only':
            return 'Sin visualización'

        active_targets = [
            target
            for target in targets or []
            if isinstance(target, dict) and bool(target.get('is_complete'))
        ]

        if not active_targets:
            return 'Sin visualización ADA Operaciones Integradas'

        target = active_targets[0]
        component_names = component_name_by_key or {}
        subcomponent_names = subcomponent_name_by_key or {}

        components = [
            component_names.get(str(component_key), str(component_key))
            for component_key in target.get('affected_component_keys') or []
        ]

        subcomponents = [
            subcomponent_names.get(str(subcomponent_key), str(subcomponent_key))
            for subcomponent_key in target.get('affected_subcomponent_keys') or []
        ]

        component_part = ', '.join(components) if components else 'sin componentes'
        subcomponent_part = ', '.join(subcomponents) if subcomponents else 'sin subcomponentes'

        return f'ADA Operaciones Integradas: {component_part} · resalta {subcomponent_part}'


def _target_order(target: dict[str, Any]) -> int:
    try:
        return int(target.get('step_order') or 0)
    except Exception:
        return 0