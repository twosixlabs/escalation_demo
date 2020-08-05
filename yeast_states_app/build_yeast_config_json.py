import json
import os
from utility.constants import *


DEFAULT_EXPERIMENT_LONG = "YeastSTATES-CRISPR-Long-Duration-Time-Series-20191208"
DEFAULT_EXPERIMENT_SHORT = "YeastSTATES-CRISPR-Short-Duration-Time-Series-35C"


circuit_function_line = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "flow_meta"},
        {
            DATA_SOURCE_TYPE: "flow_stat_wide",
            JOIN_KEYS: [("flow_meta:aliquot_id", "flow_stat_wide:aliquot_id")],
        },
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                ("flow_meta:experiment_id", "growth_rate:experiment_id_long",),
                ("flow_meta:well", "growth_rate:well"),
            ],
        },
    ],
    GRAPHIC_TITLE: "Circuit function measured by flow fluorescence",
    GRAPHIC_DESC: "",
    DATA: [{"y": "flow_stat_wide:BL1-H", "x": "flow_stat_wide:log10_bin"}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "marker"}],
        LAYOUT: {"hovermode": "closest", HEIGHT: 700},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "flow_meta:well",
                "flow_meta:strain_name",
                "flow_meta:experiment_id",
                "growth_rate:doubling_time",
            ],
        },
        GROUPBY: {COLUMN_NAME: ["flow_meta:well", "flow_meta:experiment_id"],},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "flow_meta:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {OPTION_COL: "flow_meta:strain_name", "multiple": True},
        ],
        NUMERICAL_FILTER: [{OPTION_COL: "growth_rate:doubling_time"}],
    },
}

flow_boxplot_inducer = {
    GRAPHIC_TITLE: "Circuit function across inducer concentration measured by flow fluorescence",
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "flow_meta"},
        {
            DATA_SOURCE_TYPE: "flow_stat_wide",
            JOIN_KEYS: [("flow_meta:aliquot_id", "flow_stat_wide:aliquot_id")],
        },
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                ("flow_meta:experiment_id", "growth_rate:experiment_id_long",),
                ("flow_meta:well", "growth_rate:well"),
            ],
        },
    ],
    GRAPHIC_DESC: "",
    DATA: [{"y": "flow_stat_wide:BL1H_mean_log10", "x": "flow_meta:strain_name",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box"}],
        LAYOUT: {
            "hovermode": "closest",
            "xaxis": {"automargin": True},
            "boxmode": "group",
            HEIGHT: 700,
        },
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: ["growth_rate:doubling_time", "flow_meta:inducer_type"],
        },
        GROUPBY: {COLUMN_NAME: ["flow_meta:inducer_concentration"]},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {OPTION_COL: "flow_meta:control_type", "multiple": True,},
            {OPTION_COL: "flow_meta:timepoint", "multiple": True,},
            {
                OPTION_COL: "flow_meta:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
        ],
        NUMERICAL_FILTER: [{OPTION_COL: "growth_rate:doubling_time"}],
    },
}


flow_boxplot_time = {
    GRAPHIC_TITLE: "Circuit function across time measured by flow fluorescence",
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "flow_meta"},
        {
            DATA_SOURCE_TYPE: "flow_stat_wide",
            JOIN_KEYS: [("flow_meta:aliquot_id", "flow_stat_wide:aliquot_id")],
        },
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                ("flow_meta:experiment_id", "growth_rate:experiment_id_long",),
                ("flow_meta:well", "growth_rate:well"),
            ],
        },
    ],
    GRAPHIC_DESC: "",
    DATA: [{"y": "flow_stat_wide:BL1H_mean_log10", "x": "flow_meta:strain_name",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box"}],
        LAYOUT: {
            "hovermode": "closest",
            "xaxis": {"automargin": True},
            "boxmode": "group",
            HEIGHT: 700,
        },
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: ["growth_rate:doubling_time", "flow_meta:inducer_type"],
        },
        GROUPBY: {COLUMN_NAME: ["flow_meta:timepoint"]},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "flow_meta:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {
                OPTION_COL: "flow_meta:inducer_concentration",
                "multiple": True,
            },
            {OPTION_COL: "flow_meta:control_type", "multiple": True,},
        ],
        NUMERICAL_FILTER: [{OPTION_COL: "growth_rate:doubling_time"}],
    },
}


