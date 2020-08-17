# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

from flask import current_app, render_template, Blueprint, request
from utility.constants import (
    APP_CONFIG_JSON,
    PROCESS,
    SITE_TITLE,
    SITE_DESC,
    AVAILABLE_PAGES_DICT,
    JINJA_PLOT,
    CURRENT_PAGE,
)
from controller import get_data_for_page

DATA_LAYOUT = "data_layout.html"

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/dashboard/")
@dashboard_blueprint.route("/")
def main_page():
    return render_template(DATA_LAYOUT)


@dashboard_blueprint.route("/dashboard/<page_name>", methods=["GET", "POST"])
def graphic_page(page_name):
    html_data_list = get_data_for_page(
        current_app.config.get(AVAILABLE_PAGES_DICT).get(page_name),
        # request.form[PROCESS]=='' means the reset button sent the request
        request.form if request.form and request.form[PROCESS] else None,
    )
    return render_template(
        DATA_LAYOUT, **{CURRENT_PAGE: page_name, JINJA_PLOT: html_data_list}
    )


@dashboard_blueprint.context_processor
def create_jumbotron_info():
    config_dict = current_app.config.get(APP_CONFIG_JSON)
    jumbotron_info = {
        SITE_TITLE: config_dict[SITE_TITLE],
        SITE_DESC: config_dict[SITE_DESC],
    }
    return jumbotron_info
