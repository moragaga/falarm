"""
Builds the navigation registry used for configuring navigation groups and links.

This function creates a default navigation structure consisting of groups and
links. Groups represent higher-level categories in the navigation menu, while
links represent specific menu options under these categories. The structure
is based on fallback groups and links, which can be optionally updated or used
as defaults.

Parameters
----------
app_name : str or None, optional
    The name of the application. If provided, this value will be used
    as the label for the 'Home' navigation link. If None, a default
    'Home' label will be used.

Returns
-------
tuple of tuple of NavigationGroup, tuple of NavigationLink
    A tuple containing two elements:
    1. A tuple of `NavigationGroup` objects representing all fallback navigation
       groups, configured with unique identifiers, labels, icons, and permissions.
    2. A tuple of `NavigationLink` objects representing all fallback links,
       configured with unique identifiers, paths, icons, and permissions.
"""

from __future__ import annotations

from uuid import uuid4

from src.features.configuration.models import Profile

from ..models.navigation_group import NavigationGroup
from ..models.navigation_link import NavigationLink


def build_navigation_registry(
    app_name: str | None = None,
) -> tuple[tuple[NavigationGroup, ...], tuple[NavigationLink, ...]]:
    GESTOR_GROUP = uuid4().__str__()
    NAVEGACION_GROUP = uuid4().__str__()
    IDENTIDAD_GROUP = uuid4().__str__()
    ANALYTICS_GROUP = uuid4().__str__()

    NAVIGATION_FALLBACK_GROUPS: tuple[NavigationGroup, ...] = (
        NavigationGroup(
            group_id=GESTOR_GROUP,
            label='GESTOR',
            order=60,
            icon='bi bi-pencil-square',
            allow_profiles=Profile.admin_values(),
            is_active=True,
            visible_in_menu=True,
        ),
        NavigationGroup(
            group_id=NAVEGACION_GROUP,
            label='NAVEGACIÓN',
            order=30,
            icon='bi bi-menu-button-wide',
            allow_profiles=Profile.admin_values(),
            is_active=True,
            visible_in_menu=True,
        ),
        NavigationGroup(
            group_id=IDENTIDAD_GROUP,
            label='IDENTIDAD',
            order=40,
            icon='bi bi-person-badge',
            allow_profiles=Profile.admin_values(),
            is_active=True,
            visible_in_menu=True,
        ),
        NavigationGroup(
            group_id=ANALYTICS_GROUP,
            label='ANALÍTICA',
            order=50,
            icon='bi bi-bar-chart-fill',
            allow_profiles=Profile.admin_values(),
            is_active=True,
            visible_in_menu=True,
        ),
    )

    NAVIGATION_FALLBACK_LINKS: tuple[NavigationLink, ...] = (
        NavigationLink(
            link_id=uuid4().__str__(),
            label=app_name or 'Home',
            path='/',
            link_type='internal',
            parent_group_id=None,
            icon_source='bootstrap',
            icon='bi bi-house',
            order=0,
            allow_profiles=Profile.values(),
            new_tab=False,
            is_active=True,
            force_reload=False,
            visible_in_menu=True,
        ),
        NavigationLink(
            link_id=uuid4().__str__(),
            label='Publicaciones',
            path='/admin/publication-manager',
            link_type='internal',
            parent_group_id=GESTOR_GROUP,
            icon_source='bootstrap',
            icon='bi bi-cloud-arrow-up',
            order=50,
            allow_profiles=Profile.admin_values(),
            new_tab=False,
            is_active=True,
            force_reload=False,
            visible_in_menu=True,
        ),
        NavigationLink(
            link_id=uuid4().__str__(),
            label='Links',
            path='/admin/navigation/links',
            link_type='internal',
            parent_group_id=NAVEGACION_GROUP,
            icon_source='bootstrap',
            icon='bi bi-link-45deg',
            order=70,
            allow_profiles=Profile.admin_values(),
            new_tab=False,
            is_active=True,
            force_reload=False,
            visible_in_menu=True,
        ),
        NavigationLink(
            link_id=uuid4().__str__(),
            label='Grupos',
            path='/admin/navigation/groups',
            link_type='internal',
            parent_group_id=NAVEGACION_GROUP,
            icon_source='bootstrap',
            icon='bi bi-folder-symlink',
            order=60,
            allow_profiles=Profile.admin_values(),
            new_tab=False,
            is_active=True,
            force_reload=False,
            visible_in_menu=True,
        ),
        NavigationLink(
            link_id=uuid4().__str__(),
            label='Usuarios',
            path='/admin/identity/users',
            link_type='internal',
            parent_group_id=IDENTIDAD_GROUP,
            icon_source='bootstrap',
            icon='bi bi-person-lines-fill',
            order=90,
            allow_profiles=Profile.admin_values(),
            new_tab=False,
            is_active=True,
            force_reload=False,
            visible_in_menu=True,
        ),
        NavigationLink(
            link_id=uuid4().__str__(),
            label='Uso del dashboard',
            path='/analytics/user-session',
            link_type='internal',
            parent_group_id=ANALYTICS_GROUP,
            icon_source='bootstrap',
            icon='bi bi-people',
            order=110,
            allow_profiles=Profile.admin_values(),
            new_tab=False,
            is_active=True,
            force_reload=False,
            visible_in_menu=True,
        ),
        NavigationLink(
            link_id=uuid4().__str__(),
            label='Cerrar sesión',
            path='/logout',
            link_type='internal',
            parent_group_id=None,
            icon_source='bootstrap',
            icon='bi bi-escape',
            order=999,
            allow_profiles=Profile.values(),
            new_tab=False,
            is_active=True,
            force_reload=True,
            visible_in_menu=True,
        ),
    )

    return (
        NAVIGATION_FALLBACK_GROUPS,
        NAVIGATION_FALLBACK_LINKS,
    )
