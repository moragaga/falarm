"""
A module for defining and managing field definitions and options.

This module provides classes and utility functions for handling field
definitions, their options, and various operations like normalization,
validation, and retrieval of option labels and values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

FieldType = Literal[
    'text',
    'number',
    'boolean',
    'select',
    'multiselect',
    'semicolon_list',
]


@dataclass(frozen=True)
class FieldOption:
    label: str
    value: str

    @classmethod
    def from_value(cls, value: Any) -> FieldOption:
        normalized = str(value or '').strip()

        return cls(
            label=normalized,
            value=normalized,
        )


@dataclass(frozen=True)
class FieldDefinition:
    name: str
    label: str
    field_type: FieldType
    required: bool = False
    editable: bool = True
    options: tuple[str | FieldOption, ...] = field(default_factory=tuple)
    help_text: str | None = None
    default_value: str | int | float | bool | list[str] | None = None

    def get_option_values(self) -> list[str]:
        return [_get_option_value(option) for option in self.options]

    def get_option_labels(self) -> list[str]:
        return [_get_option_label(option) for option in self.options]

    def get_option_label_by_value(self) -> dict[str, str]:
        return {_get_option_value(option): _get_option_label(option) for option in self.options}

    def get_option_value_by_label(self) -> dict[str, str]:
        return {_get_option_label(option): _get_option_value(option) for option in self.options}

    def normalize_option_value(self, value: Any) -> str:
        raw_value = str(value or '').strip()

        option_values = set(self.get_option_values())

        if raw_value in option_values:
            return raw_value

        value_by_label = self.get_option_value_by_label()

        return value_by_label.get(raw_value, raw_value)

    def is_valid_option_value(self, value: Any) -> bool:
        normalized_value = self.normalize_option_value(value)

        if normalized_value == '' and not self.required:
            return True

        return normalized_value in set(self.get_option_values())


def _get_option_value(option: str | FieldOption) -> str:
    if isinstance(option, FieldOption):
        return str(option.value or '').strip()

    return str(option or '').strip()


def _get_option_label(option: str | FieldOption) -> str:
    if isinstance(option, FieldOption):
        return str(option.label or '').strip()

    return str(option or '').strip()
