# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json

from graphics.plotly_plot import STYLES
from utility.build_plotly_schema import build_plotly_schema
from utility.constants import *

NO_DOTS = r"^[^\\.]*$"
ALPHA_NUMERIC_NO_SPACES = r"^[a-zA-Z0-9_]+$"
ONE_DOT = r"^[^\\.]*\\.[^\\.]*$"
ONE_LETTER = r"^[a-zA-Z]$"
NON_EMPTY_STRING = r"[\s\S]+"

# json schema specific constants see https://json-schema.org/
ADDITIONAL_PROPERTIES = "additionalProperties"
PROPERTIES = "properties"
PATTERN_PROPERTIES = "patternProperties"
DESCRIPTION = "description"
TITLE = "title"
TYPE = "type"
ITEMS = "items"
PATTERN = "pattern"
REQUIRED = "required"
MIN_ITEMS = "minItems"
OPTIONS = "options"
DEPENDENCIES = "dependencies"
ENUM = "enum"
ONEOF = "oneOf"


def build_settings_schema():
    """
    :param data_source_names: names from DATA_SOURCES, already checked against the file system
    :param column_names: possible column names from files or database (format data_source_name.column_name)
    :return:
    """
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "Escalation Main Config Generator",
        "description": "Main config file needed to use escalation OS",
        "type": "object",
        "required": [SITE_TITLE, SITE_DESC, DATA_BACKEND, DATA_SOURCES,],
        DEPENDENCIES: {
            DATA_BACKEND: {
                ONEOF: [
                    {
                        PROPERTIES: {DATA_BACKEND: {ENUM: [LOCAL_CSV]}},
                        REQUIRED: [DATA_FILE_DIRECTORY],
                    },
                    {PROPERTIES: {DATA_BACKEND: {ENUM: [POSTGRES, MYSQL]}}},
                ]
            }
        },
        "additionalProperties": False,
        "properties": {
            SITE_TITLE: {
                "type": "string",
                TITLE: "Site Title",
                "description": "title shown at the top of the website",
            },
            SITE_DESC: {
                "type": "string",
                "title": "Site Description",
                "description": "description shown at the top of the website",
            },
            DATA_BACKEND: {
                "type": "string",
                TITLE: "Data Backend",
                "description": "How the data is being managed on the server",
                "enum": [POSTGRES, MYSQL, LOCAL_CSV],
            },
            DATA_FILE_DIRECTORY: {
                "type": "string",
                TITLE: "Data File Directory",
                "description": "Where the data is on the server",
            },
            DATA_SOURCES: {
                "type": "array",
                TITLE: "Data Sources",
                "description": "list of tables or folders that server will use for the plots",
                MIN_ITEMS: 1,
                "items": {"type": "string"},
            },
            AVAILABLE_PAGES: {
                "type": "array",
                TITLE: "Webpages",
                DESCRIPTION: "array of webpages",
                ITEMS: {
                    "type": "object",
                    TITLE: "Page",
                    REQUIRED: [WEBPAGE_LABEL, URL_ENDPOINT],
                    PROPERTIES: {
                        WEBPAGE_LABEL: {
                            "type": "string",
                            TITLE: "Label",
                            DESCRIPTION: "UI label of the webpage",
                        },
                        URL_ENDPOINT: {
                            "type": "string",
                            TITLE: "URL",
                            DESCRIPTION: "Endpoint of a url",
                            PATTERN: ALPHA_NUMERIC_NO_SPACES,
                        },
                        GRAPHIC_CONFIG_FILES: {
                            TYPE: "array",
                            TITLE: "Graphic Config Files",
                            ITEMS: {
                                TYPE: "string",
                                DESCRIPTION: "Path to config file of the graphic for the webpage",
                            },
                        },
                    },
                },
            },
        },
    }
    return schema


