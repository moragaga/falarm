from uuid import uuid4

import dash_bootstrap_components as dbc
from dash.development.base_component import Component


def build_popover(
    target: str,
    children: Component,
    placement: str = 'left',
    trigger: str = 'hover focus',
    delay: tuple = (200, 0),
    autohide: bool = True,
    body: bool = True,
) -> dbc.Popover:
    return dbc.Popover(
        key=uuid4().__str__(),
        className='app-popover-shell',
        target=target,
        placement=placement,
        delay=delay,
        trigger=trigger,
        autohide=autohide,
        body=body,
        children=children,
    )
