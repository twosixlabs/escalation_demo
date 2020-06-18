import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

from app_settings import DATABASE_CONFIG


def create_app():
    app = Flask(__name__)
    # todo: option to build app without the sql connection if it's not needed. We'll build the config mapping based on info in the user-generated app config
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or URL(**DATABASE_CONFIG),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VERSION="0.0.1")

    db = SQLAlchemy()
    db.init_app(app)

    # register url bleuprints with the app object
    from view import bp as sub_bp
    app.register_blueprint(sub_bp)

    return app


app = create_app()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app.config["path_to_json"] = sys.argv[1]  # sanitize inputs
    else:
        app.config["path_to_json"] = "tests/test_data/test_app_config.json"

    app.run()
