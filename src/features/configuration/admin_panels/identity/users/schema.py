"""
Configuration schema for managing user administration.

Provides a predefined schema for handling user-related configurations in an admin
interface. This schema defines the fields required for managing identities, including
technical identifiers, user details, and operational profiles. The schema is initialized
with field definitions and default values for specific configurations.
"""

from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, Profile

IDENTITY_USERS_ADMIN_SCHEMA = AdminSchema(
    key='identity_users',
    title='Administración de usuarios',
    fields=(
        FieldDefinition(
            name='user_id',
            label='ID Usuario',
            field_type='text',
            required=True,
            editable=False,
            help_text='Identificador técnico automático del usuario.',
        ),
        FieldDefinition(
            name='name',
            label='Nombre',
            field_type='text',
            required=True,
            editable=True,
            help_text='Nombre visible del usuario.',
        ),
        FieldDefinition(
            name='email',
            label='Email',
            field_type='text',
            required=True,
            editable=True,
            help_text='Correo usado para resolver la identidad del usuario.',
        ),
        FieldDefinition(
            name='profile',
            label='Perfil',
            field_type='select',
            required=True,
            editable=True,
            options=Profile.assignable_values(),
            default_value=Profile.default_assignable(),
            help_text='Perfil operativo del usuario dentro de la aplicación.',
        ),
        FieldDefinition(
            name='is_active',
            label='Activo',
            field_type='boolean',
            required=True,
            editable=True,
            default_value=True,
            help_text='Si está desactivado, el usuario no podrá usar su perfil configurado.',
        ),
    ),
)
