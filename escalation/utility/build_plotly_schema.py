# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

from graphics.plotly_plot import LAYOUT
from utility.constants import *


def build_plotly_schema():
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "plotly dict",
        "description": "dictionary that follows https://plotly.com/javascript/reference/, the dictionaries from "
        "data key in get imported in with values from the database/csvs",
        "type": "object",
        "required": [DATA],
        "properties": {
            DATA: {
                "type": "array",
                "description": "list of graphs to be plotted on a single plot",
                "items": {
                    "type": "object",
                    "title": "data dictionary",
                    "required": ["type"],
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
                        },
                        "mode": {
                            "type": "string",
                            "description": "used for scatter or scattergl",
                            "enum": [
                                "lines",
                                "markers",
                                "text",
                                "lines+markers",
                                "markers+text",
                                "lines+text",
                                "lines+markers+text",
                                "none",
                                "group",
                            ],
                        },
                    },
                },
            },
            LAYOUT: {
                "title": "layout dict",
                "description": "Determines how the graph looks",
                "type": "object",
                "properties": {
                    "height": {"type": "number", "minimum": 10},
                    "width": {"type": "number", "minimum": 10},
                    "xaxis": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}},
                            },
                            "automargin": {"type": "boolean"},
                        },
                    },
                    "yaxis": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}},
                            },
                            "automargin": {"type": "boolean"},
                        },
                    },
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
                    },
                },
            },
        },
    }
    return schema
