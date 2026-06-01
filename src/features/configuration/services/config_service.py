"""
Provides the ConfigService class with functionality to validate and normalize
data rows using a specified schema.

This module facilitates the validation and normalization of rows of data
against a given schema by leveraging the ConfigValidationService. It contains
a single static method for handling the process.
"""

from __future__ import annotations

from ..models import AdminSchema
from ..services.config_validation_service import ConfigValidationService


class ConfigService:
    @staticmethod
    def validate_and_normalize(
        schema: AdminSchema,
        rows: list[dict],
    ) -> tuple[list[dict], list[str]]:
        return ConfigValidationService.normalize_rows(schema=schema, rows=rows)
