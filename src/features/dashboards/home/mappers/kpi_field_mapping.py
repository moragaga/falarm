"""
Maps fields to KPI values based on a provided field mapping dictionary.

Given a field mapping dictionary that associates field names with KPI keys,
this function creates and returns a new dictionary where each field name
is mapped to the corresponding value retrieved from the provided KPI
dictionary.

Parameters
----------
field_mapping : dict[str, str]
    A dictionary where each key is a field name and the associated value is
    a KPI key to retrieve its value from the `kpis` dictionary.
kpis : dict
    A dictionary containing KPI data, where the keys are KPI keys and the
    values are the corresponding KPI values.

Returns
-------
dict[str, object]
    A dictionary where each key is a field name from `field_mapping` and
    the associated value is the corresponding KPI value from the `kpis`
    dictionary.
"""

from __future__ import annotations


def hydrate_field_mapping(
    *,
    field_mapping: dict[str, str],
    kpis: dict,
) -> dict[str, object]:
    mapping: dict[str, object] = {}

    for field, kpi_key in field_mapping.items():
        mapping[field] = kpis.get(kpi_key)

    return mapping
