"""
Builds an AdminSchema object for configuring navigation links.

This function generates an AdminSchema instance for defining navigation
link configurations in an administration system. The schema specifies
various fields such as link ID, label, path, parent group, icon, order,
visibility, and access control profiles.

Parameters
----------
parent_group_options : tuple[FieldOption, ...]
    A tuple of FieldOption objects representing the selectable group
    options for the parent group field.

Returns
-------
AdminSchema
    An AdminSchema object that contains the configuration for navigation
    links.
"""

from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, FieldOption, Profile


def build_navigation_links_admin_schema(
    *,
    parent_group_options: tuple[FieldOption, ...],
) -> AdminSchema:
    return AdminSchema(
        key='navigation_links',
        title='Administración de links de navegación',
        fields=(
            FieldDefinition(
                name='link_id',
                label='ID',
                field_type='text',
                required=True,
                editable=False,
                help_text='Identificador técnico automático.',
            ),
            FieldDefinition(
                name='label',
                label='Etiqueta',
                field_type='text',
                required=True,
                help_text='Texto visible en el menú.',
            ),
            FieldDefinition(
                name='path',
                label='Ruta / URL',
                field_type='text',
                required=True,
                help_text='Ruta de la página. Ejemplo: /admin/navigation/links',
            ),
            FieldDefinition(
                name='link_type',
                label='Tipo de link',
                field_type='select',
                options=(
                    'internal',
                    'external',
                ),
                default_value='internal',
                required=True,
                help_text='Link pertenece a esta página o a otra.',
            ),
            FieldDefinition(
                name='parent_group_id',
                label='Grupo padre',
                field_type='select',
                required=False,
                default_value='',
                options=parent_group_options,
                help_text='Seleccionar un grupo o dejar en Sin grupo para mostrar directo en raíz.',
            ),
            FieldDefinition(
                name='icon_source',
                label='Tipo de icono',
                field_type='select',
                options=(
                    'bootstrap',
                    'asset',
                ),
                default_value='bootstrap',
                required=False,
                help_text='Fuente de iconos',
            ),
            FieldDefinition(
                name='icon',
                label='Icono',
                field_type='text',
                required=False,
                help_text='Clase de Bootstrap Icons. Ejemplo: bi bi-list o nombre del archivo',
            ),
            FieldDefinition(
                name='order',
                label='Orden',
                field_type='number',
                required=True,
                default_value=0,
                help_text=(
                    'Si no tiene grupo padre, ordena el link en el menú principal. '
                    'Si tiene grupo padre, ordena el link dentro del grupo.'
                ),
            ),
            FieldDefinition(
                name='new_tab',
                label='Abrir en nueva pestaña',
                field_type='boolean',
                required=True,
                default_value=False,
            ),
            FieldDefinition(
                name='visible_in_menu',
                label='Visible en menú',
                field_type='boolean',
                required=True,
                default_value=True,
            ),
            FieldDefinition(
                name='is_active',
                label='Activo',
                field_type='boolean',
                required=True,
                default_value=True,
            ),
            FieldDefinition(
                name='force_reload',
                label='Forzar recarga',
                field_type='boolean',
                required=True,
                default_value=False,
            ),
            FieldDefinition(
                name='allow_profiles',
                label='Perfiles',
                field_type='semicolon_list',
                required=False,
                editable=True,
                options=Profile.values(),
                default_value='',
                help_text=(
                    'Separar perfiles con ;. '
                    'Si el link tiene grupo padre y este campo queda vacío, heredará los perfiles del grupo.'
                ),
            ),
        ),
    )
