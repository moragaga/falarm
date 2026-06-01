from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmRuleVisualTargetConfig:
    rule_key: str
    tool_key: str
    visualization_mode: str
    main_component_key: str
    affected_component_keys: list[str]
    affected_subcomponent_keys: list[str]
    highlight_target_key: str
    position_group_key: str
    min_position: int | None
    max_position: int | None
    is_complete: bool
