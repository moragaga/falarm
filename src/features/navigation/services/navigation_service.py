"""
A service for managing and building navigation menus based on runtime configuration
and user profiles.

The module provides methods to construct structured navigation menu nodes, check
accessibility of paths for user profiles, validate active links, confirm active child
elements in groups, and normalize paths for comparison.
"""

from __future__ import annotations

from ..models.navigation_group import NavigationGroup
from ..models.navigation_link import NavigationLink
from ..models.navigation_menu_node import NavigationMenuNode
from ..models.navigation_runtime_config import (
    NavigationRuntimeConfig,
)


class NavigationService:
    @staticmethod
    def build_menu_nodes_for_profile(
        config: NavigationRuntimeConfig,
        profile: str | None,
    ) -> list[NavigationMenuNode]:
        if not profile:
            return []

        visible_groups = {
            group.group_id: group
            for group in config.groups
            if _is_group_visible_for_profile(
                group=group,
                profile=profile,
            )
        }

        root_links: list[NavigationLink] = []
        children_by_parent: dict[str, list[NavigationLink]] = {}

        for link in config.links:
            if not _is_link_visible_for_profile(
                link=link,
                profile=profile,
            ):
                continue

            if link.parent_group_id and link.parent_group_id in visible_groups:
                children_by_parent.setdefault(link.parent_group_id, []).append(link)
                continue

            if not link.parent_group_id:
                root_links.append(link)

        nodes: list[NavigationMenuNode] = [
            NavigationMenuNode.from_link(link) for link in root_links
        ]

        for group in visible_groups.values():
            children = tuple(
                sorted(
                    children_by_parent.get(group.group_id, []),
                    key=lambda child: (
                        child.order,
                        child.label,
                        child.link_id,
                    ),
                )
            )

            if not children:
                continue

            nodes.append(
                NavigationMenuNode.from_group(
                    group=group,
                    children=children,
                )
            )

        return sorted(
            nodes,
            key=lambda node: (
                node.order,
                _node_label(node),
            ),
        )

    @staticmethod
    def can_access_path(
        config: NavigationRuntimeConfig,
        profile: str | None,
        path: str,
    ) -> bool:
        if not profile:
            return False

        normalized_path = NavigationService.normalize_path(path)

        for link in config.links:
            if NavigationService.normalize_path(link.path) != normalized_path:
                continue

            return profile in link.allow_profiles

        return False

    @staticmethod
    def is_active_link(
        link: NavigationLink,
        current_path: str | None,
    ) -> bool:
        return NavigationService.normalize_path(link.path) == NavigationService.normalize_path(
            current_path,
        )

    @staticmethod
    def group_has_active_child(
        children: tuple[NavigationLink, ...],
        current_path: str | None,
    ) -> bool:
        return any(
            NavigationService.is_active_link(
                link=child,
                current_path=current_path,
            )
            for child in children
        )

    @staticmethod
    def normalize_path(path: str | None) -> str:
        if not path:
            return '/'

        return path.rstrip('/') or '/'


def _is_group_visible_for_profile(
    group: NavigationGroup,
    profile: str,
) -> bool:
    if not group.visible_in_menu:
        return False

    return profile in group.allow_profiles


def _is_link_visible_for_profile(
    link: NavigationLink,
    profile: str,
) -> bool:
    if not link.visible_in_menu:
        return False

    return profile in link.allow_profiles


def _node_label(node: NavigationMenuNode) -> str:
    if node.node_type == 'group' and node.group:
        return node.group.label

    if node.node_type == 'link' and node.link:
        return node.link.label

    return ''
