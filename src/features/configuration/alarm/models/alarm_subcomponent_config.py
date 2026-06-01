from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmSubcomponentConfig:
    subcomponent_key: str
    subcomponent_code: str
    subcomponent_name: str
    parent_component_key: str
    display_order: int
    is_active: bool
