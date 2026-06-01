"""
This module provides utilities for parsing and extracting data from principal headers
and their associated payloads.

The module includes functionality to decode base64-encoded principal headers,
parse them as JSON, and retrieve specific claims such as the name attribute.

Functions
---------
parse_principal_header(principal_header: str | None) -> dict[str, Any] | None
    Decodes and parses a base64-encoded principal header into a dictionary.

get_name_from_principal(principal_payload: dict | None, fallback_email: str) -> str
    Extracts the name claim from the principal payload or derives a name from the
    fallback email.
"""

from __future__ import annotations

import base64
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse_principal_header(principal_header: str | None) -> dict[str, Any] | None:
    if not principal_header:
        return None

    try:
        decoded = base64.b64decode(principal_header).decode('utf-8')
        return json.loads(decoded)
    except Exception as e:
        logger.exception(f'Failed to decode principal header {principal_header} - {e}')
        return None


def get_name_from_principal(principal_payload: dict | None, fallback_email: str) -> str:
    claims = (principal_payload or {}).get('claims', [])
    for claim in claims:
        if claim.get('typ') == 'name':
            return claim.get('val') or fallback_email.split('@')[0]
    return fallback_email.split('@')[0]
