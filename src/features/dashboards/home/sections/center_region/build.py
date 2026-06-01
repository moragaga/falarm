"""
Builds the `center-region-section` for the Planta Molibdeno interface.

This function constructs a section that acts as the central component of the
Planta Molibdeno user interface. It assembles a layout structure by including
multiple rows of content and defining their properties.

Returns
-------
Any
    The constructed 'center-region-section' object containing the
    specified layout and its children components.
"""

from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.display_card import build_display_card



def build_center_region_section():
    return build_section_shell(
        title='CENTER REGION',
        content_id='flotacion-selectiva-center-region-section',
        children=[
            build_display_card(
                uuid='center-region-main-card',
                name='Center Region',
                class_name_component='background-primary h-100 d-flex',
                class_name_wrapper='d-flex flex-fill p-0 m-0',
                show_identifier=False,
                show_definition=True,
                children=[
                    'Integrar contenido desde el builder del proyecto especifico (center region)'
                ],
            )
        ],
    )
