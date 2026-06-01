"""
A collection of TypedDict definitions relevant to dashboard operations.

This module defines several TypedDicts which are used to structure data
across different dashboard-related operations. These TypedDicts ensure
stronger type checking and readability of the code.

"""

from __future__ import annotations

from typing import Any, TypedDict


class DashboardRefreshSignal(TypedDict):
    token: str
    request_at: str


class DashboardRefreshLock(TypedDict):
    is_running: bool
    active_token: str | None
    started_at: str | None


class DashboardRuntimeStore(TypedDict):
    data: dict[str, Any] | None
    last_update_pi_utc: str | None
    changed: bool


class DashboardInformationStatusStore(TypedDict):
    last_update_pi_utc: str | None
    last_update_pi_santiago: str | None
    expired: bool
    age_seconds: float | None
