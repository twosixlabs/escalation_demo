# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

import json
import os
from types import MappingProxyType

from flask import Flask
from sqlalchemy.engine.url import URL

from controller import create_labels_for_available_pages, make_pages_dict
from utility.app_utilities import configure_backend
from utility.constants import (
    APP_CONFIG_JSON,
    AVAILABLE_PAGES,
    AVAILABLE_PAGES_DICT,
    CONFIG_FILE_FOLDER,
    TEST_APP_DEPLOY_DATA,
    APP_DEPLOY_DATA,
)
from app_deploy_data.app_settings import DATABASE_CONFIG


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")
        or URL(**DATABASE_CONFIG),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VERSION="0.0.1",
    )

    # register url blueprints with the app object
    from views.dashboard import dashboard_blueprint

    app.register_blueprint(dashboard_blueprint)
    from views.file_upload import upload_blueprint

    app.register_blueprint(upload_blueprint)
    from views.admin import admin_blueprint

    app.register_blueprint(admin_blueprint)

    @app.context_processor
    def get_dashboard_pages():
        # used for the navigation bar
        available_pages = app.config.get(APP_CONFIG_JSON)[AVAILABLE_PAGES]
        dashboard_pages = create_labels_for_available_pages(available_pages)
        return dict(dashboard_pages=dashboard_pages)

    return app


def configure_app(app, config_dict):
    # write the config dict to app config as a read-only proxy of a mutable dict
    # todo: these lines will change as we adding the wizard and the separate app
    app.config[APP_CONFIG_JSON] = MappingProxyType(config_dict)
    app.config[CONFIG_FILE_FOLDER] = APP_DEPLOY_DATA
    app.config[AVAILABLE_PAGES_DICT] = make_pages_dict(
        config_dict[AVAILABLE_PAGES], app.config[CONFIG_FILE_FOLDER]
    )
    configure_backend(app)
    app.config.active_data_source_filters = {}
    return app

# config_file_path = os.path.join("app_deploy_data", "app_config.json")
# config_file_path = "test_app_deploy_data/data/test_sql_app_config.json"
config_file_path = "test_app_deploy_data/test_app_local_config.json"
# config_file_path = "../yeast_states_app/yeast_states_config.json"
with open(config_file_path, "r") as config_file:
    config_dict = json.load(config_file)
app = create_app()
app = configure_app(app, config_dict)

if __name__ == "__main__":
    app.run()
