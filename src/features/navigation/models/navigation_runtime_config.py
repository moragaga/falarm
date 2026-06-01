"""
A configuration object representing runtime settings for navigation.

This class encapsulates navigation groups and links, allowing the runtime
configuration to be easily serialized, deserialized, and manipulated. It is
immutable, ensuring runtime safety by preventing changes after instantiation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .navigation_group import NavigationGroup
from .navigation_link import NavigationLink


@dataclass(frozen=True)
class NavigationRuntimeConfig:
    groups: tuple[NavigationGroup, ...] = field(default_factory=tuple)
    links: tuple[NavigationLink, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> NavigationRuntimeConfig:
        if not isinstance(data, dict):
            return cls()

        return cls(
            groups=tuple(
                NavigationGroup.from_dict(item)
                for item in data.get('groups', [])
                if isinstance(item, dict)
            ),
            links=tuple(
                NavigationLink.from_dict(item)
                for item in data.get('links', [])
                if isinstance(item, dict)
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'groups': [group.to_dict() for group in self.groups],
            'links': [link.to_dict() for link in self.links],
        }

    @property
    def is_empty(self) -> bool:
        return not self.groups and not self.links
