from graphics.plotly_plot import PlotlyPlot

"""
List of the available graphics
"""
AVAILABLE_GRAPHICS = {
    "table": PlotlyPlot("table"),
    "bar plot": PlotlyPlot("bar"),
    "heatmap": PlotlyPlot("heatmap"),
    "pie chart": PlotlyPlot("pie"),
    "scatter plot": PlotlyPlot("scatter"),
    "box plot": PlotlyPlot("box"),
    "violin plot": PlotlyPlot("violin"),
    "histogram": PlotlyPlot("histogram"),
    "3D scatter plot": PlotlyPlot("scatter3d"),
    "surface plot": PlotlyPlot("surface"),
}
