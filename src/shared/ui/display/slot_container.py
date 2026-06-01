"""
Provides functions to construct reusable HTML components for a Dash application.

This module contains functions that facilitate the creation of customized
HTML components using Dash's HTML library. It is designed to simplify the
process of defining standardized containers and markers for various UI
elements.

Functions:
- build_slot_container: Creates a customizable HTML container with a specified ID and class.
- build_slot_ready_flag_container: Creates a hidden HTML container used as a marker with a data-ready attribute.
"""

from __future__ import annotations

from dash import html


def build_slot_container(
    component_id: str,
    class_name: str,
) -> html.Div:
    return html.Div(
        id=component_id,
        className=class_name,
    )


def build_slot_ready_flag_container(id_flag: str):
    return html.Div(
        id=id_flag,
        className='d-none',
        **{'data-ready': 'false'},
    )
