"""Defines the structure and properties for building KPI components.

This module contains the `KpiBuildDefinition` class, which serves as a
data container for defining how KPI components should be constructed,
including the builder logic, presentation size, and any parameters
to be excluded.

Classes
-------
KpiBuildDefinition
    Represents the definition for constructing a specific KPI component.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal

Parameters = Literal['kpis', 'timeseries', 'timestamps']


@dataclass(frozen=True, slots=True)
class KpiBuildDefinition:
    slot_name: str
    builder: Callable[..., Any]
    ui_size: str = 'large'
    exclude_parameters: tuple[Parameters, ...] | None = None
    explicit_list: bool = False