def build_graphic_schema(data_source_names=None, column_names=None):
    """
    :param data_source_names: names from DATA_SOURCES, already checked against the file system
    :param column_names: possible column names from files or database (format data_source_name.column_name)
    :return:
    """
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "type": "object",
        "title": "Escalation Graphic Config Generator",
        "description": "Have a unique one of these for each graphic on the page",
        "required": [
            PLOT_MANAGER,
            GRAPHIC_TITLE,
            GRAPHIC_DESC,
            DATA_SOURCES,
            PLOT_SPECIFIC_INFO,
        ],
        "additionalProperties": False,
        PROPERTIES: {
            PLOT_MANAGER: {
                "type": "string",
                "description": "plot library you would like to use"
                " (only plotly is currently available)",
                "enum": ["plotly"],
            },
            GRAPHIC_TITLE: {"type": "string", "description": "Graph title (optional)",},
            GRAPHIC_DESC: {
                "type": "string",
                "description": "Text caption shown above the graph (optional)",
            },
            DATA_SOURCES: {
                "type": "array",
                "description": "Define which data tables are used in this graphic,"
                " and on which columns the data tables are joined",
                "items": {
                    "type": "object",
                    REQUIRED: [DATA_SOURCE_TYPE],
                    "properties": {
                        DATA_SOURCE_TYPE: {
                            "type": "string",
                            "enum": data_source_names,
                        },
                        JOIN_KEYS: {
                            "type": "array",
                            "description": "Column names along which to join the tables"
                            " (in the case of 2 or more tables)",
                            "items": {
                                "type": "array",
                                "uniqueItems": True,
                                "minItems": 2,
                                "maxItems": 2,
                                "items": {"type": "string", "enum": column_names},
                            },
                        },
                    },
                },
            },
            PLOT_SPECIFIC_INFO: {
                "type": "object",
                "title": "Plot Dictionary",
                "description": "this dictionary depends on the graphing library",
            },
            VISUALIZATION_OPTIONS: {
                "type": "object",
                "title": "Visualization List",
                "description": "modifications to the existing graph",
                "additionalProperties": False,
                PROPERTIES: {
                    HOVER_DATA: {
                        "type": "object",
                        "title": "Hover data",
                        "description": "data shown on hover over by mouse",
                        "required": [COLUMN_NAME],
                        "properties": {
                            COLUMN_NAME: {
                                "type": "array",
                                "items": {"type": "string", "enum": column_names,},
                            }
                        },
                    },
                    GROUPBY: {
                        "type": "object",
                        "title": "Group by",
                        "description": "Grouping of the data see https://plotly.com/javascript/group-by/",
                        "required": [COLUMN_NAME],
                        "properties": {
                            COLUMN_NAME: {
                                "type": "array",
                                "items": {"type": "string", "enum": column_names},
                            },
                            STYLES: {TYPE: "object"},
                        },
                    },
                    AGGREGATE: {
                        "type": "object",
                        "title": "Aggregate",
                        "description": "see https://plotly.com/javascript/aggregations/",
                        "required": [COLUMN_NAME],
                        "properties": {
                            COLUMN_NAME: {
                                "type": "array",
                                "items": {"type": "string", "enum": column_names,},
                            },
                            AGGREGATIONS: {
                                "type": "object",
                                "description": "axis to function on the data e.g. x:avg",
                                "patternProperties": {
                                    ONE_LETTER: {
                                        "type": "string",
                                        "description": "function on the data",
                                        "enum": [
                                            "avg",
                                            "sum",
                                            "min",
                                            "max",
                                            "mode",
                                            "median",
                                            "count",
                                            "stddev",
                                            "first",
                                            "last",
                                        ],
                                    }
                                },
                            },
                        },
                    },
                },
            },
            SELECTABLE_DATA_DICT: {
                "type": "object",
                "title": "Selector List",
                "description": "dictionary of data selectors for a graphic",
                ADDITIONAL_PROPERTIES: False,
                PROPERTIES: {
                    FILTER: {
                        "type": "array",
                        "title": "Filter",
                        DESCRIPTION: "a filter operation based on label",
                        "items": {
                            "type": "object",
                            "required": [COLUMN_NAME],
                            "additionalProperties": False,
                            PROPERTIES: {
                                COLUMN_NAME: {
                                    "type": "string",
                                    "description": "name in table",
                                    "enum": column_names,
                                },
                                "multiple": {"type": "boolean"},
                                DEFAULT_SELECTED: {
                                    "type": "array",
                                    "description": "default filter, list of column values",
                                    "items": {"type": "string"},
                                },
                                UNFILTERED_SELECTOR: {"type": "boolean"},
                            },
                        },
                    },
                    NUMERICAL_FILTER: {
                        "type": "array",
                        "title": "Numerical Filter",
                        DESCRIPTION: "a filter operation on numerical data",
                        "items": {
                            "type": "object",
                            "required": [COLUMN_NAME],
                            "additionalProperties": False,
                            PROPERTIES: {
                                COLUMN_NAME: {
                                    "type": "string",
                                    "description": "name in table",
                                    "enum": column_names,
                                }
                            },
                        },
                    },
                    AXIS: {
                        "type": "array",
                        "title": "Axis Selector",
                        DESCRIPTION: "change what column data is shown on a axis",
                        "items": {
                            "type": "object",
                            "required": [COLUMN_NAME, ENTRIES],
                            "additionalProperties": False,
                            PROPERTIES: {
                                COLUMN_NAME: {
                                    "type": "string",
                                    "description": "axis name",
                                    "pattern": ONE_LETTER,
                                },
                                ENTRIES: {
                                    "type": "array",
                                    "items": {"type": "string", "enum": column_names,},
                                },
                            },
                        },
                    },
                    GROUPBY: {
                        "type": "object",
                        "title": "Group By Selector",
                        "required": [ENTRIES],
                        "additionalProperties": False,
                        PROPERTIES: {
                            ENTRIES: {
                                "type": "array",
                                "items": {"type": "string", "enum": column_names},
                            },
                            "multiple": {"type": "boolean"},
                            DEFAULT_SELECTED: {
                                "type": "array",
                                "description": "default filter, list of column values",
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
    }
    return schema


def build_graphic_schema_with_plotly(data_source_names=None, column_names=None):
    """
    If you are using the app with plotly this puts the plotly schema into the graphic schema
    :param data_source_names:
    :param column_names:
    :return:
    """
    schema = build_graphic_schema(data_source_names, column_names)
    plotly_schema = build_plotly_schema(column_names)
    schema[PROPERTIES][PLOT_SPECIFIC_INFO] = plotly_schema
    return schema


def convert_python_dict_to_schema_json_file():
    """
    Makes the schema dictionaries into files (currently only used for generating documentation)
    :return:
    """
    for file_name, schema_dict in zip(
        ["main.schema.json", "graphic.schema.json"],
        [build_settings_schema(), build_graphic_schema_with_plotly()],
    ):
        json_object = json.dumps(schema_dict, indent=4)
        with open(file_name, "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    # if the schema is needed as a json file
    convert_python_dict_to_schema_json_file()
