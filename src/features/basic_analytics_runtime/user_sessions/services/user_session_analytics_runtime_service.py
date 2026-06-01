from __future__ import annotations

from typing import Any

from ..repositories import UserSessionAnalyticsRepository


class UserSessionAnalyticsRuntimeService:
    def __init__(
        self,
        *,
        repository: UserSessionAnalyticsRepository,
    ) -> None:
        self._repository = repository

    def get_snapshot(self) -> dict[str, Any]:
        return self._repository.get_snapshot()


def get_user_session_analytics_runtime_service() -> UserSessionAnalyticsRuntimeService:
    return UserSessionAnalyticsRuntimeService(
        repository=UserSessionAnalyticsRepository(),
    )