"""
Provides functions to build navigation menu content for a web application.

This module implements utilities for dynamically generating a navigation menu
based on the user's profile and permissions. The generated content includes user
information, navigation links, and group nodes, organized hierarchically as
specified by the runtime configuration of the application.

Attributes
----------
ADA_PROJECTS_URL : str
    A constant URL to redirect to the ADA projects page.

Functions
---------
build_navigation_menu_content(current_path=None)
    Builds the main content of the navigation menu.

_build_user_content(identity)
    Builds the user information card for the navigation menu.

_build_user_avatar(name, photo_src)
    Builds the avatar component for the user, based on an image or fallback to initials.

_build_master_projects_button()
    Builds a link button that redirects to the ADA projects page.

_build_navigation_nodes(nodes, current_path)
    Builds the navigation menu tree based on the provided nodes.

_build_node(node, current_path)
    Constructs an appropriate navigation component (group or link) for a single node.

_build_group_node(group, children, current_path)
    Builds a group navigation node with collapsible child items.

_build_link_node(link, current_path, is_child)
    Builds a link navigation node as a root or child-level item.

_build_link_button_class_name(is_active, is_child)
    Constructs CSS class names for a link button based on its state.

_build_group_button_class_name(is_open)
    Constructs CSS class names for a group button based on its state.
"""

from __future__ import annotations

import base64
from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html
from flask import session

from src.features.navigation.models import (
    NavigationGroup,
    NavigationLink,
    NavigationMenuNode,
    NavigationRuntimeConfig,
)
from src.features.navigation.services import NavigationService

from .ids import AppNavigationIds

ADA_PROJECTS_URL = 'https://ada.pelambres.cl/'


def build_navigation_menu_content(current_path: str | None = None) -> html.Div:
    raw_config = session.get('navigation_runtime_config')
    identity = session.get('identity') or {}
    current_profile = identity.get('profile')

    config = NavigationRuntimeConfig.from_dict(raw_config)

    nodes = NavigationService.build_menu_nodes_for_profile(
        config=config,
        profile=current_profile,
    )

    return html.Div(
        className='app-navigation-content d-flex flex-column h-100',
        children=[
            _build_user_content(identity=identity),
            _build_master_projects_button(),
            html.Div(className='app-navigation-soft-divider'),
            _build_navigation_nodes(
                nodes=nodes,
                current_path=current_path,
            ),
        ],
    )


