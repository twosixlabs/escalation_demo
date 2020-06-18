import json

import pytest

from controller import create_link_buttons_for_available_pages, create_select_info
from datastorer.local_handler import LocalCSVHandler


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


def test_create_select_info(json_file):
    new_data = LocalCSVHandler("tests/test_data/penguins_size/")
    select_dict = {"type": "select", "columns": ["sex", "island"]}
    select_html_file, select_info = create_select_info(select_dict, new_data)
    print(select_info)
    assert select_html_file == "select.html"
    assert "MALE" in select_info["sex"]
    assert "FEMALE" in select_info["sex"]
    assert "." in select_info["sex"]
    assert "Torgersen" in select_info["island"]
    assert "Biscoe" in select_info["island"]
    assert "Dream" in select_info["island"]
