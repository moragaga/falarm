from __future__ import annotations

from typing import Any

import plotly.graph_objects as go


GRAPH_CONFIGURATION: dict[str, Any] = {
    'displayModeBar': False,
    'responsive': True,
    'staticPlot': False,
    'scrollZoom': False,
    'doubleClick': False,
    'displaylogo': False,
    'modeBarButtonsToRemove': [
        'zoom2d',
        'pan2d',
        'select2d',
        'lasso2d',
        'zoomIn2d',
        'zoomOut2d',
        'autoScale2d',
        'resetScale2d',
    ],
}


GRAPH_LAYOUT: dict[str, Any] = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'margin': {
        'l': 42,
        'r': 20,
        't': 35,
        'b': 42,
    },
    'font': {
        'family': 'Inter, Roboto, sans-serif, Arial',
        'color': '#4B5563',
    },
    'hoverlabel': {
        'font_family': 'Inter, Roboto, sans-serif, Arial',
        'font': {'color': '#000000'}
    },
    'hovermode': 'x unified',
    'clickmode': 'none',
    'dragmode': False,
    'legend': {
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'center',
        'x': 0.5,
    },
    'xaxis': {
        'gridwidth': 0,
        'linewidth': 1,
        'fixedrange': True,
        'showgrid': False,
        'zeroline': False,
        'title': '',
    },
    'yaxis': {
        'fixedrange': True,
        'showgrid': True,
        'zeroline': False,
        'title': 'Cantidad',
    },
}


def build_weekly_comparison_figure(
    *,
    weekly_comparison: dict[str, Any],
) -> go.Figure:
    series = weekly_comparison.get('series')

    if not isinstance(series, list) or not series:
        return build_empty_weekly_comparison_figure(
            message='Sin datos de comparación semanal.',
        )

    x_values = weekly_comparison.get('x_labels') or [
        'Lun',
        'Mar',
        'Mié',
        'Jue',
        'Vie',
        'Sáb',
        'Dom',
    ]

    figure = go.Figure()

    for item in series:
        if not isinstance(item, dict):
            continue

        name = item.get('label') or item.get('key') or 'Serie'
        figure.add_trace(
            go.Scatter(
                name=name,
                x=x_values,
                y=item.get('values') or [],
                mode='lines+markers',
                line={
                    'dash': item.get('dash') or 'solid',
                    'width': 2,
                },
                hovertemplate=(
                    f'{name}: <b>%{{y}}</b>'
                    '<extra></extra>'
                )
            )
        )

    figure.update_layout(**GRAPH_LAYOUT)
    figure.update_xaxes(tickmode='array', tickvals=x_values, ticktext=x_values)

    return figure


def build_empty_weekly_comparison_figure(
    *,
    message: str,
) -> go.Figure:
    figure = go.Figure()

    figure.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref='paper',
        yref='paper',
        showarrow=False,
    )

    figure.update_layout(
        margin={
            'l': 30,
            'r': 20,
            't': 30,
            'b': 30,
        },
        xaxis={
            'visible': False,
        },
        yaxis={
            'visible': False,
        },
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font={
            'size': 11,
        },
    )

    return figure