plate_reader_circuit_function = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
    GRAPHIC_TITLE: "Circuit function from plate reader",
    GRAPHIC_DESC: "The plots on this page are supposed to look at variance in outcome within an experiment",
    DATA: [{"y": "plate_reader:fluor_gain_0.16/od", "x": "plate_reader:strain_name",},],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box", "mode": "group"}],
        LAYOUT: {"boxmode": "group", HEIGHT: 700, "xaxis": {"automargin": True}},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "plate_reader:replicate_group_string",
                "plate_reader:strain",
                "plate_reader:experiment_reference",
            ],
        },
        GROUPBY: {COLUMN_NAME: ["plate_reader:experiment_reference"]},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "plate_reader:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {
                OPTION_COL: "plate_reader:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {
                OPTION_COL: "plate_reader:control_type",
                "multiple": True,
            },
            {OPTION_COL: "plate_reader:strain", "multiple": True,},
        ],
        AXIS:[
                {
                OPTION_COL: "y",
                "entries": [
                    "plate_reader:fluor_gain_0.10/od",
                    "plate_reader:fluor_gain_0.16/od",
                    "plate_reader:fluor_gain_0.20/od",
                ]
            },
        ]
    },
}


plate_reader_od = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
    GRAPHIC_TITLE: "Growth data from plate reader",
    GRAPHIC_DESC: "",
    DATA: [{"y": "plate_reader:od", "x": "plate_reader:timepoint",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box", "mode": "group"}],
        LAYOUT: {"boxmode": "group", HEIGHT: 700},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "plate_reader:well",
                "plate_reader:sample_contents",
                "plate_reader:experiment_reference",
            ],
        },
        GROUPBY: {COLUMN_NAME: ["plate_reader:sample_contents"],},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "plate_reader:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {
                OPTION_COL: "plate_reader:control_type",
                "multiple": True,
            },
            {OPTION_COL: "plate_reader:strain", "multiple": True,},
        ],
    },
}

flow_cell_density = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [{DATA_SOURCE_TYPE: "flow_meta"}],
    GRAPHIC_TITLE: "Growth data from flow",
    GRAPHIC_DESC: "",
    DATA: [{"x": "flow_meta:timepoint", "y": "flow_meta:cells/mL",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "lines+markers"}],
        LAYOUT: {"hovermode": "closest", HEIGHT: 700},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "flow_meta:well",
                "flow_meta:replicate_group_string",
                "flow_meta:date_of_experiment",
            ],
        },
        GROUPBY: {COLUMN_NAME: ["flow_meta:well", "flow_meta:experiment_id"],},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "flow_meta:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {OPTION_COL: "flow_meta:control_type", "multiple": True,},
            {OPTION_COL: "flow_meta:strain", "multiple": True,},
            {
                OPTION_COL: "flow_meta:date_of_experiment",
                "multiple": True,
            },
        ]
    },
}


growth_rate_plate_data = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "plate_reader"},
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                ("plate_reader:well", "growth_rate:well"),
                ("plate_reader:experiment_id", "growth_rate:experiment_id_long",),
                ("plate_reader:strain", "growth_rate:strain"),
            ],
        },
    ],
    GRAPHIC_TITLE: "Growth data from plate reader with rate calculations",
    GRAPHIC_DESC: "",
    DATA: [{"y": "plate_reader:od", "x": "plate_reader:timepoint",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "lines+markers"}],
        LAYOUT: {"hovermode": "closest", "height": 700},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "plate_reader:well",
                "plate_reader:strain",
                "plate_reader:sample_contents",
                "growth_rate:doubling_time",
                "plate_reader:inducer_concentration",
            ],
        },
        GROUPBY: {
            COLUMN_NAME: [
                "plate_reader:inducer_concentration",
                "plate_reader:well",
                "plate_reader:experiment_id",
                "plate_reader:strain",
            ],
        },
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "plate_reader:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_LONG],
                UNFILTERED_SELECTOR: True,
            },
            {
                OPTION_COL: "plate_reader:control_type",
                "multiple": True,
            },
            {OPTION_COL: "plate_reader:well", "multiple": True,},
            {OPTION_COL: "plate_reader:strain", "multiple": True,},
        ],
        NUMERICAL_FILTER: [{OPTION_COL: "growth_rate:doubling_time", }],
    },
}


