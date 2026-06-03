from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.features.configuration.alarm.options import (
    AlarmBusinessCategory,
    AlarmColor,
    AlarmCriticality,
    AlarmKind,
    AlarmVisibilityMode,
)


class AlarmRuleRowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]
        rule_suffix = uuid4().hex[:8]

        return {
            'rule_key': f'alarm_rule_{rule_suffix}',
            'family_key': '',
            'rule_name': '',
            'display_name': '',
            'title_template': '',
            'cause_template': '',
            'content_key': f'alarm_content_{rule_suffix}',
            'kind': AlarmKind.RISK.value,
            'criticality_code': AlarmCriticality.C3.value,
            'business_category': AlarmBusinessCategory.OPERATIONAL.value,
            'visibility_mode': AlarmVisibilityMode.VISIBLE.value,
            'scope_key': '',
            'priority_order': AlarmRuleRowFactoryService._resolve_next_priority(rows=rows),
            'origin_tool_key': '',
            'operator_bucket': 'default',
            'color': AlarmColor.YELLOW.value,
            'reappear_if_still_active_enabled': True,
            'reappear_after_management_minutes': 60,
            'continue_escalation_clock_when_hidden': True,
            'use_message_management_override': True,
            'escalation_summary': '',
            'visual_summary': '',
            'is_active': True,
        }

    @staticmethod
    def _resolve_next_priority(
        *,
        rows: list[dict[str, Any]],
    ) -> int:
        priorities: list[int] = []

        for row in rows:
            try:
                priority = int(row.get('priority_order') or 0)
            except Exception:
                continue

            if priority > 0:
                priorities.append(priority)

        if not priorities:
            return 100

        return max(priorities) + 10