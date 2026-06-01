from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AlarmToolLevel = Literal['1', '2', '3']
AlarmVisualizationMode = Literal['generic', 'distributed', 'queue_for_queue']


@dataclass(frozen=True, slots=True)
class AlarmToolConfig:
    tool_key: str
    tool_name: str
    tool_level: AlarmToolLevel
    visualization_mode: AlarmVisualizationMode
    display_order: int
    is_active: bool
