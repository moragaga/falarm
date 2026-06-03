from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmProcessComponentConfig:
    component_key: str
    component_name: str

    component_type: str
    parent_component_key: str

    position_index: int | None
    additional_position_keys: list[str]

    applies_to_tool_tier: str

    display_order: int
    is_active: bool