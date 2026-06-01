"""A module containing a dataclass for defining alarm shell configuration.

This module provides a frozen dataclass for describing the configuration of an
alarm shell system, including attributes for setting the alarm intervals and
enabling or disabling the display of alarms.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlarmShellDefinition:
    alarms_interval_ms: int
    show_alarms: bool = True
