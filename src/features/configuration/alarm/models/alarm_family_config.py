from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmFamilyConfig:
    family_key: str
    family_name: str
    dashboard_group_name: str
    description: str
    display_order: int
    is_available: bool
