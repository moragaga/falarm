"""
Builds the left region section of the UI dashboard.

This function constructs a specific section of the dashboard labeled "AGUAS ARRIBA."
The section is composed of two display cards: one for "Flotación Colectiva" and another
for "Tendencias Courier." Both cards include dynamically generated content that is
specific to their respective contexts.

Returns
-------
SectionShell
    The constructed section shell containing the left region elements.
"""

from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.display_card import build_display_card


def build_left_region_section():
    return build_section_shell(
        title='LEFT REGION',
        content_id='flotacion-selectiva-left-region-section',
        children=[
            build_display_card(
                uuid='left-region-card-1',
                name='Left region 1',
                class_name_component='background-secondary h-100 d-flex',
                class_name_wrapper='d-flex flex-fill p-0 m-0',
                show_identifier=True,
                show_definition=True,
                children=['Integrar contenido desde el builder del proyecto especifico (left region)'],
            ),
        ],
    )
