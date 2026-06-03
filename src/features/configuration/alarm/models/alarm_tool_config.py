from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmToolConfig:
    tool_key: str
    tool_name: str

    tool_tier: str
    visualization_mode: str

    display_order: int
    is_active: bool