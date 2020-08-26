# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

from flask import current_app, render_template, Blueprint, request

from utility.constants import DATA_SOURCES

ADMIN_HTML = "admin.html"
INACTIVE = "inactive"
ACTIVE = "active"
admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin", methods=("GET",))
def admin_page():
    data_inventory = current_app.config.data_backend_writer
    existing_data_sources = data_inventory.get_available_data_sources()
    data_sources = sorted(existing_data_sources)
    data_source_dict = data_inventory.get_identifiers_for_data_sources(data_sources)
    data_source_active_dict = data_inventory.get_identifiers_for_data_sources(
        data_sources, active_filter=True
    )
    return render_template(
        ADMIN_HTML,
        data_source_dict=data_source_dict,
        data_source_active_dict=data_source_active_dict,
    )


@admin_blueprint.route("/admin", methods=("POST",))
def submission():
    active_data_dict = request.form.to_dict()
    data_source_name = active_data_dict.pop(DATA_SOURCES)
    data_inventory = current_app.config.data_backend_writer
    data_inventory.update_data_upload_metadata_active(
        data_source_name, active_data_dict
    )
    return admin_page()
