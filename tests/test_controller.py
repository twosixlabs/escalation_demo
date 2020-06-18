import json

import pytest

from controller import create_link_buttons_for_available_pages


@pytest.fixture()
def json_file():
    with open("tests/test_data/test_app_config.json", "r") as config_file:
        config_dict = json.load(config_file)

    return config_dict


def test_get_graphic():
    assert False


def test_extract_buttons(json_file):
    aval_pg = json_file["available_pages"]
    buttons = create_link_buttons_for_available_pages(aval_pg)

    button1 = {"name": "Penguins", "link": "penguins"}
    button2 = {"name": "More Penguins!", "link": "more_penguins"}
    assert button1 in buttons
    assert button2 in buttons
