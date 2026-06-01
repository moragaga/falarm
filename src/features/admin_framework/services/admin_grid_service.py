"""
Provides services and utilities for managing and manipulating grids in a Dash-based UI.

This module contains the `AdminGridService` class, offering static methods to
handle grid creation, row transformations, and manipulations. It integrates with
the Dash AG Grid library and provides helper functions for common grid-related
tasks like adding, deleting, and cleaning rows.

Classes
-------
AdminGridService
    Provides static methods for grid-related operations such as table creation
    and row manipulation.
"""

from __future__ import annotations

from typing import Any

import dash_ag_grid as dag

from src.shared.ui.grid.constants import GRID_ROW_UID_FIELD
from src.shared.ui.grid.models import (
    GridConfiguration,
    GridRowSelectionConfiguration,
)
from src.shared.ui.grid.services import DashAgGridService, GridRowService


class AdminGridService:
    @staticmethod
    def create_table(
        *,
        table_id: dict[str, str] | str,
        row_data: list[dict[str, Any]],
        column_defs: list[dict[str, Any]],
        configuration: GridConfiguration | None = None,
    ) -> dag.AgGrid:
        final_column_defs = GridRowService.prepend_technical_uid_column(
            column_defs=column_defs,
        )

        final_configuration = configuration or AdminGridService.default_configuration()

        if final_configuration.get_row_id_function is None:
            final_configuration = AdminGridService._with_default_row_id(
                configuration=final_configuration,
            )

        return DashAgGridService().create_table(
            table_id=table_id,
            row_data=GridRowService.attach_row_uids(rows=row_data),
            column_defs=final_column_defs,
            configuration=final_configuration,
        )

    @staticmethod
    def prepare_rows_for_grid(
        *,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        return GridRowService.attach_row_uids(rows=rows)

    @staticmethod
    def clean_rows_for_save(
        *,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        return GridRowService.strip_technical_fields(rows=rows)

    @staticmethod
    def append_row(
        *,
        rows: list[dict[str, Any]] | None,
        row: dict[str, Any],
    ) -> list[dict[str, Any]]:
        return GridRowService.append_row(
            rows=rows,
            row=row,
        )

    @staticmethod
    def delete_selected_rows(
        *,
        rows: list[dict[str, Any]] | None,
        selected_rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        return GridRowService.delete_selected_rows(
            rows=rows,
            selected_rows=selected_rows,
        )

    @staticmethod
    def default_configuration() -> GridConfiguration:
        return GridConfiguration(
            editable=True,
            pagination=True,
            pagination_page_size=20,
            pagination_page_size_selector=(10, 20, 50, 100),
            row_selection=GridRowSelectionConfiguration(
                mode='multiRow',
                checkboxes=True,
                header_checkbox=True,
                enable_click_selection=True,
            ),
            get_row_id_function=f'params.data.{GRID_ROW_UID_FIELD}',
            animate_rows=True,
            stop_editing_when_cells_lose_focus=True,
        )

    @staticmethod
    def _with_default_row_id(
        *,
        configuration: GridConfiguration,
    ) -> GridConfiguration:
        return GridConfiguration(
            editable=configuration.editable,
            pagination=configuration.pagination,
            pagination_page_size=configuration.pagination_page_size,
            pagination_page_size_selector=configuration.pagination_page_size_selector,
            min_width=configuration.min_width,
            class_name=configuration.class_name,
            style=configuration.style,
            row_selection=configuration.row_selection,
            get_row_id_function=f'params.data.{GRID_ROW_UID_FIELD}',
            animate_rows=configuration.animate_rows,
            enable_columns_reorder=configuration.enable_columns_reorder,
            column_hover_highlight=configuration.column_hover_highlight,
            stop_editing_when_cells_lose_focus=(configuration.stop_editing_when_cells_lose_focus),
            default_col_def_overrides=configuration.default_col_def_overrides,
            dash_grid_options_overrides=configuration.dash_grid_options_overrides,
        )
