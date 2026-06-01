from __future__ import annotations

from src.features.admin_framework.services import build_admin_layout

from .definition import ALARM_TOOLS_ADMIN_DEFINITION


def build_alarm_tools_admin_layout():
    return build_admin_layout(ALARM_TOOLS_ADMIN_DEFINITION)
