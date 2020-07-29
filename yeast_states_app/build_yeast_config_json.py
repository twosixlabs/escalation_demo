import json
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
    DATA: {"points_0": {"y": "flow_stat_wide:BL1-H", "x": "flow_stat_wide:log10_bin"}},
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "marker"}],
        LAYOUT: {"hovermode": "closest", HEIGHT: 700},
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: [
                "flow_meta:well",
                "flow_meta:strain_name",
                "flow_meta:experiment_id",
                "growth_rate:doubling_time",
            ],
        },
        {
            "type": "groupby",
            COLUMN_NAME: ["flow_meta:well", "flow_meta:experiment_id"],
        },
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:strain_name",
            SELECT_OPTION: {"multiple": True},
        },
        {SELECTOR_TYPE: "numerical_filter", OPTION_COL: "growth_rate:doubling_time"},
    ],
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
    DATA: {
        "points_0": {
            "y": "flow_stat_wide:BL1H_mean_log10",
            "x": "flow_meta:strain_name",
        }
    },
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box"}],
        LAYOUT: {
            "hovermode": "closest",
            "xaxis": {"automargin": True},
            "boxmode": "group",
            HEIGHT: 700,
        },
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: ["growth_rate:doubling_time", "flow_meta:inducer_type"],
        },
        {"type": "groupby", COLUMN_NAME: ["flow_meta:inducer_concentration"]},
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:timepoint",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:control_type",
            SELECT_OPTION: {"multiple": True},
        },
        {"type": "numerical_filter", OPTION_COL: "growth_rate:doubling_time"},
    ],
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
    DATA: {
        "points_0": {
            "y": "flow_stat_wide:BL1H_mean_log10",
            "x": "flow_meta:strain_name",
        }
    },
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box"}],
        LAYOUT: {
            "hovermode": "closest",
            "xaxis": {"automargin": True},
            "boxmode": "group",
            HEIGHT: 700,
        },
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: ["growth_rate:doubling_time", "flow_meta:inducer_type"],
        },
        {"type": "groupby", COLUMN_NAME: ["flow_meta:timepoint"]},
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:inducer_concentration",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:control_type",
            SELECT_OPTION: {"multiple": True},
        },
        {"type": "numerical_filter", OPTION_COL: "growth_rate:doubling_time"},
    ],
}


plate_reader_circuit_function = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
    GRAPHIC_TITLE: "Circuit function from plate reader",
    GRAPHIC_DESC: "The plots on this page are supposed to look at variance in outcome within an experiment",
    "data": {
        "points_0": {
            "y": "plate_reader:fluor_gain_0.16/od",
            "x": "plate_reader:strain_name",
        },
    },
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box", "mode": "group"}],
        LAYOUT: {"boxmode": "group", HEIGHT: 700, "xaxis": {"automargin": True}},
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: [
                "plate_reader:replicate_group_string",
                "plate_reader:strain",
                "plate_reader:experiment_reference",
            ],
        },
        {"type": "groupby", COLUMN_NAME: ["plate_reader:experiment_reference"]},
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:control_type",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
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
}


plate_reader_od = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [{DATA_SOURCE_TYPE: "plate_reader"}],
    GRAPHIC_TITLE: "Growth data from plate reader",
    GRAPHIC_DESC: "",
    "data": {"points_0": {"y": "plate_reader:od", "x": "plate_reader:timepoint",}},
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "box", "mode": "group"}],
        LAYOUT: {"boxmode": "group", HEIGHT: 700},
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
        {"type": "groupby", COLUMN_NAME: ["plate_reader:sample_contents"],},
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:control_type",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:strain",
            SELECT_OPTION: {"multiple": True},
        },
    ],
}

flow_cell_density = {
    PLOT_MANAGER: "plotly",
    DATA_SOURCES: [{DATA_SOURCE_TYPE: "flow_meta"}],
    GRAPHIC_TITLE: "Growth data from flow",
    GRAPHIC_DESC: "",
    "data": {"points_0": {"x": "flow_meta:timepoint", "y": "flow_meta:cells/mL",}},
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "lines+markers"}],
        LAYOUT: {"hovermode": "closest", HEIGHT: 700},
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
            COLUMN_NAME: ["flow_meta:well", "flow_meta:experiment_id"],
        },
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:control_type",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:strain",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "flow_meta:date_of_experiment",
            SELECT_OPTION: {"multiple": True},
        },
    ],
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
    "data": {"points_0": {"y": "plate_reader:od", "x": "plate_reader:timepoint",}},
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "lines+markers"}],
        LAYOUT: {"hovermode": "closest", "height": 700},
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: [
                "plate_reader:well",
                "plate_reader:strain",
                "plate_reader:sample_contents",
                "growth_rate:doubling_time",
                "plate_reader:inducer_concentration",
            ],
        },
        {
            "type": "groupby",
            COLUMN_NAME: [
                "plate_reader:inducer_concentration",
                "plate_reader:well",
                "plate_reader:experiment_id",
                "plate_reader:strain",
            ],
        },
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_LONG,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:control_type",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:well",
            SELECT_OPTION: {"multiple": True},
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "plate_reader:strain",
            SELECT_OPTION: {"multiple": True},
        },
        {"type": "numerical_filter", OPTION_COL: "growth_rate:doubling_time",},
    ],
}


