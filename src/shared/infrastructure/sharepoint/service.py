"""
Provides a service interface for interacting with a SharePoint-based file storage system.

This class includes methods for saving and loading files, particularly JSON and binary
content, to and from a SharePoint file storage platform. It supports handling JSON
data files and other binary content, encoding and decoding content as needed, and
allows uploading, downloading, or working with files as base64-encoded strings or
data URIs. Configuration and file path management are facilitated through associated
settings and services.

Classes
-------
SharepointService
    A service for managing file-related operations in a SharePoint-based system.

Methods
-------
save_json(filename, data, file_type=SharepointFileType.CONFIGURATION, relative_path=None)
    Save JSON data to a SharePoint storage as a compressed and encoded file.

load_json(filename, file_type=SharepointFileType.CONFIGURATION, relative_path=None, default=None)
    Load JSON data from a SharePoint storage.

load_image_as_data_uri(filename, file_type=SharepointFileType.CONFIGURATION, relative_path=None, default=None)
    Load an image file from SharePoint and return it as a data URI.

upload_file(filename, content, file_type=SharepointFileType.CONFIGURATION, relative_path=None, content_type=None)
    Upload a binary file to the SharePoint storage.

download_file(filename, file_type=SharepointFileType.CONFIGURATION, relative_path=None, default=None)
    Download a binary file from SharePoint.

load_file_base64(filename, file_type=SharepointFileType.CONFIGURATION, relative_path=None)
    Load a file from SharePoint as a base64-encoded string.
"""

from __future__ import annotations

from requests import Response
from typing import Any

import base64
import gzip
import json
import logging
import mimetypes

import requests

from .file_type import SharepointFileType
from .path_service import SharepointPathService
from .settings import SharepointSettings

logger = logging.getLogger(__name__)


class SharepointService:
    def __init__(self, settings: SharepointSettings, timeout: int = 30) -> None:
        self._settings = settings
        self._timeout = timeout

    def save_json(
        self,
        filename: str,
        data: dict | list,
        *,
        file_type: SharepointFileType = SharepointFileType.CONFIGURATION,
        relative_path: str | None = None,
    ) -> bool:
        response = None
        try:
            encoded_data = self._encode_json_in_gzip_base64(data=data)
            path = self._build_full_path(file_type=file_type, relative_path=relative_path)

            payload = {
                'filename': filename,
                'content': encoded_data,
                'relative_path': path,
            }
            response = requests.post(
                url=self._settings.post_endpoint,
                headers=self._settings.headers,
                json=payload,
                timeout=self._timeout,
            )

            response.raise_for_status()
            return response.status_code in (200, 201)
        except Exception as e:
            return self._response_exception(
                exception=e,
                response=response,
                default=False
            )

    def load_json(
        self,
        filename: str,
        *,
        file_type: SharepointFileType = SharepointFileType.CONFIGURATION,
        relative_path: str | None = None,
        default: dict | list | None = None,
    ) -> dict | list | None:
        response = None
        try:
            path = self._build_full_path(file_type=file_type, relative_path=relative_path)

            payload = {
                'filename': filename,
                'relative_path': path,
            }

            response = requests.post(
                url=self._settings.get_endpoint,
                headers=self._settings.headers,
                json=payload,
                timeout=self._timeout,
            )

            response.raise_for_status()
            data = response.json()
            return self._decode_json_from_gzip_base64(file_content=data.get('content'))
        except Exception as e:
            return self._response_exception(
                exception=e,
                type_action='loading',
                response=response,
                default=default
            )

    def upload_file(
        self,
        filename: str,
        content: bytes,
        *,
        file_type: SharepointFileType = SharepointFileType.CONFIGURATION,
        relative_path: str | None = None,
        content_type: str | None = None,
    ) -> bool:
        response = None
        try:
            path = self._build_full_path(
                file_type=file_type,
                relative_path=relative_path,
            )

            encoded_content = base64.b64encode(content).decode('utf-8')
            resolved_content_type = (
                content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            )

            payload = {
                'filename': filename,
                'content': encoded_content,
                'relative_path': path,
                'content_type': resolved_content_type,
                'encoding': 'base64',
            }

            response = requests.post(
                url=self._settings.post_endpoint,
                headers=self._settings.headers,
                json=payload,
                timeout=self._timeout,
            )

            response.raise_for_status()
            return response.status_code in (200, 201)

        except Exception as e:
            return self._response_exception(
                exception=e,
                type_action='uploading',
                type_file='image',
                response=response,
                default=False
            )

    def download_file(
        self,
        filename: str,
        *,
        file_type: SharepointFileType = SharepointFileType.CONFIGURATION,
        relative_path: str | None = None,
        default: bytes | None = None,
    ) -> bytes | None:
        response = None
        try:
            path = self._build_full_path(
                file_type=file_type,
                relative_path=relative_path,
            )

            payload = {
                'filename': filename,
                'relative_path': path,
            }

            response = requests.post(
                url=self._settings.get_endpoint,
                headers=self._settings.headers,
                json=payload,
                timeout=self._timeout,
            )

            response.raise_for_status()
            data = response.json()
            content = data.get('content').strip()
            if not content:
                return default

            return base64.b64decode(content.encode('utf-8'))

        except Exception as e:
            return self._response_exception(
                exception=e,
                type_action='loading',
                type_file='file',
                response=response,
                default=None
            )

    def _build_full_path(
        self, *, file_type: SharepointFileType, relative_path: str | None = None
    ) -> str:
        relative = SharepointPathService.build_relative_path(
            file_type=file_type, relative_path=relative_path
        )
        root = self._settings.root_path.rstrip('/\\')
        relative = relative.rstrip('/\\')
        return f'{root}/{relative}'

    @staticmethod
    def _encode_json_in_gzip_base64(data: dict | list) -> str:
        json_bytes = json.dumps(
            data, ensure_ascii=False, indent=None, separators=(',', ':')
        ).encode('utf-8')

        gzip_bytes = gzip.compress(json_bytes, compresslevel=9)
        return base64.b64encode(gzip_bytes).decode('utf-8')

    @staticmethod
    def _decode_json_from_gzip_base64(file_content: str) -> dict | list:
        gzip_bytes = base64.b64decode(file_content.encode('utf-8'))
        json_bytes = gzip.decompress(gzip_bytes)
        return json.loads(json_bytes.decode('utf-8'))

    @staticmethod
    def _response_exception(
            exception: Exception,
            type_action: str = 'saving',
            type_file: str = 'json',
            response: Response | None = None,
            default: Any | None = None,
    ) -> Any:
        message = ''
        if response:
            data: dict = response.json()
            message = data.get('message')
        logger.exception('Error {0} {1} to SharePoint: {2} - {3}'.format(
            type_action, type_file, message, exception
        ))
        return default