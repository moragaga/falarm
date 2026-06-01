"""
A dataclass representation of a navigation link model for user interfaces.

This module provides a `NavigationLink` class, which encapsulates the
properties and functionality required to manage navigation items in a
menu structure. It supports hierarchical navigation, visibility toggles,
and associated permissions for profile-based visibility.

Functions from the `ensure_validations` module are used for data
transformation and validation.

Classes
-------
NavigationLink
    A class representing a single menu link with attributes like label,
    path, and parent group information to represent navigation structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..support.ensure_validations import clean_optional_string, normalize_profiles, to_bool, to_int


@dataclass(frozen=True)
class NavigationLink:
    link_id: str
    label: str
    path: str
    link_type: str
    parent_group_id: str | None = None
    icon_source: str | None = None
    icon: str | None = None
    order: int = 0
    allow_profiles: tuple[str, ...] = field(default_factory=tuple)
    new_tab: bool = False
    is_active: bool = True
    force_reload: bool = False
    visible_in_menu: bool = True

    @property
    def is_child(self) -> bool:
        return bool(self.parent_group_id)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NavigationLink:
        return cls(
            link_id=str(data.get('link_id', '') or '').strip(),
            label=str(data.get('label', '') or '').strip(),
            path=str(data.get('path', '') or '').strip(),
            link_type=str(data.get('link_type', '') or '').strip(),
            parent_group_id=clean_optional_string(data.get('parent_group_id')),
            icon_source=str(data.get('icon_source', '') or '').strip(),
            icon=clean_optional_string(data.get('icon')),
            order=to_int(data.get('order'), default=0),
            allow_profiles=normalize_profiles(data.get('allow_profiles')),
            new_tab=to_bool(data.get('new_tab'), default=False),
            is_active=to_bool(data.get('is_active'), default=True),
            force_reload=to_bool(data.get('force_reload'), default=False),
            visible_in_menu=to_bool(data.get('visible_in_menu'), default=True),
        )

    def with_allow_profiles(self, allow_profiles: tuple[str, ...]) -> NavigationLink:
        return NavigationLink(
            link_id=self.link_id,
            label=self.label,
            path=self.path,
            link_type=self.link_type,
            parent_group_id=self.parent_group_id,
            icon_source=self.icon_source,
            icon=self.icon,
            order=self.order,
            allow_profiles=allow_profiles,
            new_tab=self.new_tab,
            is_active=self.is_active,
            force_reload=self.force_reload,
            visible_in_menu=self.visible_in_menu,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'link_id': self.link_id,
            'label': self.label,
            'path': self.path,
            'link_type': self.link_type,
            'parent_group_id': self.parent_group_id,
            'icon_source': self.icon_source,
            'icon': self.icon,
            'order': self.order,
            'allow_profiles': list(self.allow_profiles),
            'new_tab': self.new_tab,
            'is_active': self.is_active,
            'force_reload': self.force_reload,
            'visible_in_menu': self.visible_in_menu,
        }
