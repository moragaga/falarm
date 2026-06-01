"""
Builds and constructs the header section of the application interface.

This module defines the function responsible for assembling the header section
using reusable components. The header section includes global indicators,
status indicators, and informational notifications that are dynamically
generated and organized.

Functions
---------
build_header_section
    Constructs the application header section by aggregating components
    such as global indicators, status content, and information notifications.
"""

from __future__ import annotations

from src.shared.ui.app_header_shell.app_header_shell import build_app_header_shell



def build_header_section():
    return build_app_header_shell(
        global_indicator_content=['Integrar contenido desde el builder del proyecto especifico (indicador global) '],
        status_content=['Integrar contenido desde el builder del proyecto especifico (estado)'],
        information_content=['Integrar contenido desde el builder del proyecto especifico (información)'],
    )
