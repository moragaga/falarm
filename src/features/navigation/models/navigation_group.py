"""
Provides functionality for managing navigation groups and utility functions for data normalization.

This module defines the `NavigationGroup` class with attributes and methods for creating and
serializing navigation groups typically used in menu interfaces. It also includes internal utility
functions for transforming and cleaning data types.

Classes
-------
NavigationGroup
    Encapsulates attributes and methods for a navigation group.

Functions
---------
_normalize_profiles(value: Any) -> tuple[str, ...]
    Normalizes input into a tuple of strings to represent allowed profiles.

_to_int(value: Any, default: int = 0) -> int
    Converts input to an integer with an optional default value.

_to_bool(value: Any, default: bool = False) -> bool
    Converts input to a boolean value with an optional default.

_clean_optional_string(value: Any) -> str | None
    Cleans input to ensure it is a stripped string or None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..support.ensure_validations import clean_optional_string, normalize_profiles, to_bool, to_int


@dataclass(frozen=True)
class NavigationGroup:
    group_id: str
    label: str
    icon: str | None = None
    order: int = 0
    allow_profiles: tuple[str, ...] = field(default_factory=tuple)
    is_active: bool = True
    visible_in_menu: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NavigationGroup:
        return cls(
            group_id=str(data.get('group_id', '') or '').strip(),
            label=str(data.get('label', '') or '').strip(),
            icon=clean_optional_string(data.get('icon')),
            order=to_int(data.get('order'), default=0),
            allow_profiles=normalize_profiles(data.get('allow_profiles')),
            is_active=to_bool(data.get('is_active'), default=True),
            visible_in_menu=to_bool(data.get('visible_in_menu'), default=True),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'group_id': self.group_id,
            'label': self.label,
            'icon': self.icon,
            'order': self.order,
            'allow_profiles': list(self.allow_profiles),
            'is_active': self.is_active,
            'visible_in_menu': self.visible_in_menu,
        }
