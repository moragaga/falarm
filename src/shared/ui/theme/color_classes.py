"""
This module contains functions to resolve color classes based on semantic
color values or predefined mappings. It provides utilities for converting
semantic or string-based color inputs into class name strings.

Functions
---------
resolve_color_class : Converts a semantic color or string value into a
    type-based color class name.
resolve_h2s_color_class : Resolves specific numeric color codes into H2S
    color class names.
"""

from __future__ import annotations

from typing import Literal

TypeColor = Literal['background', 'text', 'border']
SemanticColor = Literal['red', 'yellow', 'blue', '1', '2', '3']


def resolve_color_class(value: SemanticColor | str, type_color: TypeColor = 'text') -> str:
    if not isinstance(value, str):
        return ''

    normalized_value = str(value).strip().lower()

    semantic_to_code = {'red': '1', 'yellow': '2', 'blue': '3'}

    if value in semantic_to_code.keys():
        normalized_value = semantic_to_code.get(normalized_value)

    colors = {
        '1': f'{type_color}-color-red',
        '2': f'{type_color}-color-yellow',
        '3': f'{type_color}-color-blue',
    }

    return colors.get(normalized_value, '')


def resolve_h2s_color_class(value: str) -> str:
    colors = {
        '1': 'h2s-danger',
        '2': 'h2s-warning',
    }
    return colors.get(value, 'h2s-normal')
