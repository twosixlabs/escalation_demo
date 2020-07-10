import json
import os

from utility.constants import *


def build_config_json(data_backend, data_file_directory):
    config_dict = {
        SITE_TITLE: "Escalation Test",
        "brief_desc": "This is a test/demo for the Escalation OS",
        DATA_BACKEND: data_backend,
        DATA_FILE_DIRECTORY: data_file_directory,
        DATA_SOURCES: ["penguin_size", "mean_penguin_stat", "penguin_size_small"],
        "available_pages": {
            "penguins": {
                "button_label": "Penguins",
                "graphics": {
                    "graphic_0": {
                        "plot_manager": "plotly",
                        DATA_SOURCES: [{"data_source_type": "penguin_size"}],
                        "title": "Do massive penguins have long flippers?",
                        "brief_desc": "This plot looks at the relationship between...",
                        "data": {
                            "points_0": {
                                "x": "penguin_size:body_mass_g",
                                "y": "penguin_size:flipper_length_mm",
                            }
                        },
                        PLOT_SPECIFIC_INFO: {
                            "data": [{"type": "scatter", "mode": "markers"}]
                        },
                        "visualization_options": [
                            {
                                "type": "hover_data",
                                "column": [
                                    "penguin_size:sex",
                                    "penguin_size:culmen_length_mm",
                                ],
                            },
                            {
                                "type": "groupby",
                                "column": ["penguin_size:island", "penguin_size:sex"],
                            },
                        ],
                        SELECTABLE_DATA_LIST: [
                            {
                                "type": "select",
                                "column": "penguin_size:sex",
                                "options": {"multiple": False},
                            },
                            {
                                "type": "select",
                                "column": "penguin_size:island",
                                "options": {"multiple": True},
                            },
                            {
                                "type": "numerical_filter",
                                "column": "penguin_size:culmen_length_mm",
                            },
                        ],
                    },
                    "graphic_1": {
                        "plot_manager": "plotly",
                        DATA_SOURCES: [{"data_source_type": "penguin_size"}],
                        "title": "How big are penguins?",
                        "brief_desc": "",
                        "data": {"points_0": {"x": "penguin_size:body_mass_g"}},
                        "plot_specific_info": {
                            "data": [{"type": "histogram"}],
                            "layout": {
                                "xaxis": {"title": "body mass"},
                                "yaxis": {"title": "count"},
                            },
                        },
                        "selectable_data_list": [
                            {
                                "type": "axis",
                                "column": "x",
                                "options": {
                                    "entries": [
                                        "penguin_size:culmen_length_mm",
                                        "penguin_size:flipper_length_mm",
                                        "penguin_size:body_mass_g",
                                        "penguin_size:culmen_depth_mm",
                                    ]
                                },
                            }
                        ],
                    },
                },
            },
            "more_penguins": {
                "button_label": "More Penguins!",
                "graphics": {
                    "graphic_0": {
                        "plot_manager": "plotly",
                        DATA_SOURCES: [{"data_source_type": "penguin_size"}],
                        "title": "Do long nosed penguins have long flippers by sex (avg)?",
                        "brief_desc": "A plot",
                        "data": {
                            "points_0": {
                                "x": "penguin_size:culmen_length_mm",
                                "y": "penguin_size:flipper_length_mm",
                            }
                        },
                        "selectable_data_list": [
                            {
                                "type": "axis",
                                "column": "x",
                                "options": {
                                    "entries": [
                                        "penguin_size:culmen_length_mm",
                                        "penguin_size:flipper_length_mm",
                                        "penguin_size:body_mass_g",
                                        "penguin_size:culmen_depth_mm",
                                    ]
                                },
                            }
                        ],
                        VISUALIZATION_OPTIONS: [
                            {
                                "type": "aggregate",
                                "column": ["penguin_size:sex"],
                                "options": {"aggregations": {"x": "avg", "y": "avg"}},
                            },
                            {"type": "groupby", "column": ["penguin_size:sex"]},
                        ],
                        PLOT_SPECIFIC_INFO: {
                            "data": [{"type": "scatter", "mode": "markers"}]
                        },
                    }
                },
            },
            "radio_penguins": {
                BUTTON_LABEL: "Radioactive Penguins!",
                GRAPHICS: {
                    "graphic_0": {
                        "plot_manager": "plotly",
                        DATA_SOURCES: [
                            {"data_source_type": "penguin_size"},
                            {
                                "data_source_type": "mean_penguin_stat",
                                JOIN_KEYS: [
                                    (
                                        "penguin_size:study_name",
                                        "mean_penguin_stat:study_name",
                                    ),
                                    ("penguin_size:sex", "mean_penguin_stat:sex"),
                                    (
                                        "penguin_size:species",
                                        "mean_penguin_stat:species",
                                    ),
                                ],
                            },
                        ],
                        "title": "Can we join tables to find whether radio isotopes are connected to penguin size?",
                        "brief_desc": "A plot",
                        "data": {
                            "points_0": {
                                "x": "penguin_size:culmen_length_mm",
                                "y": "mean_penguin_stat:delta_15_n",
                            }
                        },
                        "selectable_data_list": [
                            {
                                "type": "axis",
                                "column": "x",
                                "options": {
                                    "entries": [
                                        "penguin_size:culmen_length_mm",
                                        "penguin_size:flipper_length_mm",
                                        "penguin_size:body_mass_g",
                                        "penguin_size:culmen_depth_mm",
                                    ]
                                },
                            },
                            {
                                "type": "axis",
                                "column": "y",
                                "options": {
                                    "entries": [
                                        "mean_penguin_stat:delta_15_n",
                                        "mean_penguin_stat:delta_13_c",
                                    ]
                                },
                            },
                        ],
                        VISUALIZATION_OPTIONS: [
                            {
                                "type": "aggregate",
                                "column": ["penguin_size:sex"],
                                "options": {"aggregations": {"x": "avg", "y": "avg"}},
                            },
                            {"type": "groupby", "column": ["penguin_size:sex"]},
                        ],
                        PLOT_SPECIFIC_INFO: {
                            "data": [{"type": "scatter", "mode": "markers"}]
                        },
                    }
                },
            },
        },
    }
    return config_dict


# todo: don't assume we're running the script from escos root directory?
if __name__ == "__main__":

    config_file_definitions = {
        "test_app_local_handler_config.json": {
            DATA_BACKEND: LOCAL_CSV,
            DATA_FILE_DIRECTORY: "tests/test_data/",
        },
        "test_sql_app_config.json": {DATA_BACKEND: POSTGRES, DATA_FILE_DIRECTORY: ""},
    }

    path_to_test_files = os.path.join("tests", "test_data")
    for config_file_name, config in config_file_definitions.items():
        config_dict = build_config_json(**config)
        test_config_file_path = os.path.join(path_to_test_files, config_file_name)
        with open(test_config_file_path, "w") as fout:
            json.dump(config_dict, fout, indent=4)
