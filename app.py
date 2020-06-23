import json
import os
import sys

from flask import Flask
from sqlalchemy.engine.url import URL

from datastorer.local_handler import LocalCSVHandler
from datastorer.sql_handler import SqlHandler
from utility.constants import APP_CONFIG_JSON, DATA_BACKEND, POSTGRES, MYSQL, LOCAL_CSV
from app_settings import PSQL_DATABASE_CONFIG as database_config


DATA_BACKEND_CLASS_LOOKUP = {
    POSTGRES: SqlHandler,
    MYSQL: SqlHandler,
    LOCAL_CSV: LocalCSVHandler,
}


def create_app():
    app = Flask(__name__)
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
    config_file_path = "tests/test_data/test_sql_app_config.json"
    # config_file_path = "tests/test_data/test_app_config.json"

    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)

    app = create_app()
    app.config[APP_CONFIG_JSON] = config_dict
    app.config.data_handler = DATA_BACKEND_CLASS_LOOKUP[config_dict[DATA_BACKEND]]

    # setup steps unique to SQL-backended apps
    if app.config[APP_CONFIG_JSON][DATA_BACKEND] in [MYSQL, POSTGRES]:
        from datastorer.database import db, db_session

        db.init_app(app)

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

    app.run()
