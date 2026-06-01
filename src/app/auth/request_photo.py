"""
A module for handling user profile photo retrieval.

This module provides functionality to retrieve a user's profile photo either
from a remote server (by using an access token) or from a default local image
if the remote photo is unavailable. Errors during retrieval are logged.
"""

from __future__ import annotations

import logging

import requests

logger = logging.getLogger(__name__)


def get_profile_photo_bytes(access_token: str = None) -> bytes | None:
    if access_token:
        return _get_remote_photo(access_token=access_token)
    return get_default_photo()


def _get_remote_photo(access_token: str):
    pic_url = 'https://graph.microsoft.com/v1.0/me/photo/$value'
    pic_url_headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url=pic_url, headers=pic_url_headers, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.error(f'Error getting picture url: {e}')
        return None


def get_default_photo() -> bytes | None:
    pic_path = 'src/assets/img/icons/account_user.svg'
    try:
        with open(pic_path, 'rb') as file:
            return file.read()
    except Exception as e:
        logger.error(f'Error getting default picture: {e}')
        return None
