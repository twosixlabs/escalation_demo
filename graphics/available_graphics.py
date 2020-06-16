from graphics.plotly_plot import PlotlyPlot
from graphics.plotly_table import PlotlyTable

"""
List of the available graphics
"""
AVAILABLE_GRAPHICS = {
    "table": {"object": PlotlyTable, "num_data": -1, "show_name": "Table"},
    "bar": {"object": PlotlyPlot("bar"), "num_data": 2, "show_name": "bar plot"},
    "heatmap": {
        "object": PlotlyPlot("heatmap"),
        "num_data": 3,
        "show_name": "Heat map",
    },
    "scatter plot": {
        "object": PlotlyPlot("scatter"),
        "num_data": 2,
        "show_name": "Scatter/Line Plot",
    },
    "box": {"object": PlotlyPlot("box"), "num_data": 2, "show_name": "Box"},
    "histogram": {
        "object": PlotlyPlot("histogram"),
        "num_data": 1,
        "show_name": "Histogram",
    },
    "scatter3d": {
        "object": PlotlyPlot("scatter3d"),
        "num_data": 3,
        "show_name": "3D Scatter Plot",
    },
    "surface": {
        "object": PlotlyPlot("surface"),
        "num_data": 3,
        "show_name": "Surface Plot",
    },
}
