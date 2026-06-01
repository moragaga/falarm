from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.shared.time.timestamps import parse_utc_datetime, to_santiago_display

DAY_LABELS = [
    'Lun',
    'Mar',
    'Mié',
    'Jue',
    'Vie',
    'Sáb',
    'Dom',
]


def build_user_session_page_snapshot(
    *,
    analytics_snapshot: dict[str, Any] | None,
) -> dict[str, Any]:
    captured_at = datetime.now(timezone.utc)
    source_snapshot = analytics_snapshot or {}

    artifacts = _as_dict(source_snapshot.get('artifacts'))

    snapshot_timestamp = _safe_str(source_snapshot.get('snapshot_timestamp'))

    return {
        'captured_at': captured_at.isoformat(),
        'captured_at_display': _format_datetime(
            value=captured_at,
        ),
        'source_snapshot_timestamp': snapshot_timestamp,
        'source_snapshot_timestamp_display': _format_datetime(
            value=_parse_datetime(snapshot_timestamp),
        )
        if snapshot_timestamp
        else 'Sin fecha',
        'window': _as_dict(source_snapshot.get('window')),
        'activity_items': _as_list(
            _as_dict(artifacts.get('activity_items')).get('items')
        ),
        'user_items': _as_list(
            _as_dict(artifacts.get('user_items')).get('items')
        ),
        'meta': {
            'snapshot_type': _safe_str(source_snapshot.get('snapshot_type')),
            'schema_version': source_snapshot.get('schema_version'),
            'activity_items_total': len(
                _as_list(_as_dict(artifacts.get('activity_items')).get('items'))
            ),
            'user_items_total': len(
                _as_list(_as_dict(artifacts.get('user_items')).get('items'))
            ),
        },
    }


def build_page_view(
    *,
    snapshot: dict[str, Any] | None,
    profile_filter: str | None,
    device_filter: str | None,
    resolution_filter: str | None,
    exclude_admin_values: list[str] | None,
    search_text: str | None,
    sort_order: str | None,
    page: int | None,
    page_size: int,
) -> dict[str, Any]:
    has_snapshot = bool(snapshot)
    snapshot = snapshot or {}

    items = _as_list(snapshot.get('activity_items'))

    filtered_items = _filter_activity_items(
        items=items,
        profile_filter=profile_filter,
        device_filter=device_filter,
        resolution_filter=resolution_filter,
        exclude_admin=(
            'exclude_admin' in (exclude_admin_values or [])
        ),
    )

    users = _build_user_summaries(items=filtered_items)

    users = _filter_users_by_search(
        users=users,
        search_text=search_text,
    )

    users = _sort_users(
        users=users,
        sort_order=sort_order,
    )

    total_items = len(users)
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    safe_page = max(1, min(page or 1, total_pages))

    start_index = (safe_page - 1) * page_size
    end_index = start_index + page_size

    return {
        'has_snapshot': has_snapshot,
        'kpis': _build_kpis(items=filtered_items),
        'weekly_comparison': _build_weekly_comparison(items=filtered_items),
        'summary': _build_summary(items=filtered_items),
        'device_resolution': _build_device_resolution(items=filtered_items),
        'users': users[start_index:end_index],
        'total_items': total_items,
        'total_pages': total_pages,
        'page': safe_page,
        'page_size': page_size,
        'has_previous': safe_page > 1,
        'has_next': safe_page < total_pages,
        'empty_by_filter': has_snapshot
        and total_items == 0
        and _has_active_filter(
            profile_filter=profile_filter,
            device_filter=device_filter,
            resolution_filter=resolution_filter,
            exclude_admin_values=exclude_admin_values,
            search_text=search_text,
        ),
    }


def get_total_pages_for_users(
    *,
    snapshot: dict[str, Any] | None,
    profile_filter: str | None,
    device_filter: str | None,
    resolution_filter: str | None,
    exclude_admin_values: list[str] | None,
    search_text: str | None,
    sort_order: str | None,
    page_size: int,
) -> int:
    view = build_page_view(
        snapshot=snapshot,
        profile_filter=profile_filter,
        device_filter=device_filter,
        resolution_filter=resolution_filter,
        exclude_admin_values=exclude_admin_values,
        search_text=search_text,
        sort_order=sort_order,
        page=1,
        page_size=page_size,
    )

    return int(view['total_pages'])


