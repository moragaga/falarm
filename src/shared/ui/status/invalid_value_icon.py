"""
This module provides functionality to generate alerting icons for specified invalid data types.

The module uses Dash's HTML components to generate an image component that corresponds
to a specific invalid data type.
"""

from __future__ import annotations

from typing import Literal

from dash import html

InvalidType = Literal['invalid_data', 'not_mapped', 'empty_data']


def build_alerting_icon(invalid_type: InvalidType) -> html.Img:
    return html.Img(
        src=f'assets/img/icons/{invalid_type}.svg', className='img-fluid invalid-value-icon'
    )
