from flask import Flask, render_template

from controller import get_graphic

app = Flask(__name__)


@app.route("/")
def plot_test():
    """
    to be deleted
    proof of concept
    :return:
    """
    [filename, htmldata] = get_graphic("scatter plot", [], [], [])
    return render_template(filename, **htmldata)


if __name__ == "__main__":
    app.run()
