from flask import current_app, render_template, Blueprint, request, jsonify, flash
import pandas as pd

from controller import create_link_buttons_for_available_pages
from utility.constants import (
    INDEX_COLUMN,
    UPLOAD_ID,
    APP_CONFIG_JSON,
    AVAILABLE_PAGES,
    DATA_SOURCE_TYPE,
)

UPLOAD_HTML = "data_upload.html"

upload_blueprint = Blueprint("upload", __name__)


class ValidationError(Exception):
    """
    Exception class for when an Escalation validation step fails.
    This is a catchall for many Python exceptions that correspond to bad file contents
    """

    pass


def validate_data_form(request_form, request_files):
    """
    We want to validate a submitted form whether it comes from the HTML page or an API
    request. This function checks the form values, not the content of the upload.
    :param request_form: flask request.form object
    :param request_files: flask request.files object
    :return: required fields
    """
    for key in ("username", "data_source", "notes"):
        if key not in request_form:
            raise ValidationError("Key %s not present in POST" % key)
    try:
        username = request_form["username"]
        data_source_name = request_form["data_source"]
        csvfile = request_files["csvfile"]
    # todo: validate upload filename with secure_filename, sql table name validator
    except KeyError:
        raise ValidationError
    current_app.logger.info(f"POST {username} {data_source_name} {csvfile.filename}")
    return username, data_source_name, csvfile


def validate_submission_content(csvfile, data_source_schema):
    """
    This function validates the contents of an uplaoded file against the expected schema
    Raises ValidationError if the file does not have the correct format/data types
    :param csvfile: request.file from flask for the uploaded file
    :param data_source_schema: sqlalchemy columns to use for validation
    :return: pandas dataframe of the uploaded csv
    """
    try:
        df = pd.read_csv(csvfile, sep=",", comment="#")
        existing_column_names = set([x.name for x in data_source_schema])
        # if we have added an index column on the backend, don't look for it in the data
        for app_added_column in [INDEX_COLUMN, UPLOAD_ID]:
            existing_column_names.remove(app_added_column)
        # all of the columns in the existing data source are specified in upload
        assert set(df.columns).issuperset(existing_column_names)
        # todo: match data types
        # todo- additional file type specific content validation
    except (AssertionError, ValueError):
        raise ValidationError
    return df


@upload_blueprint.route("/upload", methods=("GET",))
def submission_view():
    data_inventory = current_app.config.data_backend_writer
    existing_data_sources = data_inventory.get_available_data_sources()
    data_sources = sorted(existing_data_sources)
    return render_template(UPLOAD_HTML, data_sources=data_sources)


@upload_blueprint.route("/upload", methods=("POST",))
def submission():
    try:
        # check the submission form
        username, data_source_name, csvfile = validate_data_form(
            request.form, request.files
        )
        # if the form of the submission is right, let's validate the content of the submitted file
        data_inventory = current_app.config.data_backend_writer(
            data_sources=[{DATA_SOURCE_TYPE: data_source_name}]
        )
        data_source_schema = data_inventory.get_schema_for_data_source()
        df = validate_submission_content(csvfile, data_source_schema)
        # write upload history table record at the same time
        data_inventory.write_data_upload_to_backend(df)
    except ValidationError as e:
        current_app.logger.info(e)
        # check if POST comes from script instead of web UI
        if request.headers.get("User-Agent") == "escalation-api":
            return jsonify({"error": e}), 400
        else:
            flash(e)

    # todo: log information about what the submission is
    current_app.logger.info("Added submission")

    if request.headers.get("User-Agent") == "escalation-api":
        # if the request came from a script and API
        return jsonify({"success": "Added submission"})
    else:

        # if the request came from the web browser, provide an HTML repsonse
        return render_template("success.html", username="Captain Kirk")


@upload_blueprint.context_processor
def get_dashboard_pages():
    # used for the navigation bar
    available_pages = current_app.config.get(APP_CONFIG_JSON)[AVAILABLE_PAGES]
    dashboard_pages = create_link_buttons_for_available_pages(available_pages)
    return dict(dashboard_pages=dashboard_pages)
