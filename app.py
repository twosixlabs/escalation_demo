import json
import os
from types import MappingProxyType

from flask import Flask
from sqlalchemy.engine.url import URL

from utility.constants import APP_CONFIG_JSON, DATA_BACKEND, POSTGRES, MYSQL
from app_settings import PSQL_DATABASE_CONFIG as database_config


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")
        or URL(**database_config),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VERSION="0.0.1",
    )

    # register url bleuprints with the app object
    from views.dashboard import dashboard_blueprint

    app.register_blueprint(dashboard_blueprint)
    from views.file_upload import upload_blueprint

    app.register_blueprint(upload_blueprint)

    return app


def configure_app(app, config_dict):
    # write the config dict to app config as a read-only proxy of a mutable dict
    app.config[APP_CONFIG_JSON] = MappingProxyType(config_dict)

    # setup steps unique to SQL-backended apps
    # todo: make sure we don't need postgres install reqs if running mysql
    if app.config[APP_CONFIG_JSON][DATA_BACKEND] in [MYSQL, POSTGRES]:
        from database.sql_handler import SqlHandler, SqlDataInventory
        from database.database import db, db_session

        db.init_app(app)
        data_backend_class = SqlHandler
        data_backend_writer = SqlDataInventory

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

    else:
        from database.local_handler import LocalCSVHandler, LocalCSVDataInventory

        data_backend_class = LocalCSVHandler
        data_backend_writer = LocalCSVDataInventory

    app.config.data_handler = data_backend_class
    app.config.data_backend_writer = data_backend_writer
    return app


if __name__ == "__main__":
    # config_file_path = "tests/test_data/test_sql_app_config.json"
    # config_file_path = "tests/test_data/test_app_local_handler_config.json"
    config_file_path = "yeast_states_app/yeast_states_config.json"

    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)

    app = create_app()
    app = configure_app(app, config_dict)

    app.run()
