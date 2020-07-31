# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import copy
import json

from flask import current_app, render_template, Blueprint, request, jsonify, flash

from utility.build_schema import build_settings_schema, build_graphic_schema
from utility.constants import (
    DATA_SOURCES,
    DATA_SOURCE_TYPE,
    DATA_BACKEND,
    LOCAL_CSV,
    APP_CONFIG_JSON, AVAILABLE_PAGES,
)
from validate_schema import get_data_inventory_class, get_possible_column_names

CONFIG_EDITOR_HTML = "config_editor.html"
CONFIG_FILES_HTML = "config_files.html"
ADMIN_HTML = "admin.html"
INACTIVE = "inactive"
ACTIVE = "active"
admin_blueprint = Blueprint("admin", __name__)

MAIN_MESSAGE = "Create/Edit the main config file"
GRAPHIC_MESSAGE = "Create/Edit a graphic config file"


@admin_blueprint.route("/admin", methods=("GET",))
def admin_page():
    data_inventory = current_app.config.data_backend_writer
    existing_data_sources = data_inventory.get_available_data_sources()
    data_sources = sorted(existing_data_sources)
    data_source_dict = {
        data_source: data_inventory(
            [{DATA_SOURCE_TYPE: data_source}]
        ).get_identifiers_for_data_source()
        for data_source in data_sources
    }
    data_source_active_dict = copy.deepcopy(data_source_dict)
    data_source_active_dict.update(current_app.config.active_data_source_filters)
    return render_template(
        ADMIN_HTML,
        data_source_dict=data_source_dict,
        data_source_active_dict=data_source_active_dict,
    )


@admin_blueprint.route("/admin", methods=("POST",))
def submission():
    active_data_dict = request.form.to_dict()
    data_source_name = active_data_dict.pop(DATA_SOURCES)
    if INACTIVE in active_data_dict.values():
        current_app.config.active_data_source_filters.update(
            {
                data_source_name: [
                    identifier
                    for (identifier, active_state) in active_data_dict.items()
                    if active_state == ACTIVE
                ]
            }
        )
    else:
        current_app.config.active_data_source_filters.pop(data_source_name, [])
    return admin_page()


@admin_blueprint.route("/admin/setup", methods=("GET",))
def file_tree():
    config_dict = current_app.config[APP_CONFIG_JSON]
    return render_template(CONFIG_FILES_HTML, availabe_pages=config_dict[AVAILABLE_PAGES])


@admin_blueprint.route("/admin/setup/main", methods=("GET",))
def main_config_setup():
    config_dict = current_app.config.get(APP_CONFIG_JSON, {}).copy()
    return render_template(
        CONFIG_EDITOR_HTML,
        schema=json.dumps(build_settings_schema()),
        message=MAIN_MESSAGE,
        current_config=json.dumps(config_dict)
    )


@admin_blueprint.route("/admin/setup/graphic", methods=("GET",))
def graphic_config_setup():
    config_dict = current_app.config[APP_CONFIG_JSON]
    csv_flag = config_dict[DATA_BACKEND] == LOCAL_CSV
    data_source_names = config_dict[DATA_SOURCES]
    data_inventory_class = get_data_inventory_class(csv_flag)
    possible_column_names = get_possible_column_names(
        data_source_names, data_inventory_class, csv_flag
    )
    return render_template(
        CONFIG_EDITOR_HTML,
        schema=json.dumps(
            build_graphic_schema(data_source_names, possible_column_names), indent=4
        ),
        message=GRAPHIC_MESSAGE,
    )
