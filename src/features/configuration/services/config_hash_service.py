"""
Provides functionality to generate a SHA-256 hash from a given payload.

This module includes a static method for creating a hashed string representation
of a payload. The hash generation ensures that the order of keys and values
is consistent by normalizing JSON input. This is useful for ensuring that
identical payloads always produce the same hash, regardless of the original
order or formatting.

Classes
-------
ConfigHashService
    Provides a static method for hashing payloads using SHA-256.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


class ConfigHashService:
    @staticmethod
    def build_hash(payload: Any) -> str:
        normalized_json = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':'),
            default=str,
        )

        digest = hashlib.sha256(
            normalized_json.encode('utf-8'),
        ).hexdigest()

        return f'sha256:{digest}'
