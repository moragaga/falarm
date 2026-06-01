"""Navigation service for loading and normalizing navigation runtime configurations.

This module provides functionality to load navigation configurations, deduplicate
navigation groups and links, validate links, and normalize link profiles. The primary
purpose is to manage and structure navigation elements like groups and links for use
within applications.
"""

from __future__ import annotations

from ..models.navigation_group import NavigationGroup
from ..models.navigation_link import NavigationLink
from ..models.navigation_runtime_config import NavigationRuntimeConfig
from ..registry.navigation_registry import build_navigation_registry
from ..repositories.navigation_projection_repository import (
    NavigationProjectionRepository,
)


class NavigationReadService:
    def __init__(
        self,
        projection_repository: NavigationProjectionRepository | None = None,
        app_name: str | None = None,
    ) -> None:
        self._projection_repository = projection_repository
        self._app_name = app_name

    def load_navigation(self) -> NavigationRuntimeConfig:
        runtime_config = self._load_from_projection()

        if not runtime_config.is_empty:
            return runtime_config

        groups_fallback, links_fallback = build_navigation_registry(app_name=self._app_name)

        return NavigationRuntimeConfig(
            groups=groups_fallback,
            links=links_fallback,
        )

    def _load_from_projection(self) -> NavigationRuntimeConfig:
        if self._projection_repository is None:
            return NavigationRuntimeConfig()

        group_rows = self._projection_repository.load_group_rows()
        link_rows = self._projection_repository.load_link_rows()

        return self._normalize(
            group_rows=group_rows,
            link_rows=link_rows,
        )

    @staticmethod
    def _normalize(
        group_rows: list[dict],
        link_rows: list[dict],
    ) -> NavigationRuntimeConfig:
        groups = _deduplicate_groups(
            groups=[NavigationGroup.from_dict(row) for row in group_rows if isinstance(row, dict)]
        )

        links = _deduplicate_links(
            links=[NavigationLink.from_dict(row) for row in link_rows if isinstance(row, dict)]
        )

        valid_groups = tuple(group for group in groups if group.group_id and group.label)

        groups_by_id = {group.group_id: group for group in valid_groups}

        valid_links = tuple(
            _normalize_link_profiles(
                link=link,
                groups_by_id=groups_by_id,
            )
            for link in links
            if _is_valid_link(
                link=link,
                groups_by_id=groups_by_id,
            )
        )

        return NavigationRuntimeConfig(
            groups=tuple(
                sorted(
                    valid_groups,
                    key=lambda group: (
                        group.order,
                        group.label,
                        group.group_id,
                    ),
                )
            ),
            links=tuple(
                sorted(
                    valid_links,
                    key=lambda link: (
                        link.order,
                        link.label,
                        link.link_id,
                    ),
                )
            ),
        )


def _deduplicate_groups(
    groups: list[NavigationGroup],
) -> tuple[NavigationGroup, ...]:
    deduped: dict[str, NavigationGroup] = {}

    for group in groups:
        if not group.group_id:
            continue

        deduped[group.group_id] = group

    return tuple(deduped.values())


def _deduplicate_links(
    links: list[NavigationLink],
) -> tuple[NavigationLink, ...]:
    deduped: dict[str, NavigationLink] = {}

    for link in links:
        if not link.link_id:
            continue

        deduped[link.link_id] = link

    return tuple(deduped.values())


def _is_valid_link(
    link: NavigationLink,
    groups_by_id: dict[str, NavigationGroup],
) -> bool:
    if not link.link_id or not link.label or not link.path:
        return False

    if not link.parent_group_id:
        return True

    return link.parent_group_id in groups_by_id


def _normalize_link_profiles(
    link: NavigationLink,
    groups_by_id: dict[str, NavigationGroup],
) -> NavigationLink:
    if not link.parent_group_id:
        return link

    parent = groups_by_id.get(link.parent_group_id)

    if parent is None:
        return link

    if not link.allow_profiles:
        return link.with_allow_profiles(parent.allow_profiles)

    effective_profiles = tuple(
        profile for profile in link.allow_profiles if profile in parent.allow_profiles
    )

    return link.with_allow_profiles(effective_profiles)
