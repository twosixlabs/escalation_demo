import json

from utility.constants import *

NO_DOTS = "^[^\\.]*$"
ALPHA_NUMERIC_NO_SPACES = "^[a-zA-Z0-9_]*$"
ONE_DOT = "^[^\\.]*\\.[^\\.]*$"
ONE_LETTER = "^[a-zA-Z]$"


def build_higher_level_schema(data_source_names=None, column_names=None):
    """
    :param data_source_names: names from DATA_SOURCES, already checked against the file system
    :param column_names: possible column names from files or database (format data_source_name.column_name)
    :return:
    """
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "Escalation Config File",
        "description": "config file needed to use escalation OS",
        "type": "object",
        "additionalProperties": True,
        "properties": {
            AVAILABLE_PAGES: {
                "type": "object",
                "title": "Dashboard Dictionary",
                "description": "a dictionary containing the dashboard pages of the site",
                "additionalProperties": False,
                "patternProperties": {
                    ALPHA_NUMERIC_NO_SPACES: {
                        "type": "object",
                        "title": "Dashboard Page",
                        "description": "Have one of these for each page of the site",
                        "required": [BUTTON_LABEL],
                        "properties": {
                            BUTTON_LABEL: {
                                "type": "string",
                                "description": "label of the page that will show up on the website",
                            },
                            GRAPHICS: {
                                "type": "object",
                                "title": "Graphics Dictionary",
                                "description": "a dictionary containing the graphics on the page",
                                "additionalProperties": False,
                                "patternProperties": {
                                    ALPHA_NUMERIC_NO_SPACES: {
                                        "type": "object",
                                        "title": "A single graphic",
                                        "description": "Have a unique one of these for each graphic on the page",
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
                                                "description": "plot library you would like to use,"
                                                " only plotly is currently available",
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
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        DATA_SOURCE_TYPE: {
                                                            "type": "string",
                                                            "enum": data_source_names,
                                                        }
                                                    },
                                                },
                                            },
                                            DATA: {
                                                "type": "object",
                                                "title": "Data Dictionary",
                                                "description": "which data column goes on each axis",
                                                "additionalProperties": False,
                                                "patternProperties": {
                                                    "^points_[0-9]*$": {
                                                        "type": "object",
                                                        "title": "points",
                                                        "description": "a dictionary for each plot on a single graph:"
                                                        " Key: axis (e.g. x), Value: Data Column,"
                                                        " use points_0 then points_1 etc.",
                                                        "patternProperties": {
                                                            ONE_LETTER: {
                                                                "type": "string",
                                                                "enum": column_names,
                                                            }
                                                        },
                                                    }
                                                },
                                            },
                                            PLOT_SPECIFIC_INFO: {
                                                "type": "object",
                                                "title": "Plot Dictionary",
                                                "description": "this dictionary depends on the graphing library",
                                            },
                                            VISUALIZATION_OPTIONS: {
                                                "type": "array",
                                                "title": "Visualization List",
                                                "description": "modifications to the existing graph",
                                                "items": {
                                                    "type": "object",
                                                    "title": "visualization dict",
                                                    "required": [
                                                        OPTION_TYPE,
                                                        COLUMN_NAME,
                                                    ],
                                                    "properties": {
                                                        OPTION_TYPE: {
                                                            "type": "string",
                                                            "description": "hover_data changes what data is shown"
                                                            " when scrolling over data. "
                                                            "examples of the other two:"
                                                            " groupby: https://plotly.com/javascript/group-by/"
                                                            " aggregate: https://plotly.com/javascript/aggregations/",
                                                            "enum": [
                                                                "hover_data",
                                                                "groupby",
                                                                "aggregate",
                                                            ],
                                                        },
                                                        COLUMN_NAME: {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "string",
                                                                "enum": column_names,
                                                            },
                                                        },
                                                        "options": {"type": "object"},
                                                    },
                                                },
                                            },
                                            SELECTABLE_DATA_LIST: {
                                                "type": "array",
                                                "title": "Selector List",
                                                "description": "list of data selectors for a graphic",
                                                "maxItems": 6,
                                                "items": {
                                                    "type": "object",
                                                    "title": "Selector Dict",
                                                    "required": [
                                                        SELECTOR_TYPE,
                                                        COLUMN_NAME,
                                                    ],
                                                    "additionalProperties": True,  # cannot have false and if statements
                                                    "properties": {
                                                        SELECTOR_TYPE: {
                                                            "type": "string",
                                                            "description": "select is a filter operation based on label,"
                                                            "numerical_filter is a filter operation"
                                                            " on numerical data,"
                                                            "axis you can use to change what column data "
                                                            "is shown on a axis",
                                                            "enum": [
                                                                "select",
                                                                "numerical_filter",
                                                                "axis",
                                                            ],
                                                        },
                                                    },
                                                    "if": {
                                                        "properties": {
                                                            SELECTOR_TYPE: {
                                                                "const": "axis"
                                                            }
                                                        }
                                                    },
                                                    "then": {
                                                        "properties": {
                                                            COLUMN_NAME: {
                                                                "type": "string",
                                                                "description": "name in table (select, numerical_filter) or axis name (axis)",
                                                                "pattern": ONE_LETTER,
                                                            },
                                                        },
                                                    },
                                                    "else": {
                                                        "properties": {
                                                            COLUMN_NAME: {
                                                                "type": "string",
                                                                "description": "name in table (select, numerical_filter) or axis name (axis)",
                                                                "enum": column_names,
                                                            },
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
                                                                                "type": "array",
                                                                                "items": {
                                                                                    "type": "string",
                                                                                    "enum": column_names,
                                                                                },
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


def build_first_level_schema():
    """
    :param data_source_names: names from DATA_SOURCES, already checked against the file system
    :param column_names: possible column names from files or database (format data_source_name.column_name)
    :return:
    """
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
            AVAILABLE_PAGES: {"type": "object"},
        },
    }
    return schema


def convert_dict_to_json_file():
    schema_dict = build_first_level_schema()
    schema_dict["properties"].update(build_higher_level_schema()["properties"])
    json_object = json.dumps(schema_dict, indent=4)
    with open("escos.schema.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    # if the schema is needed as a json file
    convert_dict_to_json_file()
