"""
A schema definition to represent the structure of an admin object.

This module defines the `AdminSchema` class, which represents a schema for
admin-related objects. Each schema consists of a key, a title, and a collection
of field definitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from .field_definition import FieldDefinition


@dataclass(frozen=True)
class AdminSchema:
    key: str
    title: str
    fields: tuple[FieldDefinition, ...]
