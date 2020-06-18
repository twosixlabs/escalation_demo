import json
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

from app_settings import DATABASE_CONFIG
from utility.constants import APP_CONFIG_JSON


def create_app(backend):
    app = Flask(__name__)
    # todo: option to build app without the sql connection if it's not needed. We'll build the config mapping based on info in the user-generated app config
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")
        or URL(**DATABASE_CONFIG),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VERSION="0.0.1",
    )
    if backend == "sql":
        db = SQLAlchemy()
        db.init_app(app)

    # register url bleuprints with the app object
    from view import bp as sub_bp

    app.register_blueprint(sub_bp)

    return app


if __name__ == "__main__":
    backend = "filesystem"
    if len(sys.argv) > 1:
        backend = sys.argv[1]

    app = create_app(backend)

    config_file_path = "tests/test_data/test_app_config.json"
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)
    app.config[APP_CONFIG_JSON] = config_dict
    app.run()
