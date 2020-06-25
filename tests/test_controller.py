import json

import pytest
from werkzeug.datastructures import ImmutableMultiDict

from controller import (
    create_link_buttons_for_available_pages,
    create_data_subselect_info,
    reformat_filter_form_dict,
    get_unique_set_of_columns_needed,
)
from datastorer.local_handler import LocalCSVHandler
from utility.constants import (
    COLUMN_NAME,
    JINJA_SELECT_HTML_FILE,
    ENTRIES,
    SELECT_OPTION,
    ACTIVE_SELECTORS,
    INEQUALITIES,
    SELECTOR_TYPE,
    OPERATION,
    VALUE,
    NUMERICAL_FILTER,
)


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


def test_create_data_subselect_info(json_file):
    new_data = LocalCSVHandler("tests/test_data/penguins_size/")
    select_dict = [
        {"type": "select", "columns": "sex", "options": {"multiple": False}},
        {"type": "select", "columns": "island", "options": {"multiple": True}},
        {
            "type": "axis",
            "columns": "x",
            "options": {
                "entries": ["culmen_length_mm", "flipper_length_mm", "body_mass_g"]
            },
        },
    ]
    current_axis = {"x": "body_mass_g", "y": "flipper_length_mm"}
    select_info = create_data_subselect_info(
        select_dict,
        new_data,
        {"sex": ["MALE"]},
        {"x": "body_mass_g", "y": "flipper_length_mm"},
    )
    assert select_info[0][JINJA_SELECT_HTML_FILE] == "select_filter.html"
    assert select_info[1][COLUMN_NAME] == "island"
    assert select_info[2][JINJA_SELECT_HTML_FILE] == "select_axis.html"

    assert "MALE" in select_info[0][ACTIVE_SELECTORS]
    assert "MALE" in select_info[0][ENTRIES]
    assert "FEMALE" in select_info[0][ENTRIES]
    assert "." in select_info[0][ENTRIES]  # yes this is a unique entry in the data set
    assert "Torgersen" in select_info[1][ENTRIES]
    assert len(select_info[1][ACTIVE_SELECTORS]) == 0
    assert "Biscoe" in select_info[1][ENTRIES]
    assert "Dream" in select_info[1][ENTRIES]
    assert select_info[1][SELECT_OPTION]["multiple"]
    assert not select_info[0][SELECT_OPTION]["multiple"]
    assert "culmen_length_mm" in select_info[2][ENTRIES]
    assert "flipper_length_mm" in select_info[2][ENTRIES]
    assert "body_mass_g" in select_info[2][ENTRIES]
    assert "body_mass_g" in select_info[2][ACTIVE_SELECTORS]
    assert len(select_info[2][ACTIVE_SELECTORS]) == 1


def test_reformat_filter_form_dict():
    test_dict = ImmutableMultiDict(
        [
            ("0|filter|sex", "FEMALE"),
            ("0|filter|isl|and", "Torgersen"),
            ("1|filter|sex", "FEMALE"),
            ("1|filter|sex", "MALE"),
            ("1|filter|island", "SHOW_ALL_ROW"),
            ("1|axis|x", "flipper_length_mm"),
            ("0|numerical_filter|0|operation|culmen_length_mm", ">="),
            ("0|numerical_filter|0|value|culmen_length_mm", "5"),
            ("0|numerical_filter|1|operation|culmen_length_mm", "<"),
            ("0|numerical_filter|1|value|culmen_length_mm", ""),
        ]
    )
    [filter_dict, axis_dict] = reformat_filter_form_dict(test_dict)

    assert "FEMALE" in filter_dict[0]["sex"]["value"]
    assert "Torgersen" in filter_dict[0]["isl|and"]["value"]
    assert "FEMALE" in filter_dict[1]["sex"]["value"]
    assert "MALE" in filter_dict[1]["sex"]["value"]

    with pytest.raises(KeyError):
        filter_dict[1]["island"]
    assert "flipper_length_mm" == axis_dict[1]["x"]
    assert NUMERICAL_FILTER == filter_dict[0]["culmen_length_mm"][SELECTOR_TYPE]
    dict_output = filter_dict[0]["culmen_length_mm"][INEQUALITIES]
    assert dict_output["0"][OPERATION] == ">="
    assert dict_output["0"][VALUE] == 5
    assert dict_output["1"][OPERATION] == "<"
    assert dict_output["1"][VALUE] is None


def test_get_unique_set_of_columns_needed():
    culmen = "culmen_length_mm"
    flipper = "flipper_length_mm"
    flipper2 = "flipper_length_mm2"
    island = "island"
    sex = "sex"
    test_cols_list = get_unique_set_of_columns_needed(
        [{"x": culmen, "y": flipper}, {"x": culmen, "y": flipper2}],
        [
            {"type": "hover_data", "columns": [sex, culmen]},
            {"type": "groupby", "columns": [island]},
        ],
    )
    assert culmen in test_cols_list
    assert flipper in test_cols_list
    assert flipper2 in test_cols_list
    assert island in test_cols_list
    assert sex in test_cols_list
    assert len(test_cols_list) == 5
