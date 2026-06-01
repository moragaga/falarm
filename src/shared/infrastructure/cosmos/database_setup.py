"""
Ensures the required Cosmos DB database exists, creating it if necessary.

This function uses the provided Cosmos client and settings to check
for the existence of the specified database. If the database does
not exist, it attempts to create it.

Parameters
----------
client : CosmosClient
    The client connection to the Cosmos DB account.
settings : CosmosSettings
    Configuration settings containing the required database name.

Raises
------
ValueError
    If the function fails to create the database due to an error.
"""

from __future__ import annotations

from azure.cosmos import CosmosClient

from .settings import CosmosSettings


def ensure_required_database(client: CosmosClient, settings: CosmosSettings) -> None:
    try:
        client.create_database_if_not_exists(settings.database_name)
    except Exception as e:
        raise ValueError(f'[ERROR] The database {settings.database_name} cannot be created: {e}')
