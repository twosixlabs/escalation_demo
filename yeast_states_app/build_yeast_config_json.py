import json
from utility.constants import *


DEFAULT_EXPERIMENT = "YeastSTATES-CRISPR-Long-Duration-Time-Series-20191208"


config_dict = {
    SITE_TITLE: "Yeast States Escalation",
    SITE_DESC: "Demo for the Yeast States Escalation OS",
    DATA_BACKEND: POSTGRES,
    DATA_SOURCES: ["flow_meta", "flow_stat_wide", "growth_rate", "plate_reader"],
    AVAILABLE_PAGES: {
        "replicate_summary": {
            BUTTON_LABEL: "Data Converge Replicate Summary",
            "graphics": {
                "plate_reader_circuit_function": {
                    PLOT_MANAGER: "plotly",
                    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
                    GRAPHIC_TITLE: "Circuit function from plate reader",
                    GRAPHIC_DESC: "",
                    "data": {
                        "points_0": {
                            "y": "plate_reader:fluor_gain_0.16/od",
                            "x": "plate_reader:replicate_group",
                        },
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "scatter", "mode": "markers"}],
                        "layout": {"hovermode": "closest"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            COLUMN_NAME: [
                                "plate_reader:replicate_group_string",
                                "plate_reader:experiment_reference",
                            ],
                        },
                        {
                            "type": "groupby",
                            COLUMN_NAME: ["plate_reader:replicate_group"],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:experiment_reference",
                            SELECT_OPTION: {"multiple": True},
                            DEFAULT_SELECTED: DEFAULT_EXPERIMENT,
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:control_type",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:strain",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "axis",
                            OPTION_COL: "y",
                            SELECT_OPTION: {
                                "entries": [
                                    "plate_reader:fluor_gain_0.10/od",
                                    "plate_reader:fluor_gain_0.16/od",
                                    "plate_reader:fluor_gain_0.20/od",
                                ]
                            },
                        },
                    ],
                },
            },
        },
        "growth_summary": {
            BUTTON_LABEL: "Basic Growth Summary",
            "graphics": {
                "plate_reader_od": {
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
                        "layout": {"boxmode": "group"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            COLUMN_NAME: [
                                "plate_reader:well",
                                "plate_reader:sample_contents",
                                "plate_reader:experiment_reference",
                            ],
                        },
                        {
                            "type": "groupby",
                            COLUMN_NAME: ["plate_reader:sample_contents"],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:experiment_reference",
                            SELECT_OPTION: {"multiple": True},
                            DEFAULT_SELECTED: DEFAULT_EXPERIMENT,
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:control_type",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:strain",
                            SELECT_OPTION: {"multiple": True},
                        },
                    ],
                },
                "flow_cell_density": {
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
                            COLUMN_NAME: [
                                "flow_meta:well",
                                "flow_meta:replicate_group_string",
                                "flow_meta:date_of_experiment",
                            ],
                        },
                        {
                            "type": "groupby",
                            COLUMN_NAME: [
                                "flow_meta:well",
                                "flow_meta:experiment_id_short",
                            ],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:experiment_reference",
                            SELECT_OPTION: {"multiple": True},
                            DEFAULT_SELECTED: DEFAULT_EXPERIMENT,
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:control_type",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:strain",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:date_of_experiment",
                            SELECT_OPTION: {"multiple": True},
                        },
                    ],
                },
            },
        },
        "growth_curves": {
            BUTTON_LABEL: "Growth Rate Info",
            "graphics": {
                "growth_rate_plate_data": {
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
                            COLUMN_NAME: [
                                "plate_reader:well",
                                "plate_reader:strain",
                                "plate_reader:sample_contents",
                                "growth_rate:doubling_time",
                            ],
                        },
                        {"type": "groupby", COLUMN_NAME: ["plate_reader:well"]},
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:experiment_reference",
                            SELECT_OPTION: {"multiple": True},
                            DEFAULT_SELECTED: DEFAULT_EXPERIMENT,
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:control_type",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "plate_reader:strain",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            "type": "numerical_filter",
                            OPTION_COL: "growth_rate:doubling_time",
                        },
                    ],
                },
            },
        },
        "circuit_function_hist": {
            BUTTON_LABEL: "Circuit Function Histogram",
            GRAPHICS: {
                "flow_histogram": {
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
                        "layout": {"hovermode": "closest", "barmode": "group"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            COLUMN_NAME: [
                                "flow_meta:well",
                                "flow_meta:control_type",
                                "flow_meta:strain",
                                "flow_meta:experiment_id",
                                "growth_rate:doubling_time",
                            ],
                        },
                        {
                            "type": "groupby",
                            COLUMN_NAME: [
                                "flow_meta:well",
                                "flow_meta:experiment_id_short",
                            ],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:experiment_reference",
                            SELECT_OPTION: {"multiple": True},
                            DEFAULT_SELECTED: DEFAULT_EXPERIMENT,
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:strain",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:control_type",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            "type": "numerical_filter",
                            OPTION_COL: "growth_rate:doubling_time",
                        },
                    ],
                },
            },
        },
        "circuit_function_box": {
            BUTTON_LABEL: "Circuit Function Boxplot",
            GRAPHICS: {
                "flow_boxplot": {
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
                            "y": "flow_stat_wide:BL1H_mean_log10",
                            "x": "flow_meta:inducer_concentration",
                        }
                    },
                    PLOT_SPECIFIC_INFO: {
                        "data": [{"type": "box"}],
                        "layout": {"hovermode": "closest", "boxmode": "group"},
                    },
                    VISUALIZATION_OPTIONS: [
                        {
                            "type": "hover_data",
                            COLUMN_NAME: [
                                "growth_rate:doubling_time",
                                "flow_meta:inducer_type",
                            ],
                        },
                        {
                            "type": "groupby",
                            COLUMN_NAME: ["flow_meta:strain", "flow_meta:control_type"],
                        },
                    ],
                    SELECTABLE_DATA_LIST: [
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:experiment_reference",
                            SELECT_OPTION: {"multiple": True},
                            DEFAULT_SELECTED: DEFAULT_EXPERIMENT,
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:strain",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            SELECTOR_TYPE: "select",
                            OPTION_COL: "flow_meta:control_type",
                            SELECT_OPTION: {"multiple": True},
                        },
                        {
                            "type": "numerical_filter",
                            OPTION_COL: "growth_rate:doubling_time",
                        },
                        {
                            SELECTOR_TYPE: "axis",
                            OPTION_COL: "x",
                            SELECT_OPTION: {
                                "entries": [
                                    "flow_meta:timepoint",
                                    "flow_meta:inducer_concentration",
                                ]
                            },
                        },
                    ],
                },
            },
        },
    },
}

if __name__ == "__main__":
    # with open("../yeast_states_app/yeast_states_config.json", "w") as fout:
    with open("app_deploy_data/app_config.json", "w") as fout:
        json.dump(config_dict, fout, indent=4)
