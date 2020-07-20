# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

from graphics.plotly_plot import PlotlyPlot

"""
List of the available graphics
"""

AVAILABLE_GRAPHICS = {
    "plotly": {"object": PlotlyPlot(), "graph_html_template": "plotly.html"}
}

"""
I am going to repurpose this when I am making admin UI set up
AVAILABLE_GRAPHICS = {
    "table": {
        "object": PlotlyPlot(),
        "num_data": -1,
        "show_name": "Table",
        "Reference": "https://plotly.com/javascript/reference/#table",
    },
    "bar": {
        "object": PlotlyPlot("bar"),
        "num_data": 2,
        "show_name": "Bar Plot",
        "Reference": "https://plotly.com/javascript/reference/#scatter",
    },
    "heatmap": {
        "object": PlotlyPlot("heatmap"),
        "num_data": 3,
        "show_name": "Heat map",
        "Reference": "https://plotly.com/javascript/reference/#heatmap",
    },
    "scatter": {
        "object": PlotlyPlot("scatter"),
        "num_data": 2,
        "show_name": "Scatter/Line Plot",
        "Reference": "https://plotly.com/javascript/reference/#heatmap",
    },
    "box": {
        "object": PlotlyPlot("box"),
        "num_data": 2,
        "show_name": "Box",
        "Reference": "https://plotly.com/javascript/reference/#box",
    },
    "histogram": {
        "object": PlotlyPlot("histogram"),
        "num_data": 1,
        "show_name": "Histogram",
        "Reference": "https://plotly.com/javascript/reference/#histogram",
    },
    "scatter3d": {
        "object": PlotlyPlot("scatter3d"),
        "num_data": 3,
        "show_name": "3D Scatter Plot",
        "Reference": "https://plotly.com/javascript/reference/#scatter3d",
    },
    "surface": {
        "object": PlotlyPlot("surface"),
        "num_data": 3,
        "show_name": "Surface Plot",
        "Reference": "https://plotly.com/javascript/reference/#surface",
    },
}
"""
