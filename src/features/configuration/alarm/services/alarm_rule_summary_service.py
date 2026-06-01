from __future__ import annotations

from typing import Any


class AlarmRuleSummaryService:
    @staticmethod
    def build_escalation_summary(
        *,
        targets: list[dict[str, Any]] | None,
        tool_name_by_key: dict[str, str] | None = None,
    ) -> str:
        active_targets = [
            target
            for target in targets or []
            if isinstance(target, dict) and bool(target.get('is_enabled'))
        ]

        if not active_targets:
            return 'No escala'

        names = tool_name_by_key or {}
        parts: list[str] = []
        for target in sorted(active_targets, key=_target_order):
            tool_key = str(target.get('target_tool_key') or '').strip()
            tool_name = names.get(tool_key, tool_key)
            minutes = target.get('wait_minutes_from_previous_stage')
            if not tool_key:
                continue

            if minutes in (0, '0'):
                parts.append(f'{tool_name}: inmediato')
                continue

            parts.append(f'{tool_name}: +{minutes} min desde etapa anterior')

        return ' · '.join(parts) if parts else 'No escala'

    @staticmethod
    def build_visual_summary(
        *,
        targets: list[dict[str, Any]] | None,
        component_name_by_key: dict[str, str] | None = None,
        subcomponent_name_by_key: dict[str, str] | None = None,
    ) -> str:
        active_targets = [
            target
            for target in targets or []
            if isinstance(target, dict) and str(target.get('tool_key') or '') == 'nivel_0'
        ]

        if not active_targets:
            return 'Sin visualización Nivel 0'

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

        return f'Nivel 0: {component_part} · resalta {subcomponent_part}'


def _target_order(target: dict[str, Any]) -> int:
    try:
        return int(target.get('step_order') or 0)
    except Exception:
        return 0
