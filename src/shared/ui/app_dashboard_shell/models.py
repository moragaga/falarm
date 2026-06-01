"""
Defines a dataclass for representing the configuration of a dashboard shell.

This module provides a class that encapsulates the dashboard shell settings
and ensures immutability for its instances.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardShellDefinition:
    dashboard_interval_ms: int
