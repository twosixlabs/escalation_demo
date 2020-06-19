import json
import os
import sys

from flask import Flask
from sqlalchemy.engine.url import URL

from utility.constants import APP_CONFIG_JSON, DATA_BACKEND, POSTGRES, MYSQL
from app_settings import PSQL_DATABASE_CONFIG as database_config
from datastorer.database import db, db_session


def create_app():
    app = Flask(__name__)
    # todo: option to build app without the sql connection if it's not needed. We'll build the config mapping based on info in the user-generated app config
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")
        or URL(**database_config),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VERSION="0.0.1",
    )

    # register url bleuprints with the app object
    from view import dashboard_blueprint

    app.register_blueprint(dashboard_blueprint)

    return app


if __name__ == "__main__":
    config_file_path = "tests/test_data/test_app_config.json"
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)

    if len(sys.argv) > 1:
        backend = sys.argv[1]
        config_dict[DATA_BACKEND] = backend

    app = create_app()
    app.config[APP_CONFIG_JSON] = config_dict

    # setup steps unique to SQL-backended apps
    if app.config[APP_CONFIG_JSON][DATA_BACKEND] in [MYSQL, POSTGRES]:
        db.init_app(app)

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

    app.run()
