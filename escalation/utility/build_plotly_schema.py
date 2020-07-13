from graphics.plotly_plot import LAYOUT
from utility.constants import *


def build_plotly_schema():
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "plotly dict",
        "description": "what PLOT_SPECIFIC_INFO should look like if plot manager is plotly",
        "type": "object",
        "reqiured": [DATA],
        "properties": {
            DATA: {
                "type": "array",
                "description": "list of graphs to be plotted on a single plot, "
                "see https://plotly.com/javascript/reference/"
                " for options, axis information is found from data property",
                "items": {
                    "type": "object",
                    "title": "data dictionary",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "type of plot",
                            "enum": [
                                "scatter",
                                "scattergl",
                                "bar",
                                "pie",
                                "heatmap",
                                "heatmapgl",
                                "image",
                                "contour",
                                "table",
                                "box",
                                "violin",
                                "histogram",
                                "histogram2d",
                                "histogram2dcontour",
                                "scatter3d",
                                "surface",
                                "mesh3d",
                            ],
                        }
                    },
                },
            },
            LAYOUT: {
                "title": "layout dict",
                "description": "Determines how the graph looks",
                "type": "object",
                "properties": {
                    "hovermode": {
                        "type": "string",
                        "enum": [
                            "x",
                            "y",
                            "closest",
                            "false",
                            "x unified",
                            "y unified",
                        ],
                    }
                },
            },
        },
    }
    return schema
