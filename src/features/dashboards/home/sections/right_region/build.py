"""
Constructs and returns the right region section for the "Aguas Abajo" feature.

This function organizes and structures the right region section of the UI by
building cards for "stc" and "plf" components. It incorporates pre-defined
builders for rows and ready flags within these components while applying the
appropriate styling and identifiers.

Returns
-------
Any
    A structured shell for the right region section, containing two display cards
    with their respective components and children elements.
"""

from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.display_card import build_display_card



def build_right_region_section():
    return build_section_shell(
        title='RIGHT REGION',
        content_id='flotacion-selectiva-right-region-section',
        children=[
            build_display_card(
                uuid='right-region-card-1',
                name='right region 1',
                class_name_component='background-secondary h-100 d-flex',
                class_name_wrapper='d-flex flex-fill p-0 m-0',
                show_identifier=True,
                show_definition=True,
                children=['Integrar contenido desde el builder del proyecto especifico (right region)'],
            ),
        ],
    )
