"""
Service for creating Dash AG Grid components with customizable configurations.

This module provides the `DashAgGridService` class, which allows for the construction
of interactive Dash AG Grid tables with configurable options, such as row data,
column definitions, and grid behavior settings.

Classes
-------
DashAgGridService
    A service for generating Dash AG Grid components.
"""

from __future__ import annotations

from typing import Any

import dash_ag_grid as dag

from ..models.grid_configuration import GridConfiguration


class DashAgGridService:
    def create_table(
        self,
        *,
        table_id: str | dict,
        row_data: list[dict[str, Any]],
        column_defs: list[dict[str, Any]],
        configuration: GridConfiguration | None = None,
    ) -> dag.AgGrid:
        configuration = configuration or GridConfiguration()

        default_col_def = {
            'filter': True,
            'resizable': True,
            'sortable': True,
            'editable': configuration.editable,
            'minWidth': configuration.min_width,
            'suppressMovable': not configuration.enable_columns_reorder,
        }
        default_col_def.update(configuration.default_col_def_overrides)

        row_selection = {
            'mode': configuration.row_selection.mode,
            'checkboxes': configuration.row_selection.checkboxes,
            'headerCheckbox': configuration.row_selection.header_checkbox,
            'enableClickSelection': configuration.row_selection.enable_click_selection,
        }

        dash_grid_options: dict[str, Any] = {
            'pagination': configuration.pagination,
            'paginationPageSize': configuration.pagination_page_size,
            'paginationPageSizeSelector': list(configuration.pagination_page_size_selector),
            'animateRows': configuration.animate_rows,
            'rowSelection': row_selection,
            'columnHoverHighlight': configuration.column_hover_highlight,
            'stopEditingWhenCellsLoseFocus': (configuration.stop_editing_when_cells_lose_focus),
        }

        if configuration.get_row_id_function:
            dash_grid_options['getRowId'] = {
                'function': configuration.get_row_id_function,
            }

        dash_grid_options = self._deep_merge(
            base=dash_grid_options,
            overrides=configuration.dash_grid_options_overrides,
        )

        return dag.AgGrid(
            id=table_id,
            columnDefs=column_defs,
            rowData=row_data,
            defaultColDef=default_col_def,
            dashGridOptions=dash_grid_options,
            className=configuration.class_name,
            style=configuration.style,
        )

    @staticmethod
    def _deep_merge(
        *,
        base: dict[str, Any],
        overrides: dict[str, Any],
    ) -> dict[str, Any]:
        result = dict(base)

        for key, value in overrides.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = DashAgGridService._deep_merge(
                    base=result[key],
                    overrides=value,
                )
                continue

            result[key] = value

        return result
