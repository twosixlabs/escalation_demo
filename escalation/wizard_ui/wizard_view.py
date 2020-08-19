# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json
import os

from flask import current_app, render_template, Blueprint, request

from utility.app_utilities import configure_backend
from utility.build_plotly_schema import SELECTOR_DICT
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
    GRAPHIC_STATUS,
    GRAPHIC_CONFIG_FILES,
    WEBPAGE_LABEL,
    URL_ENDPOINT,
    DATABASE,
    SCATTER,
    POSTGRES,
    DATA,
    TYPE,
    PLOT_SPECIFIC_INFO,
    COPY,
    OLD,
    NEW,
)
from validate_schema import get_data_inventory_class, get_possible_column_names
from wizard_ui.schemas_for_ui import (
    build_main_schemas_for_ui,
    build_graphic_schemas_for_ui,
    BACKEND_TYPES,
)
from wizard_ui.wizard_utils import (
    load_graphic_config_dict,
    save_main_config_dict,
    set_up_backend_for_wizard,
    load_main_config_dict_if_exists,
    sanitize_string,
    invert_dict_lists,
    make_empty_component_dict,
    graphic_dict_to_graphic_component_dict,
    graphic_component_dict_to_graphic_dict,
)

GRAPHIC_CONFIG_EDITOR_HTML = "graphic_config_editor.html"
MAIN_CONFIG_EDITOR_HTML = "main_config_editor.html"
CONFIG_FILES_HTML = "config_files.html"
wizard_blueprint = Blueprint("wizard", __name__)


@wizard_blueprint.route("/", methods=("GET",))
def file_tree():
    if APP_CONFIG_JSON in current_app.config:
        config_dict = load_main_config_dict_if_exists(current_app)
        return render_template(
            CONFIG_FILES_HTML, available_pages=config_dict.get(AVAILABLE_PAGES, {})
        )
    else:
        return main_config_setup()


@wizard_blueprint.route("/", methods=("POST",))
def add_page():
    webpage_label = request.form[WEBPAGE_LABEL]
    page_dict = {
        WEBPAGE_LABEL: webpage_label,
        URL_ENDPOINT: sanitize_string(
            webpage_label
        ),  # sanitizing the string so it is valid url
        GRAPHIC_CONFIG_FILES: [],
    }
    config_dict = load_main_config_dict_if_exists(current_app)
    available_pages = config_dict.get(AVAILABLE_PAGES, [])
    available_pages.append(page_dict)
    config_dict[AVAILABLE_PAGES] = available_pages
    save_main_config_dict(config_dict)
    return file_tree()


@wizard_blueprint.route("/main", methods=("GET",))
def main_config_setup():
    config_dict = load_main_config_dict_if_exists(current_app)
    inverted_backend_types = invert_dict_lists(BACKEND_TYPES)
    return render_template(
        MAIN_CONFIG_EDITOR_HTML,
        schema=json.dumps(build_main_schemas_for_ui()),
        current_config=json.dumps(config_dict),
        # load in the right schema based on the config dict, default to database
        current_schema=inverted_backend_types.get(
            config_dict.get(DATA_BACKEND, POSTGRES), DATABASE
        ),
    )


@wizard_blueprint.route("/graphic", methods=("POST",))
def graphic_config_setup():
    config_dict = load_main_config_dict_if_exists(current_app)
    csv_flag = config_dict[DATA_BACKEND] == LOCAL_CSV
    data_source_names = config_dict[DATA_SOURCES]
    data_inventory_class = get_data_inventory_class(csv_flag)
    possible_column_names = get_possible_column_names(
        data_source_names, data_inventory_class, csv_flag
    )
    component_graphic_dict = make_empty_component_dict()
    graphic_schemas, schema_to_type = build_graphic_schemas_for_ui(
        data_source_names, possible_column_names
    )
    graphic_name = os.path.splitext(request.form[GRAPHIC])[0]
    current_schema = SCATTER

    if request.form[GRAPHIC_STATUS] in [COPY, OLD]:
        graphic_dict = json.loads(load_graphic_config_dict(request.form[GRAPHIC]))
        type_to_schema = invert_dict_lists(schema_to_type)
        current_schema = type_to_schema[
            graphic_dict[PLOT_SPECIFIC_INFO][DATA][0].get(TYPE, SCATTER)
        ]
        component_graphic_dict = graphic_dict_to_graphic_component_dict(graphic_dict)
    if request.form[GRAPHIC_STATUS] == COPY:
        graphic_name = graphic_name + "_copy"

    return render_template(
        GRAPHIC_CONFIG_EDITOR_HTML,
        schema=json.dumps(graphic_schemas, indent=4,),
        page_id=request.form[PAGE_ID],
        graphic=graphic_name,
        current_config=json.dumps(component_graphic_dict),
        graphic_status=request.form[GRAPHIC_STATUS],
        schema_selector_dict=SELECTOR_DICT,
        current_schema=current_schema,
    )


@wizard_blueprint.route("/main/save", methods=("POST",))
def update_main_json_config_with_ui_changes():
    config_dict = request.get_json()
    if APP_CONFIG_JSON not in current_app.config:
        set_up_backend_for_wizard(config_dict, current_app)
    save_main_config_dict(config_dict)

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@wizard_blueprint.route("/graphic/save", methods=("POST",))
def update_graphic_json_config_with_ui_changes():
    config_information_dict = request.get_json()
    page_id = config_information_dict[PAGE_ID]
    graphic_dict = graphic_component_dict_to_graphic_dict(
        config_information_dict[CONFIG_DICT]
    )
    graphic_filename = os.path.splitext(config_information_dict[GRAPHIC])[0]
    # sanitizing the string so it is valid filename
    graphic_filename = f"{sanitize_string(graphic_filename)}.json"
    if config_information_dict[GRAPHIC_STATUS] in [NEW, COPY]:
        main_config_dict = load_main_config_dict_if_exists(current_app)
        page_dict = main_config_dict[AVAILABLE_PAGES][page_id]
        graphic_list = page_dict.get(GRAPHIC_CONFIG_FILES, [])
        graphic_list.append(graphic_filename)
        page_dict[GRAPHIC_CONFIG_FILES] = graphic_list
        save_main_config_dict(main_config_dict)
    with open(
        os.path.join(current_app.config[CONFIG_FILE_FOLDER], graphic_filename), "w"
    ) as fout:
        json.dump(graphic_dict, fout, indent=4)

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
