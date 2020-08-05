# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json
import os
import re

from flask import current_app, render_template, Blueprint, request

from app import configure_backend
from utility.build_schema import (
    build_settings_schema,
    build_graphic_schema,
    build_graphic_schema_with_plotly,
)
from utility.constants import (
    DATA_SOURCES,
    DATA_BACKEND,
    LOCAL_CSV,
    APP_CONFIG_JSON,
    AVAILABLE_PAGES,
    PAGE_ID,
    GRAPHIC,
    MAIN_CONFIG,
    CONFIG_FILE_FOLDER,
    CONFIG_DICT,
    IS_GRAPHIC_NEW,
    GRAPHIC_CONFIG_FILES,
    WEBPAGE_LABEL,
    URL_ENDPOINT,
    JSON_FALSE,
)
from validate_schema import get_data_inventory_class, get_possible_column_names
from wizard_ui.wizard_utils import (
    load_graphic_config_dict,
    save_main_config_dict,
    main_config_to_app_config,
)

CONFIG_EDITOR_HTML = "config_editor.html"
CONFIG_FILES_HTML = "config_files.html"
wizard_blueprint = Blueprint("wizard", __name__)


@wizard_blueprint.route("/", methods=("GET",))
def file_tree():
    if APP_CONFIG_JSON in current_app.config:
        config_dict = current_app.config[APP_CONFIG_JSON]
        return render_template(
            CONFIG_FILES_HTML, available_pages=config_dict.get(AVAILABLE_PAGES, {})
        )
    else:
        return main_config_setup()


@wizard_blueprint.route("/", methods=("POST",))
def add_page():
    webpage_label = request.form[WEBPAGE_LABEL]
    # sanitizing the string so it is valid url
    pattern = re.compile("\W+", re.UNICODE)
    page_dict = {
        WEBPAGE_LABEL: webpage_label,
        URL_ENDPOINT: (pattern.sub("", webpage_label.replace(" ", "_"))).lower(),
        GRAPHIC_CONFIG_FILES: [],
    }
    current_app.config[APP_CONFIG_JSON][AVAILABLE_PAGES].append(page_dict)
    save_main_config_dict()
    return file_tree()


@wizard_blueprint.route("/main", methods=("GET",))
def main_config_setup():
    MAIN_MESSAGE = "Create/Edit the main config file"
    config_dict = current_app.config.get(APP_CONFIG_JSON, {}).copy()
    return render_template(
        CONFIG_EDITOR_HTML,
        schema=json.dumps(build_settings_schema()),
        message=MAIN_MESSAGE,
        current_config=json.dumps(config_dict),
        is_graphic_new=JSON_FALSE,
    )


@wizard_blueprint.route("/graphic", methods=("POST",))
def graphic_config_setup():
    GRAPHIC_MESSAGE = "Create/Edit a graphic config file"
    config_dict = current_app.config[APP_CONFIG_JSON]
    csv_flag = config_dict[DATA_BACKEND] == LOCAL_CSV
    data_source_names = config_dict[DATA_SOURCES]
    data_inventory_class = get_data_inventory_class(csv_flag)
    possible_column_names = get_possible_column_names(
        data_source_names, data_inventory_class, csv_flag
    )
    graphic_dict_json = "{}"
    if request.form[IS_GRAPHIC_NEW] == JSON_FALSE:
        graphic_dict_json = load_graphic_config_dict(request.form[GRAPHIC])
    return render_template(
        CONFIG_EDITOR_HTML,
        schema=json.dumps(
            build_graphic_schema_with_plotly(data_source_names, possible_column_names),
            indent=4,
        ),
        message=GRAPHIC_MESSAGE,
        page_id=request.form[PAGE_ID],
        graphic=request.form[GRAPHIC],
        current_config=graphic_dict_json,
        is_graphic_new=request.form[IS_GRAPHIC_NEW],
    )


@wizard_blueprint.route("/save", methods=("POST",))
def update_json_config_with_ui_changes():
    config_information_dict = request.get_json()
    page_id = config_information_dict[PAGE_ID]
    config_dict = config_information_dict[CONFIG_DICT]
    if page_id < 0:
        if APP_CONFIG_JSON not in current_app.config:
            main_config_to_app_config(config_dict, current_app)
        else:
            current_app.config[APP_CONFIG_JSON] = config_dict
        save_main_config_dict()
    else:
        graphic_name = config_information_dict[GRAPHIC]
        filename, ext = os.path.splitext(graphic_name)
        graphic_name = f"{filename}.json"
        if config_information_dict[IS_GRAPHIC_NEW]:
            page_dict = current_app.config[APP_CONFIG_JSON][AVAILABLE_PAGES][page_id]
            graphic_list = page_dict.get(GRAPHIC_CONFIG_FILES, [])
            graphic_list.append(graphic_name)
            page_dict[GRAPHIC_CONFIG_FILES] = graphic_list
            save_main_config_dict()
        with open(
            os.path.join(current_app.config[CONFIG_FILE_FOLDER], graphic_name), "w"
        ) as fout:
            json.dump(config_dict, fout, indent=4)

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
