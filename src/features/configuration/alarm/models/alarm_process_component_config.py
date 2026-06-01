from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AlarmProcessComponentType = Literal['component', 'subcomponent']
AlarmProcessComponentToolLevel = Literal['n0', 'all']


@dataclass(frozen=True, slots=True)
class AlarmProcessComponentConfig:
    component_key: str
    component_name: str
    component_type: AlarmProcessComponentType
    parent_component_key: str
    position_index: int | None
    additional_position_keys: list[str]
    tool_level: AlarmProcessComponentToolLevel
    display_order: int
    is_active: bool
