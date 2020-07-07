import copy

from flask import current_app, render_template, Blueprint, request, jsonify, flash

from controller import create_link_buttons_for_available_pages
from utility.constants import (
    INDEX_COLUMN,
    UPLOAD_ID,
    APP_CONFIG_JSON,
    AVAILABLE_PAGES,
    DATA_SOURCES,
)

ADMIN_HTML = "admin.html"
INACTIVE = "inactive"
ACTIVE = "active"
admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin", methods=("GET",))
def admin_page():
    data_inventory = current_app.config.data_backend_writer
    existing_data_sources = data_inventory.get_available_data_source()
    data_sources = sorted(existing_data_sources)
    data_source_dict = {
        data_source: data_inventory.get_identifier_for_data_source(data_source)
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


@admin_blueprint.context_processor
def get_dashboard_pages():
    # used for the navigation bar
    available_pages = current_app.config.get(APP_CONFIG_JSON)[AVAILABLE_PAGES]
    dashboard_pages = create_link_buttons_for_available_pages(available_pages)
    return dict(dashboard_pages=dashboard_pages)
