"""
Resolves and returns the appropriate display component or value based on the
given status and value.

This function helps determine the correct output to display based on the
input parameters `value` and `status`. It handles different scenarios for
missing, invalid, or valid statuses and ensures proper logging for invalid
status cases.

Parameters
----------
value : str or None, optional
    The string value to display when the status is valid. Defaults to None.
status : str or None, optional
    The status indicating the state of the value. It can be one of the
    following: 'missing', 'invalid', or 'ok'. Defaults to None.

Returns
-------
str or Component
    If the status is 'ok', the function returns the input `value`. If the
    status is 'missing' or 'invalid', it returns an alerting icon built using
    `build_alerting_icon`. If the status is None or an unrecognized value, it
    returns an alerting icon indicating invalid data.
"""

from __future__ import annotations

from dash.development.base_component import Component

from src.shared.runtime.logging.debug import debug_log

from .invalid_value_icon import build_alerting_icon


def resolve_latest_value_display(
    value: str | None = None,
    status: str | None = None,
) -> str | Component:
    if status is None:
        return build_alerting_icon(invalid_type='invalid_data')

    statuses = {
        'missing': build_alerting_icon(invalid_type='not_mapped'),
        'invalid': build_alerting_icon(invalid_type='invalid_data'),
        'ok': value,
    }

    data = statuses.get(status)
    if data is None:
        debug_log(f'Invalid status: {status}')
        return build_alerting_icon(invalid_type='invalid_data')

    return data
