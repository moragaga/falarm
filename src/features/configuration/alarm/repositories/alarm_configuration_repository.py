from __future__ import annotations

from src.features.configuration.repositories import ConfigurationSharepointRepository


class AlarmConfigurationRepository:
    def __init__(self, repository: ConfigurationSharepointRepository) -> None:
        self._repository = repository

    def load_rows(self, *, filename: str, relative_path: str) -> list[dict] | dict:
        return self._repository.load_rows(
            filename=filename,
            relative_path=relative_path,
        )

    def save_rows(
        self,
        *,
        filename: str,
        relative_path: str,
        rows: list[dict] | dict,
    ) -> bool:
        return self._repository.save_rows(
            filename=filename,
            relative_path=relative_path,
            rows=rows,
        )
