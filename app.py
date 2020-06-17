from flask import Flask, render_template

from controller import get_graphic

DATALAYOUT = "datalayout.html"
app = Flask(__name__)


@app.route("/")
def plot_test():
    """
    to be deleted
    proof of concept
    :return:
    """
    htmldata = get_graphic("tests/test_data/test.json")
    return render_template(DATALAYOUT, plots=htmldata)


if __name__ == "__main__":
    app.run()
