"""
Provides a decorator for logging and handling errors in Dash component callbacks.

This module includes a utility function `log_component_callback` to
decorate callback functions used in Dash applications. The decorator
logs callback execution details and handles exceptions, optionally
returning error components or preventing updates.

Functions
---------
log_component_callback(callback_name: str, components: int, flags: int, *, ui_size: str = 'large', prevent_update_on_error: bool = True) -> Callable
    Returns a decorator for a Dash callback function, which logs its
    execution and manages errors.

"""

from __future__ import annotations

import traceback
from collections.abc import Callable
from functools import wraps
from typing import Any

from dash import ctx
from dash.exceptions import PreventUpdate

from src.shared.ui.display.error_component import build_error_component


def log_component_callback(
    callback_name: str,
    components: int,
    flags: int,
    *,
    ui_size: str = 'large',
    prevent_update_on_error: bool = True,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                triggered_by = ctx.triggered_id
            except Exception as e:
                print(f'[Error] Not triggered callback {e}')
                triggered_by = None

            try:
                result = func(*args, **kwargs)
                return result
            except PreventUpdate:
                raise PreventUpdate
            except Exception as e:
                print(
                    f'[ERROR] callback={callback_name} triggered_by={triggered_by} error={e} prevent'
                )
                traceback.print_exc()

                if components != 0 or flags != 0:
                    return [build_error_component(ui_size=ui_size)] * components + ['true'] * flags

                if prevent_update_on_error:
                    raise PreventUpdate

        return wrapper

    return decorator
