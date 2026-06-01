from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmRuleEscalationTargetConfig:
    rule_key: str
    target_tool_key: str
    is_enabled: bool
    show_after_active_minutes: int | None
