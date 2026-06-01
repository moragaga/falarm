from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AlarmComponentAppliesToLevel = Literal['1', 'all']


@dataclass(frozen=True, slots=True)
class AlarmComponentConfig:
    component_key: str
    component_code: str
    component_name: str
    position_index: int
    applies_to_tool_level: AlarmComponentAppliesToLevel
    display_order: int
    is_active: bool
