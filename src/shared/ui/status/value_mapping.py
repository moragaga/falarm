"""
A utility function to map the latest values for display in a specified format.

This function processes a dictionary of data entries, extracting and transforming
the latest values using the `resolve_latest_value_display` function. The resulting
dictionary maps keys from the input to the transformed display-ready values.

Parameters
----------
data : dict[str, dict]
    A dictionary where keys are strings and values are dictionaries containing
    data to be processed for display.

Returns
-------
dict[str, str | Component]
    A dictionary mapping the input keys to their corresponding display-ready values,
    which may either be a string or a `Component` object.
"""

from __future__ import annotations

from dash.development.base_component import Component

from .latest_value_display import resolve_latest_value_display


def map_latest_values_for_display(
    *,
    data: dict[str, dict],
) -> dict[str, str | Component]:
    values: dict[str, str | Component] = {}

    for key, value in data.items():
        values[key] = resolve_latest_value_display(**value)

    return values
