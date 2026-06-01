"""
A module for configuring grid settings and row selection behavior.

This module defines two dataclasses, `GridRowSelectionConfiguration` and
`GridConfiguration`, that allow specifying detailed configuration options
for a grid. These configurations include features like pagination, row
selection modes, column customization options, and style definitions.

Classes
-------
GridRowSelectionConfiguration : dataclass
    Represents configuration for grid row selection behavior, including its
    mode and the use of checkboxes.

GridConfiguration : dataclass
    Represents the overall configuration of a grid, including pagination,
    style, minimum width, column and row customization, and overrides.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

GridRowSelectionMode = Literal['singleRow', 'multiRow']


@dataclass(frozen=True)
class GridRowSelectionConfiguration:
    mode: GridRowSelectionMode = 'singleRow'
    checkboxes: bool = False
    header_checkbox: bool = False
    enable_click_selection: bool = True


@dataclass(frozen=False)
class GridConfiguration:
    editable: bool = True

    pagination: bool = True
    pagination_page_size: int = 20
    pagination_page_size_selector: tuple[int, ...] = (10, 20, 50, 100)

    min_width: int = 150

    class_name: str = 'ag-theme-alpine w-100 app-grid-shell'
    style: dict[str, Any] = field(default_factory=dict)

    row_selection: GridRowSelectionConfiguration = field(
        default_factory=GridRowSelectionConfiguration
    )

    get_row_id_function: str | None = None

    animate_rows: bool = True
    enable_columns_reorder: bool = True
    column_hover_highlight: bool = True
    stop_editing_when_cells_lose_focus: bool = True

    default_col_def_overrides: dict[str, Any] = field(default_factory=dict)
    dash_grid_options_overrides: dict[str, Any] = field(default_factory=dict)
