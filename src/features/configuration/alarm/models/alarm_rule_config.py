from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmRuleConfig:
    rule_key: str
    family_key: str

    rule_name: str
    display_name: str

    title_template: str
    cause_template: str
    content_key: str

    kind: str
    criticality_code: str
    business_category: str
    visibility_mode: str

    scope_key: str
    priority_order: int

    origin_tool_key: str
    operator_bucket: str

    color: str

    reappear_if_still_active_enabled: bool
    reappear_after_management_minutes: int | None
    continue_escalation_clock_when_hidden: bool
    use_message_management_override: bool

    escalation_summary: str
    visual_summary: str

    is_active: bool