growth_rate_circuit_function_inducer_diff = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "fc_inducer_diff"},
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                (
                    "fc_inducer_diff:experiment_reference",
                    "growth_rate:experiment_reference",
                ),
                ("fc_inducer_diff:experiment_id", "growth_rate:experiment_id_long",),
                ("fc_inducer_diff:strain", "growth_rate:strain"),
            ],
        },
    ],
    GRAPHIC_TITLE: "Fluorescence fold change by inducer",
    GRAPHIC_DESC: "",
    DATA: [{"y": "fc_inducer_diff:wasserstein_median", "x": "fc_inducer_diff:strain",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "markers"}],
        LAYOUT: {"hovermode": "closest", HEIGHT: 700, "xaxis": {"automargin": True}},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "fc_inducer_diff:experiment_reference",
                "fc_inducer_diff:timepoint",
                "growth_rate:doubling_time",
                "growth_rate:well",
            ],
        },
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "fc_inducer_diff:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_SHORT],
                UNFILTERED_SELECTOR: True,
            },
            {OPTION_COL: "fc_inducer_diff:strain", "multiple": True,},
        ],
        NUMERICAL_FILTER: [
            {OPTION_COL: "growth_rate:doubling_time",},
            {OPTION_COL: "fc_inducer_diff:wasserstein_median"},
        ],
        AXIS:[
            {
                OPTION_COL: "y",
                "entries": [
                    "fc_inducer_diff:wasserstein_min",
                    "fc_inducer_diff:wasserstein_median",
                    "fc_inducer_diff:wasserstein_max",
                ]
            },
        ]
    },
}


growth_rate_circuit_function_time_diff = {
    GRAPHIC_TITLE: "Fluorescence fold change over time",
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "fc_time_diff"},
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                (
                    "fc_time_diff:experiment_reference",
                    "growth_rate:experiment_reference",
                ),
                ("fc_time_diff:experiment_id", "growth_rate:experiment_id_long",),
                ("fc_time_diff:strain", "growth_rate:strain"),
            ],
        },
    ],
    GRAPHIC_DESC: "",
    DATA: [{"y": "fc_time_diff:wasserstein_median", "x": "fc_time_diff:strain",}],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "markers"}],
        LAYOUT: {"hovermode": "closest", "height": 700, "xaxis": {"automargin": True}},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "fc_time_diff:experiment_reference",
                "growth_rate:doubling_time",
                "fc_time_diff:well",
            ],
        },
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "fc_time_diff:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_SHORT],
                UNFILTERED_SELECTOR: True,
            },
            {OPTION_COL: "fc_time_diff:strain", "multiple": True,},
        ],
        NUMERICAL_FILTER: [
            {OPTION_COL: "growth_rate:doubling_time",},
            {OPTION_COL: "fc_time_diff:wasserstein_median"},
        ],
        AXIS: [
            {
                OPTION_COL: "y",
                "entries": [
                    "fc_time_diff:wasserstein_min",
                    "fc_time_diff:wasserstein_median",
                    "fc_time_diff:wasserstein_max",
                ]
            },
        ]
    },
}


