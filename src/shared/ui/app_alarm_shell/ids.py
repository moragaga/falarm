"""
Defines constants for representing various alarm shell identifiers.

This module provides string constants that represent the identifiers
used in the alarm shell system. These identifiers are used to refer
to specific configurations or components of the alarm shell, such as
panels and stores.
"""

from __future__ import annotations


class AlarmShellIds:
    INTERVAL_ALARMS = 'alarm-shell-interval-alarm-panel'

    STORE_ALARM_RUNTIME_STORE = 'alarm-shell-runtime-store'
    STORE_ALARM_RESUME_STORE = 'alarm-shell-resume-store'
    STORE_ALARM_REFRESH_LOCK = 'alarm-shell-refresh-lock-store'
    STORE_ALARM_REFRESH_SIGNAL = 'alarm-shell-refresh-signal-store'
