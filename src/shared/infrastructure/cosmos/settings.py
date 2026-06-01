"""
Configuration settings for accessing a Cosmos DB account.

This module provides a dataclass that encapsulates all necessary information
required to configure and access a Cosmos DB account. It supports generating
settings from an environment configuration object.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.app.env_configuration import EnvConfiguration


@dataclass(frozen=True)
class CosmosSettings:
    account_uri: str
    account_key: str
    database_name: str
    use_gateway: bool = False

    @classmethod
    def from_env(cls, settings: EnvConfiguration) -> CosmosSettings:

        return cls(
            account_uri=settings.cosmos_account_uri,
            account_key=settings.cosmos_account_key,
            database_name=settings.cosmos_database_name,
            use_gateway=not settings.is_remote_service,
        )
