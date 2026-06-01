"""
A builder function for constructing the information section in the application UI.

The function integrates the application information content and ready status flag
into an application information shell component, creating a cohesive information
section for the user interface.
"""

from __future__ import annotations

from src.shared.ui.app_information_shell.app_information_shell import build_app_information_shell


def build_information_section():
    return build_app_information_shell(
        content=['Integrar contenido desde el builder del proyecto especifico (información)']
    )
