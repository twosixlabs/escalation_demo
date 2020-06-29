import pytest
from werkzeug.datastructures import ImmutableMultiDict

from controller import (
    create_link_buttons_for_available_pages,
    create_data_subselect_info,
    get_unique_set_of_columns_needed,
)
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
    SHOW_ALL_ROW,
)


def test_get_graphic():
    assert False


def test_extract_buttons(json_config_fixture):
    aval_pg = json_config_fixture["available_pages"]
    buttons = create_link_buttons_for_available_pages(aval_pg)

    button1 = {"button_label": "Penguins", "link": "penguins"}
    assert button1 in buttons


def test_create_data_subselect_info(local_handler_fixture, json_config_fixture):
    select_dict = [
        {
            "type": "select",
            "column": "penguin_size.sex",
            "options": {"multiple": False},
        },
        {
            "type": "select",
            "column": "penguin_size.island",
            "options": {"multiple": True},
        },
        {
            "type": "axis",
            "column": "x",
            "options": {
                "entries": [
                    "penguin_size.culmen_length_mm",
                    "penguin_size.flipper_length_mm",
                    "penguin_size.body_mass_g",
                ]
            },
        },
    ]

    single_addendum_dict = {
        "selection_0": {
            "type": "filter",
            "column": "penguin_size.sex",
            "selected": "MALE",
        },
        "selection_1": {
            "type": "filter",
            "column": "penguin_size.island",
            "selected": SHOW_ALL_ROW,
        },
        "selection_2": {
            "type": "axis",
            "column": "x",
            "selected": "penguin_size.body_mass_g",
        },
    }
    select_info = create_data_subselect_info(
        select_dict, local_handler_fixture, single_addendum_dict
    )
    assert select_info[0][JINJA_SELECT_HTML_FILE] == "select_filter.html"
    assert select_info[1][COLUMN_NAME] == "penguin_size.island"
    assert select_info[2][JINJA_SELECT_HTML_FILE] == "select_axis.html"

    assert "MALE" in select_info[0][ACTIVE_SELECTORS]
    assert "MALE" in select_info[0][ENTRIES]
    assert "FEMALE" in select_info[0][ENTRIES]
    assert "." in select_info[0][ENTRIES]  # yes this is a unique entry in the data set
    assert "Torgersen" in select_info[1][ENTRIES]
    assert SHOW_ALL_ROW in select_info[1][ACTIVE_SELECTORS]
    assert "Biscoe" in select_info[1][ENTRIES]
    assert "Dream" in select_info[1][ENTRIES]
    assert select_info[1][SELECT_OPTION]["multiple"]
    assert not select_info[0][SELECT_OPTION]["multiple"]
    assert "penguin_size.culmen_length_mm" in select_info[2][ENTRIES]
    assert "penguin_size.flipper_length_mm" in select_info[2][ENTRIES]
    assert "penguin_size.body_mass_g" in select_info[2][ENTRIES]
    assert "penguin_size.body_mass_g" == select_info[2][ACTIVE_SELECTORS]


def test_get_unique_set_of_columns_needed():
    culmen = "penguin_size.culmen_length_mm"
    flipper = "penguin_size.flipper_length_mm"
    flipper2 = "penguin_size.flipper_length_mm2"
    island = "penguin_size.island"
    sex = "penguin_size.sex"
    test_cols_list = get_unique_set_of_columns_needed(
        {
            "points_0": {"x": culmen, "y": flipper},
            "points_1": {"x": culmen, "y": flipper2},
        },
        [
            {"type": "hover_data", "column": [sex, culmen]},
            {"type": "groupby", "column": [island]},
        ],
    )
    assert culmen in test_cols_list
    assert flipper in test_cols_list
    assert flipper2 in test_cols_list
    assert island in test_cols_list
    assert sex in test_cols_list
    assert len(test_cols_list) == 5
