from flask import current_app, render_template, Blueprint

from controller import get_data_for_page


DATALAYOUT = "datalayout.html"

bp = Blueprint('', __name__)


@bp.route("/")
def main_page():
    html_data = get_data_for_page(current_app.config.get("path_to_json"), None)
    return render_template(DATALAYOUT, **html_data)


@bp.route("/<page_name>", methods=["GET"])
def graphic_page(page_name):
    html_data = get_data_for_page(current_app.config.get("path_to_json"), page_name)
    return render_template(DATALAYOUT, **html_data)
