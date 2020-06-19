from flask import current_app, render_template, Blueprint, request
from utility.constants import APP_CONFIG_JSON
from controller import get_data_for_page


DATALAYOUT = "datalayout.html"

dashboard_blueprint = Blueprint("", __name__)


@dashboard_blueprint.route("/")
def main_page():
    html_data = get_data_for_page(current_app.config.get(APP_CONFIG_JSON), None)
    return render_template(DATALAYOUT, **html_data)


@dashboard_blueprint.route("/<page_name>", methods=["GET"])
def graphic_page(page_name):
    html_data = get_data_for_page(current_app.config.get(APP_CONFIG_JSON), page_name)
    return render_template(DATALAYOUT, **html_data)


@bp.route("/<page_name>", methods=["POST"])
def new_graphic_page(page_name):
    html_data = get_data_for_page(
        current_app.config.get(APP_CONFIG_JSON), page_name, request.form
    )
    return render_template(DATALAYOUT, **html_data)


@dashboard_blueprint.route("/test", methods=["GET"])
def test_for_sql():
    from datastorer.sql_handler import SqlHandler

    sql_handler = SqlHandler("Platereader")
    print(sql_handler.get_column_names())
    response = sql_handler.get_column_data({"od": 0.034652792466308736})
    print(f"sql response: {response}")
    return render_template(DATALAYOUT)
