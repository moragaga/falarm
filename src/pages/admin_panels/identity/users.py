from __future__ import annotations

import dash

from src.features.configuration.admin_panels.identity.users.layout import (
    build_identity_users_admin_layout,
)

dash.register_page(
    __name__,
    path='/admin/identity/users',
    name='Usuarios',
)


def layout():
    return build_identity_users_admin_layout()