growth_rates_circuit_function = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [
        {DATA_SOURCE_TYPE: "fc_inducer_diff"},
        {
            DATA_SOURCE_TYPE: "fc_time_diff",
            JOIN_KEYS: [
                (
                    "fc_inducer_diff:experiment_reference",
                    "fc_time_diff:experiment_reference",
                ),
                ("fc_inducer_diff:experiment_id", "fc_time_diff:experiment_id",),
                ("fc_inducer_diff:strain", "fc_time_diff:strain"),
            ],
        },
        {
            DATA_SOURCE_TYPE: "growth_rate",
            JOIN_KEYS: [
                ("fc_time_diff:well", "growth_rate:well"),
                ("fc_time_diff:experiment_id", "growth_rate:experiment_id_long",),
                ("fc_time_diff:strain", "growth_rate:strain"),
            ],
        },
    ],
    GRAPHIC_TITLE: "Growth rate vs Fluorescence fold change",
    GRAPHIC_DESC: "",
    DATA: [
        {"y": "fc_inducer_diff:wasserstein_median", "x": "growth_rate:doubling_time",}
    ],
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "markers"}],
        LAYOUT: {"hovermode": "closest"},
    },
    VISUALIZATION_OPTIONS: {
        HOVER_DATA: {
            COLUMN_NAME: [
                "fc_inducer_diff:experiment_reference",
                "fc_inducer_diff:timepoint",
                "fc_time_diff:inducer_concentration",
                "growth_rate:doubling_time",
                "growth_rate:well",
            ],
        },
        GROUPBY: {COLUMN_NAME: ["growth_rate:strain", "growth_rate:experiment_id",],},
    },
    SELECTABLE_DATA_DICT: {
        FILTER: [
            {
                OPTION_COL: "fc_inducer_diff:experiment_reference",
                "multiple": True,
                DEFAULT_SELECTED: [DEFAULT_EXPERIMENT_SHORT],
                UNFILTERED_SELECTOR: True,
            },
            {OPTION_COL: "fc_inducer_diff:strain", "multiple": True,},
        ],
        NUMERICAL_FILTER: [
            {OPTION_COL: "growth_rate:doubling_time",},
            {OPTION_COL: "fc_inducer_diff:wasserstein_median",},
        ],
        AXIS:[
            {
                OPTION_COL: "y",

                "entries": [
                    "fc_inducer_diff:wasserstein_min",
                    "fc_inducer_diff:wasserstein_median",
                    "fc_inducer_diff:wasserstein_max",
                ]
            },
        ]
    },
}


config_dict = {
    SITE_TITLE: "Yeast States Escalation",
    SITE_DESC: "Demo for the Yeast States Escalation OS",
    DATA_BACKEND: POSTGRES,
    DATA_SOURCES: [
        "flow_meta",
        "flow_stat_wide",
        "growth_rate",
        "plate_reader",
        "fc_inducer_diff",
        "fc_time_diff",
    ],
    AVAILABLE_PAGES: [
        {
            WEBPAGE_LABEL: "Data Converge Replicate Summary",
            URL_ENDPOINT: "replicate_summary",
            GRAPHIC_CONFIG_FILES: ["plate_reader_circuit_function.json"],
        },
        {
            WEBPAGE_LABEL: "Raw Growth Observations",
            URL_ENDPOINT: "growth_summary",
            GRAPHIC_CONFIG_FILES: ["plate_reader_od.json", "flow_cell_density.json"],
        },
        {
            WEBPAGE_LABEL: "Growth Rate",
            URL_ENDPOINT: "growth_curves",
            GRAPHIC_CONFIG_FILES: ["growth_rate_plate_data.json"],
        },
        {
            WEBPAGE_LABEL: "On the Loop Assistant",
            URL_ENDPOINT: "on_the_loop",
            GRAPHIC_CONFIG_FILES: [
                "growth_rate_circuit_function_inducer_diff.json",
                "growth_rate_circuit_function_time_diff.json",
                "growth_rates_circuit_function.json",
            ],
        },
        {
            WEBPAGE_LABEL: "Circuit Function Histogram",
            URL_ENDPOINT: "circuit_function",
            GRAPHIC_CONFIG_FILES: [
                "circuit_function_line.json",
                "flow_boxplot_inducer.json",
                "flow_boxplot_time.json",
            ],
        },
    ],
}


if __name__ == "__main__":
    # with open("../yeast_states_app/yeast_states_config.json", "w") as fout:
    with open(os.path.join("app_deploy_data", "app_config.json"), "w") as fout:
        json.dump(config_dict, fout, indent=4)
    for page in config_dict[AVAILABLE_PAGES]:
        for graphic_config_filename in page[GRAPHIC_CONFIG_FILES]:
            print(graphic_config_filename)
            graphic_config_dict = locals()[graphic_config_filename.replace(".json", "")]

            with open(
                os.path.join("app_deploy_data", graphic_config_filename), "w"
            ) as fout:
                json.dump(graphic_config_dict, fout, indent=4)
