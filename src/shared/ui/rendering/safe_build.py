"""Utility functions for safely building and managing UI components.

This module provides functionality to build individual or multiple UI
components with error handling. It ensures that any errors during the
building process are gracefully handled by returning a fallback
error component instead of raising an exception. Additionally, it
filters out unwanted parameters from builder keyword arguments, as
defined in the component definitions.

Functions
---------
build_component_safely
build_components_safely
"""

from __future__ import annotations

import traceback

from dash.development.base_component import Component

from src.shared.ui.display.error_component import build_error_component
from src.shared.ui.rendering.kpis.models import KpiBuildDefinition


def build_component_safely(
    *,
    definition: KpiBuildDefinition,
    **builder_kwargs,
) -> Component:
    try:
        return definition.builder(**builder_kwargs)
    except Exception as e:
        print(f'[ERROR] slot={definition.slot_name} error={e}')
        traceback.print_exc()
        return build_error_component(ui_size=definition.ui_size)


def build_components_safely(
    *,
    definitions: list[KpiBuildDefinition],
    **builder_kwargs,
) -> list[Component]:
    components: list[Component] = []
    for definition in definitions:
        builder_kwargs_tmp = _exclude_parameters(
            exclude_parameters=definition.exclude_parameters, builder_kwargs=builder_kwargs
        )

        component = build_component_safely(definition=definition, **builder_kwargs_tmp)
        if definition.explicit_list:
            components.extend(component)
            continue
        components.append(component)
    return components


def _exclude_parameters(
    exclude_parameters: list[str],
    builder_kwargs: dict,
):
    builder_kwargs_tmp = dict(builder_kwargs).copy()
    if exclude_parameters is not None:
        for parameter in exclude_parameters:
            builder_kwargs_tmp.pop(parameter, None)
    return builder_kwargs_tmp
