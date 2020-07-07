from flask import current_app, render_template, Blueprint, request
from utility.constants import APP_CONFIG_JSON, AVAILABLE_PAGES
from controller import get_data_for_page, create_link_buttons_for_available_pages

DATALAYOUT = "datalayout.html"

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
def main_page():
    available_pages = current_app.config.get(APP_CONFIG_JSON)[AVAILABLE_PAGES]
    buttons = create_link_buttons_for_available_pages(available_pages)
    html_data = get_data_for_page(current_app.config.get(APP_CONFIG_JSON), None)
    return render_template(DATALAYOUT, buttons=buttons, **html_data)


@dashboard_blueprint.route("/dashboard/<page_name>", methods=["GET"])
def graphic_page(page_name):
    available_pages = current_app.config.get(APP_CONFIG_JSON)[AVAILABLE_PAGES]
    buttons = create_link_buttons_for_available_pages(available_pages)
    html_data = get_data_for_page(current_app.config.get(APP_CONFIG_JSON), page_name)
    return render_template(DATALAYOUT, buttons=buttons, **html_data)


@dashboard_blueprint.route("/dashboard/<page_name>", methods=["POST"])
def new_graphic_page(page_name):
    available_pages = current_app.config.get(APP_CONFIG_JSON)[AVAILABLE_PAGES]
    buttons = create_link_buttons_for_available_pages(available_pages)
    html_data = get_data_for_page(
        current_app.config.get(APP_CONFIG_JSON), page_name, request.form
    )
    return render_template(DATALAYOUT, buttons=buttons, **html_data)
