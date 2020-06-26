"""
Pytest configuration and test fixtures
"""

import json

import pytest

from datastorer.local_handler import LocalCSVHandler
from utility.constants import DATA_SOURCE_TYPE


@pytest.fixture()
def local_handler_fixture_small():
    got_data = LocalCSVHandler(
        [{DATA_SOURCE_TYPE: "tests/test_data/penguins_size_small"}]
    )
    return got_data


@pytest.fixture()
def local_handler_fixture():
    got_data = LocalCSVHandler([{DATA_SOURCE_TYPE: "tests/test_data/penguins_size"}])
    return got_data


@pytest.fixture()
def json_config_fixture():
    with open("tests/test_data/test_app_config.json", "r") as config_file:
        config_dict = json.load(config_file)

    return config_dict
