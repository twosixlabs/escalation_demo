from controller import get_graphic

from flask import render_template, Blueprint

DATALAYOUT = "datalayout.html"

bp = Blueprint('', __name__)


@bp.route("/")
def plot_test():
    """
    to be deleted
    proof of concept
    :return:
    """
    htmldata = get_graphic("tests/test_data/test.json")
    return render_template(DATALAYOUT, plots=htmldata)
