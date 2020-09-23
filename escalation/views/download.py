# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0
import json

from flask import current_app, render_template, Blueprint, request

from controller import get_meta_data
from utility.constants import DATA_SOURCES

DOWNLOAD_HTML = "view_uploaded_data.html"

download_blueprint = Blueprint("download", __name__)

@download_blueprint.route("/download", methods=("GET",))
def download_page():
    data_source_dict = get_meta_data()
    return render_template(DOWNLOAD_HTML, data_source_dict=data_source_dict, admin=False)

@download_blueprint.route("/download", methods=("POST",))
def submission():
    active_data_dict = request.form.to_dict()
    data_source_name = active_data_dict.pop(DATA_SOURCES)
    data_inventory = current_app.config.data_backend_writer
    data_inventory.get_column_data()

