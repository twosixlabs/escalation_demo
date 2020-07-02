from utility.constants import *


def build_schema():
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "escalation_config",
        "description": "config file needed to use escalation OS",
        "type": "object",
        "required": [
            SITE_TITLE,
            SITE_DESC,
            DATA_BACKEND,
            DATA_FILE_DIRECTORY,
            DATA_SOURCES,
            AVAILABLE_PAGES,
        ],
        "additionalProperties": False,
        "properties": {
            SITE_TITLE: {
                "type": "string",
                "description": "title shown at the top of the website",
            },
            SITE_DESC: {
                "type": "string",
                "description": "description shown at the top of the website",
            },
            DATA_BACKEND: {
                "type": "string",
                "description": "How the data is being managed on the server",
                "enum": [POSTGRES, MYSQL, LOCAL_CSV],
            },
            DATA_FILE_DIRECTORY: {
                "type": "string",
                "description": "Where the data is on the server",
            },
            DATA_SOURCES: {
                "type": "array",
                "description": "list of tables or folders that server will use for the plots",
                "items": {"type": "string"},
            },
            AVAILABLE_PAGES: {
                "type": "object",
                "additionalProperties": False,
                "patternProperties": {
                    ".*": {
                        "type": "object",
                        "required": [BUTTON_LABEL],
                        "properties": {
                            BUTTON_LABEL: {
                                "type": "string",
                                "description": "label on button that will show at the top of the website",
                            },
                            GRAPHICS: {
                                "type": "object",
                                "additionalProperties": False,
                                "patternProperties": {
                                    "^graphic_[0-9]*$": {
                                        "type": "object",
                                        "description": "graphic index use GRAPHIC_NUM.format(int)",
                                        "required": [
                                            PLOT_MANAGER,
                                            GRAPHIC_TITLE,
                                            GRAPHIC_DESC,
                                            DATA_SOURCES,
                                            DATA,
                                            PLOT_SPECIFIC_INFO,
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                            PLOT_MANAGER: {
                                                "type": "string",
                                                "description": "plot library you would like to use",
                                                "enum": ["plotly"],
                                            },
                                            GRAPHIC_TITLE: {
                                                "type": "string",
                                                "description": "title shown above the graph",
                                            },
                                            GRAPHIC_DESC: {
                                                "type": "string",
                                                "description": "description shown above the graph",
                                            },
                                            DATA_SOURCES: {
                                                "type": "array",
                                                "description": "What tables are use to define this graphic",
                                            },
                                            DATA: {
                                                "type": "object",
                                                "description": "contains which data goes on which plot",
                                                "additionalProperties": False,
                                                "patternProperties": {
                                                    "^points_[0-9]*$": {
                                                        "type": "object",
                                                        "description": "use POINTS_NUM.format(int) contians a dictionary: Key: axis (e.g.), Value: Data Column",
                                                    }
                                                },
                                            },
                                            PLOT_SPECIFIC_INFO: {
                                                "type": "object",
                                                "description": "this dictionary depends on the graphing library",
                                            },
                                            VISUALIZATION_OPTIONS: {
                                                "type": "array",
                                                "description": "modifications to the existing graph",
                                                "items": {
                                                    "type": "object",
                                                    "required": [
                                                        OPTION_TYPE,
                                                        COLUMN_NAME,
                                                    ],
                                                    "properties": {
                                                        OPTION_TYPE: {
                                                            "type": "string",
                                                            "enum": [
                                                                "hover_data",
                                                                "groupby",
                                                                "aggregate",
                                                            ],
                                                        },
                                                        COLUMN_NAME: {
                                                            "type": "array",
                                                            "items": {"type": "string"},
                                                        },
                                                        "options": {"type": "object"},
                                                    },
                                                },
                                            },
                                            SELECTABLE_DATA_LIST: {
                                                "type": "array",
                                                "description": "list of selectors per page",
                                                "maxItems": 6,
                                                "items": {
                                                    "type": "object",
                                                    "required": [
                                                        SELECTOR_TYPE,
                                                        COLUMN_NAME,
                                                    ],
                                                    "additionalProperties": True,  # cannot have false and if statements
                                                    "properties": {
                                                        SELECTOR_TYPE: {
                                                            "type": "string",
                                                            "enum": [
                                                                "select",
                                                                "numerical_filter",
                                                                "axis",
                                                            ],
                                                        },
                                                    },
                                                    "properties": {
                                                        COLUMN_NAME: {
                                                            "type": "string",
                                                            "description": "name in table (select, numerical_filter) or axis name (axis)",
                                                        },
                                                    },
                                                    "allOf": [
                                                        {
                                                            "if": {
                                                                "properties": {
                                                                    SELECTOR_TYPE: {
                                                                        "const": "select"
                                                                    }
                                                                }
                                                            },
                                                            "then": {
                                                                "required": [
                                                                    SELECT_OPTION
                                                                ],
                                                                "properties": {
                                                                    SELECT_OPTION: {
                                                                        "type": "object",
                                                                        "additionalProperties": False,
                                                                        "properties": {
                                                                            "multiple": {
                                                                                "type": "boolean"
                                                                            }
                                                                        },
                                                                    }
                                                                },
                                                            },
                                                        },
                                                        {
                                                            "if": {
                                                                "properties": {
                                                                    SELECTOR_TYPE: {
                                                                        "const": "axis"
                                                                    }
                                                                }
                                                            },
                                                            "then": {
                                                                "required": [
                                                                    SELECT_OPTION
                                                                ],
                                                                "properties": {
                                                                    SELECT_OPTION: {
                                                                        "type": "object",
                                                                        "additionalProperties": False,
                                                                        "properties": {
                                                                            "entries": {
                                                                                "type": "array"
                                                                            }
                                                                        },
                                                                    }
                                                                },
                                                            },
                                                        },
                                                    ],
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    }
                },
            },
        },
    }
    return schema


def build_plotly_schema():
    # todo: pull documentation from plotly website
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "plotly dict",
        "description": "what PLOT_SPECIFIC_INFO should look like if plot manager is plotly",
        "type": "object",
        "reqiured": [DATA],
        "properties": {
            DATA: {
                "type": "array",
                "description": "list of graphs to be plotted on a single plot, see https://plotly.com/javascript/reference/ for options, axis information is found from data property",
                "items": {"type": "object",},
            },
        },
    }
