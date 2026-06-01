from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AlarmKind = Literal['risk', 'impact']
AlarmRiskLevel = Literal['1', '2', '3']
AlarmReappearToolPolicy = Literal['origin_tool', 'last_visible_tool', 'fixed_tool']


@dataclass(frozen=True, slots=True)
class AlarmRuleConfig:
    rule_key: str
    family_key: str
    rule_name: str
    display_name: str
    title_template: str
    cause_template: str
    content_key: str
    dashboard_group_name: str
    kind: AlarmKind
    risk_level: AlarmRiskLevel
    priority_scope_key: str
    priority_order: int
    management_scope_key: str
    origin_tool_key: str
    operator_bucket: str
    color: str
    hide_all_tools_when_managed: bool
    reappear_if_still_active_enabled: bool
    reappear_after_management_minutes: int | None
    reappear_tool_policy: AlarmReappearToolPolicy
    reappear_tool_key: str
    continue_escalation_clock_when_hidden: bool
    reappear_if_unmanaged_enabled: bool
    reappear_after_unmanaged_minutes: int | None
    use_message_management_override: bool
    escalation_summary: str
    visual_summary: str
    is_active: bool
