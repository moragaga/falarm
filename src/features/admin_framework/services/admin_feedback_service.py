"""
Module for building customized feedback notifications for administrative operations.

This module provides predefined methods to construct specific types of feedback
notifications for success and error scenarios. These notifications are typically
used in user interfaces to convey the status of an operation in a consistent
and visually recognizable format.
"""

from __future__ import annotations

from src.shared.ui.feedback.notifications.toast import build_toast


class AdminFeedbackService:
    @staticmethod
    def build_success(message: str):
        return build_toast(
            header='Guardado exitoso',
            message=message,
            icon='success',
        )

    @staticmethod
    def build_error(message: str | list[str]):
        return build_toast(
            header='Error',
            message=message,
            icon='danger',
        )

    @staticmethod
    def build_warning(message: str | list[str]):
        return build_toast(
            header='Advertencia',
            message=message,
            icon='warning',
        )