inducer_diff_growth_rate = {
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
    "data": {
        "points_0": {
            "y": "fc_inducer_diff:wasserstein_median",
            "x": "fc_inducer_diff:strain",
        }
    },
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "markers"}],
        LAYOUT: {"hovermode": "closest", HEIGHT: 700, "xaxis": {"automargin": True}},
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: [
                "fc_inducer_diff:experiment_reference",
                "fc_inducer_diff:timepoint",
                "growth_rate:doubling_time",
                "growth_rate:well",
            ],
        },
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "fc_inducer_diff:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_SHORT,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "fc_inducer_diff:strain",
            SELECT_OPTION: {"multiple": True},
        },
        {"type": "numerical_filter", OPTION_COL: "growth_rate:doubling_time",},
        {"type": "numerical_filter", OPTION_COL: "fc_inducer_diff:wasserstein_median"},
        {
            SELECTOR_TYPE: "axis",
            OPTION_COL: "y",
            SELECT_OPTION: {
                "entries": [
                    "fc_inducer_diff:wasserstein_min",
                    "fc_inducer_diff:wasserstein_median",
                    "fc_inducer_diff:wasserstein_max",
                ]
            },
        },
    ],
}


time_diff_growth_rate = {
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
    "data": {
        "points_0": {
            "y": "fc_time_diff:wasserstein_median",
            "x": "fc_time_diff:strain",
        }
    },
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "markers"}],
        LAYOUT: {"hovermode": "closest", "height": 700, "xaxis": {"automargin": True}},
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: [
                "fc_time_diff:experiment_reference",
                "growth_rate:doubling_time",
                "fc_time_diff:well",
            ],
        },
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "fc_time_diff:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_SHORT,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "fc_time_diff:strain",
            SELECT_OPTION: {"multiple": True},
        },
        {"type": "numerical_filter", OPTION_COL: "growth_rate:doubling_time",},
        {"type": "numerical_filter", OPTION_COL: "fc_time_diff:wasserstein_median"},
        {
            SELECTOR_TYPE: "axis",
            OPTION_COL: "y",
            SELECT_OPTION: {
                "entries": [
                    "fc_time_diff:wasserstein_min",
                    "fc_time_diff:wasserstein_median",
                    "fc_time_diff:wasserstein_max",
                ]
            },
        },
    ],
}


growth_rates_vs_circuit_function = {
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
    "data": {
        "points_0": {
            "y": "fc_inducer_diff:wasserstein_median",
            "x": "growth_rate:doubling_time",
        }
    },
    PLOT_SPECIFIC_INFO: {
        "data": [{"type": "scatter", "mode": "markers"}],
        LAYOUT: {"hovermode": "closest"},
    },
    VISUALIZATION_OPTIONS: [
        {
            "type": "hover_data",
            COLUMN_NAME: [
                "fc_inducer_diff:experiment_reference",
                "fc_inducer_diff:timepoint",
                "fc_time_diff:inducer_concentration",
                "growth_rate:doubling_time",
                "growth_rate:well",
            ],
        },
        {
            "type": "groupby",
            COLUMN_NAME: ["growth_rate:strain", "growth_rate:experiment_id",],
        },
    ],
    SELECTABLE_DATA_DICT: [
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "fc_inducer_diff:experiment_reference",
            SELECT_OPTION: {"multiple": True},
            DEFAULT_SELECTED: DEFAULT_EXPERIMENT_SHORT,
            UNFILTERED_SELECTOR: True,
        },
        {
            SELECTOR_TYPE: FILTER,
            OPTION_COL: "fc_inducer_diff:strain",
            SELECT_OPTION: {"multiple": True},
        },
        {"type": "numerical_filter", OPTION_COL: "growth_rate:doubling_time",},
        {"type": "numerical_filter", OPTION_COL: "fc_inducer_diff:wasserstein_median",},
        {
            SELECTOR_TYPE: "axis",
            OPTION_COL: "y",
            SELECT_OPTION: {
                "entries": [
                    "fc_inducer_diff:wasserstein_min",
                    "fc_inducer_diff:wasserstein_median",
                    "fc_inducer_diff:wasserstein_max",
                ]
            },
        },
    ],
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
    AVAILABLE_PAGES: {
        "replicate_summary": {
            BUTTON_LABEL: "Data Converge Replicate Summary",
            GRAPHICS: {"plate_reader_circuit_function": plate_reader_circuit_function},
        },
        "growth_summary": {
            BUTTON_LABEL: "Raw Growth Observations",
            GRAPHICS: {
                "plate_reader_od": plate_reader_od,
                "flow_cell_density": flow_cell_density,
            },
        },
        "growth_curves": {
            BUTTON_LABEL: "Growth Rate",
            GRAPHICS: {"growth_rate_plate_data": growth_rate_plate_data},
        },
        "on_the_loop": {
            BUTTON_LABEL: "On the Loop Assistant",
            GRAPHICS: {
                "growth_rate_circuit_function_inducer_diff": inducer_diff_growth_rate,
                "growth_rate_circuit_function_time_diff": time_diff_growth_rate,
                "growth_rates_circuit_function": growth_rates_vs_circuit_function,
            },
        },
        "circuit_function": {
            BUTTON_LABEL: "Circuit Function Histogram",
            GRAPHICS: {
                "circuit_function_line": circuit_function_line,
                "flow_boxplot_inducer": flow_boxplot_inducer,
                "flow_boxplot_time": flow_boxplot_time,
            },
        },
    },
}


if __name__ == "__main__":
    # with open("../yeast_states_app/yeast_states_config.json", "w") as fout:
    with open("app_deploy_data/app_config.json", "w") as fout:
        json.dump(config_dict, fout, indent=4)
