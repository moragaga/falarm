from __future__ import annotations

PAGE_SIZE = 7

DEFAULT_PROFILE_FILTER = 'all'
DEFAULT_DEVICE_FILTER = 'all'
DEFAULT_RESOLUTION_FILTER = 'all'
DEFAULT_SORT_ORDER = 'sessions_desc'

EXCLUDE_ADMIN_VALUE = 'exclude_admin'

PROFILE_OPTIONS = [
    {
        'label': 'Todos',
        'value': 'all',
    },
    {
        'label': 'Visualizador',
        'value': 'Visualizador',
    },
    {
        'label': 'Analista',
        'value': 'Analista',
    },
    {
        'label': 'Gestionador',
        'value': 'Gestionador',
    },
]

DEFAULT_DEVICE_OPTIONS = [
    {
        'label': 'Todos',
        'value': 'all',
    },
]

DEFAULT_RESOLUTION_OPTIONS = [
    {
        'label': 'Todas',
        'value': 'all',
    },
]

SORT_OPTIONS = [
    {
        'label': 'Más sesiones',
        'value': 'sessions_desc',
    },
    {
        'label': 'Más tiempo visualizado',
        'value': 'active_time_desc',
    },
    {
        'label': 'Último acceso',
        'value': 'last_seen_desc',
    },
    {
        'label': 'Nombre A-Z',
        'value': 'name_asc',
    },
]