"""Configuration of modal variants for time series data visualization.

This module defines a configuration for modal variants using the
`TimeSeriesVariantsData` class. The configuration specifies attributes
related to the appearance and behavior of modals, such as backdrop
type, centering, keyboard interaction, class names for styling, and
dimensions. This setup is designed to ensure consistent presentation
and customization of modals in time series data visualizations.

Attributes
----------
MODAL_VARIANTS : TimeSeriesVariantsData
    Configuration instance of `TimeSeriesVariantsData` with predefined
    settings for modal behavior and styling.
"""

from __future__ import annotations

from .models import TimeSeriesVariantsData

MODAL_VARIANTS: TimeSeriesVariantsData = TimeSeriesVariantsData(
    backdrop='static',
    centered=True,
    keyboard=False,
    close_button=False,
    header_class_name='modal-background',
    header_font_color_class_name='text-white',
    body_class_name='background-primary',
    body_font_color_class_name='font-custom-text-color',
    footer_class_name='modal-background',
    footer_font_color_class_name='text-white',
    width='80%',
    font_size_class_name='font-custom-text-size',
)
