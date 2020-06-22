import json

import pytest
from werkzeug.datastructures import ImmutableMultiDict

from controller import (
    create_link_buttons_for_available_pages,
    create_select_info,
    reformatting_the_form_dict,
    extract_data_needed,
)
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
    assert "." in select_info["sex"]  # yes this is a unigue entry in the data set
    assert "Torgersen" in select_info["island"]
    assert "Biscoe" in select_info["island"]
    assert "Dream" in select_info["island"]


def test_turn_form_into_dict():
    test_dict = ImmutableMultiDict(
        [
            ("0_sex", "FEMALE"),
            ("0_isl_and", "Torgersen"),
            ("1_sex", "FEMALE"),
            ("1_sex", "MALE"),
            ("1_island", "SHOW_ALL_ROW"),
        ]
    )
    new_dict = reformatting_the_form_dict(test_dict)
    print(new_dict)
    assert "FEMALE" in new_dict[0]["sex"]
    assert "Torgersen" in new_dict[0]["isl_and"]
    assert "FEMALE" in new_dict[1]["sex"]
    assert "MALE" in new_dict[1]["sex"]

    with pytest.raises(KeyError):
        new_dict[1]["island"]


def test_extract_data_needed():
    culmen = "culmen_length_mm"
    flipper = "flipper_length_mm"
    flipper2 = "flipper_length_mm2"
    test_cols_list = extract_data_needed(
        [{"x": culmen, "y": flipper}, {"x": culmen, "y": flipper2}]
    )
    assert culmen in test_cols_list
    assert flipper in test_cols_list
    assert flipper2 in test_cols_list
    assert len(test_cols_list) == 3