def _build_user_content(
    *,
    identity: dict[str, Any],
) -> html.Div:
    name = str(identity.get('name') or 'Usuario').strip()
    email = str(identity.get('email') or '').strip()
    profile = str(identity.get('profile') or 'Sin perfil').strip()
    photo_src = _build_photo_src(identity.get('photo_bytes'))

    return html.Div(
        className='app-navigation-user-card',
        children=[
            _build_user_avatar(
                name=name,
                photo_src=photo_src,
            ),
            html.Div(
                className='app-navigation-user-information',
                children=[
                    html.H4(
                        className='app-navigation-user-name',
                        children=name,
                    ),
                    html.P(
                        className='app-navigation-user-email',
                        children=email,
                    )
                    if email
                    else None,
                    html.Div(
                        className='app-navigation-user-profile',
                        children=[
                            html.I(className='bi bi-person-badge me-1'),
                            html.Span(profile),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_user_avatar(
    *,
    name: str,
    photo_src: str | None,
):
    if photo_src:
        return html.Img(
            className='app-navigation-user-avatar',
            src=photo_src,
            alt=name,
        )

    return html.Div(
        className='app-navigation-user-avatar app-navigation-user-avatar-fallback',
        children=_build_initials(name=name),
    )


def _build_master_projects_button() -> html.A:
    return html.A(
        href=ADA_PROJECTS_URL,
        target='_blank',
        rel='noopener noreferrer',
        className='app-navigation-master-link text-decoration-none',
        children=[
            html.Span(
                className='app-navigation-master-link-label',
                children=[
                    html.I(className='bi bi-grid-1x2-fill me-2'),
                    html.Span('Ir a proyecto ADA'),
                ],
            ),
            html.I(className='bi bi-box-arrow-up-right'),
        ],
    )


def _build_navigation_nodes(
    *,
    nodes: list[NavigationMenuNode],
    current_path: str | None,
) -> html.Div:
    if not nodes:
        return html.Div(
            className='app-navigation-empty text-muted small',
            children='No hay opciones de navegación disponibles.',
        )

    return html.Div(
        className='app-navigation-menu d-flex flex-column',
        children=[
            _build_node(
                node=node,
                current_path=current_path,
            )
            for node in nodes
        ],
    )


def _build_node(
    node: NavigationMenuNode,
    current_path: str | None,
) -> html.Div | None:
    if node.node_type == 'group' and node.group:
        return _build_group_node(
            group=node.group,
            children=node.children,
            current_path=current_path,
        )

    if node.node_type == 'link' and node.link:
        return _build_link_node(
            link=node.link,
            current_path=current_path,
            is_child=False,
        )

    return None


def _build_group_node(
    group: NavigationGroup,
    children: tuple[NavigationLink, ...],
    current_path: str | None,
) -> html.Div:
    is_open = NavigationService.group_has_active_child(
        children=children,
        current_path=current_path,
    )

    return html.Div(
        className='app-navigation-root-item app-navigation-group {0}'.format(
            'disabled' if not group.is_active else ''
        ),
        children=[
            html.Button(
                id=AppNavigationIds.build_group_toggle_id(group.group_id),
                type='button',
                className=_build_group_button_class_name(is_open=is_open),
                children=[
                    html.Span(
                        className='app-navigation-label d-flex align-items-center',
                        children=[
                            html.I(className=f'{group.icon} me-2') if group.icon else None,
                            html.Span(group.label),
                        ],
                    ),
                    html.I(
                        className='bi bi-chevron-down app-navigation-group-chevron',
                    ),
                ],
                disabled=not group.is_active,
            ),
            dbc.Collapse(
                id=AppNavigationIds.build_group_collapse_id(group.group_id),
                is_open=is_open,
                children=html.Div(
                    className='app-navigation-group-children d-flex flex-column',
                    children=[
                        _build_link_node(
                            link=child,
                            current_path=current_path,
                            is_child=True,
                        )
                        for child in children
                    ],
                ),
            ),
        ],
    )


def _build_link_node(
    link: NavigationLink,
    current_path: str | None,
    is_child: bool,
) -> html.A | html.Button:
    is_active = NavigationService.is_active_link(
        link=link,
        current_path=current_path,
    )

    link_child = html.Button(
        type='button',
        children=[
            html.I(className=f'{link.icon} me-2') if link.icon else None,
            html.Span(link.label),
        ],
        className=_build_link_button_class_name(
            is_active=is_active,
            is_child=is_child,
        ),
    )

    is_disabled = '' if link.is_active else 'disabled'
    if link.new_tab or link.link_type == 'external':
        return html.A(
            link_child,
            href=link.path,
            target='_blank' if link.new_tab else '_self',
            rel='noopener noreferrer',
            className='app-navigation-link-wrapper d-block text-decoration-none {0}'.format(
                is_disabled
            ),
        )

    return dcc.Link(
        link_child,
        href=link.path,
        target='_self',
        className='app-navigation-link-wrapper d-block text-decoration-none {0}'.format(
            is_disabled
        ),
        refresh=link.force_reload,
    )


def _build_link_button_class_name(
    is_active: bool,
    is_child: bool,
) -> str:
    class_names = [
        'app-navigation-button',
        'app-navigation-link',
    ]

    if is_child:
        class_names.append('app-navigation-child-link')
    else:
        class_names.append('app-navigation-root-link')

    if is_active:
        class_names.append('active-nav-link')

    return ' '.join(class_names)


def _build_group_button_class_name(
    is_open: bool,
) -> str:
    class_names = [
        'app-navigation-button',
        'app-navigation-group-button',
        'd-flex',
        'align-items-center',
        'justify-content-between',
    ]

    if is_open:
        class_names.append('app-navigation-group-button-open')

    return ' '.join(class_names)


def _build_photo_src(photo_bytes) -> str | None:
    if not photo_bytes:
        return '/assets/img/icons/account_user.svg'

    if isinstance(photo_bytes, str):
        value = photo_bytes.strip()

        if not value:
            return '/assets/img/icons/account_user.svg'

        if value.startswith('data:image/'):
            return value

        return f'data:image/jpeg;base64,{value}'

    if isinstance(photo_bytes, bytes):
        mime_type = _resolve_image_mime_type(photo_bytes)
        encoded = base64.b64encode(photo_bytes).decode('utf-8')
        return f'data:{mime_type};base64,{encoded}'

    return '/assets/img/icons/account_user.svg'


def _resolve_image_mime_type(photo_bytes: bytes) -> str:
    stripped = photo_bytes.lstrip()

    if stripped.startswith(b'<svg') or stripped.startswith(b'<?xml'):
        return 'image/svg+xml'

    if photo_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'

    if photo_bytes.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'

    if photo_bytes.startswith(b'GIF87a') or photo_bytes.startswith(b'GIF89a'):
        return 'image/gif'

    return 'image/jpeg'


def _build_initials(
    *,
    name: str,
) -> str:
    parts = [part.strip() for part in name.split() if part.strip()]

    if not parts:
        return 'U'

    if len(parts) == 1:
        return parts[0][:2].upper()

    return f'{parts[0][0]}{parts[1][0]}'.upper()
