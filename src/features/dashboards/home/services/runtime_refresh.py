"""
Utilities for managing dashboard refresh locks, signals, and runtime evaluation.

This module provides functions for creating refresh signals, handling lock states,
parsing lock timestamps, checking lock expiration, and evaluating runtime results
for dashboard refresh mechanisms.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.shared.time.timestamps import (
    now_utc,
    now_utc_iso,
    parse_utc_datetime,
    to_santiago_display,
)

from ..models.dashboard_runtime import (
    DashboardInformationStatusStore,
    DashboardRefreshLock,
    DashboardRefreshSignal,
    DashboardRuntimeStore,
)

EXPIRATION_MINUTES = 5
LOCK_TIMEOUT_SECONDS = 120


def new_token() -> str:
    return str(uuid4())


def build_refresh_signal() -> DashboardRefreshSignal:
    return {
        'token': new_token(),
        'request_at': now_utc_iso(),
    }


def build_released_lock() -> DashboardRefreshLock:
    return {
        'is_running': False,
        'active_token': None,
        'started_at': None,
    }


def build_acquire_lock(signal: DashboardRefreshSignal) -> DashboardRefreshLock:
    return {
        'is_running': True,
        'active_token': signal.get('token'),
        'started_at': now_utc_iso(),
    }


def parse_lock_started_at(value: Any):
    return parse_utc_datetime(value)


def is_lock_expired(lock_data: dict[str, Any] | None) -> bool:
    if not lock_data:
        return False

    if not lock_data.get('is_running', False):
        return False

    started_at = parse_lock_started_at(lock_data.get('started_at'))
    if started_at is None:
        return False

    age_seconds = (now_utc() - started_at).total_seconds()
    return age_seconds > LOCK_TIMEOUT_SECONDS


def evaluate_runtime_result(
    current_last_update_pi_utc: str | None,
    previous_last_update_pi_utc: str | None,
    expiration_minutes: int = EXPIRATION_MINUTES,
) -> tuple[DashboardRuntimeStore, DashboardInformationStatusStore, bool]:

    changed = False
    if current_last_update_pi_utc and previous_last_update_pi_utc:
        changed = current_last_update_pi_utc != previous_last_update_pi_utc
    elif current_last_update_pi_utc:
        changed = True

    last_update_utc = parse_utc_datetime(current_last_update_pi_utc)

    expired = True
    age_seconds: float | None = None

    if last_update_utc is not None:
        age_seconds: float = (now_utc() - last_update_utc).total_seconds()
        expired = age_seconds >= expiration_minutes * 60

    runtime_store: DashboardRuntimeStore = {
        'last_update_pi_utc': current_last_update_pi_utc,
        'changed': changed,
        'runtime_error': current_last_update_pi_utc is None,
    }

    information_store: DashboardInformationStatusStore = {
        'last_update_pi_utc': current_last_update_pi_utc,
        'last_update_pi_santiago': to_santiago_display(last_update_utc),
        'expired': expired,
        'age_seconds': age_seconds,
    }

    return runtime_store, information_store, changed
