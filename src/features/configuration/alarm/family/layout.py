from __future__ import annotations

from src.features.admin_framework.services import build_admin_layout

from .definition import ALARM_FAMILY_ADMIN_DEFINITION


def build_alarm_family_admin_layout():
    return build_admin_layout(ALARM_FAMILY_ADMIN_DEFINITION)