def get_next_page(
    *,
    current_page: int | None,
    direction: str,
    total_pages: int,
) -> int:
    page = current_page or 1

    if direction == 'previous':
        return max(1, page - 1)

    if direction == 'next':
        return min(total_pages, page + 1)

    return max(1, min(page, total_pages))


def build_dynamic_device_options(
    *,
    snapshot: dict[str, Any] | None,
) -> list[dict[str, str]]:
    items = _as_list((snapshot or {}).get('activity_items'))

    values = sorted(
        {
            _safe_str(item.get('device_category'))
            for item in items
            if _safe_str(item.get('device_category'))
        }
    )

    return [
        {
            'label': 'Todos',
            'value': 'all',
        },
        *[
            {
                'label': value,
                'value': value,
            }
            for value in values
        ],
    ]


def build_dynamic_resolution_options(
    *,
    snapshot: dict[str, Any] | None,
) -> list[dict[str, str]]:
    items = _as_list((snapshot or {}).get('activity_items'))

    values = sorted(
        {
            _safe_str(item.get('resolution_bucket'))
            for item in items
            if _safe_str(item.get('resolution_bucket'))
        }
    )

    return [
        {
            'label': 'Todas',
            'value': 'all',
        },
        *[
            {
                'label': value,
                'value': value,
            }
            for value in values
        ],
    ]


def _filter_activity_items(
    *,
    items: list[dict[str, Any]],
    profile_filter: str | None,
    device_filter: str | None,
    resolution_filter: str | None,
    exclude_admin: bool,
) -> list[dict[str, Any]]:
    result = []

    selected_profile = _safe_str(profile_filter) or 'all'
    selected_device = _safe_str(device_filter) or 'all'
    selected_resolution = _safe_str(resolution_filter) or 'all'

    for item in items:
        if not isinstance(item, dict):
            continue

        if exclude_admin and bool(item.get('is_administrator')):
            continue

        if selected_profile != 'all' and _safe_str(item.get('profile')) != selected_profile:
            continue

        if selected_device != 'all' and _safe_str(item.get('device_category')) != selected_device:
            continue

        if (
            selected_resolution != 'all'
            and _safe_str(item.get('resolution_bucket')) != selected_resolution
        ):
            continue

        result.append(item)

    return result


