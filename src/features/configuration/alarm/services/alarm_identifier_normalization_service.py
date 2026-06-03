from __future__ import annotations

import re
import unicodedata


_FINAL_IDENTIFIER_PATTERN = re.compile(r'^[a-z0-9_]+$')
_NON_IDENTIFIER_CHARS_PATTERN = re.compile(r'[^a-z0-9_]+')
_REPEATED_UNDERSCORE_PATTERN = re.compile(r'_+')
_WHITESPACE_PATTERN = re.compile(r'\s+')


class AlarmIdentifierNormalizationService:
    @staticmethod
    def normalize_live_identifier(
        value: object,
    ) -> str:
        text = str(value or '')

        if not text:
            return ''

        normalized = _to_ascii_lower(text=text)
        normalized = normalized.replace('-', '_')
        normalized = _WHITESPACE_PATTERN.sub('_', normalized)
        normalized = _NON_IDENTIFIER_CHARS_PATTERN.sub('_', normalized)
        normalized = _REPEATED_UNDERSCORE_PATTERN.sub('_', normalized)

        return normalized

    @staticmethod
    def normalize_final_identifier(
        value: object,
    ) -> str:
        normalized = AlarmIdentifierNormalizationService.normalize_live_identifier(
            value=value,
        )

        return normalized.strip('_')

    @staticmethod
    def normalize_final_identifier_or_default(
        value: object,
        *,
        default_value: str,
    ) -> str:
        normalized = AlarmIdentifierNormalizationService.normalize_final_identifier(
            value=value,
        )

        if normalized:
            return normalized

        return default_value

    @staticmethod
    def is_valid_live_identifier(
        value: object,
    ) -> bool:
        text = str(value or '')

        if not text:
            return False

        return text == AlarmIdentifierNormalizationService.normalize_live_identifier(
            value=text,
        )

    @staticmethod
    def is_valid_final_identifier(
        value: object,
    ) -> bool:
        text = str(value or '').strip()

        if not text:
            return False

        return bool(_FINAL_IDENTIFIER_PATTERN.fullmatch(text))


def _to_ascii_lower(
    *,
    text: str,
) -> str:
    normalized = unicodedata.normalize('NFKD', text)
    normalized = normalized.encode('ascii', 'ignore').decode('ascii')

    return normalized.lower()