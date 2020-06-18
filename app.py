from flask import Flask, render_template
import sys
from controller import get_data_for_page

DATALAYOUT = "datalayout.html"
app = Flask(__name__)


@app.route("/")
def main_page():
    html_data = get_data_for_page(app.config.get("path_to_json"), None)
    return render_template(DATALAYOUT, **html_data)


@app.route("/<page_name>", methods=["GET"])
def graphic_page(page_name):
    html_data = get_data_for_page(app.config.get("path_to_json"), page_name)
    return render_template(DATALAYOUT, **html_data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        app.config["path_to_json"] = sys.argv[1]  # sanitize inputs
    else:
        app.config["path_to_json"] = "config_files/main.json"

    app.run()
