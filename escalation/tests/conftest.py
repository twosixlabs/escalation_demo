# Copyright [2020] [Two Six Labs, LLC]
# Licensed under the Apache License, Version 2.0

"""
Pytest configuration and test fixtures
"""

import json
import pytest
from types import MappingProxyType

from app import create_app


from database.local_handler import LocalCSVHandler
from utility.constants import DATA_SOURCE_TYPE, APP_CONFIG_JSON


@pytest.fixture()
def test_app_client(json_config_fixture):
    flask_app = create_app()
    flask_app.config[APP_CONFIG_JSON] = MappingProxyType(json_config_fixture)
    flask_app.config.active_data_source_filters = []

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    # application context needs to be pushed to be able to handle GETs and POSTs
    ctx.push()
    # provide the testing client to the tests
    yield testing_client  # this is where the testing happens!
    # remove the context to clean up the test environment
    ctx.pop()


@pytest.fixture()
def local_handler_fixture_small(test_app_client):
    got_data = LocalCSVHandler([{DATA_SOURCE_TYPE: "penguin_size_small"}])
    return got_data


@pytest.fixture()
def local_handler_fixture(test_app_client):
    got_data = LocalCSVHandler([{DATA_SOURCE_TYPE: "penguin_size"}])
    return got_data


@pytest.fixture()
def json_config_fixture():
    with open("tests/test_data/test_app_local_handler_config.json", "r") as config_file:
        config_dict = json.load(config_file)

    return config_dict
