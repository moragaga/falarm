from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmRuleEscalationTargetConfig:
    rule_key: str
    step_order: int
    target_tool_key: str
    is_enabled: bool
    wait_minutes_from_previous_step: int | None