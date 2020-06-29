from flask import current_app, render_template, Blueprint, request, jsonify, flash
import pandas as pd

from utility.constants import APP_CONFIG_JSON
from controller import get_data_for_page


UPLOAD_HTML = "data_upload.html"

upload_blueprint = Blueprint("upload", __name__)


class ValidationError(Exception):
    """Exception class for when an Escalation validation step fails"""

    pass


def validate_data_form(request_form, request_files):
    for key in ("username", "expname", "crank", "notes", "githash"):
        if key not in request_form:
            raise ValidationError("Key %s not present in POST" % key)
    username = request_form["username"]
    expname = request_form["expname"]
    crank = request_form["crank"]
    notes = request_form["notes"]
    githash = request_form["githash"]
    csvfile = request_files["csvfile"]

    current_app.logger.info(
        "POST {} {} {} {} {}".format(username, expname, crank, notes, csvfile.filename)
    )

    if not username:
        raise ValidationError("Username is required.")
    if not expname:
        raise ValidationError("Experiment name is required.")
    elif not crank:
        raise ValidationError("Crank number is required (e.g. 0015)")

    return username, expname, crank, notes, githash, csvfile


def validate_submission_content(csvfile):
    """
    Raises ValidationError if the file does not have the correct format/data types
    :param csvfile:
    :return:
    """
    try:
        df = pd.read_csv(csvfile, sep=",", comment="#")
        return df
    except ValueError:
        # todo- additional file type specific content validation
        raise ValidationError


@upload_blueprint.route("/upload", methods=("GET",))
def submission_view():
    return render_template(UPLOAD_HTML)


@upload_blueprint.route("/upload", methods=("POST",))
def submission():
    # if request.headers.get('User-Agent') != 'escalation-os':
    #     for key in ('username', 'expname', 'crank', 'notes', 'githash'):
    #         session[key] = request.form[key]

    try:
        # check the submission form
        username, expname, crank, notes, githash, csvfile = validate_data_form(
            request.form, request.files
        )
        # if the form of the submission is right, let's validate the content of the submitted file
        # df = validate_submission_content(csvfile)
        # database.add_submission(username, expname, crank, githash, df, notes)
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


# todo:
# form has drop down for existing data file types or allows new data file type
# this determines the schema of the file that is uploaded- check for validation
# upload writes the file to local storage or uses the db writer
