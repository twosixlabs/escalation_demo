import json
import os

from flask import current_app, render_template, Blueprint, request

from utility.app_utilities import configure_backend
from utility.constants import APP_CONFIG_JSON, CONFIG_FILE_FOLDER, MAIN_CONFIG


def main_config_to_app_config(config_dict, app):
    # current app needs to have the config dict before calling configure backend
    app.config[APP_CONFIG_JSON] = config_dict
    # the first time the config_dict is made configured we need to get the data backend
    configure_backend(app)


def save_main_config_dict():
    config_dict = current_app.config[APP_CONFIG_JSON]
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
        return False


def load_graphic_config_dict(graphic):
    try:
        with open(
            os.path.join(current_app.config[CONFIG_FILE_FOLDER], graphic), "r"
        ) as fout:
            graphic_dict_json = fout.read()
    except (OSError, IOError) as e:
        graphic_dict_json = "{}"
    return graphic_dict_json
