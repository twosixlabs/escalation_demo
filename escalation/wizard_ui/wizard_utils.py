import json
import os
import re

from flask import current_app, render_template, Blueprint, request

from utility.app_utilities import configure_backend
from utility.constants import (
    APP_CONFIG_JSON,
    CONFIG_FILE_FOLDER,
    MAIN_CONFIG,
    GRAPHIC,
    PLOTLY,
    SELECTOR,
    VISUALIZATION,
    VISUALIZATION_OPTIONS,
    SELECTABLE_DATA_DICT,
    PLOT_SPECIFIC_INFO,
    COLUMN_NAME,
    GROUPBY,
    ENTRIES,
    GRAPHIC_META_INFO,
    ADDITIONAL_DATA_SOURCES,
    DATA_SOURCES,
)

UI_SCHEMA_PAIRS = {
    VISUALIZATION: VISUALIZATION_OPTIONS,
    SELECTOR: SELECTABLE_DATA_DICT,
    PLOTLY: PLOT_SPECIFIC_INFO,
}


def set_up_backend_for_wizard(config_dict, app):
    # current app needs to have the config dict before calling configure backend
    app.config[APP_CONFIG_JSON] = config_dict
    # the first time the config_dict is made configured we need to get the data backend
    configure_backend(app)


def save_main_config_dict(config_dict):
    with open(
        os.path.join(current_app.config[CONFIG_FILE_FOLDER], MAIN_CONFIG), "w"
    ) as fout:
        json.dump(config_dict, fout, indent=4)


def load_main_config_dict_if_exists(app):
    try:
        with open(
            os.path.join(app.config[CONFIG_FILE_FOLDER], MAIN_CONFIG), "r"
        ) as config_file:
            config_dict = json.load(config_file)
        return config_dict
    except (OSError, IOError) as e:
        return {}


def load_graphic_config_dict(graphic):
    try:
        with open(
            os.path.join(current_app.config[CONFIG_FILE_FOLDER], graphic), "r"
        ) as fout:
            graphic_dict_json = fout.read()
    except (OSError, IOError) as e:
        graphic_dict_json = "{}"
    return graphic_dict_json


def sanitize_string(the_string):
    pattern = re.compile(r"\W+", re.UNICODE)
    return (pattern.sub("", the_string.replace(" ", "_"))).lower()


def invert_dict_lists(dict_to_invert):
    return {v: k for k, value_list in dict_to_invert.items() for v in value_list}


def graphic_dict_to_graphic_component_dict(graphic_dict):
    """
    change a graphic dictionary to components to be used by wizard ui
    which uses four separate forms.
    :param graphic_dict:
    :return:
    """
    component_dict = {}
    for ui_name, schema_name in UI_SCHEMA_PAIRS.items():
        component_dict[ui_name] = graphic_dict.pop(schema_name, {})
    component_dict[GRAPHIC_META_INFO] = graphic_dict
    return component_dict


def graphic_component_dict_to_graphic_dict(graphic_component_dict):
    """
    change the four dictionaries received from wizard ui into one graphic dictionary
    :param graphic_component_dict:
    :return:
    """
    graphic_dict = graphic_component_dict[GRAPHIC_META_INFO]
    if (
        ADDITIONAL_DATA_SOURCES in graphic_dict[DATA_SOURCES]
        and not graphic_dict[DATA_SOURCES][ADDITIONAL_DATA_SOURCES]
    ):
        del graphic_dict[DATA_SOURCES][ADDITIONAL_DATA_SOURCES]

    graphic_dict[PLOT_SPECIFIC_INFO] = graphic_component_dict[PLOTLY]

    visualization_dict = prune_visualization_dict(graphic_component_dict[VISUALIZATION])
    if visualization_dict:
        graphic_dict[VISUALIZATION_OPTIONS] = visualization_dict

    selector_dict = prune_selector_dict(graphic_component_dict[SELECTOR])
    if selector_dict:
        graphic_dict[SELECTABLE_DATA_DICT] = selector_dict

    return graphic_dict


def prune_visualization_dict(visualization_dict):
    """
    Get rid of empty entries in visualization dict
    :param visualization_dict:
    :return:
    """
    new_visualization_dict = {}
    # when the form is left blank the entries of visualization_dict have
    # COLUMN_NAME key that points to an empty list
    for vis_key, vis_dict in visualization_dict.items():
        if vis_dict[COLUMN_NAME]:
            new_visualization_dict[vis_key] = vis_dict
    return new_visualization_dict


def prune_selector_dict(selector_dict):
    """
        Get rid of empty entries in selector dict
        :param selector_dict:
        :return:
        """
    new_selector_dict = {}
    for sel_key, sel_info in selector_dict.items():
        if (sel_key == GROUPBY and sel_info[ENTRIES]) or (
            sel_key != GROUPBY and sel_info
        ):
            new_selector_dict[sel_key] = sel_info
    return new_selector_dict


def make_empty_component_dict():
    """
    mkaes an empty version of component dict to be used by wizard ui
    :return:
    """
    component_dict = {}
    for ui_name, schema_name in UI_SCHEMA_PAIRS.items():
        component_dict[ui_name] = {}
    component_dict[GRAPHIC_META_INFO] = {}
    return component_dict
