# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0
import json

from flask import current_app, render_template, Blueprint, request, Response

from controller import get_meta_data
from utility.constants import (
    DATA_SOURCES,
    MAIN_DATA_SOURCE,
    DATA_SOURCE_TYPE,
    UPLOAD_ID,
    OPTION_TYPE,
    FILTER,
    OPTION_COL,
    SELECTED,
    ACTIVE,
)
from utility.wizard_utils import get_possible_column_names_and_values

DOWNLOAD_HTML = "view_uploaded_data.html"

download_blueprint = Blueprint("download", __name__)


@download_blueprint.route("/download", methods=("GET",))
def download_page():
    data_source_dict = get_meta_data()
    return render_template(
        DOWNLOAD_HTML, data_source_dict=data_source_dict, admin=False
    )


@download_blueprint.route("/download", methods=("POST",))
def download_data():
    download_data_dict = request.form.to_dict()
    data_source_name = download_data_dict.pop(DATA_SOURCES)
    data_inventory_class = current_app.config.data_backend_writer
    data_inventory = data_inventory_class(
        data_sources={MAIN_DATA_SOURCE: {DATA_SOURCE_TYPE: data_source_name}}
    )
    column_names, _ = get_possible_column_names_and_values(
        [data_source_name], data_inventory_class, get_unique_values=False
    )
    data_source_filters = [
        {
            OPTION_TYPE: FILTER,
            OPTION_COL: f"{data_source_name}:{UPLOAD_ID}",
            SELECTED: [
                upload_id
                for upload_id, selected in download_data_dict.items()
                if selected == ACTIVE
            ],
        }
    ]
    df = data_inventory.get_column_data(
        column_names, data_source_filters, only_use_active=False
    )
    return Response(
        df.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={data_source_name}.csv"},
    )