def _build_kpis(
    *,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    current = _scope_items(
        items=items,
        scope='current',
    )
    previous = _scope_items(
        items=items,
        scope='previous',
    )

    current_sessions = _sum_int(current, 'sessions')
    previous_sessions = _sum_int(previous, 'sessions')

    current_users = _count_unique(current, 'user_identity_key')
    previous_users = _count_unique(previous, 'user_identity_key')

    current_active_seconds = _sum_int(current, 'active_seconds')
    previous_active_seconds = _sum_int(previous, 'active_seconds')

    current_avg_session = _safe_div_int(
        numerator=current_active_seconds,
        denominator=current_sessions,
    )
    previous_avg_session = _safe_div_int(
        numerator=previous_active_seconds,
        denominator=previous_sessions,
    )

    current_recurring_pct = _recurring_users_pct(items=current)
    previous_recurring_pct = _recurring_users_pct(items=previous)

    return {
        'sessions_total': _metric_payload(
            current=current_sessions,
            previous=previous_sessions,
        ),
        'unique_users': _metric_payload(
            current=current_users,
            previous=previous_users,
        ),
        'avg_session_seconds': _metric_payload(
            current=current_avg_session,
            previous=previous_avg_session,
            formatter=_format_duration,
        ),
        'total_active_seconds': _metric_payload(
            current=current_active_seconds,
            previous=previous_active_seconds,
            formatter=_format_duration,
        ),
        'recurring_users_pct': _metric_payload(
            current=current_recurring_pct,
            previous=previous_recurring_pct,
            formatter=lambda value: f'{value:.1f}%',
            delta_suffix=' p.p.',
        ),
    }


def _build_weekly_comparison(
    *,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        'x_labels': DAY_LABELS,
        'series': [
            {
                'key': 'sessions_previous',
                'label': 'Sesiones semana anterior',
                'dash': 'dash',
                'values': _daily_values(
                    items=items,
                    scope='previous',
                    metric='sessions',
                ),
            },
            {
                'key': 'sessions_current',
                'label': 'Sesiones semana actual',
                'dash': 'solid',
                'values': _daily_values(
                    items=items,
                    scope='current',
                    metric='sessions',
                ),
            },
            {
                'key': 'users_previous',
                'label': 'Usuarios semana anterior',
                'dash': 'dash',
                'values': _daily_user_values(
                    items=items,
                    scope='previous',
                ),
            },
            {
                'key': 'users_current',
                'label': 'Usuarios semana actual',
                'dash': 'solid',
                'values': _daily_user_values(
                    items=items,
                    scope='current',
                ),
            },
        ],
    }


def _build_summary(
    *,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    current = _scope_items(
        items=items,
        scope='current',
    )

    return {
        'most_active_day': _top_day(items=current),
        'top_profile': _top_dimension(
            items=current,
            column='profile',
        ),
        'top_resolution': _top_dimension(
            items=current,
            column='resolution_bucket',
        ),
        'top_device': _top_dimension(
            items=current,
            column='device_category',
        ),
        'peak_usage_range': _top_dimension(
            items=current,
            column='two_hour_bucket_label',
        ),
    }


def _build_device_resolution(
    *,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    current = _scope_items(
        items=items,
        scope='current',
    )

    return {
        'devices': _rank_dimension(
            items=current,
            column='device_category',
            limit=4,
        ),
        'resolutions': _rank_dimension(
            items=current,
            column='resolution_bucket',
            limit=6,
        ),
    }


def _build_user_summaries(
    *,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}

    for item in items:
        user_key = _safe_str(item.get('user_identity_key'))

        if not user_key:
            continue

        grouped.setdefault(user_key, []).append(item)

    users = []

    for user_identity_key, user_items in grouped.items():
        sessions = _sum_int(user_items, 'sessions')
        active_seconds = _sum_int(user_items, 'active_seconds')

        last_item = max(
            user_items,
            key=lambda item: _parse_datetime(
                _safe_str(item.get('last_seen_at_utc'))
            )
            or datetime.min.replace(tzinfo=timezone.utc),
        )

        users.append(
            {
                'user_identity_key': user_identity_key,
                'user_key': _first_value(user_items, 'user_key'),
                'email': _first_value(user_items, 'email'),
                'display_name': _first_value(user_items, 'display_name')
                or _first_value(user_items, 'email')
                or user_identity_key,
                'profile': _safe_str(last_item.get('profile')),
                'is_administrator': any(bool(item.get('is_administrator')) for item in user_items),
                'sessions': sessions,
                'views': _sum_int(user_items, 'views'),
                'active_seconds': active_seconds,
                'active_time_label': _format_duration(active_seconds),
                'avg_session_seconds': _safe_div_int(
                    numerator=active_seconds,
                    denominator=sessions,
                ),
                'avg_session_label': _format_duration(
                    _safe_div_int(
                        numerator=active_seconds,
                        denominator=sessions,
                    )
                ),
                'last_seen_at_utc': _safe_str(last_item.get('last_seen_at_utc')),
                'last_seen_display': _convert_utc_to_santiago(value=last_item.get('last_seen_at_utc')),
                'primary_device': _top_dimension_value(
                    items=user_items,
                    column='device_category',
                ),
                'primary_resolution': _top_dimension_value(
                    items=user_items,
                    column='resolution_bucket',
                ),
            }
        )

    return users


def _filter_users_by_search(
    *,
    users: list[dict[str, Any]],
    search_text: str | None,
) -> list[dict[str, Any]]:
    query = _safe_str(search_text).lower()

    if not query:
        return users

    return [
        user
        for user in users
        if query in _safe_str(user.get('display_name')).lower()
        or query in _safe_str(user.get('email')).lower()
        or query in _safe_str(user.get('profile')).lower()
    ]


def _sort_users(
    *,
    users: list[dict[str, Any]],
    sort_order: str | None,
) -> list[dict[str, Any]]:
    value = _safe_str(sort_order) or 'sessions_desc'

    if value == 'active_time_desc':
        return sorted(
            users,
            key=lambda user: (
                _safe_int(user.get('active_seconds')),
                _safe_int(user.get('sessions')),
            ),
            reverse=True,
        )

    if value == 'last_seen_desc':
        return sorted(
            users,
            key=lambda user: _parse_datetime(_safe_str(user.get('last_seen_at_utc')))
            or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

    if value == 'name_asc':
        return sorted(
            users,
            key=lambda user: _safe_str(user.get('display_name')).lower(),
        )

    return sorted(
        users,
        key=lambda user: (
            _safe_int(user.get('sessions')),
            _safe_int(user.get('active_seconds')),
        ),
        reverse=True,
    )


def _metric_payload(
    *,
    current: int | float,
    previous: int | float,
    formatter=None,
    delta_suffix: str = '%',
) -> dict[str, Any]:
    current_value = current
    previous_value = previous

    delta_abs = current_value - previous_value

    if previous_value == 0:
        delta_pct = None
    else:
        delta_pct = round(delta_abs / previous_value * 100, 1)

    format_value = formatter or _format_number

    if delta_suffix == ' p.p.':
        delta_label = f'{delta_abs:+.1f}{delta_suffix}'
    elif delta_pct is None:
        delta_label = 'Sin comparación'
    else:
        delta_label = f'{delta_pct:+.1f}% vs semana anterior'

    return {
        'current': current_value,
        'previous': previous_value,
        'delta_abs': delta_abs,
        'delta_pct': delta_pct,
        'current_label': format_value(current_value),
        'previous_label': format_value(previous_value),
        'delta_label': delta_label,
    }


def _scope_items(
    *,
    items: list[dict[str, Any]],
    scope: str,
) -> list[dict[str, Any]]:
    return [
        item
        for item in items
        if _safe_str(item.get('week_scope')) == scope
    ]


def _daily_values(
    *,
    items: list[dict[str, Any]],
    scope: str,
    metric: str,
) -> list[int]:
    values = [0] * 7

    for item in _scope_items(items=items, scope=scope):
        day_index = _optional_int(item.get('day_index'))

        if day_index is None or day_index < 0 or day_index > 6:
            continue

        values[day_index] += _safe_int(item.get(metric))

    return values


def _daily_user_values(
    *,
    items: list[dict[str, Any]],
    scope: str,
) -> list[int]:
    values = []

    scoped = _scope_items(
        items=items,
        scope=scope,
    )

    for day_index in range(7):
        users = {
            _safe_str(item.get('user_identity_key'))
            for item in scoped
            if _optional_int(item.get('day_index')) == day_index
            and _safe_str(item.get('user_identity_key'))
        }

        values.append(len(users))

    return values


def _top_day(
    *,
    items: list[dict[str, Any]],
) -> dict[str, str]:
    values = _daily_values(
        items=items,
        scope='current',
        metric='sessions',
    )

    if not values or max(values) == 0:
        return {
            'label': 'Día con mayor actividad',
            'value': 'Sin datos',
        }

    index = values.index(max(values))

    text = 'sesión' if values[index] == 1 else 'sesiones'

    return {
        'label': 'Día con mayor actividad',
        'value': f'{DAY_LABELS[index]} · {values[index]} {text}',
    }


def _top_dimension(
    *,
    items: list[dict[str, Any]],
    column: str,
) -> dict[str, str]:
    ranked = _rank_dimension(
        items=items,
        column=column,
        limit=1,
    )

    if not ranked:
        return {
            'label': column,
            'value': 'Sin datos',
        }

    item = ranked[0]

    return {
        'label': column,
        'value': f'{item["label"]} · {item["pct_label"]}',
    }


def _rank_dimension(
    *,
    items: list[dict[str, Any]],
    column: str,
    limit: int,
) -> list[dict[str, Any]]:
    total = _sum_int(items, 'sessions')

    grouped: dict[str, int] = {}

    for item in items:
        value = _safe_str(item.get(column)) or 'Sin datos'
        grouped[value] = grouped.get(value, 0) + _safe_int(item.get('sessions'))

    ranked = sorted(
        grouped.items(),
        key=lambda pair: pair[1],
        reverse=True,
    )[:limit]

    result = []

    for label, value in ranked:
        pct = round(value / total * 100, 1) if total else 0

        result.append(
            {
                'label': label,
                'value': value,
                'value_label': _format_number(value),
                'pct': pct,
                'pct_label': f'{pct:.1f}%',
            }
        )

    return result


def _top_dimension_value(
    *,
    items: list[dict[str, Any]],
    column: str,
) -> str:
    ranked = _rank_dimension(
        items=items,
        column=column,
        limit=1,
    )

    if not ranked:
        return ''

    return ranked[0]['label']


def _recurring_users_pct(
    *,
    items: list[dict[str, Any]],
) -> float:
    grouped: dict[str, int] = {}

    for item in items:
        user_key = _safe_str(item.get('user_identity_key'))

        if not user_key:
            continue

        grouped[user_key] = grouped.get(user_key, 0) + _safe_int(item.get('sessions'))

    if not grouped:
        return 0.0

    recurring = sum(1 for sessions in grouped.values() if sessions > 1)

    return round(recurring / len(grouped) * 100, 1)


def _sum_int(
    items: list[dict[str, Any]],
    column: str,
) -> int:
    return sum(_safe_int(item.get(column)) for item in items)


def _count_unique(
    items: list[dict[str, Any]],
    column: str,
) -> int:
    return len(
        {
            _safe_str(item.get(column))
            for item in items
            if _safe_str(item.get(column))
        }
    )


def _first_value(
    items: list[dict[str, Any]],
    column: str,
) -> str:
    for item in items:
        value = _safe_str(item.get(column))

        if value:
            return value

    return ''


def _has_active_filter(
    *,
    profile_filter: str | None,
    device_filter: str | None,
    resolution_filter: str | None,
    exclude_admin_values: list[str] | None,
    search_text: str | None,
) -> bool:
    return (
        (_safe_str(profile_filter) or 'all') != 'all'
        or (_safe_str(device_filter) or 'all') != 'all'
        or (_safe_str(resolution_filter) or 'all') != 'all'
        or bool(exclude_admin_values)
        or bool(_safe_str(search_text))
    )


def _format_number(value: int | float) -> str:
    try:
        return f'{int(value):,}'.replace(',', '.')
    except Exception:
        return '0'


def _format_duration(seconds: int | float | None) -> str:
    if seconds is None:
        return '0s'

    safe_seconds = max(0, int(seconds))

    hours = safe_seconds // 3600
    minutes = (safe_seconds % 3600) // 60
    remaining_seconds = safe_seconds % 60

    if hours > 0:
        return f'{hours}h {minutes:02d}m'

    if minutes > 0:
        return f'{minutes}m {remaining_seconds:02d}s'

    return f'{remaining_seconds}s'


def _safe_div_int(
    *,
    numerator: int,
    denominator: int,
) -> int:
    if denominator <= 0:
        return 0

    return int(numerator / denominator)


def _parse_datetime(value: str) -> datetime | None:
    text = _safe_str(value)

    if not text:
        return None

    try:
        parsed = datetime.fromisoformat(text.replace('Z', '+00:00'))

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    except Exception:
        return None


def _format_datetime(
    *,
    value: datetime | None,
) -> str:
    if value is None:
        return 'Sin fecha'

    try:
        return value.astimezone().strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return 'Sin fecha'

def _convert_utc_to_santiago(
    *,
    value: datetime | None,
) -> str:
    timestamp = parse_utc_datetime(value=value)
    if timestamp is None:
        return 'Sin fecha'

    return to_santiago_display(dt=timestamp)


def _optional_int(value: Any) -> int | None:
    if value is None or value == '':
        return None

    try:
        return int(float(value))
    except Exception:
        return None


def _safe_int(value: Any) -> int:
    if value is None or value == '':
        return 0

    try:
        return int(float(value))
    except Exception:
        return 0


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []