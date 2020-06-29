import json
import os

from utility.constants import DATA_BACKEND, POSTGRES, LOCAL_CSV


def build_config_json(data_backend):
    config_dict = {
        "title": "Escalation Test",
        "brief_desc": "This is a test/demo for the Escalation OS",
        "data_backend": data_backend,
        "available_pages": {
            "penguins": {
                "button_label": "Penguins",
                "graphics": {
                    "graphic_0": {
                        "plot_manager": "plotly",
                        "data_sources": [{"data_source_type": "penguin_size"}],
                        "title": "Do massive penguins have long flippers?",
                        "brief_desc": "This plot looks at the relationship between...",
                        "data": {
                            "points_0": {"x": "body_mass_g", "y": "flipper_length_mm"}
                        },
                        "plot_specific_info": {
                            "data": [{"type": "scatter", "mode": "markers"}]
                        },
                        "visualization_options": [
                            {
                                "type": "hover_data",
                                "column": ["sex", "culmen_length_mm"],
                            },
                            {
                                "type": "groupby",
                                "column": ["island"],
                                "options": {
                                    "styles": {
                                        "Torgersen": {"marker": {"color": "green"}},
                                        "Biscoe": {"marker": {"color": "blue"}},
                                        "Dream": {"marker": {"color": "red"}},
                                    }
                                },
                            },
                        ],
                        "selectable_data_list": [
                            {
                                "type": "select",
                                "column": "sex",
                                "options": {"multiple": False},
                            },
                            {
                                "type": "select",
                                "column": "island",
                                "options": {"multiple": True},
                            },
                            {"type": "numerical_filter", "column": "culmen_length_mm"},
                        ],
                    },
                    "graphic_1": {
                        "plot_manager": "plotly",
                        "data_sources": [{"data_source_type": "penguin_size"}],
                        "title": "How big are penguins?",
                        "brief_desc": "",
                        "data": {"points_0": {"x": "body_mass_g"}},
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
                                        "culmen_length_mm",
                                        "flipper_length_mm",
                                        "body_mass_g",
                                        "culmen_depth_mm",
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
                        "data_sources": [{"data_source_type": "penguin_size"}],
                        "title": "Do long nosed penguins have long flippers by sex (avg)?",
                        "brief_desc": "A plot",
                        "data": [{"x": "culmen_length_mm", "y": "flipper_length_mm"}],
                        "selectable_data_list": [
                            {
                                "type": "axis",
                                "column": "x",
                                "options": {
                                    "entries": [
                                        "culmen_length_mm",
                                        "flipper_length_mm",
                                        "body_mass_g",
                                        "culmen_depth_mm",
                                    ]
                                },
                            }
                        ],
                        "visualization_options": [
                            {
                                "type": "aggregate",
                                "columns": ["sex"],
                                "options": {"aggregations": {"x": "avg", "y": "avg"}},
                            },
                            {"type": "groupby", "columns": ["sex"]},
                        ],
                        "plot_options": {
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
        "test_app_config.json": {DATA_BACKEND: POSTGRES},
        "test_sql_app_config.json": {DATA_BACKEND: LOCAL_CSV},
    }

    path_to_test_files = os.path.join("tests", "test_data")
    for config_file_name, config in config_file_definitions.items():
        config_dict = build_config_json(**config)
        test_config_file_path = os.path.join(path_to_test_files, config_file_name)
        with open(test_config_file_path, "w") as fout:
            json.dump(config_dict, fout, indent=4)
