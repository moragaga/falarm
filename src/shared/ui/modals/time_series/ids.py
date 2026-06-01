"""
Provides identifiers used in the Time Series Modal component.

This module defines constant IDs that represent various elements and states
associated with the Time Series Modal. These IDs are primarily used for
designating HTML elements or managing state within the component.
Attributes are organized based on their purpose, such as modal elements,
graph-related elements, and state management.

Classes
-------
TimeSeriesModalIds
    Contains constant attributes used as identifiers in the Time Series Modal
    component.
"""

from __future__ import annotations


class TimeSeriesModalIds:
    TRIGGERED_ID = 'time-series-modal-triggered-id'
    MODAL = 'time-series-modal'
    CLOSE = 'time-series-modal-close'
    TITLE = 'time-series-modal-title'
    GRAPH = 'time-series-modal-graph'
    GRAPH_LOADING = 'time-series-modal-graph-loading'
    LAST_UPDATE = 'time-series-modal-last-update'

    REFRESH_BUTTON = 'time-series-modal-refresh-button'
    FILTER_SELECT_TURN_SCOPE = 'time-series-modal-filter-select-turn-scope'

    TIME_SERIES_MODAL_STATE_STORE = 'time-series-modal-state-store'
    TIME_SERIES_MODAL_MIRROR_STORE = 'time-series-modal-mirror-store'
