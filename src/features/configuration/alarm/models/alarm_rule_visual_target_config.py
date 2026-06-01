from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmRuleVisualTargetConfig:
    rule_key: str
    tool_key: str
    affected_component_keys: list[str]
    affected_subcomponent_keys: list[str]
    is_complete: bool
