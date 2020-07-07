import json
from utility.constants import *

config_dict = {
    SITE_TITLE: "Yeast States Escalation",
    SITE_DESC: "Demo for the Yeast States Escalation OS",
    DATA_BACKEND: POSTGRES,
    DATA_SOURCES: [
        "flow_meta",
        "flow_stat",
        "flow_stat_wide",
        "growth_rate",
        "plate_reader",
    ],
    AVAILABLE_PAGES: {
        "summary": {
            BUTTON_LABEL: "Data Converge Summary",
            "graphics": {
                "graphic_0": {
                    PLOT_MANAGER: "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
                    GRAPHIC_TITLE: "Growth data from plate reader",
                    GRAPHIC_DESC: "",
                    "data": {
                        "points_0": {
                            "y": "plate_reader:od",
                            "x": "plate_reader:timepoint",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "box", "mode": "group"}],
                        # "data": [{"type": "scatter", "mode": "lines+markers"}],
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "plate_reader:well",
                                "plate_reader:sample_contents",
                            ],
                        },
                        {
                            "type": "groupby",
                            "column": ["plate_reader:sample_contents"],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            "type": "select",
                            "column": "plate_reader:control_type",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "plate_reader:strain",
                            "options": {"multiple": True},
                        },
                    ],
                },
                "graphic_1": {
                    PLOT_MANAGER: "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "flow_meta"}],
                    GRAPHIC_TITLE: "Growth data from flow",
                    GRAPHIC_DESC: "",
                    "data": {
                        "points_0": {
                            "x": "flow_meta:timepoint",
                            "y": "flow_meta:cells/mL",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
                        "layout": {"hovermode": "closest"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "flow_meta:well",
                                "flow_meta:replicate_group_string",
                                "flow_meta:date_of_experiment",
                            ],
                        },
                        {
                            "type": "groupby",
                            "column": [
                                "flow_meta:well",
                                "flow_meta:experiment_id_short",
                            ],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            "type": "select",
                            "column": "flow_meta:control_type",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "flow_meta:strain",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "flow_meta:date_of_experiment",
                            "options": {"multiple": True},
                        },
                    ],
                },
                "graphic_2": {
                    PLOT_MANAGER: "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
                    GRAPHIC_TITLE: "Circuit function data from plate reader",
                    GRAPHIC_DESC: "",
                    "data": {
                        "points_0": {
                            "x": "plate_reader:timepoint",
                            "y": "plate_reader:fluor_gain_0.16/od",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
                        "layout": {"hovermode": "closest"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "plate_reader:well",
                                "plate_reader:replicate_group_string",
                            ],
                        },
                        {"type": "groupby", "column": ["plate_reader:well"]},
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            "type": "select",
                            "column": "plate_reader:control_type",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "plate_reader:strain",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "axis",
                            "column": "y",
                            "options": {
                                "entries": [
                                    # "plate_reader:fluor_gain_0.10/od", # todo: these aren't all present in individual csv uploads. e.g., not NovelChassis-OR-Circuit-Cycle0-24hour__platereader.csv
                                    "plate_reader:fluor_gain_0.16/od",
                                    # "plate_reader:fluor_gain_0.20/od",
                                ]
                            },
                        },
                        {
                            "type": "axis",
                            "column": "x",
                            "options": {
                                "entries": [
                                    "plate_reader:timepoint",
                                    "plate_reader:inducer_concentration",
                                ]
                            },
                        },
                    ],
                },
            },
        },
        "growth_curves": {
            BUTTON_LABEL: "Growth Curves",
            "graphics": {
                "graphic_0": {
                    PLOT_MANAGER: "plotly",
                    DATA_SOURCES: [
                        {DATA_SOURCE_TYPE: "plate_reader"},
                        {
                            DATA_SOURCE_TYPE: "growth_rate",
                            JOIN_KEYS: [("plate_reader:well", "growth_rate:well")],
                        },
                    ],
                    GRAPHIC_TITLE: "Growth data from plate reader with rate calculations",
                    GRAPHIC_DESC: "",
                    "data": {
                        "points_0": {
                            "y": "plate_reader:od",
                            "x": "plate_reader:timepoint",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
                        "layout": {"hovermode": "closest"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "plate_reader:well",
                                "plate_reader:strain",
                                "plate_reader:sample_contents",
                                "growth_rate:doubling_time",
                            ],
                        },
                        {"type": "groupby", "column": ["plate_reader:well"]},
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            "type": "select",
                            "column": "plate_reader:control_type",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "plate_reader:strain",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "numerical_filter",
                            "column": "growth_rate:doubling_time",
                        },
                    ],
                },
            },
        },
        "circuit_function": {
            BUTTON_LABEL: "Circuit Function",
            GRAPHICS: {
                "graphic_0": {
                    PLOT_MANAGER: "plotly",
                    DATA_SOURCES: [
                        {DATA_SOURCE_TYPE: "flow_meta"},
                        {
                            DATA_SOURCE_TYPE: "flow_stat_wide",
                            JOIN_KEYS: [
                                ("flow_meta:aliquot_id", "flow_stat_wide:aliquot_id")
                            ],
                        },
                        {
                            DATA_SOURCE_TYPE: "growth_rate",
                            # todo: this isn't the right join
                            JOIN_KEYS: [
                                (
                                    "flow_meta:experiment_id_short",
                                    "growth_rate:experiment_id",
                                ),
                                ("flow_meta:well", "growth_rate:well"),
                            ],
                        },
                    ],
                    GRAPHIC_TITLE: "Circuit function measured by flow fluorescence",
                    GRAPHIC_DESC: "",
                    DATA: {
                        "points_0": {
                            "y": "flow_stat_wide:BL1-H",
                            "x": "flow_stat_wide:log10_bin",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "bar"}],
                        "layout": {
                            "hovermode": "closest",
                            "barmode": "stack",
                            "opacity": 0.5,
                        },
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "flow_meta:well",
                                "flow_meta:control_type",
                                "flow_meta:strain",
                                "flow_meta:experiment_id",
                                "growth_rate:doubling_time",
                            ],
                        },
                        {
                            "type": "groupby",
                            "column": [
                                "flow_meta:well",
                                "flow_meta:experiment_id_short",
                            ],  # todo: is this actually grouping by both and just showing 1?
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            "type": "select",
                            "column": "flow_meta:strain",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "flow_meta:control_type",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "select",
                            "column": "flow_meta:date_of_experiment",
                            "options": {"multiple": True},
                        },
                        {
                            "type": "numerical_filter",
                            "column": "growth_rate:doubling_time",
                        },
                    ],
                },
            },
        },
    },
}

if __name__ == "__main__":
    with open("yeast_states_app/yeast_states_config.json", "w") as fout:
        json.dump(config_dict, fout, indent=4)
