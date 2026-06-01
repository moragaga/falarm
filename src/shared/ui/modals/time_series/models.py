"""
TimeSeriesModalDetailData and TimeSeriesVariantsData classes.

This module contains frozen dataclasses that define the structure and
characteristics of time series modal details and its variants. These
dataclasses are used for defining specific configurations and properties
associated with the time series modal and its related visual or stylistic
attributes.
"""

from __future__ import annotations

from dataclasses import dataclass

from dash.development.base_component import Component


@dataclass(frozen=True)
class TimeSeriesModalDetailData:
    title: str
    last_updated: str
    graph: Component


@dataclass(frozen=True)
class TimeSeriesVariantsData:
    backdrop: str
    centered: bool
    keyboard: bool
    close_button: bool
    header_class_name: str
    header_font_color_class_name: str
    body_class_name: str
    body_font_color_class_name: str
    footer_class_name: str
    footer_font_color_class_name: str
    width: str
    font_size_class_name: str
