import json
from utility.constants import *

config_dict = {
    "title": "Yeast States Escalation",
    "brief_desc": "This is a demo for the Yeast States Escalation OS",
    DATA_BACKEND: POSTGRES,
    DATA_SOURCES: ["flow_meta", "dose_response", "plate_reader"],
    AVAILABLE_PAGES: {
        "summary": {
            "button_label": "Data Converge Summary",
            "graphics": {
                "graphic_0": {
                    "plot_manager": "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
                    "title": "Growth data from plate reader",
                    "brief_desc": "",
                    "data": {
                        "points_0": {
                            "y": "plate_reader:od",
                            "x": "plate_reader:timepoint",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "box", "mode": "overlay"}],
                        # "data": [{"type": "scatter", "mode": "lines+markers"}],
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": ["plate_reader:well", "plate_reader:sample_id"],
                        },
                        {
                            "type": "groupby",
                            "column": ["plate_reader:replicate_group_string"],
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
                    "plot_manager": "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "flow_meta"}],
                    "title": "Growth data from flow",
                    "brief_desc": "",
                    "data": {
                        "points_0": {
                            "x": "flow_meta:timepoint",
                            "y": "flow_meta:cells/mL",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "flow_meta:well",
                                "flow_meta:replicate_group_string",
                            ],
                        },
                        {"type": "groupby", "column": ["flow_meta:well"]},
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
                    ],
                },
                "graphic_2": {
                    "plot_manager": "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
                    "title": "Circuit function data from plate reader",
                    "brief_desc": "",
                    "data": {
                        "points_0": {
                            "x": "plate_reader:timepoint",
                            "y": "plate_reader:fluor_gain_0.10/od",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
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
                                    "plate_reader:fluor_gain_0.10/od",
                                    "plate_reader:fluor_gain_0.16/od",
                                    "plate_reader:fluor_gain_0.20/od",
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
            "button_label": "Growth Curves",
            "graphics": {
                "graphic_0": {
                    "plot_manager": "plotly",
                    DATA_SOURCES: [
                        {DATA_SOURCE_TYPE: "plate_reader"},
                        {
                            DATA_SOURCE_TYPE: "dose_response",
                            LEFT_KEYS: ["well"],
                            RIGHT_KEYS: ["well"],
                        },
                    ],
                    "title": "Growth data from plate reader with rate calculations",
                    "brief_desc": "",
                    "data": {
                        "points_0": {
                            "y": "plate_reader:od",
                            "x": "plate_reader:timepoint",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": [
                                "plate_reader:well",
                                "plate_reader:strain",
                                "plate_reader:sample_id",
                                "dose_response:doubling_time",
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
                            "column": "dose_response:doubling_time",
                        },
                    ],
                },
            },
        },
        "circuit_function": {
            "button_label": "Circuit Function",
            "graphics": {
                "graphic_0": {
                    "plot_manager": "plotly",
                    DATA_SOURCES: [
                        {DATA_SOURCE_TYPE: "flow_meta"},
                        # {DATA_SOURCE_TYPE: "dose_response",
                        #  LEFT_KEYS: ["well"],
                        #  RIGHT_KEYS: ["well"]},
                        {
                            DATA_SOURCE_TYPE: "flow_stat",
                            LEFT_KEYS: ["aliquot_id"],
                            RIGHT_KEYS: ["aliquot_id"],
                        },
                    ],
                    "title": "Circuit function measured by flow fluorescence",
                    "brief_desc": "",
                    "data": {
                        "points_0": {
                            "y": "flow_stat:bin(log10)_0.05",
                            "x": "flow_meta:timepoint",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "lines+markers"}],
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            "column": ["flow_meta:well", "flow_meta:strain"],
                        },
                        {"type": "groupby", "column": ["flow_meta:well"]},
                    ],
                    # SELECTABLE_DATA_LIST: [
                    #     {
                    #         "type": "select",
                    #         "column": "plate_reader:control_type",
                    #         "options": {"multiple": True},
                    #     },
                    #     {
                    #         "type": "select",
                    #         "column": "plate_reader:strain",
                    #         "options": {"multiple": True},
                    #     },
                    #     {
                    #         "type": "numerical_filter",
                    #         "column": "dose_response:doubling_time"
                    #     }
                    # ]
                },
            },
        },
    },
}


if __name__ == "__main__":
    with open("yeast_states_app/yeast_states_config.json", "w") as fout:
        json.dump(config_dict, fout, indent=4)
